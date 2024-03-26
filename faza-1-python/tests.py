import unittest
import rsa
import exceptions
from HandleTxs import HandleTxs
from Transaction import Transaction
from UTXO import UTXO
from UTXOPool import UTXOPool

class Phase1(unittest.TestCase):
    def test_1(self):
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

   
    def test_2(self):
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
        test_tx.outputs[0].address = bob_pubkey
        with self.assertRaises(exceptions.VerificationError):
            handleTxs.tx_is_valid(test_tx)

   
    def test_3(self):
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
        test_tx.sign_tx(alice_privkey, 0)

        with self.assertRaises(exceptions.VerificationError):
            handleTxs.tx_is_valid(test_tx)

   
    def test_4(self):
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
        test_tx.add_output(4, alice_pubkey)
        test_tx.add_output(4, alice_pubkey)
        test_tx.add_output(3, alice_pubkey)
        test_tx.sign_tx(bob_privkey, 0)

        with self.assertRaises(exceptions.OverSpendingError):
            handleTxs.tx_is_valid(test_tx)

   
    def test_5(self):
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
        test_tx.add_input(root_tx.hash, 1)
        test_tx.add_output(3, alice_pubkey)
        test_tx.add_output(4, alice_pubkey)
        test_tx.add_output(3, alice_pubkey)
        test_tx.sign_tx(bob_privkey, 0)

        with self.assertRaises(exceptions.UTXONotFoundError):
            handleTxs.tx_is_valid(test_tx)

   
    def test_6(self):
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
        test_tx.add_input(root_tx.hash, 0)
        test_tx.add_output(3, alice_pubkey)
        test_tx.add_output(4, alice_pubkey)
        test_tx.add_output(3, alice_pubkey)
        test_tx.sign_tx(bob_privkey, 0)
        test_tx.sign_tx(bob_privkey, 1)

        with self.assertRaises(exceptions.DoubleSpendingError):
            handleTxs.tx_is_valid(test_tx)

   
    def test_7(self):
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
        test_tx.add_output(-3, alice_pubkey)
        test_tx.add_output(4, alice_pubkey)
        test_tx.add_output(3, alice_pubkey)
        test_tx.sign_tx(bob_privkey, 0)

        with self.assertRaises(exceptions.NegativeValueError):
            handleTxs.tx_is_valid(test_tx)
    

    def test_8(self):
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

 
    def test_9(self):
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


    def test_10(self):
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
            test_tx.add_output(3 if i % 2 == 0 else 6, alice_pubkey)
            test_tx.add_output(4, alice_pubkey)
            test_tx.add_output(3, alice_pubkey)
            test_tx.sign_tx(bob_privkey, 0)
            test_txs.append(test_tx)
            if i% 2 == 0:
                valid_txs.append(test_tx)

        validated_txs = handleTxs.handler(list(test_txs))
        self.assertEqual(validated_txs,valid_txs)


    def test_11(self):
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
            if i % 2 == 1:
                test_tx.add_input(root_tx.hash, i)
            test_tx.add_output(3, alice_pubkey)
            test_tx.add_output(4, alice_pubkey)
            test_tx.add_output(3, alice_pubkey)
            test_tx.sign_tx(bob_privkey, 0)
            if i % 2 == 1:
                test_tx.sign_tx(bob_privkey, 1)
            test_txs.append(test_tx)
            if i% 2 == 0:
                valid_txs.append(test_tx)

        validated_txs = handleTxs.handler(list(test_txs))
        self.assertEqual(validated_txs,valid_txs)


    def test_12(self):
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
        for i in range(5):
            test_tx = Transaction()
            test_tx.add_input(root_tx.hash, i)
            test_tx.add_output(3, alice_pubkey)
            test_tx.add_output(4, alice_pubkey)
            test_tx.add_output(3, alice_pubkey)
            test_tx.sign_tx(bob_privkey, 0)
            test_txs.append(test_tx)
            valid_txs.append(test_tx)

        for tx in valid_txs:
            test_tx = Transaction()
            test_tx.add_input(tx.hash, 0)
            test_tx.add_output(1, bob_pubkey)
            test_tx.sign_tx(alice_privkey, 0)
            test_txs.append(test_tx)

        validated_txs = handleTxs.handler(list(test_txs))
        self.assertEqual(validated_txs,test_txs)


    def test_13(self):
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
            test_tx.add_input(root_tx.hash if i % 2 == 0 else b'someRandomHash', i)
            test_tx.add_output(3, alice_pubkey)
            test_tx.add_output(4, alice_pubkey)
            test_tx.add_output(3, alice_pubkey)
            test_tx.sign_tx(bob_privkey, 0)
            test_txs.append(test_tx)
            if i% 2 == 0:
                valid_txs.append(test_tx)

        validated_txs = handleTxs.handler(list(test_txs))
        self.assertEqual(validated_txs,valid_txs)


    def test_14(self):  
        alice_pubkey, alice_privkey = rsa.newkeys(512)
        bob_pubkey, bob_privkey = rsa.newkeys(512)

        root_tx = Transaction()
        root_tx.add_input(b'', 0)
        root_tx.add_output(125232, alice_pubkey)
        root_tx.sign_tx(bob_privkey, 0)

        utxo_pool = UTXOPool()
        
        utxo_pool.add_UTXO(UTXO(root_tx.hash,0), root_tx.get_output(0))
        
        handleTxs = HandleTxs(utxo_pool)
        
        test_txs = list()
        previous_privkey = alice_privkey
        for i in range(10):
            pubkey, privkey = rsa.newkeys(512)
            tx = Transaction()
            tx.add_input(root_tx.hash if i == 0 else test_txs[i-1].hash, 0)
            tx.add_output(120000 / (i +1), pubkey)
            tx.sign_tx(previous_privkey, 0)
            test_txs.append(tx)
            previous_privkey = privkey
        

        self.assertEqual(test_txs, handleTxs.handler(test_txs[::-1]))


    def test_15(self):
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

        handleTxs.handler(list(test_txs))
        handled_second_time_txs = handleTxs.handler(list(test_txs))
        self.assertEqual(handled_second_time_txs, [])

if __name__ == "__main__":
    unittest.main()
