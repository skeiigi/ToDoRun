from datetime import datetime, date

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
# from captcha.models import CaptchaStore

from calendar import monthrange
from django.utils.timezone import make_aware

import json

from .forms import (
    CustomAuthenticationForm,
    RegisterForm,
    TaskForm,
    TaskStatusForm,
    SubtasksForm,
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


@login_required
def calendar(request):
    year = int(request.GET.get('year', datetime.now().year))
    month = int(request.GET.get('month', datetime.now().month))

    current_month = date(year, month, 1)

    prev_month = (current_month.replace(month=current_month.month-1)
                  if current_month.month > 1 else current_month.replace(year=current_month.year-1, month=12))
    next_month = (current_month.replace(month=current_month.month+1)
                  if current_month.month < 12 else current_month.replace(year=current_month.year+1, month=1))

    first_day = make_aware(datetime(year, month, 1))
    last_day = make_aware(datetime(year, month, monthrange(year, month)[1], 23, 59, 59))
    tasks = Tasks.objects.filter(
        user=request.user,
        time_create__range=(first_day, last_day)
    ).order_by('time_create')

    month_days = []

    first_weekday = current_month.weekday()

    if first_weekday > 0:
        prev_month_last_day = monthrange(prev_month.year, prev_month.month)[1]
        for day in range(prev_month_last_day - first_weekday + 1, prev_month_last_day + 1):
            month_days.append({
                'date': date(prev_month.year, prev_month.month, day),
                'day': day,
                'month': prev_month.month
            })

    days_in_month = monthrange(year, month)[1]
    for day in range(1, days_in_month + 1):
        month_days.append({
            'date': date(year, month, day),
            'day': day,
            'month': month
        })

    last_weekday = date(year, month, days_in_month).weekday()
    if last_weekday < 6:
        for day in range(1, 6 - last_weekday + 1):
            month_days.append({
                'date': date(next_month.year, next_month.month, day),
                'day': day,
                'month': next_month.month
            })

    today = datetime.now()

    context = {
        'current_month': current_month,
        'prev_month': prev_month,
        'next_month': next_month,
        'tasks': tasks,
        'month_days': month_days,
        'today': today,
    }

    return render(request, "organ/calendar.html", context)


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


@require_POST
@csrf_exempt
def ajax_check_password(request):
    try:
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')
        user = authenticate(username=username, password=password)
        return JsonResponse({'valid': user is not None})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)


@require_POST
@csrf_exempt
@login_required
def ajax_task_operation(request):
    try:
        data = json.loads(request.body)
        operation = data.get('operation')

        if operation == 'create':
            form = TaskForm(data)
            if form.is_valid():
                task = form.save(commit=False)
                task.user = request.user
                task.save()
                return JsonResponse({
                    'status': 'success',
                    'task': {
                        'id': task.id,
                        'title': task.title,
                        'descriptionn': task.descriptionn,
                        'statuss': task.statuss,
                        'time_create': task.time_create.strftime('%Y-%m-%d %H:%M')
                    }
                })
            else:
                return JsonResponse({
                    'status': 'error',
                    'message': 'Ошибка валидации',
                    'errors': form.errors.get_json_data()
                }, status=400)

        elif operation == 'delete':
            task_id = data.get('task_id')
            task = get_object_or_404(Tasks, id=task_id, user=request.user)
            task.delete()
            return JsonResponse({'status': 'success'})

        elif operation == 'toggle_status':
            task_id = data.get('task_id')
            task = get_object_or_404(Tasks, id=task_id, user=request.user)
            task.statuss = not task.statuss
            if task.statuss:
                task.time_finish = datetime.now()
            else:
                task.time_finish = None
            task.save()
            return JsonResponse({
                'status': 'success',
                'new_status': task.statuss,
                'time_finish': task.time_finish.strftime('%Y-%m-%d %H:%M') if task.time_finish else None
            })

        return JsonResponse({'status': 'error', 'message': 'Invalid operation'}, status=400)

    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e),
            'type': type(e).__name__
        }, status=500)


# def ajax_check_captcha(request):
#     if request.method == "POST":
#         import json
#         data = json.loads(request.body)
#         captcha_value = data.get("captcha", "")
#         captcha_key = data.get("captcha_key", "")

#         try:
#             store = CaptchaStore.objects.get(hashkey=captcha_key)
#             is_valid = store.response == captcha_value
#         except CaptchaStore.DoesNotExist:
#             is_valid = False

#         return JsonResponse({"valid": is_valid})
