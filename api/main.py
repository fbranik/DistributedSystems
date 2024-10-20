import requests
from flask import Flask, jsonify, request, render_template
from flask_cors import CORS
import urllib.request
import json
from os.path import dirname, realpath
from sys import path
import atexit

thisFilePath = dirname(realpath(__file__))
noobcashPath = dirname(thisFilePath)
path.append(noobcashPath)

from api.createNewTransactionListen import createNewTransactionListenConstructor
from api.syncNodesTableListen import syncNodesTableListenConstructor
from api.newNodeAddedListen import newNodeAddedListenConstructor
from api.broadcastTransactionListen import broadcastTransactionListenConstructor
from api.broadcastBlockListen import broadcastBlockListenConstructor
from api.getBalanceListen import getBalanceListenConstructor
from api.viewTransactionsListen import viewTransactionsListenConstructor
from api.runTestsListen import runTestsListenConstructor
from api.getChainListen import getChainListenConstructor
from api.getChainLengthListen import getChainLengthListenConstructor
from backend.blockchain import Blockchain
from backend.node import Node
from api.nodeWatcher import nodeWatcher
from threading import Thread
from backend.nodeInitForAPI import nodeInitForAPI
import logging
from os.path import exists
from os import remove as removeFile

app = Flask(__name__)
log = logging.getLogger('werkzeug')
log.disabled = True
CORS(app)

bootstrapPort = '5000'


def shutdown_node():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()


@app.route('/shutdown', methods=["GET"])
def shutdown():
    shutdown_node()
    return '\nNode shutting down...\n'


@app.route('/api/writeBlockLogs', methods=["GET"])
def writeBlockLogs():
    if exists(f'logs/block{myNode.Id}_{myNode.chain.sizeOfBlock}_{myNode.difficulty}_{myNode.numOfMiningThreads}.txt'):
        removeFile(
                f'logs/block{myNode.Id}_{myNode.chain.sizeOfBlock}_{myNode.difficulty}_{myNode.numOfMiningThreads}.txt')

    block_log = open(
            f'logs/block{myNode.Id}_{myNode.chain.sizeOfBlock}_{myNode.difficulty}_{myNode.numOfMiningThreads}.txt',
            'w+')
    for iBlock in myNode.chain.listOfBlocks:
        block_log.write(f'{iBlock.addedToChainTimestamp - iBlock.miningStartedTimestamp}\n')
    block_log.close()
    return 'writing block logs\n', 200


@app.route('/api/getNodeInfo', methods=["GET"])
def getNodeInfo():
    toSend = []
    for k in myNode.nodesTable.keys():
        if k == myNode.Id:
            continue
        toSend.append(k)
    return jsonify(toSend)


if __name__ == '__main__':
    from argparse import ArgumentParser

    parser = ArgumentParser()
    parser.add_argument('-p', '--port', default=5000,
                        type=int, help='port to listen on')
    parser.add_argument('-a', '--ipAddress', default='127.0.0.1',
                        type=str, help='ip address to be used')
    parser.add_argument('-b', '--bootstrapAddress', default='', type=str,
                        help='ip of Bootstrap Node')
    parser.add_argument('-n', '--numberOfNodes', default=5, type=int,
                        help='Number of Nodes that will participate')
    parser.add_argument('-d', '--miningDifficulty', default=5, type=int,
                        help='Number of of leading 0s in a valid Block hash')
    parser.add_argument('-c', '--blockSize', default=5, type=int,
                        help='Transactions per Block')
    parser.add_argument('-t', '--numOfMiningThreads', default=1, type=int,
                        help='Number of Threads to be used in mining')

    args = parser.parse_args()
    myPort = args.port
    myIp = args.ipAddress
    bootstrapAddress = args.bootstrapAddress
    isBootstrap = False
    if bootstrapAddress == '':
        bootstrapAddress = myIp
        isBootstrap = True
    numberOfNodes = args.numberOfNodes
    difficulty = args.miningDifficulty
    blockSize = args.blockSize
    numOfMiningThreads = args.numOfMiningThreads

    blockchain = Blockchain(blockSize)
    myNode = Node(blockchain=blockchain, isBootstrap=isBootstrap, difficulty=difficulty,
                  numOfMiningThreads=numOfMiningThreads)

    newNodeAdded = newNodeAddedListenConstructor(myNode)
    app.register_blueprint(newNodeAdded, url_prefix='/api/newNodeAdded')

    syncNodesTable = syncNodesTableListenConstructor(myNode)
    app.register_blueprint(syncNodesTable, url_prefix='/api/syncNodesTable')

    createNewTransaction = createNewTransactionListenConstructor(myNode)
    app.register_blueprint(createNewTransaction,
                           url_prefix='/api/createNewTransaction')

    broadcastTransaction = broadcastTransactionListenConstructor(myNode)
    app.register_blueprint(broadcastTransaction, url_prefix='/api/broadcastTransaction')

    broadcastBlock = broadcastBlockListenConstructor(myNode)
    app.register_blueprint(broadcastBlock, url_prefix='/api/broadcastBlock')

    getBalance = getBalanceListenConstructor(myNode)
    app.register_blueprint(getBalance, url_prefix='/api/getBalance')

    viewTransactions = viewTransactionsListenConstructor(myNode)
    app.register_blueprint(viewTransactions, url_prefix='/api/viewTransactions')

    runTests = runTestsListenConstructor(myNode, myIp, myPort)
    app.register_blueprint(runTests, url_prefix='/api/runTests')

    getChain = getChainListenConstructor(myNode)
    app.register_blueprint(getChain, url_prefix='/api/getChain')

    getChainLength = getChainLengthListenConstructor(myNode)
    app.register_blueprint(getChainLength, url_prefix='/api/getChainLength')

    # Write my public and private key files
    # myNode.writeWalletFiles('private{}.pem'.format(myPort),
    #                         'public{}.key'.format(myPort))

    nodeInitForAPI(myNode, blockchain, numberOfNodes, myIp, myPort, isBootstrap, bootstrapAddress, bootstrapPort)

    nodeWatcher = Thread(target=nodeWatcher, args=(myNode,))
    # nodeWatcher.start()

    app.run(host=myIp, port=myPort)
