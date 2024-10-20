from cryptography.hazmat.primitives.hashes import SHA256
import cryptography.hazmat.primitives.hashes as hashes


def TransactionOutput(transaction_id, recipient_id, amount):
    trOutDict = {}
    sha256Hasher = hashes.Hash(SHA256())
    dataToHash = str(transaction_id) + str(recipient_id) + str(amount)
    sha256Hasher.update(dataToHash.encode())
    finalDigest = sha256Hasher.finalize()

    trOutDict['transaction_output_id'] = finalDigest.hex()
    trOutDict['transaction_id'] = transaction_id
    trOutDict['recipient_id'] = recipient_id
    trOutDict['amount'] = amount

    return trOutDict
