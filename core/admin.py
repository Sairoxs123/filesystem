from django.contrib import admin
from .models import *

# Register your models here.
@admin.register(Users)

class UsersAdmin(admin.ModelAdmin):
    list_display = ['id', 'email']
    ordering = ['id']
    search_fields = ['email']

@admin.register(Files)

class FilesAdmin(admin.ModelAdmin):
    list_display = ['id', 'file']
    ordering = ['id']
    search_fields = ['file']

@admin.register(Folders)

class FolderAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'owner','url']
    ordering = ['id']
    search_fields = ['name', 'owner']
