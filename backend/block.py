from backend.transaction import Transaction, dictToTransaction
from cryptography.hazmat.primitives.hashes import SHA256
from cryptography.hazmat.primitives import hashes
from time import time
from collections import OrderedDict


class Block:
    """
    Implements blockchain block.
    Initialize after having initialized the blockchain
    """

    def __init__(self, capacity):
        """
        Initializes a block that is to be filled validated
        and then added to the blockchain
        """
        self.previousHash = None
        self.timestamp = time()
        self.hash = None
        self.nonce = None
        self.listOfTransactions = OrderedDict()
        self.capacity = capacity
        self.addedToChainTimestamp = time()
        self.miningStartedTimestamp = self.addedToChainTimestamp

    def toDict(self):
        outDict = {
                'previousHash'          : self.previousHash,
                'timestamp'             : self.timestamp,
                'nonce'                 : self.nonce,
                'listOfTransactions'    : self.listOfTransactions,
                'capacity'              : self.capacity,
                'miningStartedTimestamp': self.miningStartedTimestamp
        }

        return outDict

    def __len__(self):
        return len(self.listOfTransactions)

    def getAllTransactionsIds(self):
        """
        Aux function to return a string of
        all the transactions Ids in the block
        so that it can be hashed
        """
        transactionsIdsString = ''

        for iTransactionId in sorted(self.listOfTransactions.keys()):
            transactionsIdsString += iTransactionId

        return transactionsIdsString

    def getHash(self):
        """
        Method that returns hash of block data
        """

        sha256Hasher = hashes.Hash(SHA256())
        transactionsIdsString = self.getAllTransactionsIds()
        dataToHash = [self.previousHash.encode(), str(self.timestamp).encode(),
                      transactionsIdsString.encode(), str(self.nonce).encode()]

        for iData in dataToHash:
            sha256Hasher.update(iData)
        finalDigest = sha256Hasher.finalize()
        self.hash = finalDigest

        return self.hash.hex()

    def add_transaction(self, transaction: Transaction):
        """
        Adds transaction to the block
        Returns True if the block is full
        so that the callee can check if
        it can start mining the block.
        """
        self.listOfTransactions[transaction.transaction_id] = transaction.toDict()
        return len(self) == self.capacity


def dictToBlock(blockDict):
    previousHash = blockDict['previousHash']
    timestamp = blockDict['timestamp']
    nonce = blockDict['nonce']
    listOfTransactions = blockDict['listOfTransactions']
    capacity = blockDict['capacity']
    miningStartedTimestamp = blockDict['miningStartedTimestamp']

    block = Block(capacity)

    block.previousHash = previousHash
    block.timestamp = timestamp
    block.miningStartedTimestamp = miningStartedTimestamp
    block.nonce = nonce
    block.listOfTransactions = listOfTransactions
    # call getHash to dynamically generate the hash

    return block
