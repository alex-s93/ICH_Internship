from django.db import transaction
from django.contrib.auth import authenticate, logout
from django.db.models import QuerySet
from django.http import Http404
from rest_framework import status, serializers, generics
from rest_framework.exceptions import PermissionDenied
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
    RetrieveUpdateAPIView,
    CreateAPIView,
    get_object_or_404,
)
from rest_framework.views import APIView
from rest_framework.permissions import (
    SAFE_METHODS,
    IsAdminUser,
    IsAuthenticated,
    AllowAny,
)
from auto_graders.permissions import IsAdminOrModerator, IsOwner
from auto_graders.models import Task, TaskTests, User, Submission
from auto_graders.serializers import (
    TaskSerializer,
    SubmissionSerializer,
    TaskTestsSerializer,
    UserCreateSerializer,
    UserResponseSerializer,
    PasswordUpdateSerializer,
    UserProfileSerializer,
    UserLoginSerializer,
)
from auto_graders.utils import run_tests_in_isolated_env, set_jwt_cookies


class TaskListCreateView(ListCreateAPIView):
    """
    List all tasks, or create a new task.
    Example of request to create:
    {
    "title": "My first task",
    "description": "My first task description",
    "task_parameters": [
            {
                "input_params": "[0, 1, 2, 3]",
                "output_params": "Sum of the number is: 6"
            },
        ]
    }
    """

    queryset = Task.objects.all()
    serializer_class = TaskSerializer

    def get_permissions(self):
        if self.request.method in SAFE_METHODS:
            self.permission_classes = [IsAuthenticated]
        else:
            self.permission_classes = [IsAdminUser]

        return [permission() for permission in self.permission_classes]


