from scripts.deploy import deploy_fund_me
from scripts.helpful_scripts import get_account, LOCAL_BLOCKCHAIN_ENVIROMENTS
from brownie import network, accounts, exceptions
import pytest


def test_can_fund_and_withdrow():
    # Arrange
    fund_me = deploy_fund_me()
    account = get_account()
    entrance_fee = fund_me.getEntranceFee() + 100
    # Act
    tx1 = fund_me.fund({"from": account, "value": entrance_fee})
    tx1.wait(1)
    # Assert
    assert fund_me.addressToAmountFunded(account.address) == entrance_fee
    # Act
    tx2 = fund_me.withdraw({"from": account})
    tx2.wait(1)
    # Assert
    assert fund_me.addressToAmountFunded(account.address) == 0


def test_only_owner_can_withdraw():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIROMENTS:
        pytest.skip("only for local testing!")
    # Arrange
    fund_me = deploy_fund_me()
    bad_actor = accounts.add()
    # Act
    # Accert
    with pytest.raises(exceptions.VirtualMachineError):
        fund_me.withdraw({"from": bad_actor})
