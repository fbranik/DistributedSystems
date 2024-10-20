import requests
from flask import request, Blueprint, jsonify
from backend.node import Node
import requests
from threading import Thread
from time import sleep
from os.path import exists
from os import remove as removeFile


def runTestsListenConstructor(myNode: Node, myIp, myPort):
    runTests = Blueprint('runTests', __name__)

    @runTests.route('/', methods=['GET'])
    def runTestsActions():
        nodes = request.args.get('nodes', default=5, type=int)
        if exists(f'logs/transactions{myNode.Id}_{myNode.chain.sizeOfBlock}_{myNode.difficulty}.txt'):
            removeFile(f'logs/transactions{myNode.Id}_{myNode.chain.sizeOfBlock}_{myNode.difficulty}.txt')
        testThread = Thread(target=transactionRequest, args=(myNode, nodes, myIp, myPort,))
        testThread.start()
        return jsonify({'Status': 'Ok'}), 200

    return runTests


def transactionRequest(myNode: Node, nodes, myIp, myPort):
    f = open(f"transactions/{nodes}nodes/transactions{myNode.Id}.txt", "r")
    lines = f.readlines()
    for line in lines:
        t = line.split(' ')
        receiver = int(t[0][2:])
        amount = int(t[1])
        addressString = f'http://{myIp}:{myPort}/api/createNewTransaction/?recipientId={receiver}&amount={amount}'
        bootstrapResponse = requests.get(addressString)
        # sleep(2)
    f.close()
