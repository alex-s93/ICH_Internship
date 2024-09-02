from unittest.mock import patch
import io

from auto_graders.constants import (
    SOLUTION_FILE_NAME,
    SYS_STDOUT,
    BUILTINS_INPUT,
    COMPILE_MODE,
)
from auto_graders.informative_test_case import InformativeTestCase

EXPECTED_MSG = "Sum and product of the numbers: ({}, {})"


class TestSumProduct(InformativeTestCase):

    def format_float(self, tuple_str):
        numbers = tuple(map(float, tuple_str.strip('()').split(', ')))
        return numbers

    def run_sum_product_test(self, input_values, expected_output, mock_stdout):
        with patch(BUILTINS_INPUT, side_effect=input_values):
            with open(SOLUTION_FILE_NAME) as f:
                code = compile(f.read(), SOLUTION_FILE_NAME, COMPILE_MODE)
                exec(code)

        actual_output = mock_stdout.getvalue().strip()
        actual_numbers = self.format_float(actual_output.split(": ")[1])
        expected_output = self.format_float(expected_output.split(": ")[1])

        self.assertEqual(actual_numbers, expected_output)

    @patch(SYS_STDOUT, new_callable=io.StringIO)
    def test_int_numbers(self, mock_stdout):
        """Check if the provided solution works with integer numbers
        INPUT VALUES: ['2', '5']"""
        input_values = ['2', '5']
        expected_output = EXPECTED_MSG.format(7.0, 10.0)
        self.run_sum_product_test(input_values, expected_output, mock_stdout)

    @patch(SYS_STDOUT, new_callable=io.StringIO)
    def test_float_numbers(self, mock_stdout):
        """Check if the provided solution works with float numbers
        INPUT VALUES: ['2.0', '5.1']"""
        input_values = ['2.0', '5.1']
        expected_output = EXPECTED_MSG.format(7.1, 10.2)
        self.run_sum_product_test(input_values, expected_output, mock_stdout)

    @patch(SYS_STDOUT, new_callable=io.StringIO)
    def test_float_negative_and_positive(self, mock_stdout):
        """Check if the provided solution works with negative and positive numbers
        INPUT VALUES: ['-3.5', '4.5']"""
        input_values = ['-3.5', '4.5']
        expected_output = EXPECTED_MSG.format(1.0, -15.75)
        self.run_sum_product_test(input_values, expected_output, mock_stdout)

    @patch(SYS_STDOUT, new_callable=io.StringIO)
    def test_int_negative(self, mock_stdout):
        """Check if the provided solution works with negative integer numbers
        INPUT VALUES: ['-4', '-6']"""
        input_values = ['-4', '-6']
        expected_output = EXPECTED_MSG.format(-10.0, 24.0)
        self.run_sum_product_test(input_values, expected_output, mock_stdout)

    @patch(SYS_STDOUT, new_callable=io.StringIO)
    def test_float_negative(self, mock_stdout):
        """Check if the provided solution works with negative float numbers
        INPUT VALUES: ['-2.5', '-4.5']"""
        input_values = ['-2.5', '-4.5']
        expected_output = EXPECTED_MSG.format(-7.0, 11.25)
        self.run_sum_product_test(input_values, expected_output, mock_stdout)

    @patch(SYS_STDOUT, new_callable=io.StringIO)
    def test_float_zero_and_negative(self, mock_stdout):
        """Check if the provided solution works with zero and negative float numbers
        INPUT VALUES: ['0.0', '-2.5']"""
        input_values = ['0.0', '-2.5']
        expected_output = EXPECTED_MSG.format(-2.5, -0.0)
        self.run_sum_product_test(input_values, expected_output, mock_stdout)

    @patch(SYS_STDOUT, new_callable=io.StringIO)
    def test_float_zero_and_positive(self, mock_stdout):
        """Check if the provided solution works with positive and zero float numbers
        INPUT VALUES: ['8.3', '0.0']"""
        input_values = ['8.3', '0.0']
        expected_output = EXPECTED_MSG.format(8.3, 0.0)
        self.run_sum_product_test(input_values, expected_output, mock_stdout)

    @patch(SYS_STDOUT, new_callable=io.StringIO)
    def test_zeros(self, mock_stdout):
        """Check if the provided solution works with both zeros
        INPUT VALUES: ['0', '0']"""
        input_values = ['0', '0']
        expected_output = EXPECTED_MSG.format(0.0, 0.0)
        self.run_sum_product_test(input_values, expected_output, mock_stdout)
