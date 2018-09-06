from eth_utils import to_canonical_address

from ethpm import Package


class Deployer:
    def __init__(self, package):
        if not isinstance(package, Package):
            raise TypeError(
                "Expected a Package object, instead received {0}.".format(type(package))
            )
        self.package = package

    def deploy(self, package_name):
        factory = self.package.get_contract_factory(package_name)
        tx_hash = factory.constructor().transact()
        tx_receipt = self.package.w3.eth.waitForTransactionReceipt(tx_hash)
        contract_instance = self.package.w3.eth.contract(
            address=to_canonical_address(tx_receipt.contractAddress), abi=factory.abi
        )
        return contract_instance
