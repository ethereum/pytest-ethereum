from eth_utils import is_address
import pytest

from ethpm import Package
from pytest_ethereum.deployer import Deployer
from pytest_ethereum.exceptions import DeployerError
from pytest_ethereum.linker import deploy, link, linker


@pytest.fixture
def escrow_deployer(solc_deployer, w3, manifest_dir):
    escrow_manifest_path = manifest_dir / "escrow_manifest.json"
    return solc_deployer(escrow_manifest_path), w3


def test_linker(escrow_deployer):
    # todo test multiple links in one type
    deployer, w3 = escrow_deployer
    assert isinstance(deployer, Deployer)
    with pytest.raises(DeployerError):
        deployer.deploy("Escrow")

    escrow_strategy = linker(
        deploy("SafeSendLib"),
        link("Escrow", "SafeSendLib"),
        deploy("Escrow", w3.eth.accounts[0]),
    )
    assert hasattr(escrow_strategy, "__call__")
    deployer.register_strategy("Escrow", escrow_strategy)
    escrow_deployer = deployer.deploy("Escrow")
    linked_escrow_package, escrow_address = escrow_deployer
    assert isinstance(linked_escrow_package, Package)
    assert is_address(escrow_address)
    linked_escrow_factory = linked_escrow_package.get_contract_factory("Escrow")
    assert linked_escrow_factory.needs_bytecode_linking is False
