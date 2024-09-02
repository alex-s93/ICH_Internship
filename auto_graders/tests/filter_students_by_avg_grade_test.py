import importlib.util
from unittest.mock import patch
import io
from random import randint, uniform

from auto_graders.constants import (
    SOLUTION_FILE_NAME,
    SYS_STDOUT,
    BUILTINS_INPUT,
)
from auto_graders.informative_test_case import InformativeTestCase

EXPECTED_MSG = 'Students with an average grade above {}: {}'


class TestFilterStudents(InformativeTestCase):
    def setUp(self):
        self.common_students_list = [
            ('Student1', 25, 91.5),
            ('Student2', 21, 84.5),
            ('Student3', 27, 95.7),
            ('Student4', 23, 89.9),
            ('Student5', 19, 90.1),
            ('Student6', 31, 90.01),
            ('Student7', 26, 78.1),
        ]

    def execute_test(
        self, mock_stdout, threshold_value, students, expected_names
    ):
        with patch(BUILTINS_INPUT, return_value=threshold_value):
            spec = importlib.util.spec_from_file_location(
                SOLUTION_FILE_NAME.replace('.py', ''), SOLUTION_FILE_NAME
            )
            solution = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(solution)

            # clear output after import solution file
            mock_stdout.truncate(0)
            mock_stdout.seek(0)

            threshold = float(threshold_value)
            solution.filter_students(threshold, students)

        expected_output = EXPECTED_MSG.format(threshold, expected_names)

        self.assertEqual(mock_stdout.getvalue().strip(), expected_output)

    @patch(SYS_STDOUT, new_callable=io.StringIO)
    def test_given_values(self, mock_stdout):
        """Check if the provided solution works with usual threshold
        INPUT VALUES: 85, common_students_list = [('Student1', 25, 91.5),('Student2', 21, 84.5),('Student3', 27, 95.7),('Student4', 23, 89.9),('Student5', 19, 90.1),('Student6', 31, 90.01),('Student7', 26, 78.1),]
        """
        threshold = '85'
        expected_names = [
            'Student1',
            'Student3',
            'Student4',
            'Student5',
            'Student6',
        ]

        self.execute_test(
            mock_stdout, threshold, self.common_students_list, expected_names
        )

    @patch(SYS_STDOUT, new_callable=io.StringIO)
    def test_value_higher_than_existing(self, mock_stdout):
        """Check if the provided solution works with threshold higher than existing
        INPUT VALUES: 96, common_students_list = [('Student1', 25, 91.5),('Student2', 21, 84.5),('Student3', 27, 95.7),('Student4', 23, 89.9),('Student5', 19, 90.1),('Student6', 31, 90.01),('Student7', 26, 78.1),]
        """
        threshold = '96'
        expected_names = []

        self.execute_test(
            mock_stdout, threshold, self.common_students_list, expected_names
        )

    @patch(SYS_STDOUT, new_callable=io.StringIO)
    def test_value_below_existing(self, mock_stdout):
        """Check if the provided solution works with threshold lower than existing
        INPUT VALUES: 77, common_students_list = [('Student1', 25, 91.5),('Student2', 21, 84.5),('Student3', 27, 95.7),('Student4', 23, 89.9),('Student5', 19, 90.1),('Student6', 31, 90.01),('Student7', 26, 78.1),]
        """
        threshold = '77'
        expected_names = [
            'Student1',
            'Student2',
            'Student3',
            'Student4',
            'Student5',
            'Student6',
            'Student7',
        ]

        self.execute_test(
            mock_stdout, threshold, self.common_students_list, expected_names
        )

    @patch(SYS_STDOUT, new_callable=io.StringIO)
    def test_lower_threshold(self, mock_stdout):
        """Check if the provided solution works with lower border threshold
        INPUT VALUES: 78.1, common_students_list = [('Student1', 25, 91.5),('Student2', 21, 84.5),('Student3', 27, 95.7),('Student4', 23, 89.9),('Student5', 19, 90.1),('Student6', 31, 90.01),('Student7', 26, 78.1),]
        """
        threshold = '78.1'
        expected_names = [
            'Student1',
            'Student2',
            'Student3',
            'Student4',
            'Student5',
            'Student6',
            'Student7',
        ]

        self.execute_test(
            mock_stdout, threshold, self.common_students_list, expected_names
        )

    @patch(SYS_STDOUT, new_callable=io.StringIO)
    def test_higher_threshold(self, mock_stdout):
        """Check if the provided solution works with higher border threshold
        INPUT VALUES: 95.7, common_students_list = [('Student1', 25, 91.5),('Student2', 21, 84.5),('Student3', 27, 95.7),('Student4', 23, 89.9),('Student5', 19, 90.1),('Student6', 31, 90.01),('Student7', 26, 78.1),]
        """
        threshold = '95.7'
        expected_names = ['Student3']

        self.execute_test(
            mock_stdout, threshold, self.common_students_list, expected_names
        )

    @patch(SYS_STDOUT, new_callable=io.StringIO)
    def test_empty_student_list(self, mock_stdout):
        """Check if the provided solution return empty list of students
        INPUT VALUES: 50, empty_students_list = []
        """
        threshold = '50'
        empty_students_list = []
        expected_names = []

        self.execute_test(
            mock_stdout, threshold, empty_students_list, expected_names
        )

    @patch(SYS_STDOUT, new_callable=io.StringIO)
    def test_the_same_grades(self, mock_stdout):
        """Check if the provided solution return list of repeated students with the same score
        INPUT VALUES: 70.1, students_list = [('Student1', 25, 70.1),('Student2', 21, 70.1),('Student3', 27, 70.1),('Student4', 23, 70.1),]
        """
        threshold = '70.1'
        students_list = [
            ('Student1', 25, 70.1),
            ('Student2', 21, 70.1),
            ('Student3', 27, 70.1),
            ('Student4', 23, 70.1),
        ]
        expected_names = ['Student1', 'Student2', 'Student3', 'Student4']

        self.execute_test(
            mock_stdout, threshold, students_list, expected_names
        )

    @patch(SYS_STDOUT, new_callable=io.StringIO)
    def test_negative_grades(self, mock_stdout):
        """Check if the provided solution works with negative grades
        INPUT VALUES: 50, students_list = [('Student1', 25, 70.1),('Student2', 21, 70.1),('Student3', 27, 70.1),('Student4', 23, 70.1),]
        """
        threshold = '50'
        students_list = [
            ('Student1', 25, -50),
            ('Student2', 21, -20),
            ('Student3', 27, 70),
            ('Student4', 23, -5),
        ]
        expected_names = ['Student3']

        self.execute_test(
            mock_stdout, threshold, students_list, expected_names
        )

    @patch(SYS_STDOUT, new_callable=io.StringIO)
    def test_massive_students_list(self, mock_stdout):
        """Check if the provided solution works with massive list if students
        INPUT VALUES: 50, students_list = [(f'Student{number}', randint(18, 35), round(uniform(50.0, 100.0), 2)) for number in range(1, 1001)], expected_names = [item[0] for item in students_list if item[2] >= float(threshold)]
        """
        threshold = '50'
        students_list = [
            (
                f'Student{number}',
                randint(18, 35),
                round(uniform(50.0, 100.0), 2),
            )
            for number in range(1, 1001)
        ]
        expected_names = [
            item[0] for item in students_list if item[2] >= float(threshold)
        ]

        self.execute_test(
            mock_stdout, threshold, students_list, expected_names
        )
