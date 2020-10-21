from django.forms import ModelForm 
from django.contrib.auth import get_user_model

class RegisterForm(ModelForm):
    class Meta:
        model = get_user_model()
        fields = ["first_name","last_name","email","password"]

class LoginForm(ModelForm):
    class Meta:
        model = get_user_model()
        fields = ["email","password"]
