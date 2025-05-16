from django.contrib import admin
from django.contrib.auth.views import LogoutView
from django.urls import path, include
from django.views.decorators.cache import cache_page

from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", views.home, name="home"),
    path("admin/", admin.site.urls, name="admin"),
    path("login/", views.auth_login, name="auth_login"),
    path("register/", views.auth_register, name="auth_register"),
    path("about/", cache_page(60 * 15)(views.about), name="about"),
    path("account/", views.account, name="account"),
    path("logout/", LogoutView.as_view(next_page="home"), name="logout"),
    path("calendar/", views.calendar, name="calendar"),
    path("tasks/", views.tasks, name="tasks"),
    path("tasks/delete/<int:task_id>/", views.delete_task, name="delete_task"),
    path("account/delete/", views.delete_account, name="delete_account"),
    path('delete-all-tasks/', views.delete_all_tasks, name='delete_all_tasks'),
    path("tasks/<int:task_id>/subtasks/", views.subtasks, name='subtasks'),
    path("subtasks/delete/<int:subtask_id>/", views.delete_subtask, name="delete_subtask"),
    path('captcha/', include('captcha.urls')),
    path("ajax/check-password/", views.ajax_check_password, name="ajax_check_password"),
    path("ajax/task-operation/", views.ajax_task_operation, name="ajax_task_operation"),
]
