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

expected_output_message = "List of element pairs: {}"


class TestPairElementsFromLists(InformativeTestCase):

    @patch(SYS_STDOUT, new_callable=io.StringIO)
    def execute_solution_code(self, *args) -> str:
        with patch(BUILTINS_INPUT, side_effect=[*args]):
            with open(SOLUTION_FILE_NAME) as solution_file:
                code = compile(
                    solution_file.read(), SOLUTION_FILE_NAME, COMPILE_MODE
                )
                exec(code)
        return args[-1].getvalue().strip()

    def test_if_code_use_zip(self):
        """Check if the provided solution uses 'zip' method"""
        is_use_zip = False
        with open(SOLUTION_FILE_NAME) as solution_file:
            solution_code = solution_file.read()
        tree = ast.parse(solution_code)
        for node in ast.walk(tree):
            if isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
                if node.func.id == "zip":
                    if len(node.args) == 2:
                        is_use_zip = True
                    break
        self.assertTrue(
            is_use_zip, msg="The zip function is not used in the code."
        )

    def test_given_lists_of_digit_and_characters(self):
        """Check if the provided solution works with list of digits and list of characters
        INPUT VALUES: '1 2 3', 'A B C'"""
        result = self.execute_solution_code(
            "1 2 3",
            "A B C",
        )
        self.assertEqual(
            result,
            expected_output_message.format("[(1, 'A'), (2, 'B'), (3, 'C')]"),
        )

    def test_given_lists_of_string_and_digit(self):
        """Check if the provided solution works with list of characters and list of digits
        INPUT VALUES: 'Q W E', '0 9 8'"""
        result = self.execute_solution_code(
            "Q W E",
            "0 9 8",
        )
        self.assertEqual(
            result,
            expected_output_message.format("[('Q', 0), ('W', 9), ('E', 8)]"),
        )

    def test_given_mixed_lists(self):
        """Check if the provided solution works with mixed lists
        INPUT VALUES: '1 B 3 D', 'N 2 # 4'"""
        result = self.execute_solution_code(
            "1 B 3 D",
            "N 2 # 4",
        )
        self.assertEqual(
            result,
            expected_output_message.format(
                "[(1, 'N'), ('B', 2), (3, '#'), ('D', 4)]"
            ),
        )

    def test_given_lists_of_digits(self):
        """Check if the provided solution works with lists of digits
        INPUT VALUES: '1 2 3 4', '5 6 7 8'"""
        result = self.execute_solution_code(
            "1 2 3 4",
            "5 6 7 8",
        )
        self.assertEqual(
            result,
            expected_output_message.format("[(1, 5), (2, 6), (3, 7), (4, 8)]"),
        )

    def test_given_lists_of_characters(self):
        """Check if the provided solution works with lists of characters
        INPUT VALUES: 'A B', 'C D'"""
        result = self.execute_solution_code(
            "A B",
            "C D",
        )
        self.assertEqual(
            result, expected_output_message.format("[('A', 'C'), ('B', 'D')]")
        )

    def test_given_empty_lists(self):
        """Check if the provided solution works with empty lists
        INPUT VALUES: '', ''"""
        result = self.execute_solution_code(
            "",
            "",
        )
        self.assertEqual(result, expected_output_message.format("[]"))

    def test_given_first_list_is_empty(self):
        """Check if the provided solution works if first list is empty
        INPUT VALUES: '', 'A'"""
        result = self.execute_solution_code(
            "",
            "A",
        )
        self.assertEqual(result, expected_output_message.format("[]"))

    def test_given_second_list_is_empty(self):
        """Check if the provided solution works if second list is empty
        INPUT VALUES: 'B C D', ''"""
        result = self.execute_solution_code(
            "B C D",
            "",
        )
        self.assertEqual(result, expected_output_message.format("[]"))
