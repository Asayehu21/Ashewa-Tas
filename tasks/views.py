
# Create your views here.

from rest_framework import generics, permissions, filters, status
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from .models import Task, TaskSecondary
from .serializers import TaskSerializer, RegisterSerializer, UserSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import api_view, permission_classes



# Register API
class RegisterAPI(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer

# Login API returning token
class LoginAPI(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)
        if user:
            token, created = Token.objects.get_or_create(user=user)
            return Response({'token': token.key})
        return Response({'error': 'Invalid Credentials'}, status=status.HTTP_401_UNAUTHORIZED)

# Task CRUD API
class TaskListCreateAPI(generics.ListCreateAPIView):
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.OrderingFilter, DjangoFilterBackend]
    filterset_fields = ['status', 'due_date']
    ordering_fields = ['due_date', 'created_at']

    def get_queryset(self):
        return Task.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class TaskDetailAPI(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Task.objects.filter(user=self.request.user)

# Admin user list API
class AdminUserListAPI(generics.ListAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAdminUser]
    queryset = User.objects.all()
   

# Import API - sync Tasks from primary DB to secondary DB
class ImportTasksAPI(APIView):
    permission_classes = [permissions.IsAdminUser]

    def post(self, request):
        # Clear secondary DB table before import (optional)
        TaskSecondary.objects.all().delete()

        tasks = Task.objects.all()
        for task in tasks:
            TaskSecondary.objects.create(
                user_id=task.user_id,
                title=task.title,
                description=task.description,
                due_date=task.due_date,
                status=task.status
            )
        return Response({"message": "Import completed"}, status=status.HTTP_200_OK)


