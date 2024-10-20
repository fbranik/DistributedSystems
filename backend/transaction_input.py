def TransactionInput(previous_output_id, amount):
    trInDict = {}
    trInDict['previous_output_id'] = previous_output_id
    trInDict['amount'] = amount  # added this
    return trInDict
