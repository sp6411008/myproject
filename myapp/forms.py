from django import forms
from .models import User

class SignUpForm(forms.ModelForm):
	class Meta:
		widgets = {
        'password': forms.PasswordInput(),
        'confirm_password': forms.PasswordInput(),}
		model=User
		fields=('first_name','last_name','email','address','mobile','password','confirm_password')
class LoginForm(forms.ModelForm):
	class Meta:
		widgets = {
        'password': forms.PasswordInput(),}
		model=User
		fields=('email','password')