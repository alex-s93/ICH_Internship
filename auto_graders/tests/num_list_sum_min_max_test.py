from unittest.mock import patch
import io
import ast

from auto_graders.informative_test_case import InformativeTestCase
from auto_graders.constants import (
    SOLUTION_FILE_NAME,
    SYS_STDOUT,
    BUILTINS_INPUT,
    COMPILE_MODE,
)

ANSWER_MSG = '''Sum of the numbers: {}
Minimum value: {}
Maximum value: {}
'''


class TestNumListSumMinMax(InformativeTestCase):
    def execute_test(
        self, mock_stdout, input_values: str, expected_values: tuple
    ):
        with patch(BUILTINS_INPUT, return_value=input_values):
            with open(SOLUTION_FILE_NAME) as f:
                code = compile(f.read(), SOLUTION_FILE_NAME, COMPILE_MODE)
                exec(code)
        expected_output = ANSWER_MSG.format(*expected_values)
        self.assertEqual(mock_stdout.getvalue(), expected_output)

    def test_is_func_exists(self):
        """Check if the provided solution has required function which returns 3 arguments."""
        is_func_return_3_args = False
        with open(SOLUTION_FILE_NAME) as solution_file:
            solution_code = solution_file.read()
            tree = ast.parse(solution_code)
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    for child in ast.walk(node):
                        if isinstance(child, ast.Return):
                            if (
                                isinstance(child.value, ast.Tuple)
                                and len(child.value.elts) == 3
                            ):
                                is_func_return_3_args = True

        self.assertTrue(is_func_return_3_args)

    @patch(SYS_STDOUT, new_callable=io.StringIO)
    def test_several_positive_numbers(self, mock_stdout):
        """Check if the provided solution works with several positive numbers.
        INPUT VALUES: 3, 7, 2, 9, 1, 5"""
        self.execute_test(mock_stdout, '3, 7, 2, 9, 1, 5', (27, 1, 9))

    @patch(SYS_STDOUT, new_callable=io.StringIO)
    def test_one_number(self, mock_stdout):
        """Check if the provided solution works with only one number.
        INPUT VALUES: 5"""
        self.execute_test(mock_stdout, '5', (5, 5, 5))

    @patch(SYS_STDOUT, new_callable=io.StringIO)
    def test_same_numbers(self, mock_stdout):
        """Check if the provided solution works with multiple identical numbers.
        INPUT VALUES: 4, 4, 4, 4"""
        self.execute_test(mock_stdout, '4, 4, 4, 4', (16, 4, 4))

    @patch(SYS_STDOUT, new_callable=io.StringIO)
    def test_without_spaces(self, mock_stdout):
        """Check if the provided solution works without spaces between numbers.
        INPUT VALUES: 4,4,4,4"""
        self.execute_test(mock_stdout, '4,4,4,4', (16, 4, 4))

    @patch(SYS_STDOUT, new_callable=io.StringIO)
    def test_negative_num_in_list(self, mock_stdout):
        """Check if the provided solution works with negative numbers in the list.
        INPUT VALUES: -3, 7, -2, 9, -1, 5"""
        self.execute_test(mock_stdout, '-3, 7, -2, 9, -1, 5', (15, -3, 9))

    @patch(SYS_STDOUT, new_callable=io.StringIO)
    def test_big_numbers(self, mock_stdout):
        """Check if the provided solution works with big numbers.
        INPUT VALUES: 9999999, 8888888, 7777777"""
        self.execute_test(
            mock_stdout,
            '9999999, 8888888, 7777777',
            (26666664, 7777777, 9999999),
        )

    @patch(SYS_STDOUT, new_callable=io.StringIO)
    def test_long_num_list(self, mock_stdout):
        """Check if the provided solution works with big amount numbers (1000).\nINPUT VALUES: from 0 to 999, step 1"""
        self.execute_test(
            mock_stdout,
            ", ".join(str(i) for i in range(1000)),
            (499500, 0, 999),
        )
