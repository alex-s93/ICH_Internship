from unittest.mock import patch
import io

from auto_graders.constants import (
    SOLUTION_FILE_NAME,
    SYS_STDOUT,
    BUILTINS_INPUT,
    COMPILE_MODE,
)
from auto_graders.informative_test_case import InformativeTestCase

RESULT_MSG = "Reversed sentence: "


class TestReverseWordsInSentence(InformativeTestCase):

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
        INPUT VALUES: 'Programming is interesting and useful'"""
        input_values = "Programming is interesting and useful"
        expected_output = RESULT_MSG + "useful and interesting is Programming"
        self.run_test(input_values, expected_output, mock_stdout)

    @patch(SYS_STDOUT, new_callable=io.StringIO)
    def test_non_english_letters(self, mock_stdout):
        """Check if the provided solution works with non-english letters
        INPUT VALUES: 'Программировать интересно и полезно!'"""
        input_values = "Программировать интересно и полезно!"
        expected_output = RESULT_MSG + "полезно! и интересно Программировать"
        self.run_test(input_values, expected_output, mock_stdout)

    @patch(SYS_STDOUT, new_callable=io.StringIO)
    def test_with_unicode_symbols(self, mock_stdout):
        """Check if the provided solution works with unicode symbols
        INPUT VALUES: 'PROGRAMMING is interesting AND useful 🌍'"""
        input_values = "PROGRAMMING is interesting AND useful 🌍"
        expected_output = (
            RESULT_MSG + "🌍 useful AND interesting is PROGRAMMING"
        )
        self.run_test(input_values, expected_output, mock_stdout)

    @patch(SYS_STDOUT, new_callable=io.StringIO)
    def test_only_numbers(self, mock_stdout):
        """Check if the provided solution works with only numbers
        INPUT VALUES: '111111 22222 33333'"""
        input_values = "111111 22222 33333"
        expected_output = RESULT_MSG + "33333 22222 111111"
        self.run_test(input_values, expected_output, mock_stdout)

    @patch(SYS_STDOUT, new_callable=io.StringIO)
    def test_with_special_characters(self, mock_stdout):
        """Check if the provided solution works with special characters
        INPUT VALUES: 'a!@#b$c%d^e&*f(g) e&*f(g) a!@#b'"""
        input_values = "a!@#b$c%d^e&*f(g) e&*f(g) a!@#b"
        expected_output = RESULT_MSG + "a!@#b e&*f(g) a!@#b$c%d^e&*f(g)"
        self.run_test(input_values, expected_output, mock_stdout)

    @patch(SYS_STDOUT, new_callable=io.StringIO)
    def test_empty_string(self, mock_stdout):
        """Check if the provided solution works with empty string
        INPUT VALUES: ''"""
        input_values = ""
        expected_output = RESULT_MSG[:-1]
        self.run_test(input_values, expected_output, mock_stdout)
