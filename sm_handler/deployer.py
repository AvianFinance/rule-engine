from web3 import Web3
import json

def deploy_compiled_contract(contract_name):

    contract_name = 'abis/Avian' + contract_name.capitalize() + 'Exchange.json'

    private_key = "7e0dd21cba3952c769b9a90376893a351d4ac356aeacd0e537f5022e08593528"

    w3 = Web3(Web3.HTTPProvider('https://api.avax-test.network/ext/bc/C/rpc'))

    acct = w3.eth.account.privateKeyToAccount(private_key)

    with open(contract_name) as json_file:
        contract_abi = json.load(json_file)

    contract_ = w3.eth.contract(abi=contract_abi['abi'],bytecode=contract_abi['bytecode']).constructor()

    gas_estimate = 2*contract_.estimate_gas()

    construct_txn = contract_.build_transaction({
        'from': acct.address,
        'nonce': w3.eth.get_transaction_count(acct.address),
        'gas': gas_estimate,
        'gasPrice': w3.toWei('25', 'gwei')})

    signed = acct.sign_transaction(construct_txn)

    transaction_hash = w3.eth.send_raw_transaction(signed.rawTransaction)

    transaction_receipt = w3.eth.wait_for_transaction_receipt(transaction_hash)

    contract_address = transaction_receipt['contractAddress']

    return(contract_address)



