from datetime import datetime, date
from calendar import monthrange
import random
import smtplib
from django.utils.timezone import make_aware
from django.conf import settings

from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.views.decorators.cache import cache_page
from django.core.mail import send_mail
from django.contrib.auth import get_user_model
from django.core.exceptions import PermissionDenied
from functools import wraps

import logging
logger = logging.getLogger(__name__)

import json

from .forms import (
    CustomAuthenticationForm,
    RegisterForm,
    VerificationCodeForm,
    TaskForm,
    TaskStatusForm,
    SubtasksForm,
    PasswordResetRequestForm,
    SetNewPasswordForm
)
from .models import Tasks, EmailVerification, Subtasks, TaskCategory
from .services import send_verification_email

from django.http import JsonResponse
from django.contrib import messages


def email_verification_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('auth_login')
            
        verification = EmailVerification.objects.filter(
            user=request.user,
            is_verified=True
        ).first()
        
        if not verification:
            send_verification_email(request.user)
            verification_form = VerificationCodeForm()
            return render(request, "organ/verify_email.html", {
                "form": verification_form,
                "message": "Ваш email не подтвержден. Мы отправили новый код подтверждения."
            })
            
        return view_func(request, *args, **kwargs)
    return _wrapped_view


@login_required
@email_verification_required
def tasks(request):
    if request.method == "POST":
        if "title" in request.POST:
            form = TaskForm(request.POST)
            if form.is_valid():
                task = form.save(commit=False)
                task.user = request.user
                task.save()
                return redirect("tasks")
        elif "task_id" in request.POST:
            task = Tasks.objects.get(
                id=request.POST.get("task_id"), user=request.user
            )
            form = TaskStatusForm(request.POST, instance=task)
            if form.is_valid():
                task = form.save(commit=False)
                print("Создана задача с категорией:", task.category)
                if task.statuss:
                    task.time_finish = datetime.now()
                else:
                    task.time_finish = None
                task.save()
        return redirect("tasks")
    
    tasks = Tasks.objects.filter(user=request.user)
    form = TaskForm()  # Создаем форму с пустыми данными
    return render(
        request, 
        "organ/tasks.html", 
        {
            "tasks": tasks, 
            "form": form,
            "categories": TaskCategory.objects.all()
        }
    )


@login_required
@email_verification_required
def delete_task(request, task_id):
    task = get_object_or_404(Tasks, id=task_id, user=request.user)
    task.delete()
    return redirect("tasks")


@login_required
@email_verification_required
def subtasks(request, task_id):
    task = get_object_or_404(Tasks, id=task_id)
    sbtasks = Subtasks.objects.filter(task=task)

    if request.method == "POST":
        if 'add_subtask' in request.POST:
            form = SubtasksForm(request.POST)
            if form.is_valid():
                sbtask = form.save(commit=False)
                sbtask.task = task
                sbtask.save()
                return redirect('subtasks', task_id=task.id)

        elif 'update_status' in request.POST:
            subtask_id = request.POST.get('subtask_id')
            if subtask_id:
                subtask = get_object_or_404(Subtasks, id=subtask_id)
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
@email_verification_required
def delete_subtask(request, subtask_id):
    subtask = get_object_or_404(Subtasks, id=subtask_id)
    task_id = subtask.task.id
    subtask.delete()
    return redirect("subtasks", task_id=task_id)


@login_required
@email_verification_required
def account(request):
    return render(request, "organ/account.html")


@login_required
@email_verification_required
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


@cache_page(60 * 15)
def about(request):
    return render(request, "organ/about.html")


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
                # Проверяем, подтвержден ли email
                verification = EmailVerification.objects.filter(
                    user=user,
                    is_verified=True
                ).first()
                
                if not verification:
                    # Если email не подтвержден, отправляем новый код
                    send_verification_email(user)
                    login(request, user)
                    verification_form = VerificationCodeForm()
                    return render(request, "organ/verify_email.html", {
                        "form": verification_form,
                        "message": "Ваш email не подтвержден. Мы отправили новый код подтверждения."
                    })
                
                login(request, user)
                return redirect("home")  # Изменено с "account" на "home"
    else:
        form = CustomAuthenticationForm()
    return render(request, "organ/auth_login.html", {"form": form})

    
