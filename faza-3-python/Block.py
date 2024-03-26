from Transaction import Transaction
import rsa
import hashlib
class Block():
    COINBASE = 6.25
    def __init__(self, prev_hash: bytes, address: rsa.PublicKey):
        self.prev_block_hash = prev_hash
        self.coinbase = Transaction.create_coinbase(self.COINBASE, address)
        self.txs = list()
    
    def add_tx(self, tx: Transaction):
        self.txs.append(tx)

    def get_block(self) -> bytes:
        raw = b''
        if self.prev_block_hash is not None:
            raw += self.prev_block_hash
        for tx in self.txs:
            raw += tx.get_tx()

        return raw
   
    def finalize(self):
        self.hash = hashlib.sha256(self.get_block()).digest()
    

        
        
