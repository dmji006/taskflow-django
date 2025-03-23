from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.db import IntegrityError
from .models import Task, Project, User
from datetime import date


def index(request):
    # Ensure user is logged out when viewing landing page
    if request.user.is_authenticated:
        logout(request)
    return render(request, "main/index.html")


def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("dashboard")
        else:
            messages.error(request, "Invalid username or password.")

    return render(request, "main/login.html")


def signup_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")

        if not username or not email or not password1 or not password2:
            messages.error(request, "All fields are required.")
            return render(request, "main/signup.html")

        if password1 != password2:
            messages.error(request, "Passwords do not match.")
            return render(request, "main/signup.html")

        try:
            # Check if username already exists
            if User.objects.filter(username=username).exists():
                messages.error(request, "Username already exists.")
                return render(request, "main/signup.html")

            # Check if email already exists
            if User.objects.filter(email=email).exists():
                messages.error(request, "Email already exists.")
                return render(request, "main/signup.html")

            # Create new user using our custom User model
            user = User.objects.create_user(
                username=username, email=email, password=password1
            )

            # Set additional fields if needed
            user.save()

            messages.success(
                request, "Account created successfully! Please login to continue."
            )
            return redirect("login")

        except IntegrityError:
            messages.error(request, "Username or email already exists.")
        except Exception as e:
            messages.error(request, f"Error creating account: {str(e)}")

    return render(request, "main/signup.html")


def logout_view(request):
    logout(request)
    return redirect("index")


@login_required
def dashboard(request):
    today = date.today()

    # Get counts for tasks
    tasks_today = Task.objects.filter(user=request.user, due_date=today).count()
    completed_tasks = Task.objects.filter(user=request.user, status="completed").count()
    pending_tasks = Task.objects.filter(user=request.user, status="pending").count()

    # Get today's tasks
    today_tasks = Task.objects.filter(user=request.user, due_date=today).order_by(
        "created_at"
    )

    context = {
        "tasks_today": tasks_today,
        "completed_tasks": completed_tasks,
        "pending_tasks": pending_tasks,
        "today_tasks": today_tasks,
    }

    return render(request, "main/dashboard.html", context)


@login_required
def tasks(request):
    all_tasks = Task.objects.filter(user=request.user).order_by("due_date")

    context = {
        "tasks": all_tasks,
    }

    return render(request, "main/tasks.html", context)


@login_required
def projects(request):
    user_projects = Project.objects.filter(user=request.user).order_by("name")

    context = {
        "projects": user_projects,
    }

    return render(request, "main/projects.html", context)


@login_required
def update_task_status(request, task_id):
    if request.method == "POST":
        task = Task.objects.get(id=task_id, user=request.user)

        # Toggle task status
        if task.status == "pending":
            task.status = "completed"
        else:
            task.status = "pending"

        task.save()

        # Redirect back to the page where the request came from
        return redirect(request.META.get("HTTP_REFERER", "dashboard"))