def auth_register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            # Создаем пользователя
            user = form.save()
            
            try:
                # Отправляем код подтверждения
                verification = send_verification_email(user)
                
                # Авторизуем пользователя
                login(request, user)
                
                # Показываем форму подтверждения
                verification_form = VerificationCodeForm()
                return render(request, 'organ/verify_email.html', {
                    'form': verification_form,
                    'message': 'Код подтверждения отправлен на ваш email.'
                })
                
            except Exception as e:
                # Если произошла ошибка при отправке email, удаляем пользователя
                user.delete()
                return render(request, 'organ/auth_register.html', {
                    'form': form,
                    'register_error': f"Ошибка при отправке email: {str(e)}"
                })
        else:
            return render(request, 'organ/auth_register.html', {
                'form': form,
                'register_error': "Пожалуйста, проверьте введённые данные!"
            })
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
@require_POST
@login_required
def delete_all_tasks(request):
    if request.method == 'POST':
        Tasks.objects.all().delete()
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
@email_verification_required
def ajax_task_operation(request):
    try:
        data = json.loads(request.body)
        operation = data.get('operation')

        if operation == 'create':
            form_data = {
                'title': data.get('title'),
                'descriptionn': data.get('descriptionn'),
                'deadline': data.get('deadline') if data.get('deadline') else None,
                'category': data.get('category')
            }
            
            form = TaskForm(form_data)
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
                        'time_create': task.time_create.strftime('%Y-%m-%d %H:%M'),
                        'deadline': task.deadline.strftime('%Y-%m-%d') if task.deadline else None,
                        'category': task.category.name if task.category else None,
                        'category_display': task.category.get_name_display() if task.category else 'Без категории'
                    }
                })
            else:
                return JsonResponse({
                    'status': 'error',
                    'message': 'Ошибка валидации',
                    'errors': form.errors.as_json()
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


@require_POST
def resend_code(request):
    try:
        # Получаем пользователя из контекста или сессии
        user = request.user if request.user.is_authenticated else None
        if not user and 'user_id' in request.POST:
            user = get_user_model().objects.get(id=request.POST['user_id'])
        
        if not user:
            return JsonResponse({
                'status': 'error',
                'message': 'Пользователь не найден'
            }, status=400)
            
        # Удаляем старые коды
        EmailVerification.objects.filter(
            user=user,
            is_verified=False
        ).delete()
        
        # Отправляем новый код
        send_verification_email(user)
        return JsonResponse({'status': 'success'})
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=400)


@login_required
def verify_email(request):
    if request.method == "POST":
        form = VerificationCodeForm(request.POST)
        if form.is_valid():
            code = form.cleaned_data['code']
            
            # Проверяем код
            verification = EmailVerification.objects.filter(
                user=request.user,
                code=code,
                is_verified=False
            ).first()
            
            if verification and not verification.is_expired():
                verification.is_verified = True
                verification.save()
                return redirect('home')
            else:
                form.add_error('code', 'Неверный или устаревший код подтверждения')
    else:
        form = VerificationCodeForm()
    
    return render(request, 'organ/verify_email.html', {
        'form': form,
        'message': 'Пожалуйста, введите код подтверждения'
    })


def password_reset_request(request):
    if request.method == "POST":
        form = PasswordResetRequestForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            user = get_user_model().objects.get(email=email)
            
            # Генерируем код для сброса пароля
            code = EmailVerification.generate_code()
            
            # Создаем запись о сбросе пароля
            verification = EmailVerification.objects.create(
                user=user,
                code=code,
                is_verified=False
            )
            
            # Отправляем email с кодом
            subject = 'Сброс пароля'
            message = f'''
            Здравствуйте, {user.username}!
            
            Вы запросили сброс пароля. Для установки нового пароля, пожалуйста, введите следующий код:
            
            {code}
            
            Код действителен в течение 24 часов.
            
            Если вы не запрашивали сброс пароля, проигнорируйте это письмо.
            
            С уважением,
            Команда ToDoRun
            '''
            
            try:
                send_mail(
                    subject=subject,
                    message=message,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[email],
                    fail_silently=False,
                )
                
                # Сохраняем email в сессии для последующего использования
                request.session['reset_email'] = email
                
                return render(request, 'organ/verify_email.html', {
                    'form': VerificationCodeForm(),
                    'message': 'Код для сброса пароля отправлен на ваш email.',
                    'is_password_reset': True
                })
                
            except Exception as e:
                verification.delete()
                form.add_error('email', f'Ошибка при отправке email: {str(e)}')
    else:
        form = PasswordResetRequestForm()
    
    return render(request, 'organ/password_reset_request.html', {
        'form': form
    })

def password_reset_confirm(request):
    if 'reset_email' not in request.session:
        return redirect('password_reset_request')
        
    if request.method == "POST":
        form = VerificationCodeForm(request.POST)
        if form.is_valid():
            code = form.cleaned_data['code']
            email = request.session['reset_email']
            
            # Проверяем код
            verification = EmailVerification.objects.filter(
                user__email=email,
                code=code,
                is_verified=False
            ).first()
            
            if verification and not verification.is_expired():
                # Если код верный, показываем форму для нового пароля
                verification.is_verified = True
                verification.save()
                
                # Сохраняем email в сессии для следующего шага
                request.session['reset_email_confirmed'] = email
                
                return render(request, 'organ/password_reset_confirm.html', {
                    'form': SetNewPasswordForm(),
                    'email': email
                })
            else:
                form.add_error('code', 'Неверный или устаревший код')
    else:
        form = VerificationCodeForm()
    
    return render(request, 'organ/password_reset_confirm.html', {
        'form': SetNewPasswordForm,
        'email': email,
        'message': 'Введите код для сброса пароля',
        'is_password_reset': True
    })

def password_reset_complete(request):
    if 'reset_email_confirmed' not in request.session:
        return redirect('password_reset_request')
        
    if request.method == "POST":
        form = SetNewPasswordForm(request.POST)
        if form.is_valid():
            email = request.session['reset_email_confirmed']
            user = get_user_model().objects.get(email=email)
            
            # Устанавливаем новый пароль
            user.set_password(form.cleaned_data['password1'])
            user.save()
            
            # Удаляем данные из сессии
            del request.session['reset_email_confirmed']
            
            # Удаляем все неиспользованные коды верификации для этого пользователя
            EmailVerification.objects.filter(
                user=user,
                is_verified=False
            ).delete()
            
            # Перенаправляем на страницу входа с сообщением об успехе
            messages.success(request, 'Пароль успешно изменен. Теперь вы можете войти с новым паролем.')
            return redirect('auth_login')
    else:
        form = SetNewPasswordForm()
    
    return render(request, 'organ/password_reset_confirm.html', {
        'form': form
    })
