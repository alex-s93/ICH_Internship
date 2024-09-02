import re

from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers

from auto_graders.models import (
    Task,
    Submission,
    User,
    UserProfile,
    TaskParameters,
    TaskTests,
    RoleEnum,
)


class TaskParametersSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskParameters
        fields = '__all__'


class TaskSerializer(serializers.ModelSerializer):
    task_parameters = TaskParametersSerializer(many=True, required=True)

    class Meta:
        model = Task
        fields = '__all__'

    def create(self, validated_data):
        task_parameters_data: list[dict[str:str]] = validated_data.pop(
            'task_parameters'
        )
        task = Task(**validated_data)
        task.save()

        for task_parameter in task_parameters_data:
            task_parameter_model = TaskParameters(**task_parameter)
            task_parameter_model.task = task
            task_parameter_model.save()
        return task

    def update(self, instance, validated_data):
        instance.description = validated_data.get(
            'description', instance.description
        )
        instance.title = validated_data.get('title', instance.title)
        instance.save()
        return instance


class TaskTestsSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskTests
        fields = '__all__'
        read_only_fields = ['task']


class SubmissionSerializer(serializers.ModelSerializer):
    solution_code = serializers.CharField(
        required=True,
        error_messages={
            'required': 'Вы должны предоставить код решения для выполнения задачи.'
        },
    )

    class Meta:
        model = Submission
        exclude = ['created_at', 'user', 'task', 'score']


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['phone_number', 'address', 'photo', 'bio']
        read_only_fields = ['user']


class UserCreateSerializer(serializers.ModelSerializer):
    user_profile = UserProfileSerializer(write_only=True, required=False)
    re_password = serializers.CharField(max_length=128, write_only=True)

    class Meta:
        model = User
        fields = [
            'email',
            'first_name',
            'last_name',
            'role',
            'group',
            'password',
            're_password',
            'user_profile',
        ]

    def create(self, validated_data):
        user_profile_data = validated_data.get('user_profile')
        if user_profile_data:
            user_profile: UserProfile = UserProfile(**user_profile_data)
        else:
            user_profile: UserProfile = UserProfile()
        user_profile.save()

        validated_data.pop('re_password')
        password = validated_data.get('password')

        user: User = User(
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            role=validated_data['role'],
            group=validated_data['group'],
        )
        user.set_password(password)
        user.user_profile = user_profile
        user.save()

        return user

    def validate(self, attrs):
        password = attrs.get('password')
        re_password = attrs.get('re_password')

        if self.instance is None:
            if not password:
                raise serializers.ValidationError(
                    {
                        'password': 'The field is mandatory when creating a user.'
                    }
                )
            if not re_password:
                raise serializers.ValidationError(
                    {
                        're_password': 'The field is mandatory when creating a user.'
                    }
                )

        if password or re_password:
            if password != re_password:
                raise serializers.ValidationError(
                    {'password': 'The passwords do not match.'}
                )
            try:
                validate_password(password)
            except serializers.ValidationError as err:
                raise serializers.ValidationError({'password': err.messages})

        first_name = attrs.get('first_name')
        last_name = attrs.get('last_name')

        if first_name and not re.match('^[A-Za-z]+$', first_name):
            raise serializers.ValidationError(
                {'first_name': 'The first_name must be alphabet characters.'}
            )
        if last_name and not re.match('^[A-Za-z]+$', last_name):
            raise serializers.ValidationError(
                {'last_name': 'The last_name must be alphabet characters.'}
            )

        return attrs


class PasswordUpdateSerializer(serializers.Serializer):
    password = serializers.CharField(write_only=True)
    re_password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        password = attrs.get('password')
        re_password = attrs.get('re_password')

        if password and re_password:
            if password != re_password:
                raise serializers.ValidationError(
                    {"password": "Passwords do not match."}
                )
            try:
                validate_password(password)
            except serializers.ValidationError as err:
                raise serializers.ValidationError({"password": err.messages})
        else:
            raise serializers.ValidationError(
                {
                    "password": "Both password and re_password fields are required."
                }
            )

        return attrs

    def update(self, instance, validated_data):
        instance.set_password(validated_data['password'])
        instance.save()
        return instance


class UserResponseSerializer(serializers.ModelSerializer):
    user_profile = UserProfileSerializer(read_only=True)

    class Meta:
        model = User
        fields = [
            "email",
            "first_name",
            "last_name",
            "group",
            "role",
            "user_profile",
        ]


class UserLoginSerializer(serializers.Serializer):

    class Meta:

        model = User
        fields = ['email', 'password']
        extra_kwargs = {
            "password": {
                "write_only": True,
            }
        }
