from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

from authtools.models import User
from .models import *

def approve(modeladmin, request, queryset):
    queryset.update(appr=True)
approve.short_description = "Approve"

class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    fields = ['name', 'email', 'password']

class UserAdmin(UserAdmin):
    inlines = [ProfileInline]

class CourseAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'school', 'appr')
    actions = [approve]

class ItrAdmin(admin.ModelAdmin):
    list_display = ('course', 'year', 'sem', 'inst', 'appr')
    actions = [approve]

class ItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'desc', 'op', 'itr', 'fl')

admin.site.register(Course, CourseAdmin)
admin.site.register(School)
admin.site.register(Itr, ItrAdmin)
admin.site.register(Item, ItemAdmin)
admin.site.register(Comment)
admin.site.register(CommentReport)
admin.site.register(UserReport)
admin.site.register(ItemReport)
