from unittest.mock import patch
import io

from auto_graders.constants import (
    SOLUTION_FILE_NAME,
    SYS_STDOUT,
    BUILTINS_INPUT,
    COMPILE_MODE,
)
from auto_graders.informative_test_case import InformativeTestCase

EXPECTED_MSG = "Modified list of numbers: {}\n"


class TestModifyList(InformativeTestCase):

    def run_modify_list_test(self, input_values, expected_output):
        with patch(SYS_STDOUT, new_callable=io.StringIO) as mock_stdout:
            with patch(BUILTINS_INPUT, return_value=input_values):
                with open(SOLUTION_FILE_NAME) as f:
                    code = compile(f.read(), SOLUTION_FILE_NAME, COMPILE_MODE)
                    exec(code)

        self.assertEqual(mock_stdout.getvalue(), expected_output)

    def test_integers(self):
        """Check if the provided solution works with positive integers
        INPUT VALUES: '1 2 3 4 5'"""
        input_values = '1 2 3 4 5'
        expected_output = EXPECTED_MSG.format('[2, 1, 6, 2, 10]')
        self.run_modify_list_test(input_values, expected_output)

    def test_negative_integers(self):
        """Check if the provided solution works with negative integers
        INPUT VALUES: '-2 -3 -4 -5'"""
        input_values = '-2 -3 -4 -5'
        expected_output = EXPECTED_MSG.format('[-1, -6, -2, -10]')
        self.run_modify_list_test(input_values, expected_output)

    def test_integers_with_zero(self):
        """Check if the provided solution works with positive integers and zero
        INPUT VALUES: '0 1 2 3 6 9'"""
        input_values = '0 1 2 3 6 9'
        expected_output = EXPECTED_MSG.format('[0, 2, 1, 6, 3, 18]')
        self.run_modify_list_test(input_values, expected_output)

    def test_integers_with_one_even(self):
        """Check if the provided solution works with one even number
        INPUT VALUES: '4'"""
        input_values = '4'
        expected_output = EXPECTED_MSG.format('[2]')
        self.run_modify_list_test(input_values, expected_output)

    def test_integers_with_one_odd(self):
        """Check if the provided solution works with one odd number
        INPUT VALUES: '5'"""
        input_values = '5'
        expected_output = EXPECTED_MSG.format('[10]')
        self.run_modify_list_test(input_values, expected_output)

    def test_empty_list(self):
        """Check if the provided solution works with empty list
        INPUT VALUES: ''"""
        input_values = ''
        expected_output = EXPECTED_MSG.format('[]')
        self.run_modify_list_test(input_values, expected_output)
