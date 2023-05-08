from django.db import models
from django.contrib import admin
# from django.contrib.auth import get_user_model

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
class UserManager(BaseUserManager):
    def create_user(self, name, email, password):
        if not email:
            raise ValueError("Users must have an email address")
        if not name:
            raise ValueError("Users must have a name")

        user = self.model(
            email=self.normalize_email(email),
            name=name,
     
       
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, name, email, password):
        if not email:
            raise ValueError("Users must have an email address")
        if not name:
            raise ValueError("Users must have a name")
        user = self.create_user(
            email=self.normalize_email(email),
            name=name,
            password=password,
       
        )
        user.is_admin = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class CustomUser(AbstractBaseUser, PermissionsMixin):
    name = models.CharField(max_length=60)
   
    email = models.EmailField(verbose_name="email", max_length=60, unique=True)
    date_joined = models.DateTimeField(verbose_name="date joined", auto_now_add=True)
    last_login = models.DateTimeField(verbose_name="last login", auto_now_add=True)
    logged_in = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
   
    is_seller = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["name" ]

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin


# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to='category_images')

 
    def __str__(self):
        return self.name
    
class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    image = models.ImageField(upload_to='product_images')
    categories = models.ManyToManyField(Category)
    fbx_file = models.FileField(upload_to='product_fbx_files', null=True, blank=True)
    seller = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='seller_products', null=True, blank=True)
    # other product fields

    def save(self, *args, **kwargs):
        if self.seller is not None and not self.sellers.filter(id=self.seller.id).exists():
            self.sellers.add(self.seller)
        super().save(*args, **kwargs) 

    def __str__(self):
        return self.name
    
class Order(models.Model):
    STATUS_CHOICES = (
        ('P', 'Pending'),
        ('C', 'Confirmed'),
        ('D', 'Delivered'),
    )

    customer_name = models.CharField(max_length=255)
    customer_email = models.EmailField()
    customer_phone = models.CharField(max_length=20) 
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default='P')

    def __str__(self):
        return f"{self.customer_name} - {self.created_at}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()


class Review(models.Model):
    RATING_CHOICES = (
        (1, '1 star'),
        (2, '2 stars'),
        (3, '3 stars'),
        (4, '4 stars'),
        (5, '5 stars'),
    )

    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    rating = models.IntegerField(choices=RATING_CHOICES)
    text = models.TextField(blank=True)



    def __str__(self):
        return f"{self.user.username}'s review of {self.product.name}"


class Payment(models.Model):
    PAYMENT_METHOD_CHOICES = (
        ('CC', 'Credit Card'),
        ('PP', 'PayPal'),
        ('BK', 'Bank Transfer'),
    )

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    payment_method = models.CharField(max_length=2, choices=PAYMENT_METHOD_CHOICES)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}'s {self.payment_method} payment for {self.order}"
                
class SomeModelAdmin(admin.ModelAdmin):
    def has_view_permission(self, request, obj=None):
        user = request.user
        if not user.is_superuser:
            return False
        return super().has_view_permission(request, obj=obj)

    def has_change_permission(self, request, obj=None):
        user = request.user
        if not user.is_superuser:
            return False
        return super().has_change_permission(request, obj=obj)

    def has_delete_permission(self, request, obj=None):
        user = request.user
        if not user.is_superuser:
            return False
        return super().has_delete_permission(request, obj=obj)