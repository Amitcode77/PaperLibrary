from django.contrib import admin
from .models import *
from django.contrib.auth.models import Permission


# Register your models here.
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('user', 'name')
    list_filter = ('user',)


class SpaceAdmin(admin.ModelAdmin):
    list_display = ('user', 'filesize')


class PaperAdmin(admin.ModelAdmin):
    list_display = ('user', 'project', 'name', 'author', 'filesize')
    list_filter = ('user', 'filesize')


class PermissionAdmin(admin.ModelAdmin):
    list_filter = ('content_type',)
    list_display = ('name', 'content_type', 'codename')


admin.site.register(Permission, PermissionAdmin)
admin.site.register(Project, ProjectAdmin)
admin.site.register(Space, SpaceAdmin)
admin.site.register(Paper, PaperAdmin)
