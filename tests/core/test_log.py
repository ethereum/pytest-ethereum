import logging

import pytest

from pytest_ethereum.exceptions import LogError
from pytest_ethereum.testing import Log

logging.getLogger("evm").setLevel(logging.INFO)


@pytest.fixture
def ping(vyper_project_dir, vy_deployer):
    ping = vy_deployer.deploy("ping")
    return ping.deployments.get_contract_instance("ping")


def test_log_is_present(ping, w3):
    # Requires *args, asserts that every arg is present in event log values
    tx_hash = ping.functions.ping(b"1", b"2").transact()
    receipt = w3.eth.waitForTransactionReceipt(tx_hash)
    assert Log(ping.events.Ping, b"1").is_present(receipt)
    assert Log(ping.events.Ping, b"3").is_present(receipt) is False
    assert Log(ping.events.Ping, b"1", b"2").is_present(receipt)
    assert Log(ping.events.Ping, b"1", b"3").is_present(receipt) is False
    # Requires args
    with pytest.raises(LogError):
        Log(ping.events.Ping).is_present(receipt)
        Log(ping.events.Ping, first=b"1").is_present(receipt)


def test_log_exact_match(ping, w3):
    # Requires *kwargs, asserts that kwargs match exactly event logs
    tx_hash = ping.functions.ping(b"1", b"2").transact()
    receipt = w3.eth.waitForTransactionReceipt(tx_hash)
    assert Log(ping.events.Ping, first=b"1", second=b"2").exact_match(receipt)
    assert Log(ping.events.Ping, first=b"1").exact_match(receipt) is False
    # Doesn't allow kwargs not part of event signature
    with pytest.raises(LogError):
        Log(ping.events.Ping, third=b"1").exact_match(receipt) is False
    # Requires kwargs
    with pytest.raises(LogError):
        Log(ping.events.Ping).exact_match(receipt)
        Log(ping.events.Ping, b"1").exact_match(receipt)


def test_log_not_present(ping, w3):
    # Requires *args, asserts that every args is not in event log values
    tx_hash = ping.functions.ping(b"1", b"2").transact()
    receipt = w3.eth.waitForTransactionReceipt(tx_hash)
    assert Log(ping.events.Ping, b"y").not_present(receipt)
    assert Log(ping.events.Ping, b"y", b"1").not_present(receipt) is False
    assert Log(ping.events.Ping, b"1", b"2").not_present(receipt) is False
    # Requires args
    with pytest.raises(LogError):
        Log(ping.events.Ping).not_present(receipt)
        Log(ping.events.Ping, first=b"1").not_present(receipt)
