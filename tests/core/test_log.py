import logging

import pytest

from pytest_ethereum.testing import Log

logging.getLogger("evm").setLevel(logging.INFO)


@pytest.fixture
def ping_setup(deployer, manifest_dir):
    ping_deployer = deployer(manifest_dir / "ping" / "1.0.0.json")
    ping_package = ping_deployer.deploy("ping")
    ping = ping_package.deployments.get_instance("ping")
    tx_hash = ping.functions.ping(b"1", b"2").transact()
    receipt = ping_package.w3.eth.waitForTransactionReceipt(tx_hash)
    return ping, receipt


@pytest.mark.parametrize(
    "args,kwargs,expected",
    (
        ((b"1".ljust(32, b"\00"),), {}, True),
        ((), {"first": b"1".ljust(32, b"\00")}, True),
        ((), {"first": b"1".ljust(32, b"\00"), "second": b"2".ljust(32, b"\00")}, True),
        ((b"1".ljust(32, b"\00"), b"2".ljust(32, b"\00")), {}, True),
        ((b"1".ljust(32, b"\00"),), {"second": b"2".ljust(32, b"\00")}, True),
        ((b"3".ljust(32, b"\00"),), {}, False),
        ((), {"first": b"3".ljust(32, b"\00")}, False),
        ((b"1".ljust(32, b"\00"),), {"second": b"3".ljust(32, b"\00")}, False),
    ),
)
def test_log_is_present(ping_setup, w3, args, kwargs, expected):
    ping, receipt = ping_setup
    # Asserts that every arg is present in event log values
    assert Log(ping.events.Ping, *args, **kwargs).is_present(receipt) is expected


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
    with pytest.raises(TypeError):
        Log(ping.events.Ping, *args, **kwargs).is_present(receipt)


@pytest.mark.parametrize(
    "args,kwargs,expected",
    (
        ((), {"first": b"1".ljust(32, b"\00"), "second": b"2".ljust(32, b"\00")}, True),
        ((), {"first": b"1".ljust(32, b"\00")}, False),
        ((), {"second": b"2".ljust(32, b"\00")}, False),
    ),
)
def test_log_exact_match(ping_setup, w3, args, kwargs, expected):
    ping, receipt = ping_setup
    # Requires *kwargs, asserts that kwargs match exactly event logs
    assert Log(ping.events.Ping, *args, **kwargs).exact_match(receipt) is expected


@pytest.mark.parametrize(
    "args,kwargs", (((), {}), ((b"1"), {}), ((b"1"), {"first": b"2"}))
)
def test_log_exact_match_raises_exception_with_invalid_args_kwargs(
    ping_setup, args, kwargs
):
    ping, receipt = ping_setup
    with pytest.raises(TypeError):
        Log(ping.events.Ping, *args, **kwargs).exact_match(receipt)


@pytest.mark.parametrize(
    "kwargs", (({"invalid": b"1"}), ({"first": b"1", "invalid": b"2"}))
)
def test_invalid_keywords_raise_exception_on_log_instantiation(ping_setup, kwargs):
    ping, receipt = ping_setup
    with pytest.raises(TypeError):
        Log(ping.events.Ping, **kwargs)


@pytest.mark.parametrize(
    "args,kwargs,expected",
    (
        ((b"y".ljust(32, b"\00"),), {}, True),
        ((), {"first": b"y".ljust(32, b"\00")}, True),
        ((), {"first": b"1".ljust(32, b"\00")}, False),
        ((b"y",), {"second": b"1".ljust(32, b"\00")}, False),
        ((b"1",), {"second": b"2".ljust(32, b"\00")}, False),
        ((b"y",), {"second": b"1".ljust(32, b"\00")}, False),
        (
            (),
            {"first": b"y".ljust(32, b"\00"), "second": b"1".ljust(32, b"\00")},
            False,
        ),
    ),
)
def test_log_not_present(ping_setup, w3, args, kwargs, expected):
    ping, receipt = ping_setup
    # asserts that every args is not in event log values
    assert Log(ping.events.Ping, *args, **kwargs).not_present(receipt) is expected


@pytest.mark.parametrize("args,kwargs", (((), {}), ((b"1"), {"first": b"2"})))
def test_log_not_present_raises_exception_with_invalid_args_kwargs(
    ping_setup, args, kwargs
):
    ping, receipt = ping_setup
    with pytest.raises(TypeError):
        Log(ping.events.Ping, *args, **kwargs).not_present(receipt)
