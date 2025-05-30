from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User

from captcha.fields import CaptchaField
from .models import TaskCategory, Tasks, Subtasks


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
        fields = ["title", "descriptionn", "deadline", "category"]

        labels = {
            "title": "Название",
            "descriptionn": "Описание",
            "deadline": "Дедлайн",
            "category": "Категория",
        }

        widgets = {
            "title": forms.TextInput(
                attrs={
                    "size": 50,
                    "placeholder": "Назовите задачу",
                }
            ),
            "descriptionn": forms.Textarea(
                attrs={
                    "placeholder": "Опишите задачу",
                }
            ),
            "deadline": forms.DateInput(
                attrs={
                        "type": "date",
                        "class": "task__deadline-input"
                }
            ),
            "category": forms.Select(attrs={"class": "task__category-select"}),
        }

    def __init__(self, *args, **kwargs):
        super(TaskForm, self).__init__(*args, **kwargs)
        self.fields['category'].queryset = TaskCategory.objects.all()
        self.fields['category'].required = False
        self.fields['category'].empty_label = "Без категории"


class SubtasksForm(forms.ModelForm):
    class Meta:
        model = Subtasks
        fields = ["text"]


class SubtasksStatusForm(forms.ModelForm):
    class Meta:
        model = Subtasks
        fields = ["is_finished"]


class RegisterForm(UserCreationForm):
    captcha = CaptchaField()

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

        self.fields['username'].error_messages = {
            'required': 'Пожалуйста, введите имя пользователя',
            'unique': 'Это имя пользователя уже занято',
            'invalid': 'Имя пользователя может содержать только буквы, цифры и символы @/./+/-/_',
        }
        
        self.fields['email'].error_messages = {
            'required': 'Пожалуйста, введите email',
            'invalid': 'Введите корректный email адрес',
            'unique': 'Этот email уже зарегистрирован',
        }
        
        self.fields['password1'].error_messages = {
            'required': 'Пожалуйста, введите пароль',
            'password_too_short': 'Пароль должен содержать минимум 8 символов',
            'password_too_common': 'Этот пароль слишком простой',
            'password_entirely_numeric': 'Пароль не может состоять только из цифр',
        }
        
        self.fields['password2'].error_messages = {
            'required': 'Пожалуйста, подтвердите пароль',
            'password_mismatch': 'Пароли не совпадают',
        }

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")

        if password1 and password2 and password1 != password2:
            self.add_error('password2', 'Пароли не совпадают')

        return cleaned_data


class CustomAuthenticationForm(AuthenticationForm):
    captcha = CaptchaField()

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


class VerificationCodeForm(forms.Form):
    code = forms.CharField(
        max_length=6,
        min_length=6,
        widget=forms.TextInput(attrs={
            'id': 'id_verification_code',
            'placeholder': ' ',
            'class': 'form-control'
        })
    )
