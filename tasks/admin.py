from django.contrib import admin
from .models import Task


class TaskAdmin(admin.ModelAdmin):
    readonly_fields = ('created',)
    search_fields = ('title',)


# Register your models here.
admin.site.register(Task, TaskAdmin)
