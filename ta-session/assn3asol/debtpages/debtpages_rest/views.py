from rest_framework import status
from rest_framework.decorators import api_view
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from rest_framework import generics
from debtpages_rest.models import Debt
from debtpages_rest.serializers import DebtSerializer
from debtpages_rest.serializers import DebtSerializerForUpdate
from django.contrib.auth.models import User
from debtpages_rest.serializers import UserSerializer
from debtpages_rest.serializers import UserSumSerializer
from rest_framework.response import Response
from rest_framework import permissions
from debtpages_rest.permissions import UserPermission
from debtpages_rest.permissions import UsersPermission
from debtpages_rest.permissions import DebtPermission
from debtpages_rest.permissions import DebtsPermission

# Create your views here.
class DebtList(generics.ListCreateAPIView):
    queryset = Debt.objects.all()
    serializer_class = DebtSerializer
    permission_classes = (permissions.IsAuthenticated, DebtsPermission)
    def perform_create(self, serializer):
        serializer.save(borrower=self.request.user)

class DebtDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Debt.objects.all()
    serializer_class = DebtSerializerForUpdate
    permission_classes = (permissions.IsAuthenticated, DebtPermission)

class UserSumList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSumSerializer
    permission_classes = (permissions.IsAuthenticated, UsersPermission)

class UserSumDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSumSerializer
    permission_classes = (permissions.IsAuthenticated, UserPermission)

class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAuthenticated, UsersPermission,)

class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAuthenticated, UserPermission)
