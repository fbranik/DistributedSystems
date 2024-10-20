import requests
from threading import Thread


def broadcastRequest(destinationPath, infoDict: dict, exclusionId, method=requests.put, json=None):
    reqThreads = []
    responses = []

    for id, commInfo in infoDict.items():
        if id != exclusionId:
            iAddress = f"http://{commInfo['ip']}:{commInfo['port']}{destinationPath}"
            iReqThread = Thread(target=reqTask(iAddress, responses, method=method, json=json))
            iReqThread.start()
            reqThreads.append(iReqThread)

    for iThread in reqThreads:
        iThread.join()
    return responses


def reqTask(addressString, responses, method=requests.put, json=None):
    if json is not None:
        responses.append(method(addressString, json=json, timeout=100))
    else:
        responses.append(method(addressString, timeout=100))
