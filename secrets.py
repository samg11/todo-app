from cryptography.fernet import Fernet
import os
import sys

def readSecret(key):
    #key_value_pairs = {}
    #with open('secretKeys.txt') as f:

    #    for key_value_pair in f.read().split('\n'):
    #        
    #        key_value_pair_splitted = key_value_pair.split('==')
    #        key_value_pairs[key_value_pair_splitted[0]] = key_value_pair_splitted[1]

    #return key_value_pairs[key]

    return os.environ[key]

def encrypt(string):
    encoded = string.encode()
    print(type(encoded))
    f = Fernet(readSecret('encryptionkey'))
    return f.encrypt(encoded).decode()

def decrypt(string):
    encoded = string.encode()
    print(type(encoded))
    f = Fernet(readSecret('encryptionkey'))
    decrypted = f.decrypt(encoded)
    print(type(decrypted))
    return decrypted.decode()

def test():

    string = 'test'
    print(string)
    
    encrypted = encrypt(string)
    print(encrypted)

    decrypted = decrypt(encrypted)
    print(decrypted.decode())

if __name__ == "__main__":
    test()