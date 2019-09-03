from web3 import Web3

from flask import Flask, request
from flask_cors import CORS

import configparser
import json

app = Flask(__name__)
CORS(app)

class UserListController(object):
    def __init__(self, ipc_file, contract_address, contract_json, address, keyfile, passwordfile, explorer_format):
        self.address = Web3.toChecksumAddress(address)
        self.explorer_format = explorer_format

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

    def _base_tx(self):
        return {
            "nonce": self.client.eth.getTransactionCount(self.address),
            "gasPrice": self.client.eth.gasPrice,
            "gas": 100000,
        }

    def create_user(self, nameCardID):
        tx_data = self._base_tx()
        tx = self.contract.functions.createUser(nameCardID).buildTransaction(tx_data)
        signed_tx = self.client.eth.account.signTransaction(tx, self.private_key)
        return self.client.eth.sendRawTransaction(signed_tx.rawTransaction)

    def get_explorer_url(self, txid):
        return self.explorer_format.format(tx=txid.hex())


config = configparser.ConfigParser()
config.read('config.ini')
contracting = config['contracting']
ulc = UserListController(contracting['IPC'], contracting['ContractAddress'], contracting['ContractJSON'], contracting['Address'], contracting['KeyFile'], contracting['PasswordFile'], contracting['ExplorerFormat'])

@app.route('/newuser', methods=['POST'])
def create_user():
    try:
        userid = request.json.get('UserID')
        txid = ulc.create_user(userid)
        return { "status": "Success", "transaction": ulc.get_explorer_url(txid) }
    except Exception as e:
        return { "status": "Failure", "reason": str(e) }

if __name__ == "__main__":
    # This is a test creation invoked directly, this should be replaced with a web server
    #ulc.create_user(999999)
    app.run(port=80, host='0.0.0.0', debug=True)
