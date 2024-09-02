from importlib import util
import ast

from auto_graders.constants import (
    SOLUTION_FILE_NAME,
)
from auto_graders.informative_test_case import InformativeTestCase

not_a_subset_output_message = "Set 1 is not a subset of Set 2"
is_a_subset_output_message = "Set 1 is a subset of Set 2"


class TestCheckSet1IsSubsetOfSet2(InformativeTestCase):

    def execute_solution_code(self, *args) -> str:
        spec = util.spec_from_file_location('code', SOLUTION_FILE_NAME)
        code = util.module_from_spec(spec)
        spec.loader.exec_module(code)
        result = code.is_subset(args[0], args[1])
        return result

    def test_is_use_issubset(self):
        """Check if the provided solution uses 'issubset' method"""
        is_use_issubset = False
        with open(SOLUTION_FILE_NAME) as solution_file:
            solution_code = solution_file.read()
        tree = ast.parse(solution_code)
        for node in ast.walk(tree):
            if isinstance(node, ast.Call) and isinstance(
                node.func, ast.Attribute
            ):
                if node.func.attr == "issubset":
                    is_use_issubset = True
                    break
        self.assertFalse(
            is_use_issubset, msg="The issubset is used in the code."
        )

    def test_is_use_gr_or_eq(self):
        """Check if the provided solution uses 'gr' or 'eq' method"""
        is_use_compare = False
        with open(SOLUTION_FILE_NAME) as solution_file:
            solution_code = solution_file.read()
        tree = ast.parse(solution_code)
        for node in ast.walk(tree):
            if isinstance(node, ast.Compare):
                for op in node.ops:
                    if isinstance(op, ast.GtE) or isinstance(op, ast.LtE):
                        is_use_compare = True
                        break
        self.assertFalse(is_use_compare, msg="Compare is used in the code.")

    def test_if_set1_is_subset_of_set2(self):
        """Check if the provided solution works if the first set is subset of the second
        INPUT VALUES: {100, 200, 307}, {100, 200, 307, 754}"""
        set1 = {100, 200, 307}
        set2 = {100, 200, 307, 754}
        result = self.execute_solution_code(set1, set2)
        self.assertTrue(result, not_a_subset_output_message)

    def test_char_if_set1_is_subset_of_set2(self):
        """Check if the provided solution works if the first set of chars is subset of the second
        INPUT VALUES: {"a", "b", "c"}, {"a", "b", "c", "d"}"""
        set1 = {"a", "b", "c"}
        set2 = {"a", "b", "c", "d"}
        result = self.execute_solution_code(set1, set2)
        self.assertTrue(result, not_a_subset_output_message)

    def test_if_set1_is_not_subset_of_set2(self):
        """Check if the provided solution works if the first set is not subset of the second
        INPUT VALUES: {54, 67, 32}, {14, 25, 39, 43}"""
        set1 = {54, 67, 32}
        set2 = {14, 25, 39, 43}
        result = self.execute_solution_code(set1, set2)
        self.assertFalse(result, is_a_subset_output_message)

    def test_if_set1_greater_of_set2(self):
        """Check if the provided solution works if the first set is greater than the second
        INPUT VALUES: {1, 2, 3, 4, 8}, {1, 2, 3, 4}"""
        set1 = {1, 2, 3, 4, 8}
        set2 = {1, 2, 3, 4}
        result = self.execute_solution_code(set1, set2)
        self.assertFalse(result, is_a_subset_output_message)

    def test_if_set1_is_empty(self):
        """Check if the provided solution works if the first set is empty
        INPUT VALUES: set(), {54, 34, 256, 453}"""
        set1 = set()
        set2 = {54, 34, 256, 453}
        result = self.execute_solution_code(set1, set2)
        self.assertTrue(result, is_a_subset_output_message)

    def test_if_set1_and_set2_are_empty(self):
        """Check if the provided solution works if both sets are empty
        INPUT VALUES: set(), set()"""
        set1 = set()
        set2 = set()
        result = self.execute_solution_code(set1, set2)
        self.assertTrue(result, is_a_subset_output_message)

    def test_if_set2_is_empty(self):
        """Check if the provided solution works if the second set is empty
        INPUT VALUES: {35, 23, 56}, set()"""
        set1 = {35, 23, 56}
        set2 = set()
        result = self.execute_solution_code(set1, set2)
        self.assertFalse(result, is_a_subset_output_message)
