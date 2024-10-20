from argparse import ArgumentParser
from threading import Thread
import requests

parser = ArgumentParser()
parser.add_argument('-n', '--numberOfNodes', default=5,
                    type=int, help='port to listen on')
parser.add_argument('-s', '--subnet', default="192.168.0.",
                    type=str, help='port to listen on')

args          = parser.parse_args()
numberOfNodes = args.numberOfNodes
subnet        = args.subnet

def reqTask(addressString):
    resp = requests.get(addressString)

threadList = []
if subnet == "127.0.0.1":
    subnet+=":500"

if numberOfNodes == 5:
    for i in range(5):
        iAddress = subnet+str(i)
        
        if not subnet == "127.0.0.1:500":
            iAddress +=":5000"
        addressString = f'http://{iAddress}/api/runTests/'
        iThread = Thread(target=reqTask, args=(addressString,))
        iThread.start()
        threadList.append(iThread)



if numberOfNodes == 10:
    if subnet == "127.0.0.1":
        print("not running tests locally for 10 nodes!")
        exit() 
    for i in range(5):
        iAddress1 = subnet+str(i)+":5000"
        iAddress2 = subnet+str(i)+":5001"
        addressString1 = f'http://{iAddress1}/api/runTests/'
        addressString2 = f'http://{iAddress2}/api/runTests/'
        iThread1 = Thread(target=reqTask, args=(addressString1,))
        iThread2 = Thread(target=reqTask, args=(addressString2,))
        iThread1.start()
        iThread2.start()
        threadList.append(iThread1)
        threadList.append(iThread2)

for iThread in threadList:
    iThread.join()


print("Sent test requests")


