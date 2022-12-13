import pytest

from morse import LETTER_TO_MORSE, MORSE_TO_LETTER, decode


@pytest.mark.parametrize(
    'morse_message, decode_message', 
    [
        ('... --- ...', 'SOS'),
        ('- . ... -', 'TEST'),
        ('-- --- .-. ... .', 'MORSE'),
    ]
)

def test_decode(morse_message, decode_message):
    assert decode(morse_message) == decode_message 

def test_letter_not_in_morse():
    with pytest.raises(KeyError):
        decode('test')