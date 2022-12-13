import unittest

from one_hot_encoder import fit_transform


class TestFitTransform(unittest.TestCase):

    def test_equal(self):
        cities = ['Moscow', 'New York', 'Moscow', 'London']
        exp_transformed_cities = [
            ('Moscow', [0, 0, 1]),
            ('New York', [0, 1, 0]),
            ('Moscow', [0, 0, 1]),
            ('London', [1, 0, 0]),
        ]
        transformed_cities = fit_transform(cities)
        self.assertEqual(transformed_cities, exp_transformed_cities, msg=cities)

    def test_in(self):
        cities = ['Moscow', 'New York', 'Moscow', 'London']
        exp_first_elem = ('Moscow', [0, 0, 1])
        self.assertIn(exp_first_elem,  fit_transform(cities), msg=cities)

    def test_empty(self):
        cities = []
        self.assertFalse(fit_transform(cities), msg=cities)

    def test_raise_if_not_len(self):
        with self.assertRaises(TypeError):
            fit_transform()


if __name__ == '__main__':
   unittest.main()