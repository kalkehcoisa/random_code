import random
import unittest


class Fixture(unittest.TestCase):
    def setUp(self):
        self.sequence = range(10)

    def test_case(self):
        element = self.sequence[random.choice(self.sequence)]
        del self.sequence[element]
        self.assertTrue(element not in self.sequence)


if __name__ == '__main__':
    unittest.main()
