from rest_framework import serializers
from .models import Product 
from django.contrib.auth.models import Permission ,Group ,Permission

from .models import CustomUser
class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('id', 'name', 'description', 'price' ,"image","fbx_file")
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('name','id')
class PermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permission
        fields = '__all__'
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = "__all__"
class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = '__all__'

