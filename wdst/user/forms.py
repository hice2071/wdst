import re
from django import forms
from django.core.exceptions import ValidationError
from user.models import Users


class RegisterForm(forms.Form):
    username = forms.CharField(
        label="用户名",
        required=True,
        max_length=50,
        min_length=2,
        error_messages={
            "required": "用户名不能为空",
            "max_length": "用户名最长不能超过50个字符",
            "min_length": "用户名最小长度为2"
        })
    password = forms.CharField(
        label="密码",
        required=True,
        max_length=50,
        min_length=5,
        error_messages={
            "required": "密码不能为空",
            "max_length": "密码最长不能超过50个字符",
            "min_length": "密码最小长度为5"
        })
    r_password = forms.CharField(
        required=True,
        max_length=50,
        min_length=5,
        label="确认密码",
        error_messages={
            "required": "确认密码不能为空",
            "max_length": "确认密码最长不能超过50个字符",
            "min_length": "确认密码最小长度为5"
        })
    email = forms.CharField(
        min_length=5,
        required=True,
        label="邮箱",
        error_messages={
            "required": "邮箱不能为空",
            "max_length": "邮箱最长不能超过50个字符",
            "min_length": "邮箱最小长度为5"
        }
    )

    def clean_username(self):
        val = self.cleaned_data.get("username")
        ret = Users.objects.filter(username=val)
        if not ret:
            return val
        else:
            raise ValidationError("该用户名已注册!")

    def clean_email(self):
        val = self.cleaned_data.get("email")
        if re.match(r'^[0-9a-zA-Z_]{0,19}@[0-9a-zA-Z]{1,13}\.[com,cn,net]{1,3}$', val):
            return val
        else:
            raise ValidationError("邮箱格式不正确!")

    # 走完所有的校验才走clean
    def clean(self):
        pwd = self.cleaned_data.get("password")
        r_pwd = self.cleaned_data.get("r_password")
        if pwd and r_pwd:
            if pwd != r_pwd:
                raise forms.ValidationError("两次密码不一致")
        return self.cleaned_data
