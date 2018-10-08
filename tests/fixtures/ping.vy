Ping: event({first: indexed(bytes32), second: bytes32})

@public
def __init__():
    pass

@public
def ping(_first: bytes32, _second: bytes32):
    log.Ping(_first, _second)
