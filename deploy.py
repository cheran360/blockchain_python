"""
    address and privatekey should be changed 
    according to ganache simulation accounts
    
"""

from solcx import compile_standard, install_solc
import json
import os
from web3 import Web3
from dotenv import load_dotenv

load_dotenv()


install_solc("0.8.0")

with open("./SimpleStorage.sol", "r") as file:
    simple_storage_file = file.read()
    # print(simple_storage_file)

# compile our solidity storage file

compiled_sol = compile_standard({
    "language": "Solidity",
    "sources": {"SimpleStorage.sol": {"content" : simple_storage_file}},
    "settings": {
        "outputSelection": {
            "*":{
                "*":["abi", "metadata", "evm.bytecode", "evm.sourceMap"]
            }
        },
    },
}, solc_version="0.8.0",)

with open("compiled_code.json", "w") as file:
    json.dump(compiled_sol, file)

# get the bytecode
bytecode = compiled_sol["contracts"]["SimpleStorage.sol"]["SimpleStorage"]["evm"]["bytecode"]["object"]

# get the abi
abi = compiled_sol["contracts"]["SimpleStorage.sol"]["SimpleStorage"]["abi"]

# for connecting to ganache

w3 = Web3(Web3.HTTPProvider("HTTP://127.0.0.1:7545"))


chain_id = 1337
my_address = "0x47Fb0c4c929529144aE97c1D91e421342c66cb7d"
private_key = os.getenv("PRIVATE_KEY")

# whenever we are importing private_key or addresses we should mention 0x infront of it in python
#(hexadecimal version of the private key)

# Create a smart contract in python with the help of ganache
SimpleStorage = w3.eth.contract(abi=abi, bytecode=bytecode)

# Get the latest transaction
nonce = w3.eth.getTransactionCount(my_address)

# print(SimpleStorage)
# print(nonce)

# steps for doing a transaction
# 1. Build the Contract Deploy Transaction
# 2. Sign the Transaction
# 3. Send the Transaction



# should include gas price here (in course video it was not there)
print("deployong contract...")
transaction = SimpleStorage.constructor().buildTransaction(
    {"chainId": chain_id, "gasPrice":w3.eth.gas_price, "from":my_address, "nonce": nonce}
)
signed_txn = w3.eth.account.sign_transaction(transaction, private_key=private_key)
tx_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
print("Deployed!!")



# Working with the contract need these two things
# contract address 
# contract abi
simple_storage = w3.eth.contract(address=tx_receipt.contractAddress, abi=abi)

# call -> Simulate making call and getting a return value(no state change)
# Transact -> Actually make a state change  

# Initial value of favourite number
# call() is just a simulation , state of the variable doesnot change
print(simple_storage.functions.retrieve().call())



print("Updating Contract...")
# nonce plus 1 because we used nonce for the constructor transaction
store_transaction = simple_storage.functions.store(15).buildTransaction(
    {"chainId":chain_id, "gasPrice":w3.eth.gas_price, "from":my_address, "nonce": nonce + 1}
)
signed_store_txn = w3.eth.account.sign_transaction(store_transaction, private_key=private_key)
send_store_tx = w3.eth.send_raw_transaction(signed_store_txn.rawTransaction)
tx_receipt = w3.eth.wait_for_transaction_receipt(send_store_tx)
print("Updated!!")



# state was changed
print(simple_storage.functions.retrieve().call())