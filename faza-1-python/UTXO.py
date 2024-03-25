class UTXO():
    def __init__(self, tx_hash: bytes, index: int):
        self.__tx_hash = tx_hash
        self.__index = index
       

    def get_tx_hash(self):
        return self.__tx_hash

    def get_index(self):
        return self.__index 


    def __eq__(self, other):
        if not isinstance(other, UTXO):
            raise TypeError("Comprassion between objects of different classes not allowed")
        return self.__tx_hash == other.__tx_hash and self.__index == other.__index


    def __hash__(self):
        hash_value = 1
        hash_value = hash_value * 17 + self.__index
        hash_value = hash_value * 31 + hash(self.__tx_hash)
        return hash_value

    def __lt__(self, other):
            hash = other.tx_hash
            in_ = other.index

            if in_ > self.index:
                return True
            elif in_ < self.index:
                return False
            else:
                len1 = len(self.tx_hash)
                len2 = len(hash)

                if len2 > len1:
                    return True
                elif len2 < len1:
                    return False
                else:
                    for i in range(len1):
                        if hash[i] > self.tx_hash[i]:
                            return True
                        elif hash[i] < self.tx_hash[i]:
                            return False
                    return False
    
    def __gt__(self, other):
        return not self.__lt__(other)
