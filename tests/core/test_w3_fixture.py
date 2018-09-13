from web3 import Web3


def test_w3_fixture_is_available(request):
    w3 = request.getfixturevalue("w3")
    assert isinstance(w3, Web3)
