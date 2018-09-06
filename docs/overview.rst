Overview
========

Pytest-Ethereum is still under active development, and yet to reach a stable release. It should not be used in production yet. 

Usage
-----

This library automatically reveals a ``deployer`` fixture available for your tests. The ``deployer`` fixture will automatically compile all vyper contracts found in a subdirectory "contracts/" of the current working directory into a manifest according to the EthPM spec..

To deploy any of these contracts onto the default ``w3`` instance, simply call ``deploy`` on the deployer and a ``w3.contract.Contract`` instance will be returned representing the freshly deployed contract.

.. code:: python

    @pytest.fixture
    def contract_name(deployer):
        return deployer.deploy("ContractName")

