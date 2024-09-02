from unittest.mock import patch
import io

from auto_graders.constants import (
    SOLUTION_FILE_NAME,
    SYS_STDOUT,
    BUILTINS_INPUT,
    COMPILE_MODE,
)
from auto_graders.informative_test_case import InformativeTestCase

GUESS_NUM_MSG = "Guess the number between 1 and 100: \n"
SECRET_IS_HIGHER_MSG = "The actual number is higher. Try again: \n"
SECRET_IS_LOWER_MSG = "The actual number is lower. Try again: \n"
SUCCESS_MSG = "Congratulations! You've guessed the number {}!\n"
RANDOM = "random.randint"


class TestGuessNumberGame(InformativeTestCase):
    def custom_input(self, prompt):
        print(prompt)
        return self.input_values.pop(0)

    def execute_test(self, mock_stdout, expected_value):
        with patch(BUILTINS_INPUT, side_effect=self.custom_input):
            with open(SOLUTION_FILE_NAME) as f:
                code = compile(f.read(), SOLUTION_FILE_NAME, COMPILE_MODE)
                exec(code)
        expected_output = expected_value
        self.assertEqual(mock_stdout.getvalue(), expected_output)

    @patch(RANDOM, return_value=50)
    @patch(SYS_STDOUT, new_callable=io.StringIO)
    def test_correct_guess_first_attempt(self, mock_stdout, mock_randint):
        """Check if the provided solution works if you guess it the first time
        INPUT VALUES: 50, hidden_number = 50"""
        self.input_values = ['50']
        self.execute_test(
            mock_stdout,
            GUESS_NUM_MSG + SUCCESS_MSG.format(self.input_values[0]),
        )

    @patch(RANDOM, return_value=50)
    @patch(SYS_STDOUT, new_callable=io.StringIO)
    def test_guess_lower_then_correct(self, mock_stdout, mock_randint):
        """Check if the provided solution works with lower value then correct
        INPUT VALUES: 30, 50, hidden_number = 50"""
        self.input_values = ['30', '50']

        self.execute_test(
            mock_stdout,
            GUESS_NUM_MSG
            + SECRET_IS_HIGHER_MSG
            + SUCCESS_MSG.format(self.input_values[1]),
        )

    @patch(RANDOM, return_value=50)
    @patch(SYS_STDOUT, new_callable=io.StringIO)
    def test_guess_higher_then_correct(self, mock_stdout, mock_randint):
        """Check if the provided solution works with higher value then correct
        INPUT VALUES: 70, 50, hidden_number = 50"""
        self.input_values = ['70', '50']

        self.execute_test(
            mock_stdout,
            GUESS_NUM_MSG
            + SECRET_IS_LOWER_MSG
            + SUCCESS_MSG.format(self.input_values[1]),
        )

    @patch(RANDOM, return_value=50)
    @patch(SYS_STDOUT, new_callable=io.StringIO)
    def test_multiple_incorrect_guesses_then_correct(
        self, mock_stdout, mock_randint
    ):
        """Check if the provided solution works with several incorrect values then correct
        INPUT VALUES: 10, 60, 50, hidden_number = 50"""
        self.input_values = ['10', '60', '50']

        self.execute_test(
            mock_stdout,
            GUESS_NUM_MSG
            + SECRET_IS_HIGHER_MSG
            + SECRET_IS_LOWER_MSG
            + SUCCESS_MSG.format(self.input_values[2]),
        )
