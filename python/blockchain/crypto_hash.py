"""
" Won Seok Yang
" Blockchain 
" Playing with the different hasing functions of Bitcoin and Ethereum to get a better understanding
"""

from cryptos import *
import bitcoin
import random
import sha3
import hashlib

bitcoinBlockchain = Bitcoin(testnet=True)

class CryptoGen:
    def genPrivateKey_(self):
        valid_key = False
        while not valid_key:
            priv_key=bitcoin.random_key()
            decoded_priv_key=bitcoin.decode_privkey(priv_key, 'hex')
            valid_key=0<decoded_priv_key<bitcoin.N
        return priv_key, decoded_priv_key

    # Generate public key (also to be used for Ethereum)
    def genPublicKey_(self, decoded_private_key):
        #Public key is a pair of x,y coords
        public_key = bitcoin.fast_multiply(bitcoin.G, decoded_private_key)
        # print ("Public Key (x,y) coordinates is:", public_key)
        hex_encoded_public_key = bitcoin.encode_pubkey(public_key,'hex')
        return public_key, hex_encoded_public_key

    def genCompressedPublicKey_(self, public_key):
        (x, y) = public_key
        if (y % 2) == 0:
            compressed_prefix = '02'
        else:
            compressed_prefix = '03'
        hex_compressed_public_key = compressed_prefix + bitcoin.encode(x, 16)
        return hex_compressed_public_key

    def kcck256(self):
        (x,y), hex_encoded_public_key = self.genPublicKey_(self.decoded_private_key)
        return sha3.keccak_256(hex_encoded_public_key[1:].encode('utf-8')).hexdigest()

    def ethAddress(self):
        #keccak256(K) where K is the public key
        K = self.hex_encoded_public_key
        K_hash = sha3.keccak_256(K[2:].encode('utf-8')).hexdigest()
        eth_addr = K_hash[40:]
        return eth_addr

    def ethAddressChecksum(self, eth_addr):
        addr_hash = sha3.keccak_256(eth_addr.encode('utf-8')).hexdigest()
        checksum_temp = ""
        for count, char in enumerate(eth_addr):
            if char in "1234567890":    #skip numbers
                checksum_temp += char
            elif char in "abcdef":      #check if the hash[count] is >=8
                addr_hash_int = int(addr_hash[count], 16)
                if addr_hash_int >= 8:
                    checksum_temp += char.upper()
                else:
                    checksum_temp += char
        return checksum_temp
    
    def __init__(self):
        self.private_key, self.decoded_private_key = self.genPrivateKey_()
        self.public_key, self.hex_encoded_public_key = self.genPublicKey_(self.decoded_private_key)
        self.hex_compressed_public_key = self.genCompressedPublicKey_(self.public_key)

    def printValues(self):
        # Generate a private key
        # print("Bitcoin Private Key hex is:\t", self.private_key)
        # print("Bitcoin Private Key decimal is:\t", self.decoded_private_key)

        # Generated public key from private key
        print("Bitcoin Public Key (hex) is:\t\t\t\t", self.hex_encoded_public_key)

        # Generated compressed public key from private key
        print ("Bitcoin Compressed Public Key (hex) is:\t\t\t", self.hex_compressed_public_key)
        
        # TestNet generated address from uncompressed public key
        print ("Bitcoin Address (b58check) is:\t\t\t\t", bitcoin.pubkey_to_address(self.public_key))
        
        # TestNet generated address from compressed public key
        print ("Bitcoin Compressed Bitcoin Address (b58check) is:\t", bitcoin.pubkey_to_address(self.hex_compressed_public_key))

        ### Ethereum
        # Generated keccak256 hash using the Bitcoin public key without prefix 
        print ("keccak256 Public Key Hash:\t\t\t\t", self.kcck256())

        # Generated checksum address using keccak256 hash
        print("Ethereum Public Address: \t\t\t\t", hex(int(self.ethAddress(), 16)))
        checksum_addr = self.ethAddressChecksum(self.ethAddress())
        print("Ethereum Public Address Checksum: \t\t\t 0x"+checksum_addr)

crypto = CryptoGen()
crypto.printValues()