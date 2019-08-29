from web3 import Web3

import configparser
import json

class UserListController(object):
    def __init__(self, ipc_file, contract_address, contract_json, address, keyfile, passwordfile):
        self.address = Web3.toChecksumAddress(address)

        self.client = Web3(Web3.IPCProvider(ipc_file))

        self.private_key = self._load_private_key(keyfile, passwordfile)

        abi = self._generate_contract_abi(contract_json)
        self.contract = self._load_contract(abi, contract_address)

    def _generate_contract_abi(self, contract_json):
        with open(contract_json, "r") as abi_definition:
            return json.load(abi_definition)['abi']

    def _load_contract(self, abi, contract_address):
        return self.client.eth.contract(contract_address, abi=abi)

    def _load_private_key(self, keyfile, passwordfile):
        with open(passwordfile, "r") as pwf:
            password = pwf.read().strip()

        with open(keyfile, "r") as kf:
            enc_key = kf.read()
            return self.client.eth.account.decrypt(enc_key, password)


    def create_user(self, nameCardID):
        tx_data = {
            "nonce": self.client.eth.getTransactionCount(self.address),
            "gasPrice": self.client.eth.gasPrice,
            "gas": 100000,
        }
        tx = self.contract.functions.createUser(nameCardID).buildTransaction(tx_data)
        signed_tx = self.client.eth.account.signTransaction(tx, self.private_key)
        res = self.client.eth.sendRawTransaction(signed_tx.rawTransaction)


if __name__ == "__main__":
    config = configparser.ConfigParser()
    config.read('config.ini')
    default = config['default']
    ulc = UserListController(default['IPC'], default['ContractAddress'], default['ContractJSON'], default['Address'], default['KeyFile'], default['PasswordFile'])

    ulc.create_user(999999)
