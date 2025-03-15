from datetime import datetime
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from .forms import RegisterForm, TaskForm, TaskStatusForm
from .models import Tasks


@login_required
def list_tasks(request):
    if request.method == 'POST':
        # Обработка формы создания задачи
        if 'title' in request.POST:
            form = TaskForm(request.POST)
            if form.is_valid():
                task = form.save(commit=False)
                task.user = request.user
                task.save()

        # Обработка изменения статуса
        elif 'task_id' in request.POST:
            task = get_object_or_404(Tasks,
                                     id=request.POST.get('task_id'),
                                     user=request.user)
            form = TaskStatusForm(request.POST, instance=task)

            if form.is_valid():
                task = form.save(commit=False)  # Не сохраняем сразу в БД
                # Обновляем время завершения
                if task.statuss:  # Если статус стал "выполнено"
                    task.time_finish = datetime.now()
                else:  # Если статус сброшен
                    task.time_finish = None
                task.save()  # Сохраняем все изменения

        return redirect('list_tasks')

    # GET-запрос
    tasks = Tasks.objects.filter(user=request.user)
    return render(request, 'organ/list_tasks.html', {
        'tasks': tasks,
        'form': TaskForm()
    })


@login_required
def for_auth(request):
    return render(request, 'organ/for_auth.html')


def task_calendar(request):
    tasks = Tasks.objects.all()
    return render(request, 'organ/task_calendar.html', {
        'tasks': tasks
    })


def faq_page(request):
    return render(request, 'organ/faq_page.html')


def noauth(request):
    return render(request, 'organ/noauth.html')


def home(request):
    return render(request, 'organ/home.html')


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('for_auth')
    else:
        form = AuthenticationForm()
    return render(request, 'organ/login.html', {'form': form})


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('for_auth')
    else:
        form = RegisterForm()

    return render(request, 'organ/register.html', {'form': form})