from brownie import FundMe, MockV3Aggregator, network, config
from .helpful_scripts import get_account, deploy_mocks, LOCAL_BLOCKCHAIN_ENVIROMENTS
from web3 import Web3

# compile contrat: brownie compile -> this will compile every contracts in contracts folder
# deploying to localchain (ganache): brownie run scripts/deploy.py
# deploying to rinkeby: brownie run scripts/deploy.py --network rinkeby
# add custom network to brownie: brownie networks add Ethereum ganache-local host=http://127.0.0.1:7545 chainid=1337
# run test: bownie test
# run test on specific def: brownie test -k test_only_owner_can_withdraw


def deploy_fund_me():
    account = get_account()

    # pass the price feed address to our fundme contract
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIROMENTS:
        price_feed_address = config["networks"][network.show_active()][
            "eth_usd_price_feed"
        ]
    else:
        deploy_mocks()
        price_feed_address = MockV3Aggregator[-1].address

    fund_me = FundMe.deploy(
        price_feed_address,
        {"from": account},
        publish_source=config["networks"][network.show_active()].get("verify"),
    )
    print(f"Contract deployed to {fund_me.address}")
    return fund_me


def main():
    deploy_fund_me()
