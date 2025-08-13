from django.urls import path
from .views import RegisterAPI, LoginAPI, TaskListCreateAPI, TaskDetailAPI, AdminUserListAPI, ImportTasksAPI

urlpatterns = [
    path('register/', RegisterAPI.as_view(), name='register'),
    path('login/', LoginAPI.as_view(), name='login'),
    path('tasks/', TaskListCreateAPI.as_view(), name='tasks_list_create'),
    path('tasks/<int:pk>/', TaskDetailAPI.as_view(), name='tasks_detail'),
    path('admin/users/', AdminUserListAPI.as_view(), name='admin_user_list'),
    path('admin/import/', ImportTasksAPI.as_view(), name='admin_import'),
    
]
