from UTXO import UTXO
from Transaction import Transaction
from typing import List,Optional
class UTXOPool():
    def __init__(self, uPool:Optional['UTXOPool'] = None ):
        if isinstance(uPool,UTXOPool):
            self.H = dict(uPool.H)
        else:
            self.H = dict()


    def add_UTXO(self, utxo: UTXO, txOut: 'Transaction.Output'):
        self.H[utxo] = txOut


    def remove_UTXO(self, utxo: UTXO):
        self.H.pop(utxo)


    def get_tx_output(self, utxo: UTXO) -> 'Transaction.Output':
        return self.H.get(utxo)

    
    def contains(self, utxo: UTXO) -> bool:
        return utxo in self.H 


    def get_all_UTXO(self) -> List:
        return list(self.H.keys())
