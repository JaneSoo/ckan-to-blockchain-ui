# ckan-to-blockchain-ui
`ckan-to-blockchain-ui` is built on top of [ckan2blockchain](https://github.com/milankowww/ckan2blockchain) and to finish off the verification part. It allows easier store and verify dataset package on ethereum blockchain through webpage.

#### Prerequisite
1. Install Geth through this [instruction](https://geth.ethereum.org/docs/install-and-build/installing-geth)
1. Create [Infura](https://infura.io/register) account, create project, copy the https endpoint of Rinkeby, and place it in the `.env` file. Follow [this instruction](https://blog.infura.io/getting-started-with-infura-28e41844cc89/) to get the https endpoint (until step 4 and remember to choose `Rinkeby`)
1. Create geth account address through terminal:
    - type `geth account new` and press `enter`
    - it will prompt for password
    - after that it will return the `public address` and the path to the `keystore` 
1. create `.env` file following `.env.example`
    - replace your own `password` with the one you were using to create account above
    - put in there the public address (Address should be similar to this `0xD2beDdA8fB2aB7D39eDaF3d735fb309322D61B42`, you might need to add the prefix`0x` by yourself)
        - **Account address should begin with "0x". You can verify the address by search it at [Rinkeby Etherscan](https://rinkeby.etherscan.io/) or even at the [mainnet](https://etherscan.io/)** 
    - don't forget to feed your account balance with ether otherwise you can't push transaction. Do it following instruction [here](https://faucet.rinkeby.io/)
        - **Ether value will only show in the Rinkeby Testnet while in the mainnet the address will not hold any ether**
    - specify the full path to the keystore (it is recommend to copy the keystore file to the project for easier run with Docker)
        - **Keystore file is by default a text file so just rename and add extension of `json` that will work**
#### Spin up the app with Docker
- Open the terminal and navigate to where the project locates
- Navigate to `ckan2blockchain` folder
- Run `docker build -t <use-any-name> .` (you should have [Docker](https://docs.docker.com/get-docker/) install first)
- Then run `docker run -p 0.0.0.0:3000:3000 <use-any-name>`
- Navigate to your browser, type `0.0.0.0:3000` and press `enter` (the console log might show different IP but try to stick with this one)
- the app should be up running now!
