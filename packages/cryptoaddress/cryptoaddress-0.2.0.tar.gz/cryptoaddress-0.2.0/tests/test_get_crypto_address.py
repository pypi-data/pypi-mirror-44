from typing import Optional

import pytest

from cryptoaddress import get_crypto_address


@pytest.mark.parametrize(('address', 'network_type', 'symbol'), (
    ('1BoatSLRHtKNngkdXEeobR76b53LETtpyT', 'mainnet', 'BTC'),
    ('mtQFox84Lx8RLQCXtVzVn1VfXP6bqbMFC1', 'testnet', 'BTC'),
    ('3QfXkWcNsUH5rRJNurn5whbKJpniVmxmV5', 'mainnet', 'LTC'),
    ('mgYdmeWGZTBoZ9wyxuAFkregSoWga585Mu', 'testnet', 'LTC'),
    ('0x059208c7109dd409f68770ea943b5f0c0eb41db8', None, 'ETH'),
    ('0x59A5208B32E627891C389EBAFC644145224006E8', None, 'ETH'),
))
def test_valid_values(address: str, network_type: Optional[str], symbol: str) -> None:
    """Verify that valid crypto addresses are successfully created."""
    kwargs = {'network_type': network_type} if network_type is not None else {}
    cryptoaddress = get_crypto_address(symbol, address, **kwargs)
    assert str(cryptoaddress) == address
