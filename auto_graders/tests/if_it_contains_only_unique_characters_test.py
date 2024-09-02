from unittest.mock import patch
import io

from auto_graders.informative_test_case import InformativeTestCase

ALL_UNIQUE = "All characters in the string are unique."
REPEATED_CHARACTERS = "The characters {} are repeated."
FILE_NAME = "solution.py"


class TestStringHaveOrNotRepeatedCharters(InformativeTestCase):

    def execute_test(self, mock_stdout, input_value: str, output_value: str):
        with patch('builtins.input', return_value=input_value):
            with open(FILE_NAME) as f:
                code = compile(f.read(), FILE_NAME, 'exec')
                exec(code)
        self.assertEqual(
            mock_stdout.getvalue().rstrip('\n'), output_value.rstrip('\n')
        )

    @patch('sys.stdout', new_callable=io.StringIO)
    def test_all_charters_are_unique(self, mock_stdout):
        """Check if the provided solution correctly identifies that all characters are unique.
        INPUT VALUES: 'Python'"""
        input_values = 'Python'
        expected_output = ALL_UNIQUE
        self.execute_test(mock_stdout, input_values, expected_output)

    @patch('sys.stdout', new_callable=io.StringIO)
    def test_string_have_repeated_charters(self, mock_stdout):
        """Check if the provided solution correctly identifies repeated characters in the string.
        INPUT VALUES: 'Hello'"""
        input_values = 'Hello'
        expected_output = REPEATED_CHARACTERS.format("l")
        self.execute_test(mock_stdout, input_values, expected_output)

    @patch('sys.stdout', new_callable=io.StringIO)
    def test_long_string_with_repeated_charters(self, mock_stdout):
        """Check if the provided solution correctly identifies repeated characters in a long string.
        INPUT VALUES: 'Python' * 1000"""
        input_values = "Python" * 1000
        expected_output = REPEATED_CHARACTERS.format("p, y, t, h, o, n")
        self.execute_test(mock_stdout, input_values, expected_output)

    @patch('sys.stdout', new_callable=io.StringIO)
    def test_empty_string(self, mock_stdout):
        """Check if the provided solution correctly handles an empty string.
        INPUT VALUES: ''"""
        input_values = ""
        expected_output = ALL_UNIQUE
        self.execute_test(mock_stdout, input_values, expected_output)

    @patch('sys.stdout', new_callable=io.StringIO)
    def test_single_charter(self, mock_stdout):
        """Check if the provided solution correctly handles a string with a single character.
        INPUT VALUES: 'P'"""
        input_values = "P"
        expected_output = ALL_UNIQUE
        self.execute_test(mock_stdout, input_values, expected_output)

    @patch('sys.stdout', new_callable=io.StringIO)
    def test_repeated_charters(self, mock_stdout):
        """
        Check if the provided solution correctly identifies repeated
        characters when the string has both uppercase and lowercase versions of the same letter.
        INPUT VALUES: 'Pp'
        """
        input_values = "Pp"
        expected_output = REPEATED_CHARACTERS.format("p")
        self.execute_test(mock_stdout, input_values, expected_output)

    @patch('sys.stdout', new_callable=io.StringIO)
    def test_long_unique_string(self, mock_stdout):
        """
        Check if the provided solution correctly identifies that all characters
        are unique in a long string with mixed characters.
        INPUT VALUES: '1234567890qwertyuiopasdfghjklzxcvbnm'
        """
        input_values = '1234567890qwertyuiopasdfghjklzxcvbnm'
        expected_output = ALL_UNIQUE
        self.execute_test(mock_stdout, input_values, expected_output)
