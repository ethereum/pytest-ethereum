import logging
from pathlib import Path

from eth_utils import is_address
import pytest
import web3

from pytest_ethereum.deployer import Deployer
from pytest_ethereum.exceptions import DeployerError

logging.getLogger("evm").setLevel(logging.INFO)


def test_deployer_fixture(request, vyper_project_dir):
    deployer = request.getfixturevalue("vy_deployer")
    assert isinstance(deployer, Deployer)


#
# Vyper Contracts
#


# User Code
@pytest.fixture
def greeter(vy_deployer):
    return vy_deployer.deploy("Greeter")


@pytest.fixture
def registry(vy_deployer):
    return vy_deployer.deploy("Registry")


def test_user_code_with_fixture(vyper_project_dir, greeter, registry):
    greeter_package, greeter_address = greeter
    greeter_instance = greeter_package.get_contract_instance("Greeter", greeter_address)
    assert isinstance(greeter_instance, web3.contract.Contract)
    registry_package, registry_address = registry
    registry_instance = registry_package.get_contract_instance(
        "Registry", registry_address
    )
    assert isinstance(registry_instance, web3.contract.Contract)
    greeting = greeter_instance.functions.greet().call()
    assert greeting == b"Hello"


MANIFEST_DIR = Path(__file__).parent.parent / "manifests"

#
# Solidity Compiler Output
#


# SIMPLE
@pytest.fixture
def owned_deployer(solc_deployer):
    owned_manifest_path = MANIFEST_DIR / "owned_manifest.json"
    owned_deployer = solc_deployer(path=owned_manifest_path)
    return owned_deployer.deploy("Owned")


def test_owned_deployer(owned_deployer):
    owned_package, owned_address = owned_deployer
    assert is_address(owned_address)


# CONSTRUCTOR ARGS
@pytest.fixture
def standard_token_deployer(solc_deployer):
    standard_token_manifest_path = MANIFEST_DIR / "standard_token_manifest.json"
    standard_token_deployer = solc_deployer(standard_token_manifest_path)
    return standard_token_deployer.deploy("StandardToken", 100)


def test_standard_token_deployer(standard_token_deployer):
    standard_token_package, standard_token_address = standard_token_deployer
    assert is_address(standard_token_address)
    standard_token_instance = standard_token_package.get_contract_instance(
        "StandardToken", standard_token_address
    )
    assert standard_token_instance.functions.totalSupply().call() == 100


# LIBRARY
@pytest.fixture
def safe_math_deployer(solc_deployer):
    safe_math_manifest_path = MANIFEST_DIR / "safe_math_manifest.json"
    safe_math_deployer = solc_deployer(safe_math_manifest_path)
    return safe_math_deployer.deploy("SafeMathLib")


def test_safe_math_deployer(safe_math_deployer):
    _, safe_math_address = safe_math_deployer
    assert is_address(safe_math_address)


# LINK REFS
@pytest.fixture
def escrow_deployer(solc_deployer, w3):
    escrow_manifest_path = MANIFEST_DIR / "escrow_manifest.json"
    return solc_deployer(escrow_manifest_path), w3


def test_escrow_deployer_unlinked(escrow_deployer):
    deployer, w3 = escrow_deployer
    with pytest.raises(DeployerError):
        deployer.deploy("Escrow", w3.eth.accounts[0])
