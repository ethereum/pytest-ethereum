def test_manifest_fixture(request, vyper_project_dir):
    manifest = request.getfixturevalue("manifest")
    assert isinstance(manifest, dict)
    assert "sources" in manifest
    assert "contract_types" in manifest
