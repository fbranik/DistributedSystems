import binascii

from cryptography.hazmat.primitives import serialization as crypto_serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.backends import default_backend as crypto_default_backend
import json
from time import time
from urllib.parse import urlparse
from uuid import uuid4
from backend.transaction import Transaction


class Wallet:

    def __init__(self, privateKeyFile=None, publicKeyFile=None, transactionsFile=None):

        privateKeyObject = rsa.generate_private_key(backend=crypto_default_backend(),
                                                    public_exponent=65537,
                                                    key_size=1024
                                                    )

        self.private_key = privateKeyObject.private_bytes(crypto_serialization.Encoding.PEM,
                                                          crypto_serialization.PrivateFormat.PKCS8,
                                                          crypto_serialization.NoEncryption()
                                                          ).hex()

        self.public_key = privateKeyObject.public_key().public_bytes(crypto_serialization.Encoding.OpenSSH,
                                                                     crypto_serialization.PublicFormat.OpenSSH
                                                                     ).hex()
        self.transactions = []

    def balance(self):
        balance = 0
        for iTransaction in self.transactions:
            balance += iTransaction.value
        if balance >= 0:
            return balance
        else:
            return -1
