from django.contrib import admin

from .models import Product, Lesson, Group, UserProductAccess


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['id', 'creator', 'name', 'start_date_time', 'cost']


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ['id', 'product', 'title', 'video_link']


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ['id', 'product', 'name', 'min_users', 'max_users']


@admin.register(UserProductAccess)
class UserProductAccessAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'product']