import requests
from flask import request, Blueprint, jsonify


def getChainLengthListenConstructor(myNode):
    getChainLength = Blueprint('getChainLength', __name__)

    @getChainLength.route('/', methods=['GET'])
    def getChainLengthActions():
        return jsonify({myNode.Id: len(myNode.chain.listOfBlocks)}), 200

    return getChainLength
