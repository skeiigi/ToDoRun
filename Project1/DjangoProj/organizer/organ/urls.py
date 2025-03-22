from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView
from django.contrib import admin

urlpatterns = [
    path('', views.home, name='home'),
    path('admin/', admin.site.urls, name='admin'),
    path('login/', views.auth_login, name='auth_login'),
    path('register/', views.auth_register, name='auth_register'),
    path('about/', views.about, name='about'),
    path('guest/', views.guest, name='guest'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('logout/', LogoutView.as_view(next_page='home'), name='logout'),
    path('calendar/', views.calendar, name='calendar'),
    path('tasks/', views.tasks, name='tasks'),
    path('tasks/delete/<int:task_id>/', views.delete_task, name='delete_task')
]
