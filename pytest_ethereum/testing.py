from typing import Any, Dict

from eth_tester.exceptions import TransactionFailed
import pytest
from web3.contract import ContractEvent

from pytest_ethereum.exceptions import LogError

TxReceipt = Dict[str, Any]


class Log:
    def __init__(
        self, contract_event: ContractEvent, *args: Any, **kwargs: Any
    ) -> None:
        """
        The ``Log`` class is available to help with testing for contract events,
        and the contents of the emitted logs.
        """
        self.event = contract_event()
        self.args = args
        self.kwargs = kwargs

    def is_present(self, receipt: TxReceipt) -> bool:
        """
        Asserts that *every* member of ``args`` is present in the emitted log dictionary values.
        Requires ``*args``, and does not accept ``*kwargs``.

        .. code:: python

           assert Log(ping.events.Ping, b"one").is_present(receipt)
           assert Log(ping.events.Ping, b"missing").is_present(receipt) is False
           assert Log(ping.events.Ping, b"one", b"missing").is_present(receipt) is False

        """
        if self.kwargs or not self.args:
            raise LogError(
                "Log.is_present() requires variable args, and cannot be used with kwargs."
            )
        logs = self._process_receipt(receipt)
        missing_args = [arg for arg in self.args if arg not in logs.values()]
        if missing_args:
            return False
        return True

    def not_present(self, receipt: TxReceipt) -> bool:
        """
        Asserts that *every* member of ``args`` are *not* present in the emitted log dictionary
        values. Requires ``*args``, and does not accept ``*kwargs``.

        .. code:: python

           assert Log(ping.events.Ping, b"missing").not_present(receipt)
           assert Log(ping.events.Ping, b"one").not_present(receipt) is False
           assert Log(ping.events.Ping, b"one", b"missing").not_present(receipt) is False
        """
        if self.kwargs or not self.args:
            raise LogError(
                "Log.not_present() requires variable args, and cannot be used with kwargs."
            )
        logs = self._process_receipt(receipt)
        matching_args = [arg for arg in self.args if arg in logs.values()]
        if matching_args:
            return False
        return True

    def exact_match(self, receipt: TxReceipt) -> bool:
        """
        Asserts that the provided ``kwargs`` match *exactly* the emitted log dictionary.
        Requires ``**kwargs``, and does not accept ``*args``.

        .. code:: python

           assert Log(ping.events.Ping, first=b"one", second=b"two").exact_match(receipt)
           assert Log(ping.events.Ping, first=b"one").exact_match(receipt) is False
           assert Log(ping.events.Ping, first=b"not_present").exact_match(receipt) is False
        """
        if self.args or not self.kwargs:
            raise LogError(
                "Log.match() requires variable kwargs, and cannot be used with args."
            )
        logs = self._process_receipt(receipt)

        if any(kwarg not in logs.keys() for kwarg in self.kwargs):
            raise LogError("Kwargs found which are not present in event signature.")

        if self.kwargs != logs:
            return False
        return True

    def _process_receipt(self, receipt: TxReceipt) -> Dict[str, bytes]:
        processed_receipt = self.event.processReceipt(receipt)[0]
        return {k: v.rstrip(b"\x00") for k, v in processed_receipt["args"].items()}


def tx_fail(*args: Any, **kwargs: Any) -> None:
    return pytest.raises(TransactionFailed, *args, **kwargs)
