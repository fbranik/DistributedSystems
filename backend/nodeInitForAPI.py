from backend.block import Block, dictToBlock
from backend.transaction import Transaction, dictToTransaction
import requests


def nodeInitForAPI(myNode, blockchain, numberOfNodes, myIp, myPort, isBootstrap, bootstrapAddress, bootstrapPort):
    # if this is the bootstap node, add the first entry to the table
    if isBootstrap:
        # Create the genesis block and add it to the blockchain
        genesisBlock = Block(blockchain.sizeOfBlock)
        transactionZero = Transaction('0', myNode.wallet.public_key, 100 * numberOfNodes, [])
        genesisBlock.add_transaction(transactionZero)
        myNode.wallet.transactions.append(transactionZero)
        genesisBlock.previousHash = '1'
        genesisBlock.getHash()
        genesisBlock.nonce = 0
        blockchain.addBlock(genesisBlock)

        # Add my info to myNode's table
        myNode.syncNodesTable(myNode.Id, myNode.wallet.public_key,
                              myNode.wallet_balance(myNode.wallet.public_key), myIp, myPort)

        # Initialize transactionZero utxos
        transactionZeroOutputs = transactionZero.transaction_outputs
        for transaction_output_id, utxo in transactionZeroOutputs.items():
            if utxo['recipient_id'] != '0':
                utxoBootstrap = utxo
        myNode.utxos[myNode.wallet.public_key][utxoBootstrap['transaction_output_id']] = utxoBootstrap

    # if the node isn't the bootstrap node, then communicate with it
    # to get my ID and to synchronise the node tables
    else:
        # make a request to the boostrap node and process the data it returns
        addressString = f'http://{bootstrapAddress}:{bootstrapPort}/api/newNodeAdded'
        bootstrapResponse = requests.get(addressString)
        myNode.Id = int(bootstrapResponse.json()['newNodeId'])
        myNode.nodeCount = myNode.Id + 1
        tempChainList = bootstrapResponse.json()['blockchainState']

        # get the blocks from the blockchain that was sent
        for iBlockDict in reversed(tempChainList):
            iBlock = dictToBlock(iBlockDict)
            myNode.chain.addBlock(iBlock)
        print(f"Valid chain: {myNode.validate_chain()}")

        # get the transactions of the unmined running block of the bootstrap node
        myNode.runningBlock.listOfTransactions.update(bootstrapResponse.json()['unminedTransactions'])

        # Add my info to myNode's table
        myNode.syncNodesTable(myNode.Id, myNode.wallet.public_key,
                              myNode.wallet.balance(), myIp, myPort)

        # Get the bootstrap node's table
        bootstrapResponse = requests.get(
                f'http://{bootstrapAddress}:{bootstrapPort}/api/syncNodesTable')
        bootstrapNodesTable = bootstrapResponse.json()['nodesTable']

        # Write the entries to myNode's table
        for id, infoDict in bootstrapNodesTable.items():
            myNode.syncNodesTable(
                    int(id), infoDict['walletAddress'], infoDict['walletBalance'], infoDict['ip'], infoDict['port'],
                    bootstrapResponse.json()['utxos'])

        # Broadcast my info to every node found on myNode's updated table using a PUT request
        for id, tableInfoDict in myNode.nodesTable.items():
            if myNode.Id != id:
                addressString = f"http://{tableInfoDict['ip']}:{tableInfoDict['port']}/api/syncNodesTable"
                requests.put(addressString, json={'myNodesTable': myNode.nodesTable, 'utxo': myNode.utxos})
