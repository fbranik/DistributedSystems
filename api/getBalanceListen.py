import requests
from flask import request, Blueprint, jsonify


def getBalanceListenConstructor(myNode):
    getBalance = Blueprint('getBalance', __name__)

    @getBalance.route('/', methods=['GET'])
    def getBalanceActions():
        return jsonify({'Balance': myNode.wallet_balance()}), 200

    return getBalance
