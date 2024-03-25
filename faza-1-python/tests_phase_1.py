import unittest
import rsa
from HandleTxs import HandleTxs
from Transaction import Transaction
from UTXO import UTXO
from UTXOPool import UTXOPool

class TestPhase1(unittest.TestCase):
    def test_valid_tx(self):
        alice_pubkey, alice_privkey = rsa.newkeys(512)
        bob_pubkey, bob_privkey = rsa.newkeys(512)
        root_tx = Transaction()
        root_tx.add_input(b'0', 0)
        root_tx.add_output(10, bob_pubkey)

        root_tx.sign_tx(bob_privkey, 0)

        utxo_pool = UTXOPool()
        utxo_pool.add_UTXO(UTXO(root_tx.hash,0), root_tx.get_output(0))
        handleTxs = HandleTxs(utxo_pool)
        
        test_tx = Transaction()
        test_tx.add_input(root_tx.hash, 0)
        test_tx.add_output(3, alice_pubkey)
        test_tx.add_output(4, alice_pubkey)
        test_tx.add_output(3, alice_pubkey)
        test_tx.sign_tx(bob_privkey, 0)

        self.assertEqual(handleTxs.tx_is_valid(test_tx),True)

    
    def test_handle_tx_wrong_sigs(self):
        alice_pubkey, alice_privkey = rsa.newkeys(512)
        bob_pubkey, bob_privkey = rsa.newkeys(512)
        root_tx = Transaction()
        root_tx.add_input(b'0', 0)
        for i in range(10):
            root_tx.add_output(10, bob_pubkey)
        utxo_pool = UTXOPool()

        root_tx.sign_tx(bob_privkey, 0)

        for i in range(10):
            utxo_pool.add_UTXO(UTXO(root_tx.hash,i), root_tx.get_output(i))

        handleTxs = HandleTxs(utxo_pool)
        
        test_txs = list()
        valid_txs = list()
        for i in range(10):
            test_tx = Transaction()
            test_tx.add_input(root_tx.hash, i)
            test_tx.add_output(3, alice_pubkey)
            test_tx.add_output(4, alice_pubkey)
            test_tx.add_output(3, alice_pubkey)
            test_tx.sign_tx(bob_privkey if i % 2 == 0 else alice_privkey, 0)
            test_txs.append(test_tx)
            if i% 2 == 0:
                valid_txs.append(test_tx)

        validated_txs = handleTxs.handler(list(test_txs))
        self.assertEqual(validated_txs,valid_txs)


    def test_handle_tx(self):
        alice_pubkey, alice_privkey = rsa.newkeys(512)
        bob_pubkey, bob_privkey = rsa.newkeys(512)
        root_tx = Transaction()
        root_tx.add_input(b'0', 0)
        for i in range(10):
            root_tx.add_output(10, bob_pubkey)
        utxo_pool = UTXOPool()

        root_tx.sign_tx(bob_privkey, 0)

        for i in range(10):
            utxo_pool.add_UTXO(UTXO(root_tx.hash,i), root_tx.get_output(i))

        handleTxs = HandleTxs(utxo_pool)
        
        test_txs = list()
        
        for i in range(10):
            test_tx = Transaction()
            test_tx.add_input(root_tx.hash, i)
            test_tx.add_output(3, alice_pubkey)
            test_tx.add_output(4, alice_pubkey)
            test_tx.add_output(3, alice_pubkey)
            test_tx.sign_tx(bob_privkey, 0)
            test_txs.append(test_tx)

        validated_txs = handleTxs.handler(list(test_txs))
        self.assertEqual(validated_txs,test_txs)


    def test_max(self):
        alice_pubkey, alice_privkey = rsa.newkeys(512)
        bob_pubkey, bob_privkey = rsa.newkeys(512)

        root_tx = Transaction()
        root_tx.add_input(b'0', 0)
        for i in range(3):
            root_tx.add_output(10, bob_pubkey)
        utxo_pool = UTXOPool()
        root_tx.sign_tx(bob_privkey, 0)
        for i in range(3):
            utxo_pool.add_UTXO(UTXO(root_tx.hash,i), root_tx.get_output(i))
            
        root_tx_2 = Transaction()
        root_tx_2.add_input(b'0',0)
        root_tx_2.add_output(10, bob_pubkey)
        root_tx_2.sign_tx(bob_privkey, 0)
        utxo_pool.add_UTXO(UTXO(root_tx_2.hash, 0), root_tx_2.get_output(i))
            
        handleTxs = HandleTxs(utxo_pool)


        test_tx_1 = Transaction()
        test_tx_1.add_input(root_tx.hash, 0)
        test_tx_1.add_input(root_tx.hash, 1)

        test_tx_1.add_output(20, alice_pubkey)

        test_tx_1.sign_tx(bob_privkey, 0)
        test_tx_1.sign_tx(bob_privkey, 1)

        test_tx_2 = Transaction()
        test_tx_2.add_input(root_tx.hash, 2)
        test_tx_2.add_input(root_tx_2.hash, 0)

        test_tx_2.add_output(20, alice_pubkey)

        test_tx_2.sign_tx(bob_privkey, 0)
        test_tx_2.sign_tx(bob_privkey, 1)

        print(handleTxs.test([test_tx_1, test_tx_2]))
        self.assertEqual(True, True)

        

        

        

if __name__ == "__main__":
    unittest.main()
