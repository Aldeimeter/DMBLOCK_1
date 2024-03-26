import sys
import rsa
from UTXO import UTXO
import struct
import hashlib
class Transaction():
    class Input():
        def __init__(self, prev_tx_hash: bytes, output_index: int):
            self.prev_tx_hash = prev_tx_hash
            self.output_index = output_index
            self.signature = b''
        

        def add_signature(self, signature: bytes):
            self.signature = signature


        def __eq__(self, other):
            return isinstance(self, Input) and isinstance(other, Input) and self.prev_tx_hash == other.prev_tx_hash and self.output_index == other.output_index and self.signature == other.signature


        def __hash__(self):
            hash = 1
            hash = hash * 17 + hash(self.prev_tx_hash)
            hash = hash * 31 + self.output_index
            hash = hash * 31 + hash(self.signature)
            return hash


    class Output():
        def __init__(self, value: float, address: rsa.PublicKey):
            self.address = address
            self.value = value
        

        def __eq__(self, other):
            return isinstance(self, Output) and isinstance(other, Output) and self.address == other.address and self.value == other.value



        def __hash__(self):
            hash = 1
            hash = hash * 17 + int(self.value * 10000)
            hash = hash * 31 + hash(address.e)
            hash = hash * 31 + hash(address.n)
            return hash


    def __init__(self, inputs = None, outputs = None, hash = None, coinbase = False):
        if inputs is not None:
            self.inputs = list(inputs)
        else:
            self.inputs = list()
        if inputs is not None:
            self.outputs = list(outputs)
        else:
            self.outputs = list()
        self.hash = hash
   
    def __eq__(self, other):
        return isinstance(self, Transaction) and isinstance(other, Transaction) and self.inputs == other.inputs and self.outputs == other.outputs and self.hash == other.hash 


    def __hash__(self):
        hash = 1 
        for input in self.inputs:
            hash = hash * 31 + hash(input)

        for output in self.outputs:
            hash = hash * 31 + hash(output)

        return hash 


    def add_input(self,prev_tx_hash: bytes, output_index: int):
        self.inputs.append(self.Input(prev_tx_hash, output_index))


    def add_output(self, value: float, address: str):
        self.outputs.append(self.Output(value, address))
    

    def remove_input_by_index(self, index: int):
        self.inputs.pop(index)
    

    def remove_input_by_UTXO(self,ut: UTXO):
        for input in self.inputs:
            utxo = UTXO(input.prev_tx_hash, input.output_index)
            if (utxo.equals(ut)):
                self.inputs.remove(input)
                return


    def get_data_to_sign(self, index: int):
        sigD = b''
        if index > len(self.inputs):
            return None
        inp = self.inputs[index]
        prev_tx_hash = inp.prev_tx_hash
        output_index = inp.output_index
        sigD = prev_tx_hash + struct.pack('i',output_index)
        for output in self.outputs:
            sigD += struct.pack("f",output.value)
            hex_str = hex(output.address.n)[2:]
            if len(hex_str) % 2 != 0:
                hex_str = '0' + hex_str
            byte_str = bytes.fromhex(hex_str)

           
            sigD += struct.pack(f'I{len(byte_str)}s', output.address.e, byte_str)
        return sigD
    

    def add_signature(self,signature: bytes, index: int):
        self.inputs[index].add_signature(signature)


    def get_tx(self) -> bytes:
        tx = b''   
        for input in self.inputs:
            tx += input.prev_tx_hash + struct.pack('i', input.output_index) + input.signature 
        for i in range(len(self.outputs)):
            hex_str = hex(self.outputs[i].address.n)[2:]
            if len(hex_str) % 2 != 0:
                hex_str = '0' + hex_str
            byte_str = bytes.fromhex(hex_str)

            tx += struct.pack(f'ii{len(byte_str)}s', i, self.outputs[i].address.e, byte_str)
        return tx


    def finalize(self):
        self.hash = hashlib.sha256(self.get_tx()).digest()
    

    def num_outputs(self):
        return len(self.outputs)


    def num_inputs(self):
        return len(self.inputs)


    def get_output(self, index: int):
        if index < len(self.outputs):
            return self.outputs[index]
        return None


    def get_input(self, index: int):
        if index < len(self.inputs):
            return self.inputs[index]
        return None

    
    def sign_tx(self, privkey: rsa.PrivateKey, input: int):
        signature = rsa.sign(self.get_data_to_sign(input), privkey, 'SHA-256')
        self.add_signature(signature, input)
        self.finalize()
    
    @staticmethod
    def create_coinbase(value, address):
        coinbase = Transaction([Transaction.Input(b'',0)],[Transaction.Output(value, address)],None, True)
        coinbase.finalize()
        return coinbase

        

