from flask import Flask, jsonify, request, render_template, flash
import logging
from flask_bootstrap import Bootstrap
import requests
import pandas as pd
from re import sub

app = Flask(__name__)
log = logging.getLogger('werkzeug')
log.disabled = True
Bootstrap(app)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'


def trViewToHTML(view):
    df = pd.DataFrame(data=view)
    df = df.fillna(' ').T
    temp = df.to_html()
    return temp


@app.route('/', methods=["GET", "POST"])
def index():
    url = f'http://{nodeIp}:{nodePort}/api/getNodeInfo'
    res = requests.get(url)
    nodes = res.json()

    url = f'http://{nodeIp}:{nodePort}/api/getBalance'
    res = requests.get(url)
    balance = res.json()['Balance']

    url = f'http://{nodeIp}:{nodePort}/api/viewTransactions'
    res = requests.get(url, verify=False)
    view = trViewToHTML(res.json())

    if request.method == 'POST':

        if request.form["action"] == 'refreshBalance':
            url = f'http://{nodeIp}:{nodePort}/api/getBalance'
            res = requests.get(url)
            balance = res.json()['Balance']
            return render_template('index.html', balance=balance, nodeList=nodes, view=view)

        elif request.form['action'] == 'transaction':
            recipientNodeId = request.form['recipient']
            transactionAmount = request.form['amount']

            if transactionAmount != '':
                url = f'http://{nodeIp}:{nodePort}/api/createNewTransaction/?recipientId={int(recipientNodeId)}&amount={int(transactionAmount)}'
                res = requests.get(url)
                if res.status_code == 500:
                    flash(res.json()['Error'])
            else:
                flash("Not a valid amount of NBCs")
            url = f'http://{nodeIp}:{nodePort}/api/getBalance'
            res = requests.get(url)
            balance = res.json()['Balance']
            return render_template('index.html', balance=balance, nodeList=nodes, view=view)

        elif request.form['action'] == 'view':
            pass
        else:
            pass  # unknown
    elif request.method == 'GET':
        return render_template('index.html', balance=balance, nodeList=nodes, view=view)

    return render_template("index.html", balance=balance, nodeList=nodes, view=view)


if __name__ == '__main__':
    from argparse import ArgumentParser

    parser = ArgumentParser()
    parser.add_argument('-p', '--nodePort', default=5000,
                        type=int, help='port the node is running')
    parser.add_argument('-a', '--nodeAddress', default='127.0.0.1',
                        type=str, help='ip address of the node')

    parser.add_argument('-fa', '--frontendAddress', default='', type=str,
                        help='ip to run frontend on')

    parser.add_argument('-fp', '--frontendPort', default='', type=str,
                        help='port to run frontend on')

    args = parser.parse_args()

    myPort = args.frontendPort
    myIp = args.frontendAddress

    nodePort = args.nodePort
    nodeIp = args.nodeAddress
    print(myIp, myPort)
    app.run(host=myIp, port=myPort)
