from typing import Any, Callable, Dict, Tuple  # noqa: F401

from eth_utils import to_canonical_address

from ethpm import Package
from ethpm.typing import Address
from pytest_ethereum.exceptions import DeployerError


class Deployer:
    def __init__(self, package: Package) -> None:
        if not isinstance(package, Package):
            raise TypeError(
                "Expected a Package object, instead received {0}.".format(type(package))
            )
        self.package = package
        self.strategies = {}  # type: Dict[str, Callable[[Package], Package]]

    def deploy(self, contract_type: str, *args: Any) -> Tuple[Package, Address]:
        factory = self.package.get_contract_factory(contract_type)
        if contract_type in self.strategies:
            strategy = self.strategies[contract_type]
            return strategy(self.package)
        if factory.needs_bytecode_linking:
            raise DeployerError(
                "Unable to deploy an unlinked factory. "
                "Please register a strategy for this contract type."
            )
        tx_hash = factory.constructor(*args).transact()
        tx_receipt = self.package.w3.eth.waitForTransactionReceipt(tx_hash)
        return self.package, to_canonical_address(tx_receipt.contractAddress)

    def register_strategy(
        self, contract_type: str, strategy: Callable[[Package], Package]
    ) -> None:
        self.strategies[contract_type] = strategy
