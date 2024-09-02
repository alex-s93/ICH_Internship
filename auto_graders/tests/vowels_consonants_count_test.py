from unittest.mock import patch
import io

from auto_graders.constants import (
    SOLUTION_FILE_NAME,
    SYS_STDOUT,
    BUILTINS_INPUT,
    COMPILE_MODE,
)
from auto_graders.informative_test_case import InformativeTestCase


class TestVowelConsonantCount(InformativeTestCase):
    template = "Number of vowels: {}\nNumber of consonants: {}"

    def run_test(self, input_values, expected_output, mock_stdout):
        with patch(BUILTINS_INPUT, return_value=input_values):
            with open(SOLUTION_FILE_NAME) as f:
                code = compile(f.read(), SOLUTION_FILE_NAME, COMPILE_MODE)
                exec(code)

        actual_output = mock_stdout.getvalue().strip()
        self.assertEqual(actual_output, expected_output)

    @patch(SYS_STDOUT, new_callable=io.StringIO)
    def test_given_values(self, mock_stdout):
        """Check if the provided solution works with common sentence
        INPUT VALUES: 'Hello World'"""
        input_values = 'Hello World'
        expected_output = self.template.format(3, 7)
        self.run_test(input_values, expected_output, mock_stdout)

    @patch(SYS_STDOUT, new_callable=io.StringIO)
    def test_empty_string(self, mock_stdout):
        """Check if the provided solution works with empty string
        INPUT VALUES: ''"""
        input_values = ''
        expected_output = self.template.format(0, 0)
        self.run_test(input_values, expected_output, mock_stdout)

    @patch(SYS_STDOUT, new_callable=io.StringIO)
    def test_no_vowels(self, mock_stdout):
        """Check if the provided solution works with sentence without vowels
        INPUT VALUES: 'bcdfgh'"""
        input_values = 'bcdfgh'
        expected_output = self.template.format(0, 6)
        self.run_test(input_values, expected_output, mock_stdout)

    @patch(SYS_STDOUT, new_callable=io.StringIO)
    def test_no_consonants(self, mock_stdout):
        """Check if the provided solution works with string without consonants
        INPUT VALUES: 'aeiouy'"""
        input_values = 'aeiouy'
        expected_output = self.template.format(6, 0)
        self.run_test(input_values, expected_output, mock_stdout)

    @patch(SYS_STDOUT, new_callable=io.StringIO)
    def test_all_uppercase(self, mock_stdout):
        """Check if the provided solution works with string where all letters in uppercase
        INPUT VALUES: 'HELLO'"""
        input_values = 'HELLO'
        expected_output = self.template.format(2, 3)
        self.run_test(input_values, expected_output, mock_stdout)

    @patch(SYS_STDOUT, new_callable=io.StringIO)
    def test_all_lowercase(self, mock_stdout):
        """Check if the provided solution works with string where all letters in lowercase
        INPUT VALUES: 'hello'"""
        input_values = 'hello'
        expected_output = self.template.format(2, 3)
        self.run_test(input_values, expected_output, mock_stdout)

    @patch(SYS_STDOUT, new_callable=io.StringIO)
    def test_with_numbers_and_symbols(self, mock_stdout):
        """Check if the provided solution works with numbers and symbols
        INPUT VALUES: 'h3ll0 w0orld!'"""
        input_values = 'h3ll0 w0orld!'
        expected_output = self.template.format(1, 7)
        self.run_test(input_values, expected_output, mock_stdout)

    @patch(SYS_STDOUT, new_callable=io.StringIO)
    def test_with_spaces(self, mock_stdout):
        """Check if the provided solution works with spaces
        INPUT VALUES: 'h e l l o'"""
        input_values = 'h e l l o'
        expected_output = self.template.format(2, 3)
        self.run_test(input_values, expected_output, mock_stdout)

    @patch(SYS_STDOUT, new_callable=io.StringIO)
    def test_long_string(self, mock_stdout):
        """Check if the provided solution works with long string
        INPUT VALUES: 'the quick brown fox jumps over the lazy dog'"""
        input_values = 'the quick brown fox jumps over the lazy dog'
        expected_output = self.template.format(12, 23)
        self.run_test(input_values, expected_output, mock_stdout)

    @patch(SYS_STDOUT, new_callable=io.StringIO)
    def test_only_numbers(self, mock_stdout):
        """Check if the provided solution works with only numbers
        INPUT VALUES: '111111 22222 33333'"""
        input_values = '111111 22222 33333'
        expected_output = self.template.format(0, 0)
        self.run_test(input_values, expected_output, mock_stdout)

    @patch(SYS_STDOUT, new_callable=io.StringIO)
    def test_with_unicode_symbols(self, mock_stdout):
        """Check if the provided solution works with unicode symbols
        INPUT VALUES: 'hello 🌍'"""
        input_values = 'hello 🌍'
        expected_output = self.template.format(2, 3)
        self.run_test(input_values, expected_output, mock_stdout)

    @patch(SYS_STDOUT, new_callable=io.StringIO)
    def test_non_english_letters(self, mock_stdout):
        """Check if the provided solution works with non-english letters
        INPUT VALUES: 'привет мир'"""
        input_values = 'привет мир'
        expected_output = self.template.format(0, 0)
        self.run_test(input_values, expected_output, mock_stdout)

    @patch(SYS_STDOUT, new_callable=io.StringIO)
    def test_with_newline_and_tab(self, mock_stdout):
        """Check if the provided solution works with special 'newline' and 'tab' symbols
        INPUT VALUES: 'hello\nworld\t!'"""
        input_values = 'hello\nworld\t!'
        expected_output = self.template.format(3, 7)
        self.run_test(input_values, expected_output, mock_stdout)

    @patch(SYS_STDOUT, new_callable=io.StringIO)
    def test_with_special_characters(self, mock_stdout):
        """Check if the provided solution works with special characters
        INPUT VALUES: 'a!@#b$c%d^e&*f(g)'"""
        input_values = 'a!@#b$c%d^e&*f(g)'
        expected_output = self.template.format(2, 5)
        self.run_test(input_values, expected_output, mock_stdout)
