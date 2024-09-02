from unittest.mock import patch
import io
from math import pi

from auto_graders.constants import (
    SOLUTION_FILE_NAME,
    SYS_STDOUT,
    BUILTINS_INPUT,
    COMPILE_MODE,
)
from auto_graders.informative_test_case import InformativeTestCase

POSITIVE_MESSAGE = "Circumference: {:.2f}\nArea: {:.2f}\n"


class CircumferenceAndAreaCalculatorTest(InformativeTestCase):

    def execute_test(self, mock_stdout, input_value: str, output_value: str):
        with patch(BUILTINS_INPUT, return_value=input_value):
            with open(SOLUTION_FILE_NAME) as f:
                code = compile(f.read(), SOLUTION_FILE_NAME, COMPILE_MODE)
                exec(code)
        self.assertEqual(mock_stdout.getvalue(), output_value)

    @patch(SYS_STDOUT, new_callable=io.StringIO)
    def test_positive_integer_radius(self, mock_stdout):
        """Check if the provided solution works with positive integer radius
        INPUT VALUES: '4'"""
        input_value = "4"
        expected_output = POSITIVE_MESSAGE.format(25.13, 50.27)
        self.execute_test(mock_stdout, input_value, expected_output)

    @patch(SYS_STDOUT, new_callable=io.StringIO)
    def test_positive_float_radius(self, mock_stdout):
        """Check if the provided solution works with positive float radius
        INPUT VALUES: '4.7'"""
        input_value = "4.7"
        expected_output = POSITIVE_MESSAGE.format(29.53, 69.40)
        self.execute_test(mock_stdout, input_value, expected_output)

    @patch(SYS_STDOUT, new_callable=io.StringIO)
    def small_positive_float_radius(self, mock_stdout):
        """Check if the provided solution works with small positive float radius
        INPUT VALUES: '1e-6'"""
        input_value = "1e-6"
        expected_output = POSITIVE_MESSAGE.format(6.28, 3.14)
        self.execute_test(mock_stdout, input_value, expected_output)

    @patch(SYS_STDOUT, new_callable=io.StringIO)
    def test_big_positive_float_radius(self, mock_stdout):
        """Check if the provided solution works with big positive float radius
        INPUT VALUES: '1e-6'"""
        input_value = "1e6"
        expected_output = POSITIVE_MESSAGE.format(6283185.31, 3141592653589.79)
        self.execute_test(mock_stdout, input_value, expected_output)
