import pytest

GREETER_SOURCE = """
# Vyper Greeter Contract

greeting: bytes[20]


@public
def __init__():
    self.greeting = "Hello"


@public
def setGreeting(x: bytes[20]):
    self.greeting = x


@public
def greet() -> bytes[40]:
    return self.greeting
"""

REGISTRY_SOURCE = """
registry: address[bytes[100]]


@public
def register(name: bytes[100], owner: address):
    assert self.registry[name] == ZERO_ADDRESS  # check name has not been set yet.
    self.registry[name] = owner


@public
@constant
def lookup(name: bytes[100]) -> address:
    return self.registry[name]
"""


@pytest.fixture
def vyper_project_dir(tmpdir, monkeypatch):
    p = tmpdir.mkdir("vyper_project")
    monkeypatch.chdir(str(p))
    contracts_dir = p.mkdir("contracts")
    greeter = contracts_dir.join("Greeter.vy")
    registry_dir = contracts_dir.mkdir("registry")
    registry = registry_dir.join("Registry.vy")
    greeter.write(GREETER_SOURCE)
    registry.write(REGISTRY_SOURCE)
    return str(p)
