# ckan-to-blockchain-ui
`ckan-to-blockchain-ui` is built on top of [ckan2blockchain](https://github.com/milankowww/ckan2blockchain) and to finish off the verification part. It allows easier store and verify dataset package on ethereum blockchain through webpage.

#### Prerequisite
1. Python 3
1. Flask
1. Install Geth through this [instruction](https://geth.ethereum.org/docs/install-and-build/installing-geth)
1. Create address through terminal:
    - type `geth account new` and press `enter`
    - it will prompt for password
    - after that it will return the `public address` and the path to the `keystore` 
1. create `.env` file following `.env.example`
    - replace your own `password` using to create account above
    - put in there the public address
    - specify the full path to the keystore

#### To start the app
Navigate to `ckan2blockchain` folder and run `python3 main.py`
