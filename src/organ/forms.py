from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User

from .models import Tasks, Subtasks


class TaskStatusForm(forms.ModelForm):
    class Meta:
        model = Tasks
        fields = ["statuss"]
        widgets = {
            "statuss": forms.CheckboxInput(attrs={"class": "status-checkbox"})
        }  # noqa: E501


class TaskForm(forms.ModelForm):
    class Meta:
        model = Tasks
        fields = ["title", "descriptionn"]

        labels = {
            "title": "Название",
            "descriptionn": "Описание",
        }

        widgets = {
            "title": forms.TextInput(
                attrs={
                    "size": 50,  # Ширина поля в символах
                    # "style": "width: 300px;",  # Или задайте размер через CSS
                    "placeholder": "Назовите задачу",
                }
            ),
            "descriptionn": forms.Textarea(
                attrs={
                    "placeholder": "Опишите задачу",
                }
            ),
        }


class SubtasksForm(forms.ModelForm):
    class Meta:
        model = Subtasks
        fields = ["text"]


class SubtasksStatusForm(forms.ModelForm):
    class Meta:
        model = Subtasks
        fields = ["is_finished"]


class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field_name in self.fields:
            self.fields[field_name].help_text = None

        self.fields["username"].widget.attrs.update(
            {"id": "id_username", "placeholder": " "}
        )
        self.fields["email"].widget.attrs.update(
            {"id": "id_email", "placeholder": " "}
        )  # noqa: E501
        self.fields["password1"].widget.attrs.update(
            {"id": "id_password1", "placeholder": " "}
        )
        self.fields["password2"].widget.attrs.update(
            {"id": "id_password2", "placeholder": " "}
        )


class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(
        label="",
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": ""}
        ),  # noqa: E501
    )
    password = forms.CharField(
        label="",
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "placeholder": ""}
        ),  # noqa: E501
    )
