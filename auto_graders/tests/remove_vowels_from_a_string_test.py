from unittest.mock import patch
import io

from auto_graders.constants import (
    SOLUTION_FILE_NAME,
    SYS_STDOUT,
    BUILTINS_INPUT,
    COMPILE_MODE,
)
from auto_graders.informative_test_case import InformativeTestCase

RESULT_MSG = "Result: "


class TestRemoveVowelsFromString(InformativeTestCase):

    def run_test(self, input_values, expected_output, mock_stdout):
        with patch(BUILTINS_INPUT, return_value=input_values):
            with open(SOLUTION_FILE_NAME) as f:
                code = compile(f.read(), SOLUTION_FILE_NAME, COMPILE_MODE)
                exec(code)

        actual_output = mock_stdout.getvalue().strip()
        self.assertEqual(actual_output, expected_output)

    @patch(SYS_STDOUT, new_callable=io.StringIO)
    def test_output_sample(self, mock_stdout):
        """Check if the provided solution works with simple sentence
        INPUT VALUES: 'Hello, world!'"""
        input_values = "Hello, world!"
        expected_output = RESULT_MSG + "Hll, wrld!"
        self.run_test(input_values, expected_output, mock_stdout)

    @patch(SYS_STDOUT, new_callable=io.StringIO)
    def test_non_english_letters(self, mock_stdout):
        """Check if the provided solution works with non-english letters
        INPUT VALUES: 'Привет, мир!'"""
        input_values = "Привет, мир!"
        expected_output = RESULT_MSG + "Привет, мир!"
        self.run_test(input_values, expected_output, mock_stdout)

    @patch(SYS_STDOUT, new_callable=io.StringIO)
    def test_with_unicode_symbols(self, mock_stdout):
        """Check if the provided solution works with unicode symbols
        INPUT VALUES: 'We shall rul the World ! 🌍'"""
        input_values = "We shall rul the World ! 🌍"
        expected_output = RESULT_MSG + "W shll rl th Wrld ! 🌍"
        self.run_test(input_values, expected_output, mock_stdout)

    @patch(SYS_STDOUT, new_callable=io.StringIO)
    def test_only_numbers(self, mock_stdout):
        """Check if the provided solution works with only numbers
        INPUT VALUES: '111111 22222 33333'"""
        input_values = "111111 22222 33333"
        expected_output = RESULT_MSG + "111111 22222 33333"
        self.run_test(input_values, expected_output, mock_stdout)

    @patch(SYS_STDOUT, new_callable=io.StringIO)
    def test_with_special_characters(self, mock_stdout):
        """Check if the provided solution works with special characters
        INPUT VALUES: 'a!@#b$c%d^e&*f(g)'"""
        input_values = "a!@#b$c%d^e&*f(g)"
        expected_output = RESULT_MSG + "!@#b$c%d^&*f(g)"
        self.run_test(input_values, expected_output, mock_stdout)

    @patch(SYS_STDOUT, new_callable=io.StringIO)
    def test_empty_string(self, mock_stdout):
        """Check if the provided solution works with empty string
        INPUT VALUES: ''"""
        input_values = ""
        expected_output = RESULT_MSG[:-1]
        self.run_test(input_values, expected_output, mock_stdout)

    @patch(SYS_STDOUT, new_callable=io.StringIO)
    def test_with_newline_and_tab(self, mock_stdout):
        """Check if the provided solution works with 'newline' and 'tab' special symbols
        INPUT VALUES: 'hello\nworld\t!'"""
        input_values = "hello\nworld\t!"
        expected_output = RESULT_MSG + "hll\nwrld\t!"
        self.run_test(input_values, expected_output, mock_stdout)
