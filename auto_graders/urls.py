from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from auto_graders.views import (
    TaskListCreateView,
    TaskDetailUpdateDeleteView,
    SolveTaskView,
    UserProfileView,
    TaskTestsListCreateView,
    TestRetrieveUpdateDestroyView,
    UserListCreateView,
    UserDetailUpdateDeleteView,
    UserLoginAPIView,
    LogoutUserAPIView,
)


urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('login/', UserLoginAPIView.as_view(), name='login'),
    path('logout/', LogoutUserAPIView.as_view(), name='logout'),
    path('tasks/', TaskListCreateView.as_view()),
    path('tasks/<int:pk>/', TaskDetailUpdateDeleteView.as_view()),
    path('tasks/<int:pk>/solve/', SolveTaskView.as_view()),
    path('tasks/<int:task_id>/tests/', TaskTestsListCreateView.as_view()),
    path('profile/', UserProfileView.as_view()),
    path(
        'tasks/<int:task_id>/tests/<int:pk>/',
        TestRetrieveUpdateDestroyView.as_view(),
    ),
    path('users/', UserListCreateView.as_view()),
    path('users/<int:pk>/', UserDetailUpdateDeleteView.as_view()),
]
