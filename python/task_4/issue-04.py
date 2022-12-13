import pytest

from one_hot_encoder import fit_transform


def test_equal():
        cities = ['Moscow', 'New York', 'Moscow', 'London']
        exp_transformed_cities = [
            ('Moscow', [0, 0, 1]),
            ('New York', [0, 1, 0]),
            ('Moscow', [0, 0, 1]),
            ('London', [1, 0, 0]),
        ]
        transformed_cities = fit_transform(cities)
        assert transformed_cities == exp_transformed_cities, cities

def test_in():
    cities = ['Moscow', 'New York', 'Moscow', 'London']
    exp_first_elem = ('Moscow', [0, 0, 1])
    assert exp_first_elem in fit_transform(cities), cities

def test_empty():
    cities = []
    assert bool(fit_transform(cities)) is False, cities

def test_raise_if_not_len():
    with pytest.raises(TypeError):
        fit_transform()