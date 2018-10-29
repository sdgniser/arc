from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

from authtools.models import User
from .models import Profile, Course, School, Itr, Item

class ProfileInline(admin.StackedInline):
	model = Profile
	can_delete = False
	fields = ['name', 'email', 'password']

class UserAdmin(UserAdmin):
	inlines = [ProfileInline]

admin.site.register([Course, School, Itr, Item])
