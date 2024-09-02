from unittest.mock import patch
import io

from auto_graders.constants import (
    SOLUTION_FILE_NAME,
    SYS_STDOUT,
    BUILTINS_INPUT,
    COMPILE_MODE,
)
from auto_graders.informative_test_case import InformativeTestCase

STRING_IS_A_PANGRAM = "The string is a pangram."
STRING_IS_NOT_A_PANGRAM = "The string is not a pangram."


class TestStringIsPangram(InformativeTestCase):

    @patch(SYS_STDOUT, new_callable=io.StringIO)
    def execute_test(self, mock_stdout, input_value: str, output_value: str):
        with patch(BUILTINS_INPUT, return_value=input_value):
            with open(SOLUTION_FILE_NAME) as f:
                code = compile(f.read(), SOLUTION_FILE_NAME, COMPILE_MODE)
                exec(code)
        self.assertEqual(
            mock_stdout.getvalue().rstrip('\n'), output_value.rstrip('\n')
        )

    def test_pangram_string(self, mock_stdout):
        """Check if the provided solution works with a pangram string
        INPUT VALUES: 'The quick brown fox jumps over the lazy dog'"""
        input_value = 'The quick brown fox jumps over the lazy dog'
        self.execute_test(mock_stdout, input_value, STRING_IS_A_PANGRAM)

    def test_no_pangram_string(self, mock_stdout):
        """Check if the provided solution works with a non-pangram string
        INPUT VALUES: 'The quick brown fox jumps over the lazy'"""
        input_value = 'The quick brown fox jumps over the lazy'
        self.execute_test(mock_stdout, input_value, STRING_IS_NOT_A_PANGRAM)

    def test_empty_string(self, mock_stdout):
        """Check if the provided solution works with an empty string
        INPUT VALUES: ''"""
        input_value = ''
        self.execute_test(mock_stdout, input_value, STRING_IS_NOT_A_PANGRAM)

    def test_string_with_special_simbols(self, mock_stdout):
        """Check if the provided solution works with special symbols in a pangram string
        INPUT VALUES: 'The quick brown fox jumps over the lazy dog $!'"""
        input_value = 'The quick brown fox jumps over the lazy dog $!'
        self.execute_test(mock_stdout, input_value, STRING_IS_A_PANGRAM)

    def test_string_with_cyrillic_letters(self, mock_stdout):
        """Check if the provided solution works with cyrillic symbols in a string
        INPUT VALUES: 'The quick brown fox jumps over the lazy дог'"""
        input_value = 'The quick brown fox jumps over the lazy дог'
        self.execute_test(mock_stdout, input_value, STRING_IS_NOT_A_PANGRAM)

    def test_string_without_spaces(self, mock_stdout):
        """Check if the provided solution works without spaces in a pangram string
        INPUT VALUES: 'Thequickbrownfoxjumpsoverthelazydog'"""
        input_value = 'Thequickbrownfoxjumpsoverthelazydog'
        self.execute_test(mock_stdout, input_value, STRING_IS_A_PANGRAM)
