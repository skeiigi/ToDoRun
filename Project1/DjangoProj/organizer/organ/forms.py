from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Tasks
from django.contrib.auth.forms import AuthenticationForm


class TaskStatusForm(forms.ModelForm):
    class Meta:
        model = Tasks
        fields = ['statuss']
        widgets = {
            'statuss': forms.CheckboxInput(attrs={'class': 'status-checkbox'})
        }


class TaskForm(forms.ModelForm):
    class Meta:
        model = Tasks
        fields = ['title', 'descriptionn']

        labels = {
            'title': 'Название',
            'descriptionn': 'Описание',
        }

        widgets = {
            'title': forms.TextInput(attrs={
                'size': 50,  # Ширина поля в символах
                'style': 'width: 300px;',  # Или задайте размер через CSS
                'placeholder': 'Назовите задачу',
            }),
            'descriptionn': forms.Textarea(attrs={
                'placeholder': 'Опишите задачу',
            }),
        }


class RegisterForm(UserCreationForm):
    # email = forms.EmailField(
    #     help_text="Введите действительный email (например: user@example.com)"
    # )

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]
        widget=forms.TextInput(
            attrs={
                "class": "special",
                "size": "40",
                "label": "comment",
                "placeholder": "Comma Seperated",
            }
        ),


class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(
        label='',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': ''
        })
    )
    password = forms.CharField(
        label='',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': ''
        })
    )
