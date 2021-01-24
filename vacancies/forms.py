from django import forms


class SignUpForm(forms.Form):
    login = forms.CharField(min_length=3)
    first_name = forms.CharField()
    last_name = forms.CharField()
    password = forms.PasswordInput()
