from datetime import datetime

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import DetailView

from .forms import (  # noqa: E501
    CustomAuthenticationForm,
    RegisterForm,
    TaskForm,
    TaskStatusForm,
    SubtasksForm,
    SubtasksStatusForm
)
from .models import Tasks, Subtasks

from django.http import JsonResponse


@login_required
def tasks(request):
    if request.method == "POST":
        if "title" in request.POST:
            form = TaskForm(request.POST)
            if form.is_valid():
                task = form.save(commit=False)
                task.user = request.user
                task.save()
        elif "task_id" in request.POST:
            task = Tasks.objects.get(
                id=request.POST.get("task_id"), user=request.user
            )  # noqa: E501
            form = TaskStatusForm(request.POST, instance=task)
            if form.is_valid():
                task = form.save(commit=False)
                if task.statuss:
                    task.time_finish = datetime.now()
                else:
                    task.time_finish = None
                task.save()
        return redirect("tasks")
    tasks = Tasks.objects.filter(user=request.user)
    return render(
        request, "organ/tasks.html", {"tasks": tasks, "form": TaskForm()}
    )  # noqa: E501


@login_required
def delete_task(request, task_id):
    task = get_object_or_404(Tasks, id=task_id, user=request.user)
    task.delete()
    return redirect("tasks")


@login_required
def subtasks(request, task_id):
    task = get_object_or_404(Tasks, id=task_id)
    sbtasks = Subtasks.objects.filter(task=task)

    # Форма для добавления новой подзадачи
    if request.method == "POST":
        # Проверяем, какая форма была отправлена
        if 'add_subtask' in request.POST:  # Форма для добавления новой подзадачи
            form = SubtasksForm(request.POST)
            if form.is_valid():
                sbtask = form.save(commit=False)
                sbtask.task = task
                sbtask.save()
                return redirect('subtasks', task_id=task.id)

        elif 'update_status' in request.POST:  # Форма для обновления статуса
            subtask_id = request.POST.get('subtask_id')  # Получаем ID подзадачи
            if subtask_id:
                subtask = get_object_or_404(Subtasks, id=subtask_id)
                # Обновляем статус выполнения
                subtask.is_finished = 'is_finished' in request.POST
                subtask.save()
                return redirect('subtasks', task_id=task.id)

    else:
        form = SubtasksForm()

    return render(request, "organ/subtasks.html", {
        "subtasks": sbtasks,
        "task": task,
        "form": form
    })


@login_required
def delete_subtask(request, subtask_id):
    subtask = get_object_or_404(Subtasks, id=subtask_id)
    task_id = subtask.task.id
    subtask.delete()
    return redirect("subtasks", task_id=task_id)


@login_required
def account(request):
    return render(request, "organ/account.html")


def calendar(request):
    tasks = Tasks.objects.all()
    return render(request, "organ/calendar.html", {"tasks": tasks})


def about(request):
    return render(request, "organ/about.html")


# def account(request):
#     return render(request, 'organ/account.html')


def home(request):
    return render(request, "organ/index.html")


def auth_login(request):
    if request.method == "POST":
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("account")
    else:
        form = CustomAuthenticationForm()
    return render(request, "organ/auth_login.html", {"form": form})


def auth_register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("account")
    else:
        form = RegisterForm()
    return render(request, "organ/auth_register.html", {"form": form})


@login_required
def delete_account(request):
    if request.method == "POST":
        user = request.user
        logout(request)
        user.delete()
        return redirect("home")
    return redirect("account")

@csrf_exempt
def delete_all_tasks(request):
    if request.method == 'POST':
        Tasks.objects.all().delete()  # Удалить все задачи
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error'}, status=400)
