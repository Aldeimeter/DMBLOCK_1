from typing import List, Optional
from UTXOPool import UTXOPool
from Transaction import Transaction
import rsa
import exceptions
from UTXO import UTXO
class HandleTxs():
    def __init__(self, utxo_pool: Optional[UTXOPool] = None):
        self.utxo_pool = UTXOPool(utxo_pool)


    def get_utxo_pool(self):
        if self.utxo_pool is None:
            self.utxo_pool = UTXOPool()
        return self.utxo_pool


    def tx_is_valid(self, tx: Transaction) -> bool:
        sum = 0
        utxo_set = set()
        for input in tx.inputs:
            utxo = UTXO(input.prev_tx_hash,input.output_index)
            utxo_set.add(utxo)
            output = self.utxo_pool.get_tx_output(utxo)
            if output is None:
                raise exceptions.UTXONotFoundError
            try: 
                rsa.verify(tx.get_data_to_sign(tx.inputs.index(input)), input.signature, output.address )
            except rsa.pkcs1.VerificationError:
                raise exceptions.VerificationError 

            sum += output.value
        if len(utxo_set) != len(tx.inputs):
            raise exceptions.DoubleSpendingError
        
        for output in tx.outputs:
            if output.value < 0:
                raise exceptions.NegativeValueError
            sum -= output.value

        if sum < 0:
            raise exceptions.OverSpendingError

        return True
                
    
    def handle_tx(self, tx: Transaction) -> Transaction:
        try:
            self.tx_is_valid(tx)
            for input in tx.inputs:
                self.utxo_pool.remove_UTXO(UTXO(input.prev_tx_hash, input.output_index))
            for i in range(len(tx.outputs)):
                self.utxo_pool.add_UTXO(UTXO(tx.hash, i), tx.outputs[i])
            return tx
        except exceptions.PhaseOneError as e:
            print(f"Exception caught: {type(e).__name__}")

            
    def handler(self, possible_txs: List[Transaction]) -> List[Transaction]:
        tx_to_valid = list(possible_txs)
        validated_txs = list()
        while True:
            new_possible_txs = []
            for tx in tx_to_valid:
                handled_tx = self.handle_tx(tx)
                if handled_tx is not None:
                    validated_txs.append(handled_tx)
                else:
                    new_possible_txs.append(tx)
            for tx in validated_txs:
                tx_to_valid.remove(tx)
            if len(new_possible_txs) == len(tx_to_valid):
                break
            tx_to_valid = new_possible_txs
        return validated_txs
        
            
