from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework import generics
from .models import Product, Category 
from django.contrib.auth.models import  Group ,Permission
from .models import CustomUser
from .serializers import ProductSerializer, CategorySerializer ,UserSerializer  , GroupSerializer ,PermissionSerializer
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
# Create your views here.


class ProductList(generics.ListCreateAPIView):
     
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class ProductDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class CategoryList(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class CategoryDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class UserList(generics.ListAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer

class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer

class PermissionList(generics.ListAPIView):
    queryset = Permission.objects.all()
    serializer_class = PermissionSerializer