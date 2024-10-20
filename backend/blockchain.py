from time import time


class Blockchain:
    """
    Implements the list of blocks.
    Initialise with a given size of block
    (maximum number of transactions per block)
    """

    def __init__(self, blockSize):
        self.listOfBlocks = []
        self.sizeOfBlock = blockSize

    def addBlock(self, block, fromConflict=False):
        if not fromConflict:
            block.addedToChainTimestamp = time()
        self.listOfBlocks.append(block)

    def getlistOfDictBlocks(self, count=None):
        # used to easily transfer the state of the blockchain using requests
        if count is not None:
            return [block.toDict() for block in self.listOfBlocks[-count:]]
        return [block.toDict() for block in self.listOfBlocks]

    def getLastBlock(self):
        if len(self.listOfBlocks) == 0:
            return None
        return self.listOfBlocks[-1]
