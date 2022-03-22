from solcx import compile_standard, install_solc
import json
import os
from web3 import Web3


install_solc("0.8.0")

with open("./SimpleStorage.sol", "r") as file:
    simple_storage_file = file.read()
    print(simple_storage_file)

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
my_address = "0xC40959CbF723fF578a71DA9301FE44bE8E118De9"


# whenever we are importing private_key or addresses we should mention 0x infront of it in python
#(hexadecimal version of the private key)
private_key = "0xf0a3a80abf563c15a5c4a62881fcc6d6e2489190fd26c776c518171a31399c93"


# Create a smart contract in python woith the help of ganache
SimpleStorage = w3.eth.contract(abi=abi, bytecode=bytecode)

# Get the latest transaction
nonce = w3.eth.getTransactionCount(my_address)
print("nonce of the transaction: ", nonce)

print(SimpleStorage)
print(nonce)

# steps for doing a transaction
# 1. Build the Contract Deploy Transaction
# 2. Sign the Transaction
# 3. Send the Transaction

# should include gas price here
transaction = SimpleStorage.constructor().buildTransaction(
    {"chainId": chain_id, "gasPrice":w3.eth.gas_price, "from":my_address, "nonce": nonce}
)

print(transaction)