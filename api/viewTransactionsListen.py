import requests
from flask import request, Blueprint, jsonify


def viewTransactionsListenConstructor(myNode):
    viewTransactions = Blueprint('viewTransactions', __name__)

    @viewTransactions.route('/', methods=['GET'])
    def viewTransactionsActions():
        return jsonify(myNode.view_transactions()), 200

    return viewTransactions
