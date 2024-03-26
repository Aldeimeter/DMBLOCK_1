import unittest
import rsa
from HandleTxs import HandleTxs
from Transaction import Transaction
from UTXO import UTXO
from UTXOPool import UTXOPool
from Block import Block
from HandleBlocks import HandleBlocks
from Blockchain import Blockchain
class Phase3(unittest.TestCase):

    def test_1(self):
        # Create key-pairs
        alice_pubkey, alice_privkey = rsa.newkeys(512)
        bob_pubkey, bob_privkey = rsa.newkeys(512)
        # Creat Genesis block and init blockchain
        genesis_block = Block(None, bob_pubkey)
        genesis_block.finalize()
        blockchain = Blockchain(genesis_block)
        handle_blocks = HandleBlocks(blockchain)
        

        # Create block without transactions.
        block_1 = Block(genesis_block.hash, alice_pubkey)
        block_1.finalize()

        self.assertEqual(handle_blocks.block_process(block_1), True)    

    
    def test_2(self):
        # Create key-pairs
        alice_pubkey, alice_privkey = rsa.newkeys(512)
        bob_pubkey, bob_privkey = rsa.newkeys(512)
        # Creat Genesis block and init blockchain
        genesis_block = Block(None, bob_pubkey)
        genesis_block.finalize()
        blockchain = Blockchain(genesis_block)
        handle_blocks = HandleBlocks(blockchain)
        

        # Create block.
        block_1 = Block(genesis_block.hash, alice_pubkey)
        # Create and add tx to block 
        tx_1 = Transaction()
        tx_1.add_input(genesis_block.coinbase.hash, 0)
        tx_1.add_output(2, alice_pubkey)
        tx_1.add_output(2, alice_pubkey)
        tx_1.add_output(2.25, alice_pubkey)
        tx_1.sign_tx(bob_privkey, 0)
        block_1.add_tx(tx_1)
        block_1.finalize()

        self.assertEqual(handle_blocks.block_process(block_1), True)    
    

    def test_3(self):
        # Create key-pairs
        alice_pubkey, alice_privkey = rsa.newkeys(512)
        bob_pubkey, bob_privkey = rsa.newkeys(512)
        charlie_pubkey, charlie_privkey = rsa.newkeys(512)
        # Creat Genesis block and init blockchain
        genesis_block = Block(None, bob_pubkey)
        root_tx = Transaction()
        root_tx.add_input(b'', 0)
        root_tx.add_output(3, bob_pubkey)
        root_tx.add_output(5, bob_pubkey)
        root_tx.add_output(4, bob_pubkey)
        root_tx.sign_tx(bob_privkey, 0)
        genesis_block.add_tx(root_tx) 
        genesis_block.finalize()
        blockchain = Blockchain(genesis_block)
        handle_blocks = HandleBlocks(blockchain)
        

        # Create block.
        block_1 = Block(genesis_block.hash, alice_pubkey)
        # Create and add tx to block 
        tx_1 = Transaction()
        tx_1.add_input(genesis_block.coinbase.hash, 0)
        tx_1.add_output(2, alice_pubkey)
        tx_1.add_output(2, alice_pubkey)
        tx_1.add_output(2.25, alice_pubkey)
        tx_1.sign_tx(bob_privkey, 0)
        block_1.add_tx(tx_1)
        # Create and add more txs to block.
        tx_2 = Transaction([Transaction.Input(genesis_block.txs[0].hash, 0)], [Transaction.Output(2, alice_pubkey)])
        tx_2.sign_tx(bob_privkey, 0)
        block_1.add_tx(tx_2)
        tx_3 = Transaction([Transaction.Input(genesis_block.txs[0].hash, 1)], [Transaction.Output(3, charlie_pubkey)])
        tx_3.sign_tx(bob_privkey, 0)
        block_1.add_tx(tx_3)
        block_1.finalize()

        self.assertEqual(handle_blocks.block_process(block_1), True)    
    

    def test_4(self):
        # Create key-pairs
        alice_pubkey, alice_privkey = rsa.newkeys(512)
        bob_pubkey, bob_privkey = rsa.newkeys(512)
        # Creat Genesis block and init blockchain
        genesis_block = Block(None, bob_pubkey)
        genesis_block.finalize()
        blockchain = Blockchain(genesis_block)
        handle_blocks = HandleBlocks(blockchain)
        block_1 = Block(genesis_block.hash, alice_pubkey)
        
        tx_1 = Transaction([Transaction.Input(genesis_block.coinbase.hash, 0)], [Transaction.Output(5, alice_pubkey)])
        tx_1.sign_tx(bob_privkey, 0)
        block_1.add_tx(tx_1)
        tx_2 = Transaction([Transaction.Input(genesis_block.coinbase.hash, 0)], [Transaction.Output(5, alice_pubkey)])
        tx_2.sign_tx(bob_privkey, 0)
        block_1.add_tx(tx_2)
        block_1.finalize()

        self.assertEqual(handle_blocks.block_process(block_1), False)
        

    def test_5(self):
        # Create key-pairs
        alice_pubkey, alice_privkey = rsa.newkeys(512)
        bob_pubkey, bob_privkey = rsa.newkeys(512)
        # Creat Genesis block and init blockchain
        genesis_block = Block(None, bob_pubkey)
        genesis_block.finalize()
        blockchain = Blockchain(genesis_block)
        handle_blocks = HandleBlocks(blockchain)
        new_genesis_block = Block(None, alice_pubkey)
        new_genesis_block.finalize() 

        self.assertEqual(handle_blocks.block_process(new_genesis_block), False)


    def test_6(self):
        # Create key-pairs
        alice_pubkey, alice_privkey = rsa.newkeys(512)
        bob_pubkey, bob_privkey = rsa.newkeys(512)
        # Creat Genesis block and init blockchain
        genesis_block = Block(None, bob_pubkey)
        genesis_block.finalize()
        blockchain = Blockchain(genesis_block)
        handle_blocks = HandleBlocks(blockchain)
        block_1 = Block(b'someRandomHashMoment', alice_pubkey)
        block_1.finalize()
        self.assertEqual(handle_blocks.block_process(block_1), False)


    def test_7(self):
        # Create key-pairs
        alice_pubkey, alice_privkey = rsa.newkeys(512)
        bob_pubkey, bob_privkey = rsa.newkeys(512)
        # Creat Genesis block and init blockchain
        genesis_block = Block(None, bob_pubkey)
        genesis_block.finalize()
        blockchain = Blockchain(genesis_block)
        handle_blocks = HandleBlocks(blockchain)
        block_1 = Block(genesis_block.hash, alice_pubkey)
        # Overspending
        tx_1 = Transaction()
        tx_1.add_input(genesis_block.coinbase.hash, 0)
        tx_1.add_output(6.5, alice_pubkey)
        tx_1.sign_tx(bob_privkey, 0)

        # Double spedning

        tx_2 = Transaction()
        tx_2.add_input(genesis_block.coinbase.hash, 0)
        tx_2.add_input(genesis_block.coinbase.hash, 1)
        tx_2.add_output(6.0, alice_pubkey)
        tx_2.sign_tx(bob_privkey, 0)
        tx_2.sign_tx(bob_privkey, 1)
        
        # Negative spending
        tx_3 = Transaction()
        tx_3.add_input(genesis_block.coinbase.hash, 0)
        tx_3.add_output(-6.0, alice_pubkey)
        tx_3.sign_tx(bob_privkey, 0)

        # Wrong Signature
        tx_4 = Transaction()
        tx_4.add_input(genesis_block.coinbase.hash, 0)
        tx_4.add_output(-6.0, alice_pubkey)
        tx_4.sign_tx(alice_privkey, 0)
        
        block_1.add_tx(tx_1)
        block_1.add_tx(tx_2)
        block_1.add_tx(tx_3)
        block_1.add_tx(tx_4)
        block_1.finalize()

        self.assertEqual(handle_blocks.block_process(block_1), False)


    def test_8(self):
        alice_pubkey, alice_privkey = rsa.newkeys(512)
        bob_pubkey, bob_privkey = rsa.newkeys(512)
        # Creat Genesis block and init blockchain
        genesis_block = Block(None, bob_pubkey)
        genesis_block.finalize()
        blockchain = Blockchain(genesis_block)
        handle_blocks = HandleBlocks(blockchain)

        # Create 5 blocks process it above genesis, compare genesis_block children blocks with blocks that were created.
        blocks = []
        for _ in range(5):
            block = Block(genesis_block.hash, alice_pubkey)
            block.finalize()
            if handle_blocks.block_process(block):
                blocks.append(block)
        children_blocks = []
        for node in blockchain.blocks.get(genesis_block.hash).children:
            children_blocks.append(node.b)

        self.assertEqual(children_blocks, blocks)


    def test_9(self):
        alice_pubkey, alice_privkey = rsa.newkeys(512)
        bob_pubkey, bob_privkey = rsa.newkeys(512)
        charlie_pubkey, charlie_privkey = rsa.newkeys(512)
        # Creat Genesis block and init blockchain
        genesis_block = Block(None, bob_pubkey)
        genesis_block.finalize()
        blockchain = Blockchain(genesis_block)
        handle_blocks = HandleBlocks(blockchain)

        block_1 = Block(genesis_block.hash, alice_pubkey)
        tx_1 = Transaction()
        tx_1.add_input(genesis_block.coinbase.hash, 0)
        tx_1.add_output(6, alice_pubkey)
        tx_1.sign_tx(bob_privkey, 0)
        block_1.add_tx(tx_1)
        block_1.finalize()
        handle_blocks.block_process(block_1)
        
        block_2 = Block(block_1.hash, charlie_pubkey)
        tx_2 = Transaction()
        tx_2.add_input(genesis_block.coinbase.hash, 0)
        tx_2.add_output(6, charlie_pubkey)
        tx_2.sign_tx(bob_privkey, 0)
        block_2.add_tx(tx_2)
        block_2.finalize()
        
        self.assertEqual(handle_blocks.block_process(block_2), False)


    def test_10(self):
        alice_pubkey, alice_privkey = rsa.newkeys(512)
        bob_pubkey, bob_privkey = rsa.newkeys(512)
        charlie_pubkey, charlie_privkey = rsa.newkeys(512)
        # Creat Genesis block and init blockchain
        genesis_block = Block(None, bob_pubkey)
        genesis_block.finalize()
        blockchain = Blockchain(genesis_block)
        handle_blocks = HandleBlocks(blockchain)

        block_1 = Block(genesis_block.hash, alice_pubkey)
        tx_1 = Transaction()
        tx_1.add_input(genesis_block.coinbase.hash, 0)
        tx_1.add_output(6, alice_pubkey)
        tx_1.sign_tx(bob_privkey, 0)
        block_1.add_tx(tx_1)
        block_1.finalize()
        handle_blocks.block_process(block_1)
        
        block_2 = Block(genesis_block.hash, charlie_pubkey)
        tx_2 = Transaction()
        tx_2.add_input(genesis_block.coinbase.hash, 0)
        tx_2.add_output(2, charlie_pubkey)
        tx_2.add_output(2, charlie_pubkey)
        tx_2.add_output(2, charlie_pubkey)
        tx_2.sign_tx(bob_privkey, 0)
        block_2.add_tx(tx_2)
        block_2.finalize()
        handle_blocks.block_process(block_2)

        block_3 = Block(block_1.hash, bob_pubkey)
        tx_3 = Transaction()
        tx_3.add_input(tx_2.hash, 1)
        tx_3.add_output(2, bob_pubkey)
        tx_3.sign_tx(charlie_privkey, 0)
        block_3.add_tx(tx_3)
        block_3.finalize()

        self.assertEqual(handle_blocks.block_process(block_3), False)


    def test_11(self):
        alice_pubkey, alice_privkey = rsa.newkeys(512)
        bob_pubkey, bob_privkey = rsa.newkeys(512)
        charlie_pubkey, charlie_privkey = rsa.newkeys(512)
       
        # Creat Genesis block and init blockchain
        genesis_block = Block(None, bob_pubkey)
        genesis_block.finalize()
        blockchain = Blockchain(genesis_block)
        handle_blocks = HandleBlocks(blockchain)

        block_1 = Block(genesis_block.hash, alice_pubkey)
        tx_1 = Transaction()
        tx_1.add_input(genesis_block.coinbase.hash, 0)
        tx_1.add_output(2, alice_pubkey)
        tx_1.add_output(2, alice_pubkey)
        tx_1.add_output(2, alice_pubkey)
        tx_1.sign_tx(bob_privkey, 0)
        block_1.add_tx(tx_1)
        block_1.finalize()
        handle_blocks.block_process(block_1)

        block_2 = Block(block_1.hash, charlie_pubkey)
        tx_2 = Transaction()
        tx_2.add_input(tx_1.hash, 0)
        tx_2.add_output(2, charlie_pubkey)
        tx_2.sign_tx(alice_privkey, 0)
        block_2.add_tx(tx_2)
        block_2.finalize()
        handle_blocks.block_process(block_2)

        block_3 = Block(block_2.hash, bob_pubkey)
        tx_3 = Transaction()
        tx_3.add_input(tx_1.hash, 1)
        tx_3.add_output(2, bob_pubkey)
        tx_3.sign_tx(alice_privkey, 0)
        block_3.add_tx(tx_3)
        block_3.finalize()

        self.assertEqual(handle_blocks.block_process(block_3), True)


    def test_12(self):
        bob_pubkey, bob_privkey = rsa.newkeys(512)
       
        # Creat Genesis block and init blockchain
        genesis_block = Block(None, bob_pubkey)
        genesis_block.finalize()
        blockchain = Blockchain(genesis_block)
        handle_blocks = HandleBlocks(blockchain)
        
        block_1 = Block(genesis_block.hash, bob_pubkey)
        block_1.finalize()
        handle_blocks.block_process(block_1)

        block_2 = Block(block_1.hash, bob_pubkey)
        block_2.finalize()
        handle_blocks.block_process(block_2)
        
        block_3 = Block(block_2.hash, bob_pubkey)
        block_3.finalize()
        self.assertEqual(handle_blocks.block_process(block_3), True)


    def test_13(self):
        bob_pubkey, bob_privkey = rsa.newkeys(512)
       
        # Creat Genesis block and init blockchain
        genesis_block = Block(None, bob_pubkey)
        genesis_block.finalize()
        blockchain = Blockchain(genesis_block)
        handle_blocks = HandleBlocks(blockchain)
        
        previous_block = genesis_block
        for _ in range(11):
            block = Block(previous_block.hash, bob_pubkey)
            block.finalize()
            handle_blocks.block_process(block)
            previous_block = block

        block = Block(genesis_block.hash, bob_pubkey)
        block.finalize()
        self.assertEqual(handle_blocks.block_process(block), True)


    def test_14(self):
        bob_pubkey, bob_privkey = rsa.newkeys(512)
       
        # Creat Genesis block and init blockchain
        genesis_block = Block(None, bob_pubkey)
        genesis_block.finalize()
        blockchain = Blockchain(genesis_block)
        handle_blocks = HandleBlocks(blockchain)
        
        previous_block = genesis_block
        for _ in range(12):
            block = Block(previous_block.hash, bob_pubkey)
            block.finalize()
            handle_blocks.block_process(block)
            previous_block = block

        block = Block(genesis_block.hash, bob_pubkey)
        block.finalize()
        self.assertEqual(handle_blocks.block_process(block), False)
        
    def test_15(self):
        bob_pubkey, bob_privkey = rsa.newkeys(512)
       
        # Create Genesis block and init blockchain
        genesis_block = Block(None, bob_pubkey)
        genesis_block.finalize()
        blockchain = Blockchain(genesis_block)
        handle_blocks = HandleBlocks(blockchain)
        
        self.assertIsNotNone(handle_blocks.block_create(bob_pubkey))
        
        
    def test_16(self):
        bob_pubkey, bob_privkey = rsa.newkeys(512)
        alice_pubkey, alice_privkey = rsa.newkeys(512)
       
        # Create Genesis block and init blockchain
        genesis_block = Block(None, bob_pubkey)
        genesis_block.finalize()
        blockchain = Blockchain(genesis_block)
        handle_blocks = HandleBlocks(blockchain)
        
        tx_1 = Transaction()
        tx_1.add_input(genesis_block.coinbase.hash, 0)
        tx_1.add_output(6, alice_pubkey)
        tx_1.sign_tx(bob_privkey, 0)

        blockchain.tx_pool.add_tx(tx_1)
        self.assertIsNotNone(handle_blocks.block_create(bob_pubkey))


    def test_17(self):
        bob_pubkey, bob_privkey = rsa.newkeys(512)
        alice_pubkey, alice_privkey = rsa.newkeys(512)
       
        # Create Genesis block and init blockchain
        genesis_block = Block(None, bob_pubkey)
        genesis_block.finalize()
        blockchain = Blockchain(genesis_block)
        handle_blocks = HandleBlocks(blockchain)
        
        tx_1 = Transaction()
        tx_1.add_input(genesis_block.coinbase.hash, 0)
        tx_1.add_output(6, alice_pubkey)
        tx_1.sign_tx(bob_privkey, 0)
        blockchain.tx_pool.add_tx(tx_1)
        handle_blocks.block_create(bob_pubkey)
        self.assertIsNotNone(handle_blocks.block_create(bob_pubkey))


    def test_18(self):
        bob_pubkey, bob_privkey = rsa.newkeys(512)
        alice_pubkey, alice_privkey = rsa.newkeys(512)
       
        # Create Genesis block and init blockchain
        genesis_block = Block(None, bob_pubkey)
        genesis_block.finalize()
        blockchain = Blockchain(genesis_block)
        handle_blocks = HandleBlocks(blockchain)

        tx_1 = Transaction()
        tx_1.add_input(genesis_block.coinbase.hash, 0)
        tx_1.add_output(6, alice_pubkey)
        tx_1.sign_tx(bob_privkey, 0)

        handle_blocks.tx_process(tx_1)
        handle_blocks.block_create(alice_pubkey)

        handle_blocks.tx_process(tx_1)

        self.assertEqual(handle_blocks.block_create(bob_pubkey).txs, [] )


    def test_19(self):
        bob_pubkey, bob_privkey = rsa.newkeys(512)
        alice_pubkey, alice_privkey = rsa.newkeys(512)
       
        # Create Genesis block and init blockchain
        genesis_block = Block(None, bob_pubkey)
        genesis_block.finalize()
        blockchain = Blockchain(genesis_block)
        handle_blocks = HandleBlocks(blockchain)
        
        tx_1 = Transaction()
        tx_1.add_input(genesis_block.coinbase.hash, 0)
        tx_1.add_output(6, alice_pubkey)
        tx_1.sign_tx(bob_privkey, 0)
        blockchain.tx_pool.add_tx(tx_1)
        handle_blocks.block_create(alice_pubkey)
        tx_2 = Transaction()
        tx_2.add_input(genesis_block.coinbase.hash, 0)
        tx_2.add_output(6, alice_pubkey)
        tx_2.sign_tx(bob_privkey, 0)
        blockchain.tx_pool.add_tx(tx_2)
        self.assertEqual(handle_blocks.block_create(bob_pubkey).txs, [])

    def test_20(self):
        bob_pubkey, bob_privkey = rsa.newkeys(512)
        alice_pubkey, alice_privkey = rsa.newkeys(512)
       
        # Create Genesis block and init blockchain
        genesis_block = Block(None, bob_pubkey)
        genesis_block.finalize()
        blockchain = Blockchain(genesis_block)
        handle_blocks = HandleBlocks(blockchain)
        
        tx_1 = Transaction()
        tx_1.add_input(genesis_block.coinbase.hash, 0)
        tx_1.add_output(6, alice_pubkey)
        tx_1.sign_tx(bob_privkey, 0)
        handle_blocks.tx_process(tx_1)
        self.assertEqual(handle_blocks.block_create(alice_pubkey).txs, [tx_1])

    def test_21(self):
        bob_pubkey, bob_privkey = rsa.newkeys(512)
        alice_pubkey, alice_privkey = rsa.newkeys(512)
       
        # Create Genesis block and init blockchain
        genesis_block = Block(None, bob_pubkey)
        genesis_block.finalize()
        blockchain = Blockchain(genesis_block)
        handle_blocks = HandleBlocks(blockchain)
        
        tx_negative = Transaction()
        tx_negative.add_input(genesis_block.coinbase.hash, 0)
        tx_negative.add_output(-6, alice_pubkey)
        tx_negative.sign_tx(bob_privkey, 0)
        
        tx_over = Transaction()
        tx_over.add_input(genesis_block.coinbase.hash, 0)
        tx_over.add_output(6.26, alice_pubkey)
        tx_over.sign_tx(bob_privkey, 0)
        
        tx_wrong_sig = Transaction()
        tx_wrong_sig.add_input(genesis_block.coinbase.hash, 0)
        tx_wrong_sig.add_output(6.25, alice_pubkey)
        tx_wrong_sig.sign_tx(alice_privkey, 0)
        
        handle_blocks.tx_process(tx_negative)
        handle_blocks.tx_process(tx_over)
        handle_blocks.tx_process(tx_wrong_sig)
        self.assertEqual(handle_blocks.block_create(alice_pubkey).txs, [])
        
    def test_22(self):
        bob_pubkey, bob_privkey = rsa.newkeys(512)
        alice_pubkey, alice_privkey = rsa.newkeys(512)
       
        # Create Genesis block and init blockchain
        genesis_block = Block(None, bob_pubkey)
        genesis_block.finalize()
        blockchain = Blockchain(genesis_block)
        handle_blocks = HandleBlocks(blockchain)

        tx_1 = Transaction()
        tx_1.add_input(genesis_block.coinbase.hash, 0)
        tx_1.add_output(2, alice_pubkey)
        tx_1.add_output(2, alice_pubkey)
        tx_1.add_output(2, alice_pubkey)
        tx_1.sign_tx(bob_privkey, 0)

        handle_blocks.tx_process(tx_1)
        handle_blocks.block_create(alice_pubkey)

        tx_2 = Transaction()
        tx_2.add_input(tx_1.hash, 0)
        tx_2.add_output(2, bob_pubkey)
        tx_2.sign_tx(alice_privkey, 0)

        handle_blocks.tx_process(tx_2)
        handle_blocks.block_create(bob_pubkey)

        tx_3 = Transaction()
        tx_3.add_input(tx_1.hash, 1)
        tx_3.add_output(2, bob_pubkey)
        tx_3.sign_tx(alice_privkey, 0)

        handle_blocks.tx_process(tx_3)
        handle_blocks.block_create(bob_pubkey)

        self.assertEqual(blockchain.max_height_block.height, 4)
        
    def test_23(self):
        bob_pubkey, bob_privkey = rsa.newkeys(512)
        alice_pubkey, alice_privkey = rsa.newkeys(512)
       
        # Create Genesis block and init blockchain
        genesis_block = Block(None, bob_pubkey)
        genesis_block.finalize()
        blockchain = Blockchain(genesis_block)
        handle_blocks = HandleBlocks(blockchain)

        tx_1 = Transaction()
        tx_1.add_input(genesis_block.coinbase.hash, 0)
        tx_1.add_output(2, alice_pubkey)
        tx_1.add_output(2, alice_pubkey)
        tx_1.add_output(2, alice_pubkey)
        tx_1.sign_tx(bob_privkey, 0)

        handle_blocks.tx_process(tx_1)
        handle_blocks.block_create(alice_pubkey)

        tx_2 = Transaction()
        tx_2.add_input(tx_1.hash, 0)
        tx_2.add_output(2, bob_pubkey)
        tx_2.sign_tx(alice_privkey, 0)

        handle_blocks.tx_process(tx_2)

        self.assertEqual(handle_blocks.block_create(bob_pubkey).txs, [tx_2])


    def test_24(self):
        bob_pubkey, bob_privkey = rsa.newkeys(512)
        alice_pubkey, alice_privkey = rsa.newkeys(512)
       
        # Create Genesis block and init blockchain
        genesis_block = Block(None, bob_pubkey)
        genesis_block.finalize()
        blockchain = Blockchain(genesis_block)
        handle_blocks = HandleBlocks(blockchain)

        tx_1 = Transaction()
        tx_1.add_input(genesis_block.coinbase.hash, 0)
        tx_1.add_output(2, alice_pubkey)
        tx_1.add_output(2, alice_pubkey)
        tx_1.add_output(2, alice_pubkey)
        tx_1.sign_tx(bob_privkey, 0)

        handle_blocks.tx_process(tx_1)
        handle_blocks.block_create(alice_pubkey)
        
        new_block = Block(genesis_block.hash, bob_pubkey)
        tx_2 = Transaction()
        tx_2.add_input(tx_1.hash, 0)
        tx_2.add_output(2, bob_pubkey)
        tx_2.sign_tx(alice_privkey, 0)
        new_block.add_tx(tx_2)
        new_block.finalize()

        self.assertEqual(handle_blocks.block_process(new_block), False)


    def test_25(self):
        bob_pubkey, bob_privkey = rsa.newkeys(512)
        alice_pubkey, alice_privkey = rsa.newkeys(512)
       
        # Create Genesis block and init blockchain
        genesis_block = Block(None, bob_pubkey)
        genesis_block.finalize()
        blockchain = Blockchain(genesis_block)
        handle_blocks = HandleBlocks(blockchain)
            
        block = Block(genesis_block.hash, alice_pubkey)
        block.finalize()
        handle_blocks.block_process(block)
        for _ in range(5):
            block = Block(genesis_block.hash, alice_pubkey)
            block.finalize()
            handle_blocks.block_process(block)

        self.assertEqual(handle_blocks.block_create(bob_pubkey).prev_block_hash, block.hash)
    
    def test_26(self):
        bob_pubkey, bob_privkey = rsa.newkeys(512)
        alice_pubkey, alice_privkey = rsa.newkeys(512)
       
        # Create Genesis block and init blockchain
        genesis_block = Block(None, bob_pubkey)
        genesis_block.finalize()
        blockchain = Blockchain(genesis_block)
        handle_blocks = HandleBlocks(blockchain)
        # Branch 1 
        block_1 = Block(genesis_block.hash, alice_pubkey)
        block_1.finalize()
        handle_blocks.block_process(block_1)
        
        block_2 = Block(block_1.hash, alice_pubkey)
        block_2.finalize()
        handle_blocks.block_process(block_2)
        
        block_3 = Block(block_2.hash, alice_pubkey)
        block_3.finalize()
        handle_blocks.block_process(block_3)
        
        block_4 = Block(block_3.hash, alice_pubkey)
        block_4.finalize()
        handle_blocks.block_process(block_4)
        
        block_5 = Block(block_4.hash, alice_pubkey)
        block_5.finalize()
        handle_blocks.block_process(block_5)
        
        # Branch 2
        block_1_1 = Block(genesis_block.hash, alice_pubkey)
        block_1_1.finalize()
        handle_blocks.block_process(block_1_1)
        
        block_2_1 = Block(block_1_1.hash, alice_pubkey)
        block_2_1.finalize()
        handle_blocks.block_process(block_2_1)
        
        block_3_1 = Block(block_2_1.hash, alice_pubkey)
        block_3_1.finalize()
        handle_blocks.block_process(block_3_1)
        
        block_4_1 = Block(block_3_1.hash, alice_pubkey)
        block_4_1.finalize()
        handle_blocks.block_process(block_4_1)


        self.assertEqual(handle_blocks.block_create(bob_pubkey).prev_block_hash, block_5.hash)


    def test_27(self):
        bob_pubkey, bob_privkey = rsa.newkeys(512)
        alice_pubkey, alice_privkey = rsa.newkeys(512)
       
        # Create Genesis block and init blockchain
        genesis_block = Block(None, bob_pubkey)
        genesis_block.finalize()
        blockchain = Blockchain(genesis_block)
        handle_blocks = HandleBlocks(blockchain)
        # Branch 1 
        block_1 = Block(genesis_block.hash, alice_pubkey)
        block_1.finalize()
        handle_blocks.block_process(block_1)
        
        block_2 = Block(block_1.hash, alice_pubkey)
        block_2.finalize()
        handle_blocks.block_process(block_2)
        
        block_3 = Block(block_2.hash, alice_pubkey)
        block_3.finalize()
        handle_blocks.block_process(block_3)
        
        block_4 = Block(block_3.hash, alice_pubkey)
        block_4.finalize()
        handle_blocks.block_process(block_4)
        
        block_5 = Block(block_4.hash, alice_pubkey)
        block_5.finalize()
        handle_blocks.block_process(block_5)
        
        block_6 = Block(block_5.hash, alice_pubkey)
        block_6.finalize()
        handle_blocks.block_process(block_6)
        
        block_7 = Block(block_6.hash, alice_pubkey)
        block_7.finalize()
        handle_blocks.block_process(block_7)
        
        block_8 = Block(block_7.hash, alice_pubkey)
        block_8.finalize()
        handle_blocks.block_process(block_8)
        
        block_9 = Block(block_8.hash, alice_pubkey)
        block_9.finalize()
        handle_blocks.block_process(block_9)
        
        block_10 = Block(block_9.hash, alice_pubkey)
        block_10.finalize()
        handle_blocks.block_process(block_10)
        
        block_11 = Block(block_10.hash, alice_pubkey)
        block_11.finalize()
        handle_blocks.block_process(block_11)
        
        block_12 = Block(block_11.hash, alice_pubkey)
        block_12.finalize()
        handle_blocks.block_process(block_12)
        
         
        # Branch 2
        block_1_1 = Block(genesis_block.hash, alice_pubkey)
        block_1_1.finalize()
        handle_blocks.block_process(block_1_1)
        
        block_2_1 = Block(block_1_1.hash, alice_pubkey)
        block_2_1.finalize()
        handle_blocks.block_process(block_2_1)
        
        block_3_1 = Block(block_2_1.hash, alice_pubkey)
        block_3_1.finalize()
        handle_blocks.block_process(block_3_1)
        
        block_4_1 = Block(block_3_1.hash, alice_pubkey)
        block_4_1.finalize()
        handle_blocks.block_process(block_4_1)

        block_5_1 = Block(block_4_1.hash, alice_pubkey)
        block_5_1.finalize()
        handle_blocks.block_process(block_5_1)
        
        block_6_1 = Block(block_5_1.hash, alice_pubkey)
        block_6_1.finalize()
        handle_blocks.block_process(block_6_1)
        
        block_7_1 = Block(block_6_1.hash, alice_pubkey)
        block_7_1.finalize()
        handle_blocks.block_process(block_7_1)
        
        block_8_1 = Block(block_7_1.hash, alice_pubkey)
        block_8_1.finalize()
        handle_blocks.block_process(block_8_1)
        
        block_9_1 = Block(block_8_1.hash, alice_pubkey)
        block_9_1.finalize()
        handle_blocks.block_process(block_9_1)
        
        block_10_1 = Block(block_9_1.hash, alice_pubkey)
        block_10_1.finalize()
        handle_blocks.block_process(block_10_1)
        
        block_11_1 = Block(block_10_1.hash, alice_pubkey)
        block_11_1.finalize()
        handle_blocks.block_process(block_11)
        
        block = Block(genesis_block.hash, alice_pubkey)
        block.finalize()
        self.assertEqual(handle_blocks.block_process(block), False)


if __name__ == "__main__":
    unittest.main()
