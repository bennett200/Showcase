from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import User


class CustomUserAdmin(UserAdmin):
    model = User
    add_form = CustomUserCreationForm
    # form = CustomUserChangeForm
    list_display = ['email', 'username']
   

class ProfileAdmin(admin.ModelAdmin):
    filter_horizontal = ('groups', 'user_permissions')
admin.site.register(User, ProfileAdmin)




# from django.contrib import admin
# from django.contrib.auth.admin import UserAdmin

# #Models imports
# from .models import User
# # Register your models here.
# from .forms import RegisterForm



# @admin.register(User)
# class CustomUserAdmin(UserAdmin):
#     model = User
#     fieldsets = (
#         (None, {'fields': ('email', 'password', 'last_login')}),
#         ('Additional Info', {'fields': (('first_name', 'last_name'), 'address', 'phone',)}),
#         ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions',)}),
#     )
#     add_fieldsets = (
#         (None, {
#             'fields': ('email', 'password1', 'password2'),
#             'classes': ('wide',)
#         }),
#     )
#     list_display = ('email', 'is_staff', 'is_superuser', 'last_login')
#     list_filter = ('is_staff', 'is_active')
#     search_fields = ('email',)
#     ordering = ('email',)
#     filter_horizontal = ('groups', 'user_permissions')
#     readonly_fields = ('last_login',)
