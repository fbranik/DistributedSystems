from backend.transaction_input import TransactionInput
from backend.transaction_output import TransactionOutput
from cryptography.hazmat.primitives import serialization as serialization
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives.hashes import SHA256
import cryptography.hazmat.primitives.hashes as hashes
from time import time


class Transaction:
    """
    Implements a transaction
    """

    def __init__(self, sender_address, recipient_address, value, transaction_inputs):

        self.sender_address = sender_address  # wallet's public key
        self.receiver_address = recipient_address  # wallet's public key
        self.amount = value
        self.signature = None

        # The transaction_id uses a
        # timestamp as well as the transaction string
        sha256Hasher = hashes.Hash(SHA256())
        self.timestamp = time()
        dataToHash = str(self)
        sha256Hasher.update(dataToHash.encode())

        finalDigest = sha256Hasher.finalize()
        self.transaction_id = finalDigest.hex()

        self.transaction_inputs = transaction_inputs
        receiver_out = TransactionOutput(self.transaction_id, recipient_address, self.amount)
        change = -self.amount

        for transaction_input in transaction_inputs:
            change += transaction_input['amount']

        sender_out = TransactionOutput(self.transaction_id, sender_address, change)

        self.transaction_outputs = {}
        self.transaction_outputs[receiver_out['transaction_output_id']] = receiver_out
        self.transaction_outputs[sender_out['transaction_output_id']] = sender_out

    def __str__(self):
        return f'{self.sender_address}{self.receiver_address}{str(self.amount)}{self.timestamp}'

    def toDict(self):
        outDict = {
                'sender_address'     : self.sender_address,
                'receiver_address'   : self.receiver_address,
                'amount'             : self.amount,
                'timestamp'          : self.timestamp,
                'transaction_id'     : self.transaction_id,
                'transaction_inputs' : self.transaction_inputs,
                'transaction_outputs': self.transaction_outputs
        }
        if self.signature is not None:
            outDict['signature'] = self.signature.hex()
        return outDict

    def getHash(self):
        return self.transaction_id

    def sign_transaction(self, private_key):
        """
        Sign transaction with private key
        """
        sender_private_key = serialization.load_pem_private_key(bytes.fromhex(private_key), password=None)
        signatureData = (str(self)).encode()
        self.signature = sender_private_key.sign(signatureData,
                                                 padding.PSS(mgf=padding.MGF1(SHA256()),
                                                             salt_length=padding.PSS.MAX_LENGTH),
                                                 SHA256()
                                                 )

    def verify_signature(self):
        """
        Verfiy a Transaction using a public key
        If the tansaction id matches the
        give publi_key matches the senders return true
        else False
        """
        sender_public_key = serialization.load_ssh_public_key(bytes.fromhex(self.sender_address))
        signatureData = (str(self)).encode()

        try:
            sender_public_key.verify(self.signature,
                                     signatureData,
                                     padding.PSS(
                                             mgf=padding.MGF1(SHA256()),
                                             salt_length=padding.PSS.MAX_LENGTH),
                                     SHA256()
                                     )
        except:
            print('not signed well')
            return False

        return True


def dictToTransaction(transactionDict):
    sender_address = transactionDict['sender_address']
    receiver_address = transactionDict['receiver_address']
    amount = transactionDict['amount']
    timestamp = transactionDict['timestamp']
    transaction_id = transactionDict['transaction_id']
    transaction_inputs = transactionDict['transaction_inputs']
    transaction_outputs = transactionDict['transaction_outputs']

    transaction = Transaction(sender_address, receiver_address, amount, transaction_inputs)

    if sender_address != '0':
        # case for transaction Zero in the genesis block
        signature = transactionDict['signature']
        transaction.signature = bytes.fromhex(signature)

    transaction.timestamp = timestamp
    transaction.transaction_id = transaction_id
    transaction.transaction_outputs = transaction_outputs

    return transaction
