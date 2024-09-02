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

expected_output_message = "Dynamic list: {}"


class TestDynamicListFromInput(InformativeTestCase):

    @patch(SYS_STDOUT, new_callable=io.StringIO)
    def execute_solution_code(self, *args) -> str:
        with patch(BUILTINS_INPUT, side_effect=[*args]):
            with open(SOLUTION_FILE_NAME) as solution_file:
                code = compile(
                    solution_file.read(), SOLUTION_FILE_NAME, COMPILE_MODE
                )
                exec(code)
        return args[-1].getvalue().strip()

    def test_if_code_uses_append(self):
        """Check if the provided solution uses 'append' method"""
        is_use_append = False
        with open(SOLUTION_FILE_NAME) as solution_file:
            solution_code = solution_file.read()
        tree = ast.parse(solution_code)
        for node in ast.walk(tree):
            if isinstance(node, ast.Call) and isinstance(
                node.func, ast.Attribute
            ):
                if node.func.attr == "append":
                    is_use_append = True
                    break
        self.assertTrue(
            is_use_append, msg="The 'append' is not used in the code."
        )

    def test_given_lists_of_numbers_and_exit_at_end(self):
        """Check if the provided solution works with two lists and 'Exit' at end
        INPUT VALUES: '1 2', '3 4 5', 'Exit'"""
        result = self.execute_solution_code(
            "1 2",
            "3 4 5",
            "Exit",
        )
        self.assertEqual(
            result,
            expected_output_message.format("[1, 2, 3, 4, 5]"),
        )

    def test_given_one_list_of_one_number_and_list_with_numbers(self):
        """Check if the provided solution works with one number, list and 'Exit' at end
        INPUT VALUES: '1', '0 9 8', 'Exit'"""
        result = self.execute_solution_code("1", "0 9 8", "Exit")
        self.assertEqual(
            result, expected_output_message.format("[1, 0, 9, 8]")
        )

    def test_given_one_list_is_empty_and_list_with_numbers(self):
        """Check if the provided solution works with empty list, normal list and 'Exit' at end
        INPUT VALUES: '', '0 9 8', 'Exit'"""
        result = self.execute_solution_code("", "0 9 8", "Exit")
        self.assertEqual(result, expected_output_message.format("[0, 9, 8]"))

    def test_given_five_lists_with_numbers(self):
        """Check if the provided solution works with five lists and 'Exit' at end
        INPUT VALUES: '1', '2 3 4', '5 6 7', '-10 -6 -3', '2 -15 -999', 'Exit'
        """
        result = self.execute_solution_code(
            "1", "2 3 4", "5 6 7", "-10 -6 -3", "2 -15 -999", "Exit"
        )
        self.assertEqual(
            result,
            expected_output_message.format(
                "[1, 2, 3, 4, 5, 6, 7, -10, -6, -3, 2, -15, -999]"
            ),
        )

    def test_given_empty_list(self):
        """Check if the provided solution works with empty list, normal list and 'Exit' at end
        INPUT VALUES: '', 'Exit'"""
        result = self.execute_solution_code("", "Exit")
        self.assertEqual(result, expected_output_message.format("[]"))
