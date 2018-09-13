from pathlib import Path
import shutil

import pytest

BASE_FIXTURES_DIR = Path(__file__).parent / "fixtures"


@pytest.fixture
def vyper_project_dir(tmpdir, monkeypatch):
    p = tmpdir.mkdir("vyper_project")
    shutil.copytree(BASE_FIXTURES_DIR, p / "contracts")
    monkeypatch.chdir(str(p))
    return str(p)
