import requests
from flask import request, Blueprint, jsonify


def getChainListenConstructor(myNode):
    getChain = Blueprint('getChain', __name__)

    @getChain.route('/', methods=['GET'])
    def getChainActions():
        return jsonify({"chain": myNode.chain.getlistOfDictBlocks()}), 200

    return getChain
