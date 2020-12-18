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
    try:
        encoded = string.encode()
        f = Fernet(readSecret('encryptionkey'))
        return f.encrypt(encoded).decode()

    except:
        print('encryption error')

def decrypt(string):
    try:
        encoded = string.encode()
        f = Fernet(readSecret('encryptionkey'))
        decrypted = f.decrypt(encoded)
        return decrypted.decode()
    
    except:
        print('decryption error')

def test():

    if not len(sys.argv) < 2:
        string = sys.argv[1]
        
    else:
        string = 'test'

    print(f"original string:  {string}")
    
    encrypted = encrypt(string)
    print(f"encrypted string: {encrypted}")

    decrypted = decrypt(encrypted)
    print(f"decrypted string: {decrypted}")

if __name__ == "__main__":
    test()