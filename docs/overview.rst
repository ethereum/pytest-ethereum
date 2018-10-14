.. warning::

   Pytest-Ethereum is still under active development, and yet to reach a stable release. It should not be used in production yet. 

Overview
========

This library is designed to make deploying and testing smart contracts simple, using `Py-EthPM` and `pytest`. 


Vyper
-----

This library automatically reveals a ``vy_deployer`` fixture available to compile and package your vyper contracts. The ``vy_deployer`` fixture will automatically compile all vyper contracts found in a subdirectory "contracts/" of the current working directory into a manifest according to the EthPM spec(link).




Solidity
--------

This library automatically reveals a ``solc_deployer`` fixture available to package up a given solidity manifest, expose a ``Deployer`` instance. To create a manifest (link).

.. code:: python

   from ethpm import Package

   @pytest.fixture
   def owned_deployer(solc_deployer):
       owned_manifest_path = Path('to/owned/manifest.json')
       owned_deployer = solc_deployer(path=owned_manifest_path)
       return owned_deployer.deploy("Owned")


Deployer
--------

A ``Deployer`` object is created to help create contract instances for any provided contracts.

To deploy any of the available `contract types` onto the default ``w3`` instance, simply call ``deploy`` on the deployer and a newly created ``Package`` instance (which contains the newly created contract instance in its `deployments`) will be returned, along with the address of the newly deployed contract type.

.. code:: python

   from ethpm import Package
   from eth_utils import is_same_address

   @pytest.fixture
   def owned_deployer(solc_deployer):
       owned_manifest_path = Path('to/owned/manifest.json')
       owned_deployer = solc_deployer(path=owned_manifest_path)
       return owned_deployer.deploy("Owned")

   def test_owned_contract(owned_deployer)
       owned_package, owned_address = owned_deployer
       assert isinstance(owned_package, Package) 
       owned_contract_instance = owned_deployer.deployments.get_deployment_instance("Owned")
       assert is_same_address(owned_contract_instance.address, owned_address)


.. py:method:: Deployer.deploy(contract_type)

   Deploys an instance of given `contract_type` if sufficient data is present in the manifest. To add transaction kwargs (i.e. "from"), pass them in as a dict to the ``transaction`` keyword.

.. code:: python

   deploy("Contract", arg1, transaction={"from": web3.eth.accounts[1]})

.. py:method:: Deployer.register_strategy(contract_type, strategy)

   If a `contract_type` requires linking, then you *must* register a valid strategy constructed with the ``Linker`` before you can deploy an instance of the `contract_type`.


Linker
------

If a contract factory requires linking, you must register a "strategy" for a particular contract factory with the deployer. It is up to you to design an appropriate strategy for a contract factory. 

Two ``linker`` functions are made available:

.. py:method:: deploy(contract_name, *args=None)

   To deploy an instance of `contract_name`. If the contract constructor requires arguments, they must also be passed in.

.. py:method:: link(contract_name, linked_type)

   Links a `contract_name` to a `linked_type`. The `linked_type` must have already been deployed.

For example, the `Escrow` contract factory requires linking to an instance of the `SafeSendLib` before an `Escrow` contract instance can be deployed. This is how you would set up a strategy for `Escrow`

.. code:: python
  
   @pytest.fixture
   def escrow_deployer(solc_deployer, w3, manifest_dir):
       escrow_manifest_path = manifest_dir / "escrow_manifest.json"
       return solc_deployer(escrow_manifest_path), w3


   @pytest.fixture
   def escrow_contract_instance(escrow_deployer):
       deployer, w3 = escrow_deployer
       escrow_strategy = linker(
           deploy("SafeSendLib"),
           link("Escrow", "SafeSendLib"),
           deploy("Escrow", w3.eth.accounts[0]),
       )
       deployer.register_strategy("Escrow", escrow_strategy)
       linked_escrow_package, _ = deployer.deploy("Escrow") 
       return linked_escrow_package.deployments.get_deployment("Escrow")


Log
---

The ``Log`` class is available to help with testing for contract events, and the contents of the emitted logs.


``tests/fixtures/ping.vy``

.. include:: ../tests/fixtures/ping.vy
   :code: python


.. code:: python

   # SETUP
   ping_deployer = vy_deployer.deploy("ping")
   ping_instance = ping_deployer.deployments.get_contract_instance("ping")
   tx_hash = ping_instance.functions.ping(b"one", b"two")
   receipt = w3.eth.waitForTransactionReceipt(tx_hash)


.. autoclass:: pytest_ethereum.testing.Log
   :members: is_present, not_present, exact_match
