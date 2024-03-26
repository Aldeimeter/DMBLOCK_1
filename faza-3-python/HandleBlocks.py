from Blockchain import Blockchain
from Block import Block
import rsa
from HandleTxs import HandleTxs
from Transaction import Transaction
class HandleBlocks():
    def __init__(self, blockchain: Blockchain):
        self.blockchain = blockchain

    def block_process(self, block: Block) -> bool:
        if block is None:
            return False
        return self.blockchain.block_add(block)


    def block_create(self, my_address: rsa.PublicKey) -> Block:
        parent = self.blockchain.max_height_block
        parent_hash = parent.b.hash
        current = Block(parent_hash, my_address)
        u_pool = self.blockchain.get_utxo_pool_at_max_height()
        tx_pool = self.blockchain.get_tx_pool()
        handler = HandleTxs(u_pool)
        txs = tx_pool.get_txs()
        r_txs = handler.handler(txs)
        for tx in r_txs:
            current.add_tx(tx)
        current.finalize()
        if self.blockchain.block_add(current):
            return current
        else:
            return None 


    def tx_process(self,tx: Transaction):
        self.blockchain.tx_add(tx)

