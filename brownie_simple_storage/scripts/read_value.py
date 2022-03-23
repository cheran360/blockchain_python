# this file reads the contracts that we already deployed..
from brownie import SimpleStorage, accounts, config


def read_contract():
    # print(SimpleStorage[0])
    # -1 -> grab the most recent deployed contract
    simple_storage = SimpleStorage[-1]
    print(simple_storage.retrieve())

def main():
    read_contract()