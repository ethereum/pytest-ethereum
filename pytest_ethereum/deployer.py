from eth_utils import to_canonical_address

from ethpm import Package


class Deployer:
    def __init__(self, package):
        if not isinstance(package, Package):
            raise TypeError(
                "Expected a Package object, instead received {0}.".format(type(package))
            )
        self.package = package

    def deploy(self, contract_type, *args):
        factory = self.package.get_contract_factory(contract_type)
        if factory.has_linkable_bytecode():
            raise TypeError("don't support link refs yet.")
        tx_hash = factory.constructor(*args).transact()
        tx_receipt = self.package.w3.eth.waitForTransactionReceipt(tx_hash)
        return self.package, to_canonical_address(tx_receipt.contractAddress)
