import logging

import pytest

from pytest_ethereum.exceptions import LogError
from pytest_ethereum.testing import Log

logging.getLogger("evm").setLevel(logging.INFO)


@pytest.fixture
def ping_setup(vyper_project_dir, vy_deployer, w3):
    ping_deployer = vy_deployer.deploy("ping")
    ping = ping_deployer.deployments.get_contract_instance("ping")
    tx_hash = ping.functions.ping(b"1", b"2").transact()
    receipt = w3.eth.waitForTransactionReceipt(tx_hash)
    return ping, receipt


def test_log_is_present(ping_setup, w3):
    ping, receipt = ping_setup
    # Requires *args, asserts that every arg is present in event log values
    assert Log(ping.events.Ping, b"1").is_present(receipt)
    assert Log(ping.events.Ping, first=b"1").is_present(receipt)
    assert Log(ping.events.Ping, first=b"1", second=b"2").is_present(receipt)
    assert Log(ping.events.Ping, b"1", b"2").is_present(receipt)
    assert Log(ping.events.Ping, b"1", second=b"2").is_present(receipt)
    assert Log(ping.events.Ping, b"3").is_present(receipt) is False
    assert Log(ping.events.Ping, first=b"3").is_present(receipt) is False
    assert Log(ping.events.Ping, b"1", b"3").is_present(receipt) is False


@pytest.mark.parametrize(
    "args,kwargs",
    (
        ((), {}),
        ((), {"invalid": b"1"}),
        ((), {"first": b"1", "invalid": b"2"}),
        ((b"1"), {"first": b"2"}),
    ),
)
def test_log_is_present_raises_exception_with_invalid_args_kwargs(
    ping_setup, args, kwargs
):
    ping, receipt = ping_setup
    with pytest.raises(LogError):
        Log(ping.events.Ping, *args, **kwargs).is_present(receipt)


def test_log_exact_match(ping_setup, w3):
    ping, receipt = ping_setup
    # Requires *kwargs, asserts that kwargs match exactly event logs
    assert Log(ping.events.Ping, first=b"1", second=b"2").exact_match(receipt)
    assert Log(ping.events.Ping, first=b"1").exact_match(receipt) is False
    assert Log(ping.events.Ping, second=b"2").exact_match(receipt) is False


@pytest.mark.parametrize(
    "args,kwargs",
    (
        ((), {}),
        ((b"1"), {}),
        ((), {"invalid": b"1"}),
        ((), {"first": b"1", "invalid": b"2"}),
        ((b"1"), {"first": b"2"}),
    ),
)
def test_log_exact_match_raises_exception_with_invalid_args_kwargs(
    ping_setup, args, kwargs
):
    ping, receipt = ping_setup
    with pytest.raises(LogError):
        Log(ping.events.Ping, *args, **kwargs).exact_match(receipt)


def test_log_not_present(ping_setup, w3):
    ping, receipt = ping_setup
    # asserts that every args is not in event log values
    assert Log(ping.events.Ping, b"y").not_present(receipt)
    assert Log(ping.events.Ping, first=b"y").not_present(receipt)
    assert Log(ping.events.Ping, first=b"1").not_present(receipt) is False
    assert Log(ping.events.Ping, b"y", b"1").not_present(receipt) is False
    assert Log(ping.events.Ping, b"1", b"2").not_present(receipt) is False
    assert Log(ping.events.Ping, b"y", second=b"1").not_present(receipt) is False
    assert Log(ping.events.Ping, first=b"y", second=b"1").not_present(receipt) is False


@pytest.mark.parametrize(
    "args,kwargs",
    (
        ((), {}),
        ((), {"invalid": b"1"}),
        ((), {"first": b"1", "invalid": b"2"}),
        ((b"1"), {"first": b"2"}),
    ),
)
def test_log_not_present_raises_exception_with_invalid_args_kwargs(
    ping_setup, args, kwargs
):
    ping, receipt = ping_setup
    with pytest.raises(LogError):
        Log(ping.events.Ping, *args, **kwargs).not_present(receipt)
