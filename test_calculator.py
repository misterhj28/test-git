import unittest

from Calculate import CalculatorApp


class CalculatorTests(unittest.TestCase):
    def setUp(self):
        self.app = CalculatorApp.__new__(CalculatorApp)

    def test_simple_addition(self):
        expr = self.app._sanitize_expression("1+1")
        self.assertEqual(expr, "1+1")
        self.assertEqual(self.app._evaluate(expr), 2)

    def test_simple_multiplication(self):
        expr = self.app._sanitize_expression("3*3")
        self.assertEqual(expr, "3*3")
        self.assertEqual(self.app._evaluate(expr), 9)


if __name__ == "__main__":
    unittest.main()
