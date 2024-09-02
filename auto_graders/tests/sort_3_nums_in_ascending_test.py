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


class TestSolutionSorting(InformativeTestCase):

    def format_output(self, numbers):
        return ', '.join(f"{num:.1f}" for num in numbers)

    def run_test(self, input_values, expected_output, mock_stdout):
        with patch(BUILTINS_INPUT, side_effect=input_values):
            with open(SOLUTION_FILE_NAME) as f:
                code = compile(f.read(), SOLUTION_FILE_NAME, COMPILE_MODE)
                exec(code)

        actual_output = mock_stdout.getvalue().strip()
        output_numbers = [float(num) for num in actual_output.split(', ')]
        formatted_output = self.format_output(output_numbers)
        self.assertEqual(formatted_output, expected_output)

    def test_if_code_use_if_else(self):
        """Check if the provided solution uses 'if-else' construction"""
        is_use_if = False
        is_use_else = False
        with open(SOLUTION_FILE_NAME) as solution_file:
            solution_code = solution_file.read()
        tree = ast.parse(solution_code)
        for node in ast.walk(tree):
            if isinstance(node, ast.If):
                is_use_if = True
                if node.orelse:
                    is_use_else = True
            elif isinstance(node, ast.IfExp):
                is_use_if = True
                is_use_else = True
        self.assertTrue(is_use_if)
        self.assertTrue(is_use_else)

    @patch(SYS_STDOUT, new_callable=io.StringIO)
    def test_mixed_negative_positive_numbers(self, mock_stdout):
        """Check if the provided solution works with mixed list of numbers (negative-positive)
        INPUT VALUES: ['2', '-115', '-300']"""
        input_values = ['2', '-115', '-300']
        expected_output = '-300.0, -115.0, 2.0'
        self.run_test(input_values, expected_output, mock_stdout)

    @patch(SYS_STDOUT, new_callable=io.StringIO)
    def test_negative_numbers(self, mock_stdout):
        """Check if the provided solution works with negative numbers
        INPUT VALUES: ['-2000000', '-115', '-301']"""
        input_values = ['-2000000', '-115', '-301']
        expected_output = '-2000000.0, -301.0, -115.0'
        self.run_test(input_values, expected_output, mock_stdout)

    @patch(SYS_STDOUT, new_callable=io.StringIO)
    def test_comma_space_format(self, mock_stdout):
        """Check if the provided solution returns correct amount of commas with space
        INPUT VALUES: ['3', '1', '2']"""
        input_values = ['3', '1', '2']
        expected_output = '1.0, 2.0, 3.0'
        self.run_test(input_values, expected_output, mock_stdout)
        actual_output = mock_stdout.getvalue().strip()
        self.assertEqual(actual_output.count(', '), 2)

    @patch(SYS_STDOUT, new_callable=io.StringIO)
    def test_zero(self, mock_stdout):
        """Check if the provided solution works with zero in the list
        INPUT VALUES: ['211', '-115', '0']"""
        input_values = ['211', '-115', '0']
        expected_output = '-115.0, 0.0, 211.0'
        self.run_test(input_values, expected_output, mock_stdout)

    @patch(SYS_STDOUT, new_callable=io.StringIO)
    def test_equal_numbers(self, mock_stdout):
        """Check if the provided solution works with same numbers
        INPUT VALUES: ['500', '500', '500']"""
        input_values = ['500', '500', '500']
        expected_output = '500.0, 500.0, 500.0'
        self.run_test(input_values, expected_output, mock_stdout)

    @patch(SYS_STDOUT, new_callable=io.StringIO)
    def test_large_numbers(self, mock_stdout):
        """Check if the provided solution works with big numbers
        INPUT VALUES: ['1000000000', '1000000000000', '100000000000']"""
        input_values = ['1000000000', '1000000000000', '100000000000']
        expected_output = '1000000000.0, 100000000000.0, 1000000000000.0'
        self.run_test(input_values, expected_output, mock_stdout)
