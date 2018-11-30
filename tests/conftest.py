from pathlib import Path
import shutil

import pytest

from ethpm import ASSETS_DIR

TESTS_DIR = Path(__file__).parent
FIXTURES_DIR = TESTS_DIR / "fixtures"

pytest_plugins = ["pytest_ethereum.plugins"]


@pytest.fixture
def manifest_dir():
    return TESTS_DIR / "manifests"


@pytest.fixture
def fixtures_dir():
    return FIXTURES_DIR


@pytest.fixture
def vyper_project_dir(tmpdir, monkeypatch):
    p = tmpdir.mkdir("vyper_project")
    shutil.copytree(FIXTURES_DIR, p / "contracts")
    monkeypatch.chdir(str(p))
    return str(p)


# LINK REFS
@pytest.fixture
def escrow_deployer(solc_deployer, w3):
    escrow_manifest_path = ASSETS_DIR / "escrow" / "1.0.2.json"
    return solc_deployer(escrow_manifest_path), w3
