import requests
from backend.transaction import Transaction, dictToTransaction
from backend.node import Node
from flask import Flask, jsonify, request, render_template, Blueprint
import threading
from time import sleep


def syncNodesTableListenConstructor(myNode: Node):
    syncNodesTable = Blueprint('syncNodesTable', __name__)

    @syncNodesTable.route('/', methods=['GET', 'PUT'])
    def syncNodesTableActions():

        def broadCastFirstTransaction(firstTransaction):
            sleep(1)
            myNode.broadcast_transaction(firstTransaction)

        if request.method == 'GET':
            response = {"nodesTable": myNode.nodesTable, "utxos": myNode.utxos}
            return jsonify(response), 200
        if request.method == 'PUT':
            response = {}
            payload = request.get_json()
            for id, tableInfoDict in payload['myNodesTable'].items():
                if int(id) not in myNode.nodesTable:
                    myNode.syncNodesTable(int(id), tableInfoDict['walletAddress'], tableInfoDict['walletBalance'],
                                          tableInfoDict['ip'], tableInfoDict['port'], payload['utxo'])
                    if myNode.Id == 0 and int(id) != 0:
                        print('ela')
                        firstTransaction = myNode.create_transaction(int(id), 100)
                        firstTransaction.sign_transaction(myNode.wallet.private_key)
                        for k, v in myNode.nodesTable.items():
                            print(k, myNode.wallet_balance(v['walletAddress']))

                        thread = threading.Thread(target=broadCastFirstTransaction,
                                                  kwargs={'firstTransaction': firstTransaction})
                        thread.start()
            response = jsonify({'Status': 'Added'})
            response.status_code = 201
            return response

    return syncNodesTable
