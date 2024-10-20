import requests
from flask import request, Blueprint, jsonify


def createNewTransactionListenConstructor(myNode):
    createNewTransaction = Blueprint('createNewTransaction', __name__)

    @createNewTransaction.route('/', methods=['GET'])
    def createNewTransactionActions():
        # Get the transaction details from the request and make the required changes
        senderId = myNode.Id
        recipientId = request.args.get(
                'recipientId', default=myNode.Id, type=int)
        amount = request.args.get('amount', default=0, type=int)

        # check to see if the senderAddress and the recipientAddress are in the nodesTable
        if senderId in myNode.nodesTable and recipientId in myNode.nodesTable:
            transaction = myNode.create_transaction(int(recipientId), amount)
            if transaction is not None:
                transaction.sign_transaction(myNode.wallet.private_key)
                myNode.broadcast_transaction(transaction)
                for k, v in myNode.nodesTable.items():
                    print(k, myNode.wallet_balance(v['walletAddress']))
                print("\n")
                return jsonify({'Status': 'Ok'}), 200
            else:
                myBalance = myNode.wallet_balance(myNode.wallet.public_key)
                return jsonify({'Error': "Not enough NBCs: Sender Balance={}, Transaction amount = {}\n".format(
                        myBalance, amount)}), 500
        else:
            return jsonify({'Error': "Invalid nodes Table\n"}), 500

    return createNewTransaction
