from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from auto_graders.choices.roles_choices import RoleEnum
from auto_graders.utils import UserManager


class UserProfile(models.Model):
    phone_number: int = models.CharField(max_length=32, null=True, blank=True)
    address: str = models.CharField(max_length=255, null=True, blank=True)
    photo: str = models.CharField(max_length=255, null=True, blank=True)
    bio: str = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.bio


class User(AbstractBaseUser, PermissionsMixin):
    ROLE_CHOICES = RoleEnum.choices()

    email: str = models.EmailField(unique=True)
    group: str = models.CharField(max_length=128)
    first_name: str = models.CharField(max_length=128)
    last_name: str = models.CharField(max_length=128)

    role = models.CharField(
        max_length=10, choices=ROLE_CHOICES, default=RoleEnum.STUDENT.value
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_deleted: bool = models.BooleanField(default=False)

    user_profile: UserProfile = models.OneToOneField(
        UserProfile,
        related_name='user',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )

    objects = UserManager()

    USERNAME_FIELD = 'email'

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Task(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()

    class Meta:
        verbose_name = "Task"
        verbose_name_plural = "Tasks"

    def __str__(self):
        return self.title


class TaskParameters(models.Model):
    input_params = models.CharField(max_length=255)
    output_params = models.TextField()
    task = models.ForeignKey(
        Task,
        related_name='task_parameters',
        null=True,
        blank=True,
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return f"{self.input_params} -> {self.output_params}"


class TaskTests(models.Model):
    task = models.ForeignKey(
        Task, on_delete=models.CASCADE, related_name="tests"
    )
    file_path = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        verbose_name = "Task Test"
        verbose_name_plural = "Task Tests"

    def __str__(self):
        return f"{self.task.title} tests"


class Submission(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    solution_code = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    score = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        default=5,
    )  # Оценка от 1 до 5

    def __str__(self):
        return f"{self.user.email} - {self.task.title}"
