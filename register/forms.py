from django import forms
from django.contrib.auth.models import User
from .models import Profile


class LoginForm(forms.Form):
    username = forms.CharField(max_length=255)
    password = forms.CharField(widget=forms.PasswordInput)


class NewUserForm(forms.ModelForm):
    password = forms.CharField(label='Yangi parol', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Yangi parolni takrorlang!', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email')

    def check_password2(self):
        data = self.cleaned_data
        if data['password']!=data['password2']:
            raise forms.ValidationError('parol bir xil emas')
        return data['password2']
    
    
class EditUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email')


class EditProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('image', 'date_of_brith')