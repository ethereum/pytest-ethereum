from pathlib import Path
import shutil

import pytest

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
def escrow_deployer(solc_deployer, w3, manifest_dir):
    escrow_manifest_path = manifest_dir / "escrow_manifest.json"
    return solc_deployer(escrow_manifest_path), w3
