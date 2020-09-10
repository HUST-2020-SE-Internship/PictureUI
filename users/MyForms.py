from django import forms
from django.contrib.auth.models import User
import re

from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator

def email_check(email):
    pattern = re.compile(r"\"?([-a-zA-Z0-9.'?{}]+@\w+\.\w+)\"?")
    return re.match(pattern, email)


class RegistrationForm(forms.Form):
    #username = forms.CharField(label='Username', max_length=50)
    username = forms.CharField(label='Username', 
                                min_length=3,
                                max_length=20,
                                error_messages={"min_length": "用户名至少需要3个字符",
                                                "max_length": "用户名不能超过20个字符"},
                                validators=[RegexValidator(r"^[a-zA-Z0-9_]{3,20}$", message="只能由字母,数字,下划线组成")],
                                widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "3~20个字符", "required": "required",}),
                                )
    email = forms.EmailField(label='Email',
                            validators=[RegexValidator(r"^[a-zA-Z0-9][\w\.-]*[a-zA-Z0-9]@[a-zA-Z0-9][\w\.-]*[a-zA-Z0-9]\.[a-zA-Z][a-zA-Z\.]*[a-zA-Z]$", message="请输入正确的邮箱格式")],
                            widget=forms.EmailInput(attrs={"class": "form-control", "placeholder": "邮箱, 你懂得"}))
    password1 = forms.CharField(label='Password', 
                                min_length=6,
                                max_length=20,
                                error_messages={"min_length": "密码至少6位",
                                                "max_length": "密码最多20位"},
                                validators=[RegexValidator(r"[a-zA-Z][a-zA-Z0-9.]{5,19}", message="以字母开头,只能包含字母数字小数点")],
                                widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder": "6-20位以字母开头包含小数点"}))

    password2 = forms.CharField(label='Password Confirmation', widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder": "请再次输入密码"}))

    # user clean methods to define custom validation rules

    def clean_username(self):
        username = self.cleaned_data.get('username')
    
        filter_result = User.objects.filter(username__exact=username)
        if len(filter_result) > 0:
            raise forms.ValidationError('Your username already exists')
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email_check(email):
            filter_result = User.objects.filter(email__exact=email)
            if len(filter_result) > 0:
                raise forms.ValidationError("Your email already exists")
        else:
            raise forms.ValidationError("Please enter a valid email")

        return email

    def clean_password1(self):
        password1 = self.cleaned_data.get('password1')

        return password1

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError('Password mismatch Please enter again')

        return password2



class LoginForm(forms.Form):
    username = forms.CharField(label='Username', max_length=50, 
                                error_messages={'required': 'Please Fuck yourself'},
                                widget=forms.TextInput(attrs={"class": "form-control", "required": "required",}))
    password = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={"class": "form-control"}))

    # use clean methods to define custom validation rules

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if email_check(username):
            filter_result = User.objects.filter(email__exact=username)
            if not filter_result:
                raise forms.ValidationError('This emial does not exist')
        else:
            filter_result = User.objects.filter(username__exact=username)
            if not filter_result:
                raise forms.ValidationError(message='This username does not exist Please register first')

        return username


class ProfileForm(forms.Form):
    first_name = forms.CharField(label='First Name', max_length=50, required=False)
    last_name = forms.CharField(label='Last Name', max_length=50, required=False)
    org = forms.CharField(label='Organization', max_length=50, required=False)
    telephone = forms.CharField(label='Telephone', max_length=50, required=False)
    emil = forms.CharField(label='email', max_length=50, required=False)


class PwdChangeForm(forms.Form):
    old_password = forms.CharField(label='Old Password', widget=forms.PasswordInput)

    password1 = forms.CharField(label='New Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password Confirmation', widget=forms.PasswordInput)

    # use clean methods to define custom validation rules

    def clean_password1(self):
        password1 = self.cleaned_data.get('password1')

        if len(password1) < 6:
            raise forms.ValidationError("your password is too short")
        elif len(password1) > 20:
            raise forms.ValidationError("your password is too long")

        return password1

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Password mismatch Please enter again")

        return password2
