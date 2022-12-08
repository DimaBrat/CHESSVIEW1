# Импортируем формы и модель User
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from .models import Comment

class SignUpForm(forms.Form):
    # Создаём все необходимые для регистрации поля
    username = forms.CharField(
        max_length=100,  # Максимальная длина поля
        required=True,  # Помечаем, что поле обязательно к заполнению
        widget=forms.TextInput(attrs={  # Виджет представляет поле в виде кода HTML
            'class': "form-control",
            'id': "inputUsername",
            'placeholder': "Имя пользователя",
        })
    )
    # Дальше всё по такому же принципу
    password = forms.CharField(
        required=True,
        widget=forms.PasswordInput(attrs={
            'class': "form-control",
            'id': "inputPassword",
            'placeholder': "Пароль",
        })
    )
    repeat_password = forms.CharField(
        required=True,
        widget=forms.PasswordInput(attrs={
            'class': "form-control",
            'id': "ReInputPassword",
            'placeholder': "Повторите пароль",
        })
    )

    # Метод для валидации формы (Проверка на то, что все требования соблюдены)
    def clean(self):
        username = self.cleaned_data['username']
        password = self.cleaned_data['password']  # Забираем пароли из списка cleaned_data
        confirm_password = self.cleaned_data['repeat_password']

        if password != confirm_password:  # Проверяем их на совпадение
            raise forms.ValidationError(
                "Пароли не совпадают"
            )
        elif User.objects.filter(username=username).exists():
            raise forms.ValidationError(
                "Пользователь с данным именем уже существует"
            )

    # Метод, который сохраняет данные в БД
    def save(self):
        try:
            user = User.objects.create_user(
                username=self.cleaned_data['username'],  # Создаём пользователя при помощи запроса
                password=self.cleaned_data['password'],
            )
            user.save()  # Сохраняем данные в БД
            auth = authenticate(**self.cleaned_data)  # Проверка авторизированных данных
            return auth
        except:
            pass


class SignInForm(forms.Form):
    # Точно такой же подход
    username = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs={
            'class': "form-control",
            'id': "inputUsername",
            'placeholder': "Имя пользователя",
        })
    )
    password = forms.CharField(
        required=True,
        widget=forms.PasswordInput(attrs={
            'class': "form-control",
            'id': "inputPassword",
            'placeholder': "Пароль",
        })
    )

    def clean(self):
        user = authenticate(**self.cleaned_data)
        if user is None:
            raise forms.ValidationError(
                "Неверное имя пользователя или пароль"
            )

class FeedBackForm(forms.Form):
    name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'id': 'name',
            'placeholder': "Ваше имя"
        })
    )
    email = forms.CharField(
        max_length=100,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'id': 'email',
            'placeholder': "Ваша почта"
        })
    )
    subject = forms.CharField(
        max_length=200,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'id': 'subject',
            'placeholder': "Тема"
        })
    )
    message = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control md-textarea',
            'id': 'message',
            'rows': 2,
            'placeholder': "Ваше сообщение"
        })
    )

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('text',)  # Перечисление полей формы, которые мы хотим отображать на странице
        # Внутри виджета мы указали, что поле text это TextArea и ее класс form-control, а кол-во строк в ней 3
        widgets = {
            'text': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3
            }),
        }