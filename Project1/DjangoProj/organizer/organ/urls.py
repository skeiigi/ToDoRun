from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView
from django.contrib import admin

urlpatterns = [
    path('', views.home, name='home'),
    path('admin/', admin.site.urls, name='admin'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register, name='register'),
    path('faq_page/', views.faq_page, name='faq_page'),
    path('noauth/', views.noauth, name='noauth'),
    path('for_auth/', views.for_auth, name="for_auth"),
    path('logout/', LogoutView.as_view(next_page='home'), name='logout'),
    path('task_calendar/', views.task_calendar, name='task_calendar'),
    path('list_tasks/', views.list_tasks, name='list_tasks')
]