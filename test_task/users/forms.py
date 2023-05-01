from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser


class Register(UserCreationForm):

    class Meta:
        model = CustomUser
        fields = (
            'email',
            'first_name',
            'last_name',
            'password1',
            'password2',
        )
