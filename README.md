# NFT smart contract

## Contributing 

Anyone is welcome to contribute to this repository, be it in the form of features, bug fixes, documentation or additional
tests. 
Please create a branch of your own and submit for merge via merge request. A codeowner will be assigned your merge request
and provide feedback/merge it. 

## Running tests

Requirements:
- Install the [pytest plugin](https://iportal.symbiont.io/sdk_docs/docs/testing/index/index.html)
- Have a mock-network running (we recommend using `sym` to get a mock network up and running quickly)

Steps: 
- Change directory to the root of this repository
- Run the following command:
```shell
pytest test/nft_test.py --network-config=~/.symbiont/assembly-dev/local-network/default/network-config.json --contract-path=./
```