class TaskDetailUpdateDeleteView(RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update and delete a task by id.
    Example of request to update:
    PUT:
    {
        "title": "some title",
        "description": "some description",
    }

    PATCH:
    {
        "title": "some title", [optional]
        "description": "some description", [optional]
    }
    """

    queryset = Task.objects.all()
    serializer_class = TaskSerializer

    def get_permissions(self):
        if self.request.method in SAFE_METHODS:
            self.permission_classes = [IsAuthenticated]
        else:
            self.permission_classes = [IsAdminUser]

        return [permission() for permission in self.permission_classes]

    def get_object(self):
        return get_object_or_404(Task, pk=self.kwargs['pk'])


class SolveTaskView(APIView):

    def post(self, request: Request, *args, **kwargs) -> Response:
        task: Task = get_object_or_404(Task, pk=kwargs['pk'])
        solution_code: str = request.data.get('solution_code')
        task_tests: list[TaskTests] = TaskTests.objects.filter(
            task__exact=task
        ).all()

        submission: SubmissionSerializer = SubmissionSerializer(
            data=request.data
        )
        try:
            submission.is_valid(raise_exception=True)
        except serializers.ValidationError as err:
            return Response(
                {"data": err.args[0]},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        with transaction.atomic():
            tests_file_path: list[str] = [
                test.file_path for test in task_tests
            ]

            test_result: dict[str, str | bool] = run_tests_in_isolated_env(
                tests_file_path, solution_code
            )

            if (
                test_result.get('status_code')
                == status.HTTP_503_SERVICE_UNAVAILABLE
            ):
                return Response(
                    data={
                        'message': "В данный момент мы не можем обработать Ваш запрос :( Мы работаем над этой проблемой.",
                        'errors': "Service unavailable.",
                    },
                    status=status.HTTP_503_SERVICE_UNAVAILABLE,
                )

            if (
                test_result.get('status_code')
                == status.HTTP_504_GATEWAY_TIMEOUT
            ):
                return Response(
                    data={
                        'message': "Запрос превысил максимально допустимое время выполнения. "
                        "Возможно присутствует вечный цикл в решении задачи. "
                        "Пожалуйста, попробуйте позже.",
                        'errors': "Gateway Timeout.",
                    },
                    status=status.HTTP_504_GATEWAY_TIMEOUT,
                )

            score = test_result['score']

            if test_result['success']:
                user: User = request.user
                if Submission.objects.filter(
                    task=task, user__id=user.id
                ).exists():
                    return Response(
                        data={
                            "message": f"{user.first_name} {user.last_name} has already solved this task."
                        }
                    )
                submission.save(
                    task=task,
                    user=user,
                    score=score,
                )

                return Response(
                    data={
                        'message': 'Задание выполнено верно!',
                        'score': score,
                    },
                    status=status.HTTP_200_OK,
                )
            else:
                return Response(
                    data={
                        'message': 'Задание не выполнено.',
                        'score': score,
                        'errors': test_result['errors'],
                    },
                    status=status.HTTP_200_OK,
                )


class TaskTestsListCreateView(ListCreateAPIView):
    """
    View for creating, retrieving, updating and deleting tests for task
    Example of creating/updating request:
    {
        "file_path":"auto_graders/tests/first_task_test_4.py"
    }
    NOTE: The task parameter will be automatically filled from the request data
    """

    serializer_class = TaskTestsSerializer
    permission_classes = [IsAdminUser]

    def get_queryset(self):
        test_file_paths = TaskTests.objects.filter(
            task__id=self.kwargs['task_id']
        )
        if not test_file_paths:
            raise Http404
        return test_file_paths

    def perform_create(self, serializer):
        task = Task.objects.get(pk=self.kwargs['task_id'])
        serializer.save(task=task)

    def create(self, request, *args, **kwargs):
        task_id = self.kwargs['task_id']
        if TaskTests.objects.filter(
            file_path__exact=request.data['file_path'], task_id=task_id
        ).exists():
            return Response(
                data={
                    "message": f"File path for task {task_id} already exist."
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        return super().create(request, *args, **kwargs)


class TestRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    serializer_class = TaskTestsSerializer
    permission_classes = [IsAdminUser]

    def get_object(self):
        task_tests: QuerySet = TaskTests.objects.filter(pk=self.kwargs['pk'])
        if not task_tests:
            raise Http404
        return task_tests[0]


class UserProfileView(RetrieveUpdateAPIView):
    """
    View for retrieving and updating the user's profile.

    Example of GET request to view the current user's profile:
    GET /profile/
    Authorization: Token <user-token>

    Response:
    {
        "id": 1,
        "phone_number": "+4914294336743",
        "address": "Hauptstr. 23, Rottweil",
        "photo": "https://example.com/photo.jpg",
        "bio": "I love coding"
    }

    Example of PUT request to update the user's profile:
    PUT /profile/
    Authorization: Token <user-token>

    Request Body:
    {
        "phone_number": "+4914294336743",
        "address": "Ginsterstr. 11, Schonach",
        "photo": "https://example.com/newphoto.jpg",
        "bio": "Programming is interesting"
    }

    Response:
    {
        "id": 1,
        "phone_number": "+4911114336743",
        "address": "Ginsterstr. 11, Schonach",
        "photo": "https://example.com/newphoto.jpg",
        "bio": "Programming is interesting"
    }

    Example of PATCH request to partially update the user's profile:
    PATCH /profile/
    Authorization: Token <user-token>

    Request Body:
    {
        "bio": "I like a Python."
    }

    Response:
    {
        "id": 1,
        "phone_number": "+4914294336743",
        "address": "Hauptstr. 23, Rottweil",
        "photo": "https://example.com/photo.jpg",
        "bio": "I like a Python"
    }

    NOTE: Only authenticated users can access this view. Users can only view or update their own profiles.
    """

    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user.user_profile


class UserListCreateView(generics.ListCreateAPIView):
    """
    View for listing all users or creating a new user.

    Example of GET request:
    GET /users/
    Response:
    [
        {
            "id": 1,
            "email": "user1@example.com",
            "first_name": "John",
            "last_name": "Doe",
            "role": "Student",
            "group": "Group A",
            "user_profile": {...}
        },
        ...
    ]

    Example of POST request to create a new user:
    POST /users/
    {
        "email": "newuser@example.com",
        "first_name": "Jane",
        "last_name": "Doe",
        "role": "Student",
        "password": "password123",
        "re_password": "password123",
        "group": "Group B",
        "user_profile": {...}
    }
    Response:
    {
        "id": 2,
        "email": "newuser@example.com",
        "first_name": "Jane",
        "last_name": "Doe",
        "role": "Student",
        "group": "Group B",
        "user_profile": {...}
    }
    NOTE: Only users with admin or moderator privileges can access this view.
    """

    queryset = User.objects.all()
    permission_classes = [IsAdminOrModerator]

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return UserCreateSerializer
        return UserResponseSerializer

    def create(self, request, *args, **kwargs):
        create_serializer = UserCreateSerializer(data=request.data)
        create_serializer.is_valid(raise_exception=True)
        user = create_serializer.save()

        response_serializer = UserResponseSerializer(user)
        return Response(
            response_serializer.data, status=status.HTTP_201_CREATED
        )


class UserDetailUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    """
    View for retrieving, updating, or deleting a user by their ID.

    Example of GET request:
    GET /users/{id}/
    Response:
    {
        "id": 1,
        "email": "user1@example.com",
        "first_name": "John",
        "last_name": "Doe",
        "role": "Student",
        "group": "Group A",
        "user_profile": {...}
    }

    Example of PUT request to update a user:
    PUT /users/{id}/
    {
        "email": "updateduser@example.com",
        "first_name": "John",
        "last_name": "Doe",
        "role": "Student",
        "password": "newpassword123",  # Optional for admins/moderators
        "re_password": "newpassword123",  # Optional for admins/moderators
        "group": "Group A",
        "user_profile": {...}
    }

    Example of PATCH request to partially update a user:
    PATCH /users/{id}/
    {
        "first_name": "Johnny",  # Optional field update
    }

    Example of DELETE request:
    DELETE /users/{id}/
    Response: 204 No Content

    NOTE:
    - Only admins or moderators can update all fields, including the password.
    - Users can update only their own password.
    - Users cannot delete their own profiles.
    - Admins and moderators can delete any user profile.
    """

    queryset = User.objects.all()
    permission_classes = [IsAdminOrModerator | IsOwner]

    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            if IsAdminOrModerator().has_permission(self.request, self):
                return UserCreateSerializer
            elif IsOwner().has_permission(self.request, self):
                if (
                    'password' in self.request.data
                    or 're_password' in self.request.data
                ):
                    return PasswordUpdateSerializer
                else:
                    raise PermissionDenied(
                        "You do not have permission to change these fields."
                    )
        return UserResponseSerializer

    def update(self, request, *args, **kwargs):
        user = self.get_object()

        if IsAdminOrModerator().has_permission(request, self):
            if 'password' in request.data and 're_password' in request.data:
                password = request.data.pop('password')
                re_password = request.data.pop('re_password')

                if password != re_password:
                    return Response(
                        {"password": ["The passwords do not match."]},
                        status=status.HTTP_400_BAD_REQUEST,
                    )

                user.set_password(password)
                user.save()

            serializer = UserCreateSerializer(
                user, data=request.data, partial=True
            )
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)

            response_serializer = UserResponseSerializer(user)
            return Response(
                response_serializer.data, status=status.HTTP_200_OK
            )

        elif IsOwner().has_permission(request, self):
            if 'password' in request.data and 're_password' in request.data:
                serializer = PasswordUpdateSerializer(data=request.data)
                if serializer.is_valid(raise_exception=True):
                    serializer.update(user, serializer.validated_data)
                    return Response(
                        {"status": "Password updated successfully."},
                        status=status.HTTP_200_OK,
                    )
            else:
                return Response(
                    {
                        "error": "You do not have permission to change these fields."
                    },
                    status=status.HTTP_403_FORBIDDEN,
                )

        return Response(
            {"error": "You do not have permission to perform this action."},
            status=status.HTTP_403_FORBIDDEN,
        )

    def delete(self, request, *args, **kwargs):
        if IsAdminOrModerator().has_permission(request, self):
            return super().delete(request, *args, **kwargs)

        return Response(
            {"error": "You do not have permission to delete this profile."},
            status=status.HTTP_403_FORBIDDEN,
        )


class UserLoginAPIView(CreateAPIView):
    """
    View for authenticating a user and returning JWT tokens as cookies.

    Example of request:
    {
        "email": "user@example.com",
        "password": "user password"
    }

    On successful authentication, this view sets JWT access and refresh tokens
    as cookies in the response.

    Permissions:
        - AllowAny: This view is accessible without any authentication.

    Response on success:
    - Status: 200 OK
    - Cookies: JWT access and refresh tokens

    Response on failure:
    - Status: 401 Unauthorized
    - Body: {"detail": "Invalid credentials"}
    """

    permission_classes = [AllowAny]
    serializer_class = UserLoginSerializer

    def post(self, request, *args, **kwargs):
        email = request.data.get("email")
        password = request.data.get("password")
        user = authenticate(request, email=email, password=password)

        if user:
            response = Response(status=status.HTTP_200_OK)
            return set_jwt_cookies(response, user)
        else:
            return Response(
                {"detail": "Invalid credentials"},
                status=status.HTTP_401_UNAUTHORIZED,
            )


class LogoutUserAPIView(APIView):
    """
    View for logging out the currently authenticated user.

    This view logs out the user and deletes the JWT access and refresh tokens
    from the cookies.

    Example of request:
    {
        No request body required
    }

    Permissions:
        - No special permissions required, but the user must be authenticated.

    Response on success:
    - Status: 200 OK
    - Cookies: JWT access and refresh tokens are deleted

    Note:
    - If no user is authenticated, the view still returns a 200 OK status,
      but no actions are performed.
    """

    def post(self, request: Request):
        if request.user:
            logout(request)

        response = Response(status=status.HTTP_200_OK)

        response.delete_cookie('access_token')
        response.delete_cookie('refresh_token')

        return response
