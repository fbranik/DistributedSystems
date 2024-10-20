from backend.node import Node
from time import sleep
from requests import get


def nodeWatcher(myNode: Node):
    isRunning = open('isRunning.txt', 'w+')
    isRunning.write(
        f'Running sizeOfBlock={myNode.chain.sizeOfBlock}, difficulty={myNode.difficulty}, numOfMiningThreads={myNode.numOfMiningThreads}\n')
    isRunning.close()
    sleep(100)
    while not myNode.miningQueue.empty() and len(myNode.chain.listOfBlocks) > 1:
        sleep(300)
    print("\nNode watcher detected no new blocks on the last 5 minutes\nWriting logs and ending shutdown request\n")
    sleep(20)
    chosenInfo = myNode.nodesTable[myNode.Id]
    addressString = f"http://{chosenInfo['ip']}:{chosenInfo['port']}/api/writeBlockLogs"
    _ = get(addressString, timeout=100)
    sleep(20)
    addressString = f"http://{chosenInfo['ip']}:{chosenInfo['port']}/shutdown"
    isRunning = open('isRunning.txt', 'w+')
    isRunning.write('not runnning (give it some seconds before re-running)\n')
    isRunning.close()
    _ = get(addressString, timeout=100)
