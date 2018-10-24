from eth_utils import remove_0x_prefix, to_hex
from eth_utils.toolz import assoc
import pytest

from ethpm.utils.chains import (
    create_block_uri,
    create_block_uri_from_w3,
    get_genesis_block_hash,
)
from pytest_ethereum._utils.linker import (
    contains_matching_uri,
    insert_deployment,
    pluck_matching_uri,
)
from pytest_ethereum.exceptions import LinkerError


@pytest.fixture
def chain_setup(w3):
    old_chain_id = remove_0x_prefix(to_hex(get_genesis_block_hash(w3)))
    block_hash = remove_0x_prefix(to_hex(w3.eth.getBlock("earliest").hash))
    old_chain_uri = f"blockchain://{old_chain_id}/block/{block_hash}"
    match_data = {
        old_chain_uri: {"x": "x"},
        f"blockchain://1234/block/{block_hash}": {"x": "x"},
    }
    no_match_data = {
        f"blockchain://56775ac59d0774e6b603a79c4218efeb5653b99ba0ff14db983bac2662251a8a/block/{block_hash}": {  # noqa: E501
            "x": "x"
        }
    }
    return w3, match_data, no_match_data, old_chain_uri


def test_pluck_matching_uri(chain_setup):
    w3, match_data, no_match_data, old_chain_uri = chain_setup
    w3.testing.mine(1)
    new_chain_uri = create_block_uri_from_w3(w3)

    assert pluck_matching_uri(match_data, new_chain_uri) == old_chain_uri
    with pytest.raises(LinkerError):
        assert pluck_matching_uri(no_match_data, new_chain_uri)


def test_contains_matching_uri(chain_setup):
    w3, match_data, no_match_data, _ = chain_setup
    w3.testing.mine(1)
    new_chain_uri = create_block_uri_from_w3(w3)

    assert contains_matching_uri(match_data, new_chain_uri) is True
    assert contains_matching_uri(no_match_data, new_chain_uri) is False


def test_insert_deployment(escrow_deployer):
    deployer, w3 = escrow_deployer
    escrow_package = deployer.package
    init_deployment_data = {
        "contract_type": "Escrow",
        "address": "0x",
        "transaction": "0x",
        "block": "0x",
    }
    new_deployment_data = {
        "contract_type": "Escrow",
        "address": "0x123",
        "transaction": "0x123",
        "block": "0x123",
    }
    genesis_hash = to_hex(get_genesis_block_hash(w3))
    w3.testing.mine(1)
    init_block_hash = to_hex(w3.eth.getBlock("latest")["hash"])
    init_block_uri = create_block_uri(genesis_hash, init_block_hash)
    alt_block_uri = init_block_uri[:15] + "yxz123" + init_block_uri[21:]
    init_block_deployment_data = {
        init_block_uri: {"Other": {"x": "x"}, "Escrow": init_deployment_data},
        alt_block_uri: {"alt": {"x": "x"}},
    }
    w3.testing.mine(1)
    new_block_hash = to_hex(w3.eth.getBlock("latest")["hash"])
    new_block_uri = create_block_uri(genesis_hash, new_block_hash)
    escrow_package.manifest = assoc(
        escrow_package.manifest, "deployments", init_block_deployment_data
    )
    updated_manifest = insert_deployment(
        escrow_package.manifest, new_block_uri, "Escrow", new_deployment_data
    )
    expected_deployments_data = {
        new_block_uri: {"Other": {"x": "x"}, "Escrow": new_deployment_data},
        alt_block_uri: {"alt": {"x": "x"}},
    }
    assert updated_manifest["deployments"] == expected_deployments_data
