import logging

import pytest
import web3

from pytest_ethereum.deployer import Deployer

logging.getLogger("evm").setLevel(logging.INFO)


def test_deployer_fixture(request, vyper_project_dir):
    deployer = request.getfixturevalue("deployer")
    assert isinstance(deployer, Deployer)


# User Code
@pytest.fixture
def greeter(deployer):
    return deployer.deploy("Greeter")


@pytest.fixture
def registry(deployer):
    return deployer.deploy("Registry")


def test_user_code_with_fixture(vyper_project_dir, greeter, registry):
    assert isinstance(greeter, web3.contract.Contract)
    assert isinstance(registry, web3.contract.Contract)
    greeting = greeter.functions.greet().call()
    assert greeting == b"Hello"
