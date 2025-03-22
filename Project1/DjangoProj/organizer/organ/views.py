from datetime import datetime
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from .forms import RegisterForm, TaskForm, TaskStatusForm
from .models import Tasks


@login_required
def tasks(request):
    if request.method == 'POST':
        if 'title' in request.POST:
            form = TaskForm(request.POST)
            if form.is_valid():
                task = form.save(commit=False)
                task.user = request.user
                task.save()
        elif 'task_id' in request.POST:
            task = Tasks.objects.get(
                id=request.POST.get('task_id'),
                user=request.user
            )
            form = TaskStatusForm(request.POST, instance=task)
            if form.is_valid():
                task = form.save(commit=False)
                if task.statuss:
                    task.time_finish = datetime.now()
                else:
                    task.time_finish = None
                task.save()
        return redirect('tasks')
    tasks = Tasks.objects.filter(user=request.user)
    return render(request, 'organ/tasks.html', {
        'tasks': tasks,
        'form': TaskForm()
    })


@login_required
def dashboard(request):
    return render(request, 'organ/dashboard.html')


def calendar(request):
    tasks = Tasks.objects.all()
    return render(request, 'organ/calendar.html', {'tasks': tasks})


def about(request):
    return render(request, 'organ/about.html')


def guest(request):
    return render(request, 'organ/guest.html')


def home(request):
    return render(request, 'organ/index.html')


def auth_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('guest')
    else:
        form = AuthenticationForm()
    return render(request, 'organ/auth_login.html', {'form': form})


def auth_register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard')
    else:
        form = RegisterForm()
    return render(request, 'organ/auth_register.html', {'form': form})
