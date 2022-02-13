import pytest
from solathon import utils


test_data = [
    (0, 0),
    (0.0, 0),
    (1.0, 1000000000),
    (2.0, 2 * int(utils.LAMPORT_PER_SOL)),
    (99999.0, int(99999 * utils.LAMPORT_PER_SOL)),
    (123.123, int(123.123 * utils.LAMPORT_PER_SOL)),
    (123123123123.123123123123, int(123123123123.123123123123 * utils.LAMPORT_PER_SOL))
]


@pytest.mark.parametrize("arg, expected", test_data)
def test_sol_to_lamport(arg, expected):
    actual = utils.sol_to_lamport(arg)
    assert actual == expected
    assert isinstance(actual, int)


def test_sol_to_lamport_none_passed_in():
    with pytest.raises(TypeError):
        utils.sol_to_lamport(None)


@pytest.mark.parametrize("arg, expected", [(-arg, -expected) for arg, expected in test_data])
def test_sol_to_lamport_negative_input(arg, expected):
    actual = utils.sol_to_lamport(arg)
    assert actual == expected
    assert isinstance(expected, int)
    pass


def test_sol_to_lamport_large_input():
    i = 99999999999999999999999999999.99999999999999999999999999999999
    assert utils.sol_to_lamport(i) == int(i * utils.LAMPORT_PER_SOL)
