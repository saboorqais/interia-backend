from django.contrib import admin   
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import Product,Category , Order ,OrderItem ,Payment ,Review  , CustomUser
from django.contrib.auth.models import PermissionsMixin
# Register your models here.

from .models import SomeModelAdmin

class ProductAdmin(admin.ModelAdmin):
    list_display = ["id","name","description","price"]
    ordering = ["id"]

    def get_queryset(self,request):
        qs= super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(author=request.user)




# Now register the new UserAdmin...
admin.site.register(CustomUser)

# replace default admin site with custom one

admin.site.register(Product,ProductAdmin)
admin.site.register(Category)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Payment)
admin.site.register(Review, SomeModelAdmin)
