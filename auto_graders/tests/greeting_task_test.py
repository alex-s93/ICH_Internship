from unittest.mock import patch
import io

from auto_graders.constants import (
    SOLUTION_FILE_NAME,
    SYS_STDOUT,
    BUILTINS_INPUT,
    COMPILE_MODE,
)
from auto_graders.informative_test_case import InformativeTestCase


class TestGreeting(InformativeTestCase):

    def run_test(self, name, age):
        expected_output = f"Hi, {name}! You are {age} years old.\n"
        with patch(SYS_STDOUT, new_callable=io.StringIO) as mock_stdout:
            with patch(BUILTINS_INPUT, side_effect=[name, age]):
                with open(SOLUTION_FILE_NAME) as f:
                    code = compile(f.read(), SOLUTION_FILE_NAME, COMPILE_MODE)
                    exec(code)
        self.assertEqual(mock_stdout.getvalue(), expected_output)

    def test_valid_name_age(self):
        """Check if the provided solution works with valid name and age
        INPUT VALUES: 'Alexey', '25'"""
        self.run_test('Alexey', '25')

    def test_get_user_input_empty_name(self):
        """Check if the provided solution works with empty name and age
        INPUT VALUES: ' ', '25'"""
        self.run_test(' ', '25')

    def test_return_greeting_empty_age(self):
        """Check if the provided solution works with valid name and empty age
        INPUT VALUES: 'Alexey', ' '"""
        self.run_test('Alexey', ' ')

    def test_return_greeting_empty_name_and_age(self):
        """Check if the provided solution works with empty name and age
        INPUT VALUES: ' ', ' '"""
        self.run_test(' ', ' ')
