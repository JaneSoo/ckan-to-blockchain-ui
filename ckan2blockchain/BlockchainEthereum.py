from web3 import Web3, EthereumTesterProvider, HTTPProvider
from web3.middleware import geth_poa_middleware
from eth_account import Account
from eth_tester import EthereumTester
from decouple import config
from datetime import datetime

import argparse, getpass, hashlib, time, json, binascii, sys, ethereum.exceptions, pdb

class BlockchainEthereum:

    # methods called from main.py

    # def __init__(self, cli_args, ini_args, logger):
    #     self.cli_args = cli_args
    #     self.ini_args = ini_args
    #     self.logger = logger

    #     provider = self.ini_args.get('ethereum','provider')
    #     if provider == 'test':
    #         self.w3 = Web3(EthereumTesterProvider())
    #     elif provider == 'local':
    #         self.w3 = Web3(Web3.IPCProvider())
    #     elif provider == 'network':
    #         self.w3 = Web3(HTTPProvider(config('INFURA_URL)))
    #     else:
    #         self.w3 = Web3(HTTPProvider(provider))

    def __init__(self):
        self.w3 = Web3(HTTPProvider(config('INFURA_URL')))

    def handle_command(self, command):
        if command=='eth-create-address':
            tmp = getpass.getpass('Please enter a few random words: ')
            tmp = hashlib.sha256((tmp + str(time.time())).encode('utf-8')).hexdigest()
            account = Account.create(tmp)
            # account.address
            # account.privateKey
            self.__ask_decrypt_password()
            encrypted = Account.encrypt(account.privateKey, self.decrypt_password)

            try:
                with open(self.ini_args.get('ethereum', 'private_key_file'), 'x') as keyfile:
                    keyfile.write(json.dumps(encrypted))
            except OSError as e:
                sys.exit('Error storing private key: ' + str(e))

            self.__load_private_key()
    
    def add_to_blockchain(self, dataset_hashes):
        dataset_ids = list(dataset_hashes.keys())
        if len(dataset_ids) == 0:
            return
        
        header = str(binascii.hexlify(b"ckan2blockchain.1."), 'utf-8')
        header_len = len(header)//2
        entry_len = (len(dataset_ids[0]) + len(dataset_hashes[dataset_ids[0]]))//2
        entries_per_tx = (65536 - header_len)//entry_len

        for i in range(0, len(dataset_ids), entries_per_tx):
            data1 = ''
            for x in dataset_ids[i:i+entries_per_tx]:
                data1 = header + ''.join(x+dataset_hashes[x])
            
            data = header + ''.join(x+dataset_hashes[x] for x in dataset_ids[i:i+entries_per_tx])
            trx_hash = self.send_data(data)
        return trx_hash

    # private methods
    def __ask_decrypt_password(self):
        if hasattr(self, 'decrypt_password'):
            return

        if 'password' in self.cli_args and self.cli_args.password != None:
            self.decrypt_password = self.cli_args.password
            sys.stderr.write('Using password from command line. THIS IS UNSAFE. ANYONE ON THE SAME MACHINE COULD SEE YOUR PASSWORD.\n')
        else:
            self.decrypt_password = getpass.getpass('Please enter password to decrypt the private key: ')

    def __load_private_key(self):
        if hasattr(self, 'private_key'):
            return

        self.__ask_decrypt_password()

        try:
            with open(self.ini_args.get('ethereum', 'private_key_file')) as keyfile:
                keyfile_json = keyfile.read()

            self.private_key = Account.decrypt(keyfile_json, self.decrypt_password)
        except (ValueError, OSError) as e:
            sys.exit('Error loading private key: ' + str(e))

        if self.ini_args.get('ethereum','provider') == 'test':
            # make sure the sending account is well funded 
            account = Account.privateKeyToAccount(self.private_key)

            if self.w3.eth.getBalance(account.address) == 0:
                self.w3.eth.sendTransaction({
                    'from': self.w3.eth.coinbase,
                    'to': account.address,
                    'gas': 30000,
                    'value': 0,
                    'nonce': self.w3.eth.getTransactionCount(self.w3.eth.coinbase),
                })

    def verify_transaction(self, dataset_hashes, package, full_url):
        dataset_ids = list(dataset_hashes.keys())
        if len(dataset_ids) == 0:
            return
        
        header = str(binascii.hexlify(b"ckan2blockchain.1."), 'utf-8')
        header_len = len(header)//2
        entry_len = (len(dataset_ids[0]) + len(dataset_hashes[dataset_ids[0]]))//2
        entries_per_tx = (65536 - header_len)//entry_len

        for i in range(0, len(dataset_ids), entries_per_tx):            
            data = header + ''.join(x+dataset_hashes[x] for x in dataset_ids[i:i+entries_per_tx])

        with open('data1.json') as json_file:
            trx_hashes = json.load(json_file)
            trx_hash = trx_hashes[f'{full_url}'][0].get(package)

            self.w3.middleware_onion.inject(geth_poa_middleware, layer=0)

            if trx_hash:
                transaction = self.w3.eth.getTransaction(trx_hash)
                block_num = transaction.blockNumber
                block = self.w3.eth.getBlock(block_num)
                timestamp = block.timestamp

                if transaction:
                    input_value = transaction.input[2:] if transaction.input.startswith("0x") else transaction.input
                    result = (data == input_value)
                    result_dict = {'block_num': block_num, 'trx_hash': trx_hash, 'timestamp': f'{datetime.utcfromtimestamp(timestamp)}', 'result': result}
                    return result_dict
            else:
                result = {'result': 'Transaction not found!'}
                return result

    def send_data(self, data):
        try:
            with open(config('private_key_file')) as keyfile:
                keyfile_json = keyfile.read()
            private_key = Account.decrypt(keyfile_json, config('PASSWORD'))
        except (ValueError, OSError) as e:
            sys.exit('Error loading private key: ' + str(e))

        account = Account.privateKeyToAccount(private_key)
        
        w3 = Web3(HTTPProvider(config('INFURA_URL')))
        signed_transaction = w3.eth.account.signTransaction({
            'nonce': w3.eth.getTransactionCount(account.address, 'pending'),
            'gasPrice': w3.eth.gasPrice,
            'gas': 30000,
            'to': config('ADDRESS'),
            'value': 0,
            'data': data
        }, private_key)

        try:
            return w3.eth.sendRawTransaction(signed_transaction.rawTransaction)
        except ethereum.exceptions.InsufficientBalance as e:
            print(str(e))
            return False
        return True

    # class methods

    def add_cli_commands(subparsers):
        # eth-create-address
        sub_create_address = subparsers.add_parser('eth-create-address', help='Create a new Ethereum address for sending')


# vim: ai ts=4 sts=4 et sw=4 ft=python
