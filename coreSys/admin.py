from django.contrib import admin
from .models import Member, User


# Register your models here.
@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
    list_display = ['member_id', 'name', 'phone',
                    'member_car_number', 'registration', 'expiration']


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['user_id', 'user_car_number', 'user_type',
                    'state', 'in_time', 'out_time', 'pee']
