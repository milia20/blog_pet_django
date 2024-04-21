from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from .models import Tag, Post, Comment
from typing import List


class RegistrationForm(UserCreationForm):
    """
    A form for registering a new user.
    """
    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(label='Email', widget=forms.EmailInput(attrs={'class': 'form-control'}))
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label='Повторите пароль', widget=forms.PasswordInput(attrs={'class': 'form-control'})) 

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


class LoginForm(AuthenticationForm):
    """
    A form for logging in a user.
    """
    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    error_messages = {
        'invalid_login': "Неверный логин или пароль",
        'inactive': "Ваш аккаунт неактивен.",
    }


class PostForm(forms.ModelForm):
    """
    A form for creating or updating a Post object.
    """
    image = forms.ImageField(required=False)

    class Meta:
        model: 'Post' = Post
        fields: List[str] = ['title', 'slug', 'body', 'tags', 'image']

        widgets: dict = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите заголовок'}),
            'slug': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите уникальный адрес поста'}),
            'body': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Введите текст'}),
            'tags': forms.SelectMultiple(attrs={'class': 'form-control'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control', 'accept': 'image/*', }),
            # 'image': forms.ClearableFileInput(attrs={'class': 'form-control', 'multiple': True, 'accept': 'image/*',}),
        }

        def clean_slug(self: 'PostForm') -> str:
            """
            Validates the 'slug' field to ensure that it is not the same as 'create'.
            Raises ValidationError if the 'slug' field is the same as 'create'.
            """
            new_slug: str = self.cleaned_data['slug'].lower()

            if new_slug == 'create':
                raise ValidationError(f'Адрес тега должен быть уникальным. "{new_slug}" уже используется.')
            return new_slug
        

class CommentForm(forms.ModelForm):
    """
    A form for creating or updating a Comment object.
    """
    
    class Meta:
        model: Comment = Comment
        fields: list = ['text']

        widgets: dict = {
            'text': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Введите текст', 'style': 'font-family: Ubuntu, sans-serif; font-size: 20px;', 'rows': 3, 'wrap': 'soft'}),
        }


class TagForm(forms.ModelForm):
    """
    A form for creating or updating a Tag object.
    """
    class Meta:
        model: 'Tag' = Tag
        fields: List[str] = ['title', 'slug']

        widgets: dict = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите загловок тега'}),
            'slug': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите уникальный адрес тега'})
        }

    def clean_slug(self: 'TagForm') -> str:
        """
        Validates the 'slug' field to ensure that it is unique and not the same as 'create'.
        Raises ValidationError if the 'slug' field is not unique or is the same as 'create'.
        """
        new_slug: str = self.cleaned_data['slug'].lower()

        if new_slug == 'create':
            raise forms.ValidationError('Уникальный адрес тега не может быть "create"')

        if Tag.objects.filter(slug__iexact=new_slug).count():
            raise forms.ValidationError(
                f'Адрес тега должен быть уникальным. "{new_slug}" уже используется.')

        return new_slug
