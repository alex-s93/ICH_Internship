from unittest.mock import patch
import io

from auto_graders.constants import (
    SOLUTION_FILE_NAME,
    SYS_STDOUT,
    BUILTINS_INPUT,
    COMPILE_MODE,
)
from auto_graders.informative_test_case import InformativeTestCase

IS_LEAP_MSG = "The year is a leap year.\n"
IS_NOT_LEAP_MSG = "The year is not a leap year.\n"


class TestLeapYear(InformativeTestCase):

    def execute_test(self, mock_stdout, input_value, expected_value):
        with patch(BUILTINS_INPUT, return_value=input_value):
            with open(SOLUTION_FILE_NAME) as f:
                code = compile(f.read(), SOLUTION_FILE_NAME, COMPILE_MODE)
                exec(code)
        self.assertEqual(mock_stdout.getvalue(), expected_value)

    @patch(SYS_STDOUT, new_callable=io.StringIO)
    def test_leap_year_divisible_by_400(self, mock_stdout):
        """Check if the provided solution works with leap year
        INPUT VALUES: '2000'"""
        self.execute_test(mock_stdout, '2000', IS_LEAP_MSG)

    @patch(SYS_STDOUT, new_callable=io.StringIO)
    def test_non_leap_year_divisible_by_100_not_400(self, mock_stdout):
        """Check if the provided solution works with year divisible by 100 and not 400
        INPUT VALUES: '1900'"""
        self.execute_test(mock_stdout, '1900', IS_NOT_LEAP_MSG)

    @patch(SYS_STDOUT, new_callable=io.StringIO)
    def test_leap_year_divisible_by_4_not_100(self, mock_stdout):
        """Check if the provided solution works with year divisible by 4 and not 100
        INPUT VALUES: '2024'"""
        self.execute_test(mock_stdout, '2024', IS_LEAP_MSG)

    @patch(SYS_STDOUT, new_callable=io.StringIO)
    def test_non_leap_year_not_divisible_by_4(self, mock_stdout):
        """Check if the provided solution works with year not divisible by 4
        INPUT VALUES: '2019'"""
        self.execute_test(mock_stdout, '2019', IS_NOT_LEAP_MSG)

    @patch(SYS_STDOUT, new_callable=io.StringIO)
    def test_minimum_positive_non_leap_year(self, mock_stdout):
        """Check if the provided solution works with positive non-leap year
        INPUT VALUES: '1'"""
        self.execute_test(mock_stdout, '1', IS_NOT_LEAP_MSG)

    @patch(SYS_STDOUT, new_callable=io.StringIO)
    def test_negative_leap_year(self, mock_stdout):
        """Check if the provided solution works with negative leap year
        INPUT VALUES: '1'"""
        self.execute_test(mock_stdout, '-4', IS_LEAP_MSG)

    @patch(SYS_STDOUT, new_callable=io.StringIO)
    def test_leap_year_zero(self, mock_stdout):
        """Check if the provided solution works with year '0'
        INPUT VALUES: '0'"""
        self.execute_test(mock_stdout, '0', IS_LEAP_MSG)
