from unittest.mock import patch
import io
import ast

from auto_graders.constants import (
    SOLUTION_FILE_NAME,
    SYS_STDOUT,
    BUILTINS_INPUT,
    COMPILE_MODE,
)
from auto_graders.informative_test_case import InformativeTestCase

PALINDROME_MSG = "The number is a palindrome."
NOT_PALINDROME_MSG = "The number is not a palindrome."
USED_STRINGS_MSG = "Stringing methods and comparisons are used in the solution"


class TestIsNumberPalindrome(InformativeTestCase):

    def execute_solution_code(
        self, input_data: str, expected_output: str
    ) -> str:
        with patch(BUILTINS_INPUT, return_value=input_data):
            with open(SOLUTION_FILE_NAME) as solution_file:
                code = compile(
                    solution_file.read(), SOLUTION_FILE_NAME, COMPILE_MODE
                )
                exec(code)
        return expected_output

    def test_no_string_methods_used(self):
        """Check if the provided solution does not use 'string' methods"""
        is_use_string_methods = False
        with open(SOLUTION_FILE_NAME) as solution_file:
            solution_code = solution_file.read()
            tree = ast.parse(solution_code)
            for node in ast.walk(tree):
                if isinstance(node, ast.Call):
                    func_name = getattr(node.func, 'id', None)
                    if func_name in [
                        'str',
                        'format',
                        'reversed',
                    ]:
                        is_use_string_methods = True
                        break
                elif isinstance(node, ast.Attribute):
                    if node.attr in [
                        'lower',
                        'upper',
                        'format',
                        'strip',
                        'split',
                        'replace',
                    ]:
                        is_use_string_methods = True
                        break
                elif isinstance(node, ast.Subscript):
                    if isinstance(node.slice, ast.Call):
                        func_name = getattr(node.slice.func, 'id', None)
                        if func_name in ['slice']:
                            is_use_string_methods = True
                            break
                    if isinstance(node.slice, ast.Slice):
                        is_use_string_methods = True
                    break
        self.assertFalse(is_use_string_methods, msg=USED_STRINGS_MSG)

    def test_no_string_comparison(self):
        """Check if the provided solution does not use comparison methods"""
        is_found_comparison = False
        with open(SOLUTION_FILE_NAME) as solution_file:
            solution_code = solution_file.read()
            tree = ast.parse(solution_code)
            for node in ast.walk(tree):
                if isinstance(node, ast.Compare):
                    if isinstance(node.ops[0], (ast.Eq, ast.NotEq)):
                        if (
                            isinstance(node.left, ast.Subscript)
                            and isinstance(node.comparators[0], ast.Subscript)
                            and node.left.value.id
                            == node.comparators[0].value.id
                        ):
                            is_found_comparison = True
                            break
        self.assertFalse(is_found_comparison, msg=USED_STRINGS_MSG)

    @patch(SYS_STDOUT, new_callable=io.StringIO)
    def test_when_integer_has_two_identical_numbers_in_center(
        self, mock_stdout
    ):
        """Check if the provided solution works with two identical numbers in center
        INPUT VALUES: '12344321'"""
        expected_output = self.execute_solution_code(
            "12344321", PALINDROME_MSG
        )
        self.assertEqual(mock_stdout.getvalue().strip(), expected_output)

    @patch(SYS_STDOUT, new_callable=io.StringIO)
    def test_when_integer_has_one_number_in_center(self, mock_stdout):
        """Check if the provided solution works with two one number in center
        INPUT VALUES: '12321'"""
        expected_output = self.execute_solution_code("12321", PALINDROME_MSG)
        self.assertEqual(mock_stdout.getvalue().strip(), expected_output)

    @patch(SYS_STDOUT, new_callable=io.StringIO)
    def test_when_two_identical_numbers(self, mock_stdout):
        """Check if the provided solution works with two identical numbers
        INPUT VALUES: '55'"""
        expected_output = self.execute_solution_code("55", PALINDROME_MSG)
        self.assertEqual(mock_stdout.getvalue().strip(), expected_output)

    @patch(SYS_STDOUT, new_callable=io.StringIO)
    def test_when_five_identical_numbers(self, mock_stdout):
        """Check if the provided solution works with five identical numbers
        INPUT VALUES: '99999'"""
        expected_output = self.execute_solution_code("99999", PALINDROME_MSG)
        self.assertEqual(mock_stdout.getvalue().strip(), expected_output)

    @patch(SYS_STDOUT, new_callable=io.StringIO)
    def test_when_large_palindrome_number(self, mock_stdout):
        """Check if the provided solution works with very big palindrome number
        INPUT VALUES: '987654321987654321123456789123456789987654321987654321123456789123456789'
        """
        expected_output = self.execute_solution_code(
            "987654321987654321123456789123456789987654321987654321123456789123456789",
            PALINDROME_MSG,
        )
        self.assertEqual(mock_stdout.getvalue().strip(), expected_output)

    @patch(SYS_STDOUT, new_callable=io.StringIO)
    def test_when_number_is_zero(self, mock_stdout):
        """Check if the provided solution works with zero
        INPUT VALUES: '0'"""
        expected_output = self.execute_solution_code("0", PALINDROME_MSG)
        self.assertEqual(mock_stdout.getvalue().strip(), expected_output)

    @patch(SYS_STDOUT, new_callable=io.StringIO)
    def test_when_one_number(self, mock_stdout):
        """Check if the provided solution works with one number
        INPUT VALUES: '7'"""
        expected_output = self.execute_solution_code("7", PALINDROME_MSG)
        self.assertEqual(mock_stdout.getvalue().strip(), expected_output)

    @patch(SYS_STDOUT, new_callable=io.StringIO)
    def test_when_number_is_not_a_palindrome(self, mock_stdout):
        """Check if the provided solution works with non-palindrome number
        INPUT VALUES: '123456'"""
        expected_output = self.execute_solution_code(
            "123456", NOT_PALINDROME_MSG
        )
        self.assertEqual(mock_stdout.getvalue().strip(), expected_output)

    @patch(SYS_STDOUT, new_callable=io.StringIO)
    def test_when_large_number_is_not_a_palindrome(self, mock_stdout):
        """Check if the provided solution works with very big non-palindrome number
        INPUT VALUES: '9876543219876543211234567891234564789987654321987654321123456789123456789'
        """
        expected_output = self.execute_solution_code(
            "9876543219876543211234567891234564789987654321987654321123456789123456789",
            NOT_PALINDROME_MSG,
        )
        self.assertEqual(mock_stdout.getvalue().strip(), expected_output)

    @patch(SYS_STDOUT, new_callable=io.StringIO)
    def test_when_negative_palindrome_number_is_not_a_palindrome(
        self, mock_stdout
    ):
        """Check if the provided solution works with negative palindrome number (expected not palindrome message)
        INPUT VALUES: '-12344321'"""
        expected_output = self.execute_solution_code(
            "-12344321", NOT_PALINDROME_MSG
        )
        self.assertEqual(mock_stdout.getvalue().strip(), expected_output)

    @patch(SYS_STDOUT, new_callable=io.StringIO)
    def test_when_negative_number_is_not_a_palindrome(self, mock_stdout):
        """Check if the provided solution works with negative non-palindrome number (expected not palindrome message)
        INPUT VALUES: '-12343'"""
        expected_output = self.execute_solution_code(
            "-12343", NOT_PALINDROME_MSG
        )
        self.assertEqual(mock_stdout.getvalue().strip(), expected_output)
