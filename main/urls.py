from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login/", views.login_view, name="login"),
    path("signup/", views.signup_view, name="signup"),
    path("logout/", views.logout_view, name="logout"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("tasks/", views.tasks, name="tasks"),
    path("projects/", views.projects, name="projects"),
    path(
        "update-task-status/<int:task_id>/",
        views.update_task_status,
        name="update_task_status",
    ),
]
