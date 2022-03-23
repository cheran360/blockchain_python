# add account from terminal in brownie -- brownie accounts new <account_name>
# to see all accounts --> browine accounts list
# deleteaccounts in brownie --> brownie accounts delete <account_name>
# from brownie u can import contracts 
# cmd to veiw all prebuild networks by brownie --> brownie networks list

# deploy to a specific network cmd -->
# brownie run scripts/deploy.py --network <network_name>

# to open brownie console --> brownie console

import os
from brownie import accounts, config, SimpleStorage, network


def deploy_simple_storage():
    # account = accounts[0] only works when brownie is with ganacge cli
    # account = accounts.load("<accounts_name>")
    # account = accounts.load("cheran")
    # account = accounts.add(os.getenv("PRIVATE_KEY"))
    account = get_account()
    # deploy the contract
    simple_storage = SimpleStorage.deploy({"from": account})
    # Transaction
    # call
    stored_value = simple_storage.retrieve()
    print(stored_value)
    transaction= simple_storage.store(15, {"from": account})
    # 1 -> represents how many blocks we have to wait
    transaction.wait(1)
    updated_stored_value = simple_storage.retrieve()
    print(updated_stored_value)

def get_account():
    if network.show_active() == "develpoment":
        return accounts[0]
    else:
        return accounts.add(config["wallets"]["from_key"])


def main():
    deploy_simple_storage()