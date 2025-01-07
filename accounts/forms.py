from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.forms import UserCreationForm,AdminUserCreationForm
from django.contrib.auth import get_user_model

# from .models import CustomUser

class CustomUserCreationForm(AdminUserCreationForm):
    class Meta:
        model=get_user_model()
        # model=CustomUser
        fields=('email','username',)

class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model=get_user_model()
        fields=('email','username',)