__author__ = 'jinlong'
from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP



key = RSA.generate(1024)
pubkey = key.publickey().key