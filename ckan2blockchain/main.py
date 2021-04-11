#! /usr/bin/env python3
from flask import Flask, render_template, jsonify, make_response, request, flash
from flask_restful import Resource, Api, reqparse, abort
from CkanCrawler import CkanCrawler
from BlockchainEthereum import BlockchainEthereum

import hashlib, json, time, sys, urllib.request, urllib.parse, pdb, configparser, argparse, sys, logging, logging.handlers, re

class Ckan2Blockchain:

    def __init__(self):
        self.logger = logging.getLogger('Ckan2Blockchain')

        self.logger.setLevel(logging.INFO)
        fmt = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

        out1 = logging.StreamHandler(sys.stderr)
        out1.setFormatter(fmt)
        self.logger.addHandler(out1)

        out2 = logging.handlers.SysLogHandler()
        out2.setFormatter(fmt)
        self.logger.addHandler(out2)

        self.logger.info('started')

    def add_cli_commmands(self,subparsers):
        # dataset-store
        sub_dataset_store = subparsers.add_parser('dataset-store', help='retrieve hash of selected dataset from CKAN and store it to the block chain')
        sub_dataset_store.add_argument('-d', '--dataset', action='append', help='dataset identificator').required = True

        # dataset-verify
        sub_dataset_verify = subparsers.add_parser('dataset-verify', help='retrieve hash of the dataset from the block chain and verify against CKAN')
        sub_dataset_verify.add_argument('-d', '--dataset', action='append', help='dataset identificator')

        # dataset-store-all
        sub_dataset_store_all = subparsers.add_parser('dataset-store-all', help='store all hashes from CKAN to the blockchain')

        # dataset-verify-all
        sub_dataset_verify_all = subparsers.add_parser('dataset-verify-all', help='verify hashes presently on the blockchain against CKAN')

    def handle_command(self, command):
      if command=='dataset-store-all' or command=='dataset-verify-all':
          packages = self.ckan.get_package_list()
          exit_on_fail = False
      elif command=='dataset-store' or command=='dataset-verify':
          packages = self.cli_args.dataset
          exit_on_fail = True
      else:
        return

      results = { }
      for package in packages:
          try:
              (package_hash, dataset_hash) = self.ckan.hash_package(package)
              results[package_hash] = dataset_hash
          except Exception as e:
              if exit_on_fail:
                  sys.exit("Error while obtaining hash for "+package+" from CKAN: "+str(e))
              else:
                  self.logger.error("Error while obtaining hash for "+package+" from CKAN: "+str(e))

      if command=='dataset-store' or command=='dataset-store-all':
          self.chain.add_to_blockchain(results)
      else:
          self.chain.add_to_blockchain(results)
          pass # TODO - handle verification

    def main(self):

        # command line argument parser
        parser = argparse.ArgumentParser()
        # 1. add options and flags
        parser.add_argument('-f', '--force', action='store_true', help='force the action (use with care)')
        parser.add_argument('-c', '--config-file', action='store', default='./etc/ckan2blockchain.ini', help='path to the configuration file')
        parser.add_argument('-p', '--password', action='store', help='specify password to decrypt keychain on command line. THIS IS UNSAFE in a multi-user environment. Other users may see your password plainly. Enter the password through console instead.')
        # 2. add ckan and blockchain related commands
        command_subparsers = parser.add_subparsers(dest='command')
        command_subparsers.required = True
        self.add_cli_commmands(command_subparsers)
        BlockchainEthereum.add_cli_commands(command_subparsers)
        # 3. finally, parse the command line arguments
        self.cli_args = parser.parse_args()

        # ini file settings
        ini_defaults = {
            'general': {
                'blockchain': 'ethereum'
            },
            'ethereum': {
                'maximum_transaction_size': '65536'
            },
        }
        self.ini_args = configparser.ConfigParser(defaults=ini_defaults)
        self.ini_args.read_dict(ini_defaults)

        try:
            found = self.ini_args.read(self.cli_args.config_file)
            if len(found) == 0:
                raise(ValueError('Cannot open the file '+self.cli_args.config_file))

            self.ckan = CkanCrawler(self.cli_args, self.ini_args, self.logger)

            tmp = self.ini_args.get('general','blockchain')
            if tmp == 'ethereum':
                self.chain = BlockchainEthereum(self.cli_args, self.ini_args, self.logger)
            else:
                raise(ValueError('Unsupported type of blockchain: '+tmp))

        except (ValueError,configparser.Error) as e:
            sys.exit("Configuration file error: "+str(e))

        self.handle_command(self.cli_args.command)
        self.chain.handle_command(self.cli_args.command)


app = Flask(__name__)
api = Api(app)
app.secret_key = 'my unobvious secret key'

parser = reqparse.RequestParser()
parser.add_argument('package')
parser.add_argument('url')

class PackageHash(Resource):
    def post(self):
        args = parser.parse_args()
        package = args['package']
        full_url = args['url']
        url = re.sub('/action/package.*', '', full_url)
        obj_ckan = CkanCrawler(package)
        results = {}

        (package_hash, dataset_hash) = obj_ckan.hash_package1(url, package)
        results[package_hash] = dataset_hash

        obj_blockchainethereum = BlockchainEthereum()
        confirm = obj_blockchainethereum.verify_transaction(results, package, full_url)
        return {'result': f'{confirm}'}

api.add_resource(PackageHash, '/requestPackageHash')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get-packages', methods=["POST"])
def get_packages():
    url = request.get_json()['url']
    res = urllib.request.urlopen(url).read()
    res_json = json.loads(res.decode())
    res = make_response(jsonify({"package_lists": res_json['result']}), 200)
    return res

@app.route('/store-package', methods=["POST"])
def store_package():
    url = request.get_json()['url']
    package = request.get_json()['package']

    #1 download package and hash
    obj_ckan = CkanCrawler(package)
    results = {}
    url = re.sub('/action/package.*', '', url)
    (package_hash, dataset_hash) = obj_ckan.hash_package1(url, package)
    results[package_hash] = dataset_hash

    #2 add to blockchain
    obj_blockchainethereum = BlockchainEthereum()
    obj_blockchainethereum.add_to_blockchain(results)
    # flash('Transaction has been sent!', 'info')
    return results

@app.route('/verify-package', methods=["POST"])
def verify_data():
    full_url = request.get_json()['url']
    package = request.get_json()['package']

    #1 download package and hash
    obj_ckan = CkanCrawler(package)
    results = {}
    url = re.sub('/action/package.*', '', full_url)
    (package_hash, dataset_hash) = obj_ckan.hash_package1(url, package)
    results[package_hash] = dataset_hash

    obj_blockchainethereum = BlockchainEthereum()
    confirm = obj_blockchainethereum.verify_transaction(results, package, full_url)    
    print("Dataset "+package+" is "+str(confirm))
    return str(confirm)

@app.route('/about')
def about():
    return render_template('about.html')

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=3000, debug=True)

# vim: ai ts=4 sts=4 et sw=4 ft=python
