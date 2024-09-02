import subprocess
from datetime import datetime
import tempfile
import os
import re

from rest_framework import status
from django.contrib.auth.base_user import BaseUserManager
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from rest_framework_simplejwt.exceptions import TokenError
from django.utils.deprecation import MiddlewareMixin
from rest_framework.request import Request


SOLUTION_FILE_NAME = "solution.py"
CONTAINER_APP_PATH = "/usr/src/app/"
CONTAINER_ID = 'task_tests_env'


def load_tests_from_file(test_file_path: str) -> str:
    with open(test_file_path, 'r') as test_file:
        return test_file.read()


def parse_test_results(output: str) -> tuple:
    total_tests_pattern: re.Pattern[str] = re.compile(r"Ran (\d+) test")
    total_tests_match: re.Match[str] | None = total_tests_pattern.search(
        output
    )
    total_tests: int = (
        int(total_tests_match.group(1)) if total_tests_match else 0
    )

    failed_tests_pattern: re.Pattern[str] = re.compile(r"FAILED \(.*=(\d+)\)")
    failed_tests_match: re.Match[str] | None = failed_tests_pattern.search(
        output
    )
    failed_tests: int = (
        int(failed_tests_match.group(1)) if failed_tests_match else 0
    )

    comparison_pattern: re.Pattern[str] = re.compile(
        r"AssertionError: (.*?) != (.*?)(?:\n.*)+?\s+:\s(.*)\nINPUT VALUES: (.*)"
    )

    boolean_pattern: re.Pattern[str] = re.compile(
        r"AssertionError: (False|True) is not (true|false) : (.*)"
    )

    runtime_err_pattern: re.Pattern[str] = re.compile(
        r'ERROR: (.*?) \(.*?\)(?:\n.*?)+?File "solution\.py".*?\n(.*?)\n.*?\n.*?Error: (.*)'
    )

    comparison_fails: list = comparison_pattern.findall(output)
    boolean_fails: list = boolean_pattern.findall(output)
    runtime_fails: list = runtime_err_pattern.findall(output)

    failed_details: list = (
        [
            {
                "test": failed[2],
                "input_values": failed[3],
                "failure": f"{failed[0]} != {failed[1]}",
            }
            for failed in comparison_fails
        ]
        + [
            {
                "test": failed[2],
                "failure": f"{failed[0]} != {failed[1]}",
            }
            for failed in boolean_fails
        ]
        + [
            {
                "test": failed[0],
                "failure": f"{failed[2]}: {failed[1].strip()}",
            }
            for failed in runtime_fails
        ]
    )

    return total_tests, failed_tests, failed_details


def calculate_grade(total_tests: int, failed_tests: int) -> int:
    failed_percentage = (failed_tests / total_tests) * 100

    if failed_percentage > 80:
        return 5
    elif failed_percentage > 60:
        return 4
    elif failed_percentage > 40:
        return 3
    elif failed_percentage > 20:
        return 2
    else:
        return 1


def is_solution_code_compilable(solution_file_temp_path):
    is_compilable = True
    error = None

    try:
        with open(solution_file_temp_path) as f:
            compile(f.read(), solution_file_temp_path, 'exec')
    except SyntaxError as err:
        is_compilable = False
        error = f"{err.msg}: '{err.text}'"

    return is_compilable, error


def run_tests_in_isolated_env(test_file_paths, solution_code):
    with tempfile.TemporaryDirectory() as tempdir:
        container_id: str = CONTAINER_ID
        try:
            subprocess.check_call(
                ['docker', 'exec', container_id, 'ls', '-l'],
                stdout=subprocess.DEVNULL,
            )
        except subprocess.CalledProcessError:
            return {
                'success': False,
                'errors': 'Service unavailable',
                'status_code': status.HTTP_503_SERVICE_UNAVAILABLE,
            }

        test_docker_file_paths: list[str] = []
        for test_file_path in test_file_paths:
            temp_test_file_path: str = os.path.join(
                tempdir, os.path.basename(test_file_path)
            )
            test_code: str = load_tests_from_file(test_file_path)
            with open(temp_test_file_path, 'w') as temp_test_file:
                temp_test_file.write(test_code)
            file_name = os.path.basename(test_file_path)
            docker_file_path = f'{CONTAINER_APP_PATH}{file_name}'
            test_docker_file_paths.append(docker_file_path)
            subprocess.run(
                [
                    'docker',
                    'cp',
                    temp_test_file_path,
                    f'{container_id}:{docker_file_path}',
                ]
            )

        solution_file_temp_path: str = os.path.join(
            tempdir, SOLUTION_FILE_NAME
        )
        with open(solution_file_temp_path, 'w') as solution_file:
            solution_file.write(solution_code)
        docker_file_path = f'{CONTAINER_APP_PATH}{SOLUTION_FILE_NAME}'
        test_docker_file_paths.append(docker_file_path)
        subprocess.run(
            [
                'docker',
                'cp',
                solution_file_temp_path,
                f'{container_id}:{docker_file_path}',
            ]
        )

        is_executable_code, error = is_solution_code_compilable(
            solution_file_temp_path
        )
        if not is_executable_code:
            delete_copied_files(test_docker_file_paths)
            return {
                'success': False,
                'errors': {
                    'general_info': 'compilation error',
                    'error': error,
                },
            }

        try:
            result: subprocess.CompletedProcess[str] = subprocess.run(
                [
                    'docker',
                    'exec',
                    container_id,
                    'python3',
                    '-m',
                    'unittest',
                    'discover',
                    '-s',
                    '.',
                    '-p',
                    '*_test.py',
                ],
                capture_output=True,
                text=True,
                timeout=20,
            )

            stdout: str = result.stdout
            stderr: str = result.stderr

            total_tests, failed_tests, failed_details = parse_test_results(
                stdout + stderr
            )

            if result.returncode == 0:
                return {'success': True, 'score': 1}
            else:
                errors = {
                    "general_info": f"{total_tests - failed_tests}/{total_tests} tests passed.",
                    "failed_tests": failed_details,
                }
                return {
                    'success': False,
                    'score': calculate_grade(failed_tests, total_tests),
                    'errors': errors,
                }

        except subprocess.TimeoutExpired:
            return {
                'success': False,
                'errors': 'Gateway Timeout',
                'status_code': status.HTTP_504_GATEWAY_TIMEOUT,
            }
        finally:
            delete_copied_files(test_docker_file_paths)


def delete_copied_files(file_names: list[str]):
    for docker_file in file_names:
        subprocess.run(
            ['docker', 'exec', CONTAINER_ID, 'rm', '-rf', docker_file]
        )


class UserManager(BaseUserManager):
    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if not email:
            raise ValueError('The Email field must be set.')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user


def set_jwt_cookies(response: Response, user) -> Response:

    refresh_token = RefreshToken.for_user(user)
    access_token = refresh_token.access_token

    access_expiry = datetime.fromtimestamp(access_token['exp'])
    refresh_expiry = datetime.fromtimestamp(refresh_token['exp'])

    response.set_cookie(
        key='access_token',
        value=str(access_token),
        httponly=True,
        secure=False,
        samesite='Lax',
        expires=access_expiry,
    )
    response.set_cookie(
        key='refresh_token',
        value=str(refresh_token),
        httponly=True,
        secure=False,
        samesite='Lax',
        expires=refresh_expiry,
    )

    return response
