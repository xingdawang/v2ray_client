from django import forms
# from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordChangeForm, SetPasswordForm
from .models import CustomUser

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'name@example.com'})
    )

    class Meta:
        # model = User
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '用户名'}),
            'password1': forms.PasswordInput(attrs={
                'class': 'form-control',
                'placeholder': '输入密码'}),
            'password2': forms.PasswordInput(attrs={
                'class': 'form-control',
                'placeholder': '再次确认'}),
        }

class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ['email']


class CustomPasswordChangeForm(forms.Form):
    new_password1 = forms.CharField(
        label="新密码",
        widget=forms.PasswordInput,
        required=False  # Make this field optional
    )

    def save(self, user):
        new_password = self.cleaned_data.get('new_password1')
        if new_password:
            user.set_password(new_password)
            user.save()
        return user

class PasswordResetRequestForm(forms.Form):
    username = forms.CharField(max_length=150, label='用户名')



class PasswordResetForm(SetPasswordForm):

    new_password1 = forms.CharField(
        label="新密码",
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
    )
    new_password2 = forms.CharField(
        label="确认新密码",
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
    )