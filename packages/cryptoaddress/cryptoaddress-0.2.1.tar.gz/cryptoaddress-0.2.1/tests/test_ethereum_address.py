import pytest

from cryptoaddress.core import EthereumAddress


@pytest.mark.parametrize('address', (
    '0x29793eef0ec35fba79945a32c005f7ec75ba2afc',
    '0x59a5208b32e627891c389ebafc644145224006e8',
    '0xbfa19376ce5d628f8c3928469388d625a3a79a06',
    '0x059208c7109dd409f68770ea943b5f0c0eb41db8',
    '0x3f5ce5fbfe3e9af3971dd833d26ba9b5c936f0be',
    '0x08f5a9235b08173b7569f83645d2c7fb55e8ccd8',
    '0x59a5208b32e627891c389ebafc644145224006e8',
    '0x0000000000085d4780b73119b644ae5ecd22b376',
    '0x37df0d9beccd412951500f0e33f0c3721fb4dc31',
    '0xb2930b35844a230f00e51431acae96fe543a0347',
    '0x29793EEF0EC35FBA79945A32C005F7EC75BA2AFC',
    '0x59A5208B32E627891C389EBAFC644145224006E8',
    '0xBFA19376CE5D628F8C3928469388D625A3A79A06',
    '0x059208C7109DD409F68770EA943B5F0C0EB41DB8',
    '0x3F5CE5FBFE3E9AF3971DD833D26BA9B5C936F0BE',
    '0x08F5A9235B08173B7569F83645D2C7FB55E8CCD8',
    '0x59A5208B32E627891C389EBAFC644145224006E8',
    '0x0000000000085D4780B73119B644AE5ECD22B376',
    '0x37DF0D9BECCD412951500F0E33F0C3721FB4DC31',
    '0xB2930B35844A230F00E51431ACAE96FE543A0347',
))
def test_valid_values(address: str) -> None:
    """Verify that valid Ethereum addresses are successfully created."""
    ethereum_address = EthereumAddress(address)
    assert str(ethereum_address) == address
    assert not ethereum_address.is_checksum_address


@pytest.mark.parametrize('address', (
    '',
    '0x',
    '0x123456789012345678901234567890',
    '0xn4rDEvfVYwDfRj5NBkcF9Y4EaJk7WXnfgZ',
    '3A7RgyQMesCyiyXobneBnncSDSwFKTJUSw',
))
def test_invalid_values(address: str) -> None:
    """Verify that invalid Ethereum addresses are detected."""
    with pytest.raises(ValueError):
        EthereumAddress(address)


@pytest.mark.parametrize('address', (
    '0x29793eeF0Ec35Fba79945A32C005F7Ec75Ba2Afc',
    '0x59a5208B32e627891C389EbafC644145224006E8',
    '0xBfa19376ce5d628F8C3928469388d625A3a79A06',
    '0x059208c7109dd409f68770Ea943B5F0c0Eb41dB8',
    '0x3f5CE5FBFe3E9af3971dD833D26bA9b5C936f0bE',
    '0x08f5a9235B08173b7569F83645d2c7fB55e8cCD8',
    '0x0000000000085d4780B73119b644AE5ecd22b376',
    '0x37DF0D9bEccd412951500f0e33f0c3721Fb4dC31',
    '0xb2930B35844a230f00E51431aCAe96Fe543a0347',
))
def test_checksum_address(address: str) -> None:
    ethereum_address = EthereumAddress(address)
    assert str(ethereum_address) == address
    assert ethereum_address.is_checksum_address is True


@pytest.mark.parametrize('address', (
    '0x29793eeF0Ec35Fba79945A32C105F7Ec75Ba2Afc',
    '0x59a5208B32e627891c389EbafC644145224006E8',
    '0xBfa19376ce5d628F8c3928469388d625A3a79A06',
    '0x059208c7109dd409f68770Ea943B5f0c0Eb41dB8',
    '0x3f5CD5FBFe3E9af3971dD833D26ba9b5C936f0bE',
    '0x08f2a9235B08173b7569F83645d2c7fB55e8cCD8',
    '0x59a5108B32e627891C389EbafC644145224006E8',
    '0x0000000000085d4780B73119B644AE5ecd22b376',
    '0x37DF0D9bEccd412951500F0e33f0c3721Fb4dC31',
    '0xb2930B35844a230f00E51031aCAe96Fe543a0347',
))
def test_invalid_checksum(address: str) -> None:
    with pytest.raises(ValueError):
        EthereumAddress(address)


@pytest.mark.parametrize('address', (
    '29793eeF0Ec35Fba79945A32C005F7Ec75Ba2Afc',
    '59a5208B32e627891C389EbafC644145224006E8',
    'Bfa19376ce5d628F8C3928469388d625A3a79A06',
    '29793eef0ec35fba79945a32c005f7ec75ba2afc',
    '59a5208b32e627891c389ebafc644145224006e8',
    'bfa19376ce5d628f8c3928469388d625a3a79a06',
    '059208c7109dd409f68770ea943b5f0c0eb41db8',
    '3f5ce5fbfe3e9af3971dd833d26ba9b5c936f0be',
    '08f5a9235b08173b7569f83645d2c7fb55e8ccd8',
    '08F5A9235B08173B7569F83645D2C7FB55E8CCD8',
    '59A5208B32E627891C389EBAFC644145224006E8',
    '0000000000085D4780B73119B644AE5ECD22B376',
    '37DF0D9BECCD412951500F0E33F0C3721FB4DC31',
    'B2930B35844A230F00E51431ACAE96FE543A0347',
))
def test_missing_0x(address: str) -> None:
    ethereum_address = EthereumAddress(address)
    assert str(ethereum_address) == '0x{}'.format(address)
