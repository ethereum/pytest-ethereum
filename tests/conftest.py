from pathlib import Path
import shutil

import pytest

from ethpm import ASSETS_DIR

BASE_FIXTURES_DIR = Path(__file__).parent / "fixtures"


@pytest.fixture
def manifest_dir():
    return Path(__file__).parent / "manifests"


@pytest.fixture
def vyper_project_dir(tmpdir, monkeypatch):
    p = tmpdir.mkdir("vyper_project")
    shutil.copytree(BASE_FIXTURES_DIR, p / "contracts")
    monkeypatch.chdir(str(p))
    return str(p)


# LINK REFS
@pytest.fixture
def escrow_deployer(solc_deployer, w3):
    escrow_manifest_path = ASSETS_DIR / "escrow" / "1.0.2.json"
    return solc_deployer(escrow_manifest_path), w3
