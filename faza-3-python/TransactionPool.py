from typing import List
from Transaction import Transaction
class TransactionPool():

    def __init__(self, tx_pool= None):
        if tx_pool is None:
            self.H = dict()
        else:
            self.H = dict(tx_pool)


    def add_tx(self,tx: Transaction):
        self.H[tx.hash] = tx 


    def remove_tx(self,tx: Transaction):
        self.H.pop(tx.hash)


    def get_tx(self, tx_hash: bytes) -> Transaction:
        return self.H.get(tx_hash)

    
    def get_txs(self) -> List[Transaction]:
        return self.H.values()
    
