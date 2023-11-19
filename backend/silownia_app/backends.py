# silownia_app/backends.py
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from .models import Client

# silownia_app.backends.py

class ClientAuthBackend(ModelBackend):
    def authenticate(self, request, login=None, password=None, **kwargs):
        User = get_user_model()

        try:
            user = User.objects.get(login=login)
        except User.DoesNotExist:
            return None

        # Tutaj dodajemy logi
        print(f'Authenticating user: {user.login}')
        print(f'User password: {user.password}')
        print(f'Provided login: {login}')
        print(f'Provided password: {password}')
        print(user.check_password(password))

        if user.check_password(password):
            return user

        print(f'aha')
        return None

