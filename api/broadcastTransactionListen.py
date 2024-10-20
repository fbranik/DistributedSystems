import requests
from flask import request, Blueprint
from backend.transaction import Transaction, dictToTransaction
from backend.node import Node
import json


def broadcastTransactionListenConstructor(myNode: Node):
    broadcastTransaction = Blueprint('broadcastTransaction', __name__)

    @broadcastTransaction.route('/', methods=['PUT'])
    def broadcastTransactionActions():
        response = {}
        payload = request.get_json()

        newTransaction = dictToTransaction(payload)

        if myNode.validate_transaction(newTransaction):
            for k, v in myNode.nodesTable.items():
                print(k, myNode.wallet_balance(v['walletAddress']))
            print("\n")
            myNode.addTransactionToBlock(newTransaction)

            transactions_log = open(f'logs/transactions{myNode.Id}_{myNode.chain.sizeOfBlock}_{myNode.difficulty}.txt',
                                    'a+')
            transactions_log.write(f'{newTransaction.timestamp}\n')
            transactions_log.close()
        return response, 200

    return broadcastTransaction
