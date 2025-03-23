from django.contrib import admin
from .models import Project, Task, TaskBin


# Customize Project admin
@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ("name", "user", "created_at", "updated_at")
    list_filter = ("user", "created_at")
    search_fields = ("name", "description")


# Customize Task admin
@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ("title", "user", "project", "due_date", "status", "is_deleted")
    list_filter = ("status", "due_date", "user", "project", "is_deleted")
    search_fields = ("title", "description")


# Customize TaskBin admin
@admin.register(TaskBin)
class TaskBinAdmin(admin.ModelAdmin):
    list_display = ("task", "deleted_by", "deleted_at", "restore_before")
    list_filter = ("deleted_by", "deleted_at")
    search_fields = ("task__title", "deleted_by__username")
