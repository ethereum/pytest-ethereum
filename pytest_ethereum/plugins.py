import json
from pathlib import Path
from typing import Callable, Optional

import pytest
from twig.backends.vyper import VyperBackend
from twig.utils.compiler import generate_contract_types, generate_inline_sources
from web3 import Web3

from ethpm import Package
from ethpm.tools import builder as b
from ethpm.typing import Manifest
from pytest_ethereum.deployer import Deployer


@pytest.fixture
def w3() -> Web3:
    w3 = Web3(Web3.EthereumTesterProvider())
    return w3


SOURCES_GLOB = "**/*.vy"


def vy_manifest(path: Path, name: str, version: str) -> Manifest:
    """
    Returns a manifest automatically containing the data for all vyper files found in the folder
    located at `path`, and uses the provided `name` and `version`.
    """
    all_sources = path.glob(SOURCES_GLOB)
    backend = VyperBackend()
    compiler_output = backend.compile(all_sources)
    composed_contract_types = generate_contract_types(compiler_output)
    composed_inline_sources = generate_inline_sources(compiler_output)
    manifest = b.build(
        {},
        b.package_name(name),
        b.version(version),
        b.manifest_version("2"),
        *composed_inline_sources,
        *composed_contract_types,
        b.validate(),
    )
    return manifest


@pytest.fixture
def vy_deployer(w3: Web3) -> Callable[[Path, str, str], Deployer]:
    """
    Returns a `Deployer` instance composed from a `Package` instance generated from a manifest
    that contains all of the vyper files found in the provided `path` folder. Manifest `name` and
    `version` default to `twig` and `1.0.0` respectively, if no args are provided.
    """

    def _twig_deployer(
        path: Path, name: Optional[str] = "twig", version: Optional[str] = "1.0.0"
    ) -> Deployer:
        manifest = vy_manifest(path, name, version)
        pkg = Package(manifest, w3)
        return Deployer(pkg)

    return _twig_deployer


@pytest.fixture
def solc_deployer(w3: Web3) -> Callable[[Path], Deployer]:
    """
    Returns a `Deployer` instance composed from a `Package` instance generated from the manifest
    located at the provided `path` folder.
    """

    def _solc_deployer(path: Path) -> Deployer:
        manifest = json.loads(path.read_text())
        package = Package(manifest, w3)
        return Deployer(package)

    return _solc_deployer
