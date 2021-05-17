# ckan-to-blockchain-ui
`ckan-to-blockchain-ui` is built on top of [ckan2blockchain](https://github.com/milankowww/ckan2blockchain) and to finish off the verification part. It allows easier store and verify dataset package on ethereum blockchain through webpage.

#### Prerequisite
1. Install Geth through this [instruction](https://geth.ethereum.org/docs/install-and-build/installing-geth)
1. Create [Infura](https://infura.io/register) account, create project, and copy the https endpoint of Rinkeby and place it in the `.env` file. Follow [this](https://blog.infura.io/getting-started-with-infura-28e41844cc89/) until step 4
1. Create address through terminal:
    - type `geth account new` and press `enter`
    - it will prompt for password
    - after that it will return the `public address` and the path to the `keystore` 
1. create `.env` file following `.env.example`
    - replace your own `password` using to create account above
    - put in there the public address
    - specify the full path to the keystore (it is recommend to copy the keystore file to the project for easier run with Docker)

#### Easy way start the app with Docker
- Open the project path in terminal
- Navigate to `ckan2blockchain` folder
- Run `docker build -t use-any-name .`
- Then run `docker run -p 0.0.0.0:3000:3000 use-any-name`
- Navigate to your browser, type `0.0.0.0:3000` and enter
