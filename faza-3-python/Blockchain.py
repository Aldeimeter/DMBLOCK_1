from HandleTxs import HandleTxs
from Block import Block 
from UTXOPool import UTXOPool
from UTXO import UTXO
from Transaction import Transaction
from TransactionPool import TransactionPool
class Blockchain():
    CUT_OFF_AGE = 12
    
    class BlockNode():
        def __init__(self, b: Block, parent, utxo_pool: UTXOPool):
            self.b = b 
            self.parent = parent
            self.children = list()
            self.utxo_pool = utxo_pool
            if parent is not None:
                self.height = parent.height + 1
                parent.children.append(self)
            else:
                self.height = 1


        def get_utxo_pool_copy(self):
            return UTXOPool(self.utxo_pool)

    def __init__(self, genesis_block: Block): 
        utxo_pool = UTXOPool()
        coinbase_tx = genesis_block.coinbase  
        utxo_pool.add_UTXO(UTXO(coinbase_tx.hash,0),coinbase_tx.get_output(0))
        for tx in genesis_block.txs:
            for i in range(len(tx.outputs)):
                utxo_pool.add_UTXO(UTXO(tx.hash, i), tx.get_output(i))
        self.root_node = self.BlockNode(genesis_block, None, utxo_pool)
        self.tx_pool = TransactionPool()
        self.blocks = dict()
        self.blocks[genesis_block.hash] = self.root_node
        self.max_height_block = self.root_node

        
        
    def get_utxo_pool_at_max_height(self) -> UTXOPool:
       return self.max_height_block.get_utxo_pool_copy() 

    def get_tx_pool(self) -> TransactionPool:
        return self.tx_pool


    def tx_add(self,tx: Transaction):
        self.tx_pool.add_tx(tx)

    # What should happen when Block goes through block_add:
    # 1) All transcations must be valid -> all transactions in block should be returned from HandleTxs.handler
    # 2) Block height is higher than maximum height of blockchain - CUT_OFF_AGE
    # if both condition are true add block to blockchain.
    # What should also be taken into consideration:
    # 0) Merge UtxoPools
    # 1) if block is added to blockchain -> it is added to dictionary of blocks.
    # 2) if block is new highest block -> update self.max_height_block  
    def block_add(self,block: Block):
        # Check if parent block exists
        parent_block = self.blocks.get(block.prev_block_hash, None)
        if parent_block is None:
            return False
        # check if block height is ok
        if self.max_height_block.height - self.CUT_OFF_AGE > parent_block.height + 1:
            return False
        # Check if all txs are valid
        handler = HandleTxs(parent_block.get_utxo_pool_copy())
        txs = handler.handler(block.txs)
        if txs != block.txs:
            return False
        # Actualize tx_pool
        for tx in txs:
            tx_pool_txs = self.tx_pool.get_txs()
            if tx in tx_pool_txs:
                self.tx_pool.remove_tx(tx)
        # merge utxo_pool with new utxos
        utxo_pool = handler.get_utxo_pool()

        coinbase_tx = block.coinbase  
        utxo_pool.add_UTXO(UTXO(coinbase_tx.hash,0),coinbase_tx.get_output(0))
        for tx in block.txs:
            for i in range(len(tx.outputs)):
                utxo_pool.add_UTXO(UTXO(tx.hash, i), tx.get_output(i))
        
        # create new node of Blockchain tree
        new_node = self.BlockNode(block, parent_block, utxo_pool)
        
        # Check if block is new max height block.
        if new_node.height > self.max_height_block.height:
            self.max_height_block = new_node
            # if new blockchain height is more than CUT_OFF_AGE delete all blocks with height lower than max_height - CUT_OFF_AGE
            if self.max_height_block.height - self.CUT_OFF_AGE > 0:
                for key, node in dict(self.blocks).items():
                    if node.height <= self.max_height_block.height - self.CUT_OFF_AGE:
                        self.blocks.pop(key)
        # Add block to hashmap
        self.blocks[block.hash] = new_node

        return True 


