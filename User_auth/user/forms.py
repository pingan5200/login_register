from django import forms
from django.contrib.auth.models import User
import re
from django.forms import ValidationError

from captcha.fields import CaptchaField


def name_validate(value):
    pattern="^[a-zA-Z0-9_\u4e00-\u9fa5]+$"
    if not re.match(pattern, str(value)):
        raise ValidationError('用户名只含有汉字、数字、字母、下划线，下划线位置不限')


def password_validate(value):
    pattern="^[a-zA-Z0-9_]{5,17}$"
    if not re.match(pattern, str(value)):
        raise ValidationError('密码长度在5~17 之间，只能包含字符、数字和下划线')


def email_validate(value):
    pattern="^\w+((-\w+)|(\.\w+))*\@[A-Za-z0-9]+((\.|-)[A-Za-z0-9]+)*\.[A-Za-z0-9]+$"
    if not re.match(pattern, str(value)):
        raise ValidationError('邮箱格式不合法')


class CaptchaTestForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'placeholder': '用户名',
                'class': 'form-control'
            }
        ),
        validators=[name_validate]
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'placeholder': '密码',
                'class': 'form-control'
            }
        ),
        validators=[password_validate]
    )           
    captcha = CaptchaField()


class UserForm(forms.ModelForm):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'placeholder': '用户名',
                'class': 'form-control'
            }
        ),
        validators=[name_validate]
    )

    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'placeholder': '密码',
                'class': 'form-control'
            }
        ),
        validators=[password_validate]
    )           

    email = forms.EmailField(
        widget=forms.TextInput(
            attrs={
                'placeholder': '邮箱',
                'class': 'form-control'
            }
        ),
        validators=[email_validate]
    )   

    class Meta:
        model = User
        fields = ('username', 'email', 'password')