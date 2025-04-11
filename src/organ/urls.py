from django.contrib import admin
from django.contrib.auth.views import LogoutView
from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("admin/", admin.site.urls, name="admin"),
    path("login/", views.auth_login, name="auth_login"),
    path("register/", views.auth_register, name="auth_register"),
    path("about/", views.about, name="about"),
    path("account/", views.account, name="account"),
    path("logout/", LogoutView.as_view(next_page="home"), name="logout"),
    path("calendar/", views.calendar, name="calendar"),
    path("tasks/", views.tasks, name="tasks"),
    path("tasks/delete/<int:task_id>/", views.delete_task, name="delete_task"),
    path("account/delete/", views.delete_account, name="delete_account"),
    path('delete-all-tasks/', views.delete_all_tasks, name='delete_all_tasks'),
    path("tasks/<int:task_id>/subtasks/", views.subtasks, name='subtasks'),
    path("subtasks/delete/<int:subtask_id>/", views.delete_subtask, name="delete_subtask"),
    # path("subtasks/", views.subtasks, name='subtasks')
]
