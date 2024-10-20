import sys
import requests
import json
from argparse import ArgumentParser
from colorama import Fore, Back, Style

if len(sys.argv) == 1:
    print('Usage: ./cli.py ip:port')
    print('No ip:port specified')
    print('Using 127.0.0.1:5000')
    address = '127.0.0.1:5000'
elif len(sys.argv) == 2:
    address = sys.argv[1]
else:
    print('Usage: ./cli.py ip:port')
    exit(0)

print("Give your desired action in the prompt below...")
while 1:
    print(Fore.GREEN + "➤" + Style.RESET_ALL, end=' ')
    try:
        inp = input().split(' ')
        cmd = inp[0]
        args = inp[1:]
        if cmd == 't':
            if len(args) != 2:
                raise Exception('Invalid arguments')
            if not args[0].isnumeric() & args[1].isnumeric():
                raise Exception('Invalid arguments')
            url = f'http://{address}/api/createNewTransaction/?recipientId={args[0]}&amount={args[1]}'
            res = requests.get(url, verify=False)
            print(json.dumps(res.json(), indent=4))
        elif cmd == 'view':
            if len(args) != 0:
                raise Exception('Invalid arguments')
            url = f'http://{address}/api/viewTransactions'
            res = requests.get(url, verify=False)
            print(json.dumps(res.json(), indent=4))
        elif cmd == 'balance':
            if len(args) != 0:
                raise Exception('Invalid arguments')
            url = f'http://{address}/api/getBalance'
            res = requests.get(url, verify=False)
            print(json.dumps(res.json(), indent=4))
        elif cmd == 'help':
            if len(args) != 0:
                raise Exception('Invalid arguments')
            print("""Commands:
    t <recipient_address> <amount>
        New transaction: Send to the recipient_address wallet the amount of NBC coins that will be received from the sender_address wallet.
    view
        View last transactions: Print the transactions contained in the last validated block of the noobcash blockchain.
    balance
        Show balance: Print the balance of the wallet.
    q
        Exit""")
        elif cmd == 'q':
            if len(args) != 0:
                raise Exception('Invalid arguments')
            exit(0)
        else:
            raise Exception('Invalid command')
    except Exception as exc:
        print(exc)
