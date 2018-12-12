from pathlib import Path

from ethpm import ASSETS_DIR
import pytest

TESTS_DIR = Path(__file__).parent

pytest_plugins = ["pytest_ethereum.plugins"]


@pytest.fixture
def manifest_dir():
    return TESTS_DIR / "manifests"


# LINK REFS
@pytest.fixture
def escrow_deployer(deployer):
    escrow_manifest_path = ASSETS_DIR / "escrow" / "1.0.2.json"
    return deployer(escrow_manifest_path)
