from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from .forms import RegisterForm
from .models import Tasks


@login_required
def list_tasks(request):
    return render(request, 'organ/list_tasks.html')



@login_required
def list_tasks(request):
    tasks = Tasks.objects.filter(user=request.user)
    return render(request, 'organ/list_tasks.html', {'tasks': tasks})


@login_required
def for_auth(request):
    return render(request, 'organ/for_auth.html')


def task_calendar(request):
    return render(request, 'organ/task_calendar.html')


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
    return redirect('home')