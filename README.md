# ICH Internship AutoGraders

## Project and Client Management Application

**Local launch of the Django Project**:
1. Make a local copy of the repository. In the console, select the directory where the project repository will be cloned.\
Enter the command in the console -> `git clone git@github.com:alex-s93/ICH_Internship.git`
2. Create a poetry environment in the project directory
   * Install Poetry (`curl -sSL https://install.python-poetry.org | python3 -`)
   * Make sure, that the Poetry already included into your PATH (`export PATH="$HOME/.poetry/bin:$PATH"`)
3. Configure PyCharm interpreter & Install all dependencies.\
    * Go to the `Settings` -> `Project: <project_name>` -> `Python Interpreter`
    * Click `Add`
    * Choose `Poetry Environment`
    * Do `poetry install` command in Terminal
4. Do all migrations to create `db.sqlite3` or another `DBMS`.\
Enter the command in the console -> `poetry run python manage.py makemigrations` && `poetry run python manage.py migrate`
5. Creating a superuser.\
Enter the command in the console -> `poetry run python manage.py createsuperuser`
6. Build a Docker image: `docker build --no-cache -t auto_grader .`
7. Start a docker container: `docker run -d --name task_tests_env auto_grader`
8. Install pre-commit hook:
* Add execute rights to the `check_branch_name.sh` file: `chmod +x check_branch_name.sh`
* Run `poetry run pre-commit install` command
9. Start the server.\
Enter the command in the console -> `poetry run python manage.py runserver`


## Python Code Style for Project

### Code Formatting
Use Black for code formatting. This provides a consistent coding style and consistency.

### Installing Black:
1. Add to PyCharm using the following [article](https://akshay-jain.medium.com/pycharm-black-with-formatting-on-auto-save-4797972cf5de), only until the words "Hold your Horses...",\
as the automatic real-time editing is added afterwards, it can be used, but strictly at your discretion.
2. All Black configurations are stored in pyproject.toml - do not modify!
3. Use the command -> `poetry run black .` in the console to format the entire project code.
All code must comply with `Flake8` standards.

### Installing Flake8:
1. Add to PyCharm by turning on real-time checking using the [article](https://johschmidt42.medium.com/automate-linting-formatting-in-pycharm-with-your-favourite-tools-de03e856ee17), [article rus](https://tirinox.ru/flake8-pycharm/) do everything\
according to the guide except the commands after "Git hook!". In the working directory, add the address to the\
local storage of the .flake8 file (/home/intership/).
2. You can also check by using the command -> `poetry run flake8 .` in the project console.
Follow PEP 8 recommendations.

### Git Commit Messages
Use commit messages that contain a single sentence starting with a short prefix at the beginning of the\
line, followed by a description of the commit.\
**Example**: "feat: Add user creation function".\
Use the following abbreviations for prefixes:\
* **feat**: - for new features;\
* **fix**: - for bug fixes;\
* **docs**: - for documentation updates;\
* **style**: - for changes in coding style;\
* **refactor**: - for code changes without fixing bugs or adding features;\
* **test**: - for adding or fixing tests;\
* **chore**: - for configuration or infrastructure changes.\
Start each new sentence with a capital letter and use grammatically correct form. Avoid using the second person.\
Add additional information if desired, such as links to the task that the commit solves or related commits.

### Git Branch Naming
Use names that reflect the content of the branch, such as the task name or issue number in the Internship repository\
or the issue number in the main project, separated by underscore. **Example**: `feat/user_login_1234`, `fix/bug_in_user_login_5678`.\
If the branch relates to new functionality, use `feat/` at the beginning of the branch name. **Example**: `feat/user_login`.\
If the branch relates to bug fixes, use `fix/` at the beginning of the branch name. **Example**: `fix/bug_in_user_login`.\
For example, if you are working on a task with the identifier **TASK-1234**, the branch name may be `feat/TASK_1234`,\
and if you are fixing a bug with the number **BUG-5678**, the branch name may be `fix/BUG_5678`.\
Use underscores (`_`) instead of hyphens or spaces.\
Branch names should be brief and descriptive to make them easy to identify and use.\
Avoid using branching symbols such as `*`, `^`, `~` to avoid conflicts with Git commands.

### Git Workflow
All changes should be made through a pull request, which must pass automatic CI tests and be reviewed by other\
developers (**Code Review**).\
When creating a pull request, leave a comment outlining the changes reflected in the "changed files" tab.\
If the CI tests do not pass, the code must be fixed and changes re-uploaded to the Git server.\
After changes have been accepted and successfully merged into the main branch, the branch can be deleted.\
The local repository should be updated using the git pull command before starting new work on the project. This\
will avoid conflicts with changes made by other developers.\
**Example**:\
**Create a new branch:** `git checkout -b feature-1234`\
**Make changes and save them:** `git add .` and `git commit -m "feat: added user creation function"`\
**Push changes to the Git server:** `git push origin feature-1234`\
**Create a pull request** to the main branch and wait for CI tests and Code Review to pass.\
**If the pull request is accepted**, delete the branch on the server: `git push origin --delete feature-1234`\
**Update the local repository**: git pull\

### Code Review
Code Review is an important stage in software development, and its proper conduct can significantly improve code\
quality and speed up the development process. Code review should be conducted to ensure compliance with established\
coding standards (Code Style). Make sure that the code complies with the requirements of the Flake8 linter.\
When reviewing code, pay attention to the presence of comments and their quality. Comments should be clear, informative,\
and help other developers understand the code.\
Evaluate the correctness of function and library usage. Make sure that the functions and libraries used correspond to the\
task performed by the code.\
Check the security of the code and the possibility of errors. Check the code for vulnerabilities, including possible\
attacks on security breaches.\
Pay attention to the structure and organization of the code. Check that the code is easy to read and understand, as\
well as divided into proper modules, classes, and functions.\
Provide constructive feedback. Instead of just pointing out mistakes, suggest alternative code options or ways to improve.\
Make sure that the discussed code passes testing and works correctly. Pay attention to existing tests and make sure\
that the new code does not break them and meets the requirements.\
Check that the code changes correspond to the task or issue that was created. Pay attention to comments on the code\
and tasks to understand which tasks are being solved within the changes.\
Remember that Code Review is a collaborative process and all team members should participate. Each team member should\
be ready to accept feedback and use it to improve the code. If errors are found, they should be corrected\
and a re-review should be conducted.

### Writing tests
A test class should inherit from `InformativeTestCase` instead of `unitest.TestClass`.\
For each test case, should be added the test name (short description) to the method documentation.\
Should be added also `INPUT VALUES:` on a new line for test cases that use `assertEqual`.\

**Examples:**\
Test class:
`class TestNumListSumMinMax(InformativeTestCase)`

Test case with `assertTrue|assertFalse`:
```
def test_is_func_exists(self):
   """Check if the provided solution has required function which returns 3 arguments."""
   is_func_return_3_args = False
   with open(SOLUTION_FILE_NAME) as solution_file:
      solution_code = solution_file.read()
      ...

   self.assertTrue(is_func_return_3_args)
```
Test case with `assertEqual`:
```
   @patch('sys.stdout', new_callable=io.StringIO)
   def test_several_positive_numbers(self, mock_stdout):
      """Check if the provided solution works with several positive numbers.
      INPUT VALUES: 3, 7, 2, 9, 1, 5"""
      self.execute_test(mock_stdout, '3, 7, 2, 9, 1, 5', (27, 1, 9))
```
