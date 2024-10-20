import requests
from flask import Flask, jsonify, request, render_template, Blueprint
from backend.node import Node


def newNodeAddedListenConstructor(myNode: Node):
    newNodeAdded = Blueprint('newNodeAdded', __name__)

    @newNodeAdded.route('/', methods=['GET', 'PUT'])
    def newNodeAddedActions():
        if request.method == 'GET':
            # increment the node count
            myNode.nodeCount += 1
            # send the newNode count to every registered node in the network
            # using a PUT request
            newNodeCountJSON = {'newNodeCount': myNode.nodeCount}
            for id, tableInfoDict in myNode.nodesTable.items():
                if myNode.Id != id:
                    addressString = f"http://{tableInfoDict['ip']}:{tableInfoDict['port']}/newNodeAdded"
                    requests.put(addressString, json=newNodeCountJSON)

            # send the new node id and the current state of the blockchain
            chainState = myNode.chain.getlistOfDictBlocks()
            response = {'newNodeId'          : myNode.nodeCount - 1, 'blockchainState': chainState,
                        'unminedTransactions': myNode.runningBlock.listOfTransactions}
            return jsonify(response), 200
        if request.method == 'PUT':
            # update my node count
            response = {}
            payload = request.get_json()
            myNode.nodeCount = int(payload['newNodeCount'])
            response = jsonify({'Status': 'Updated'})
            response.status_code = 201
            return response

    return newNodeAdded
