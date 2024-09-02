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

expected_output_message = "The first {} Fibonacci numbers: {}"


class TestFirstNFibonacciNumbers(InformativeTestCase):

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

    def test_if_code_use_while_loop(self):
        """Check if the provided solution uses 'while' loop"""
        is_use_while = False
        with open(SOLUTION_FILE_NAME) as solution_file:
            solution_code = solution_file.read()
        tree = ast.parse(solution_code)
        for node in ast.walk(tree):
            if isinstance(node, ast.While):
                is_use_while = True
                break
        self.assertTrue(
            is_use_while, msg="The while loop is not used in the code."
        )

    @patch(SYS_STDOUT, new_callable=io.StringIO)
    def test_given_value_7(self, mock_stdout):
        """Check if the provided solution works with common value
        INPUT VALUES: 7"""

        expected_output = self.execute_solution_code(
            "7", expected_output_message.format(7, "0, 1, 1, 2, 3, 5, 8")
        )
        self.assertEqual(mock_stdout.getvalue().strip(), expected_output)

    @patch(SYS_STDOUT, new_callable=io.StringIO)
    def test_given_value_1(self, mock_stdout):
        """Check if the provided solution works with 1
        INPUT VALUES: 1"""
        expected_output = self.execute_solution_code(
            "1", expected_output_message.format(1, "0")
        )
        self.assertEqual(mock_stdout.getvalue().strip(), expected_output)

    @patch(SYS_STDOUT, new_callable=io.StringIO)
    def test_given_value_2(self, mock_stdout):
        """Check if the provided solution works with 2
        INPUT VALUES: 2"""
        expected_output = self.execute_solution_code(
            "2", expected_output_message.format(2, "0, 1")
        )
        self.assertEqual(mock_stdout.getvalue().strip(), expected_output)

    @patch(SYS_STDOUT, new_callable=io.StringIO)
    def test_given_value_3(self, mock_stdout):
        """Check if the provided solution works with 3
        INPUT VALUES: 3"""
        expected_output = self.execute_solution_code(
            "3", expected_output_message.format(3, "0, 1, 1")
        )
        self.assertEqual(mock_stdout.getvalue().strip(), expected_output)

    @patch(SYS_STDOUT, new_callable=io.StringIO)
    def test_given_value_10(self, mock_stdout):
        """Check if the provided solution works with 10
        INPUT VALUES: 10"""
        expected_output = self.execute_solution_code(
            "10",
            expected_output_message.format(
                10, "0, 1, 1, 2, 3, 5, 8, 13, 21, 34"
            ),
        )
        self.assertEqual(mock_stdout.getvalue().strip(), expected_output)

    @patch(SYS_STDOUT, new_callable=io.StringIO)
    def test_given_value_37(self, mock_stdout):
        """Check if the provided solution works with 37
        INPUT VALUES: 37"""
        expected_output = self.execute_solution_code(
            "37",
            expected_output_message.format(
                37,
                "0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144, 233,"
                " 377, 610, 987, 1597, 2584, 4181, 6765, 10946, 17711, 28657, 46368, 75025, 121393, 196418, 317811,"
                " 514229, 832040, 1346269, 2178309, 3524578, 5702887, 9227465, 14930352",
            ),
        )
        self.assertEqual(mock_stdout.getvalue().strip(), expected_output)

    @patch(SYS_STDOUT, new_callable=io.StringIO)
    def test_given_value_0(self, mock_stdout):
        """Check if the provided solution works with 0
        INPUT VALUES: 0"""
        expected_output = self.execute_solution_code("0", "")
        self.assertEqual(mock_stdout.getvalue().strip(), expected_output)
