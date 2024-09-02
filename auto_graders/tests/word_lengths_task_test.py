from unittest.mock import patch
import io

from auto_graders.constants import (
    SOLUTION_FILE_NAME,
    SYS_STDOUT,
    BUILTINS_INPUT,
    COMPILE_MODE,
)
from auto_graders.informative_test_case import InformativeTestCase

EXPECTED_MSG = "Lengths of words in the sentence: {}\n"


class TestSolution(InformativeTestCase):

    def run_test(self, test_input, expected_lengths):
        expected_output = EXPECTED_MSG.format(expected_lengths)
        with patch(BUILTINS_INPUT, return_value=test_input):
            with patch(SYS_STDOUT, new_callable=io.StringIO) as mock_stdout:
                with open(SOLUTION_FILE_NAME) as f:
                    code = compile(f.read(), SOLUTION_FILE_NAME, COMPILE_MODE)
                    exec(code)
                self.assertEqual(mock_stdout.getvalue(), expected_output)

    def test_normal_case(self):
        """Check if the provided solution works with common sentence
        INPUT VALUES: 'Programming is interesting and useful'"""
        test_input = 'Programming is interesting and useful'
        expected_lengths = (11, 2, 11, 3, 6)
        self.run_test(test_input, expected_lengths)

    def test_empty_string(self):
        """Check if the provided solution works with empty string
        INPUT VALUES: ''"""
        test_input = ''
        expected_lengths = ()
        self.run_test(test_input, expected_lengths)

    def test_single_word(self):
        """Check if the provided solution works with one word in the sentence
        INPUT VALUES: 'Python'"""
        test_input = 'Python'
        expected_lengths = (6,)
        self.run_test(test_input, expected_lengths)

    def test_multiple_spaces(self):
        """Check if the provided solution works with multiple spaces
        INPUT VALUES: '  Hello    world!   This is a test. '"""
        test_input = '  Hello    world!   This is a test. '
        expected_lengths = (5, 6, 4, 2, 1, 5)
        self.run_test(test_input, expected_lengths)

    def test_numerical_and_special_characters(self):
        """Check if the provided solution works with numbers and words
        INPUT VALUES: 'Test 1234 example! 56789'"""
        test_input = 'Test 1234 example! 56789'
        expected_lengths = (4, 4, 8, 5)
        self.run_test(test_input, expected_lengths)

    def test_long_word(self):
        """Check if the provided solution works with one long word
        INPUT VALUES: 'Supercalifragilisticexpialidocious'"""
        test_input = 'Supercalifragilisticexpialidocious'
        expected_lengths = (34,)
        self.run_test(test_input, expected_lengths)

    def test_special_characters(self):
        """Check if the provided solution works with special characters
        INPUT VALUES: '   !!   **   @@   ##'"""
        test_input = '   !!   **   @@   ##'
        expected_lengths = (2, 2, 2, 2)
        self.run_test(test_input, expected_lengths)

    def test_multiline_text(self):
        """Check if the provided solution works with multiline text
        INPUT VALUES: 'Line1\nLine2 with more words'"""
        test_input = 'Line1\nLine2 with more words'
        expected_lengths = (5, 5, 4, 4, 5)
        self.run_test(test_input, expected_lengths)

    def test_various_symbols(self):
        """Check if the provided solution works with various symbols
        INPUT VALUES: '@!# $%^ &*() _'"""
        test_input = '@!# $%^ &*() _'
        expected_lengths = (3, 3, 4, 1)
        self.run_test(test_input, expected_lengths)

    def test_long_and_short_words(self):
        """Check if the provided solution works with short and long words
        INPUT VALUES: 'Short supercalifragilisticexpialidocious'"""
        test_input = 'Short supercalifragilisticexpialidocious'
        expected_lengths = (5, 34)
        self.run_test(test_input, expected_lengths)

    def test_commas_and_other_delimiters(self):
        """Check if the provided solution works with comma and other delimiters
        INPUT VALUES: 'Hello,world! Test-case'"""
        test_input = 'Hello,world! Test-case'
        expected_lengths = (12, 9)
        self.run_test(test_input, expected_lengths)
