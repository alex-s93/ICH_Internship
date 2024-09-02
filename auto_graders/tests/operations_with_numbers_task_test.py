from unittest.mock import patch
import io

from auto_graders.constants import (
    SOLUTION_FILE_NAME,
    SYS_STDOUT,
    BUILTINS_INPUT,
    COMPILE_MODE,
)
from auto_graders.informative_test_case import InformativeTestCase

EXPECTED_MSG = '''Sum: {}
Difference: {}
Product: {}
Quotient: {}
Remainder: {}
First number raised to the power of the second number: {}
'''


class TestArithmeticOperations(InformativeTestCase):

    def run_arithmetic_test(self, num1, num2, expected_output):
        with patch(SYS_STDOUT, new_callable=io.StringIO) as mock_stdout:
            with patch(BUILTINS_INPUT, side_effect=[num1, num2]):
                with open(SOLUTION_FILE_NAME) as f:
                    code = compile(f.read(), SOLUTION_FILE_NAME, COMPILE_MODE)
                    exec(code)

        self.assertEqual(mock_stdout.getvalue(), expected_output)

    def test_valid_input(self):
        """Check if the provided solution works with two positive numbers.
        INPUT VALUES: '5, 2'"""
        num1, num2 = '5', '2'
        expected_output = EXPECTED_MSG.format(7, 3, 10, 2.5, 1, 25)
        self.run_arithmetic_test(num1, num2, expected_output)

    def test_first_zero_second_positive(self):
        """Check if the provided solution works with zero and positive number.
        INPUT VALUES: '0, 5'"""
        num1, num2 = '0', '5'
        expected_output = EXPECTED_MSG.format(5, -5, 0, 0.0, 0, 0)
        self.run_arithmetic_test(num1, num2, expected_output)

    def test_first_positive_second_zero(self):
        """Check if the provided solution works with positive number and zero.
        INPUT VALUES: '5, 0'"""
        num1, num2 = '5', '0'
        expected_output = EXPECTED_MSG.format(
            5, 5, 0, 'undefined', 'undefined', 1
        )
        self.run_arithmetic_test(num1, num2, expected_output)

    def test_both_zero(self):
        """Check if the provided solution works with two zeros.
        INPUT VALUES: '0, 0'"""
        num1, num2 = '0', '0'
        expected_output = EXPECTED_MSG.format(
            0, 0, 0, 'undefined', 'undefined', 1
        )
        self.run_arithmetic_test(num1, num2, expected_output)

    def test_first_negative_second_positive(self):
        """Check if the provided solution works with negative and positive numbers.
        INPUT VALUES: '-3, 4'"""
        num1, num2 = '-3', '4'
        expected_output = EXPECTED_MSG.format(1, -7, -12, -0.75, 1, 81)
        self.run_arithmetic_test(num1, num2, expected_output)

    def test_first_positive_second_negative(self):
        """Check if the provided solution works with positive and negative numbers.
        INPUT VALUES: '2, -3'"""
        num1, num2 = '2', '-3'
        expected_output = EXPECTED_MSG.format(
            -1, 5, -6, -0.6666666666666666, -1, 0.125
        )
        self.run_arithmetic_test(num1, num2, expected_output)

    def test_both_negative(self):
        """Check if the provided solution works with both negative numbers.
        INPUT VALUES: '-2, -5'"""
        num1, num2 = '-2', '-5'
        expected_output = EXPECTED_MSG.format(-7, 3, 10, 0.4, -2, -0.03125)
        self.run_arithmetic_test(num1, num2, expected_output)

    def test_first_negative_second_zero(self):
        """Check if the provided solution works with negative number and zero.
        INPUT VALUES: '-4, 0'"""
        num1, num2 = '-4', '0'
        expected_output = EXPECTED_MSG.format(
            -4, -4, 0, 'undefined', 'undefined', 1
        )
        self.run_arithmetic_test(num1, num2, expected_output)
