from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.utils.translation import gettext_lazy as _
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages


class ClientManager(BaseUserManager):
    def create_user(self, login, password=None):
        if not login:
            raise ValueError(_('Użytkownik musi mieć login'))

        user = self.model(
            login=login,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, login, password):
        user = self.create_user(
            login,
            password=password,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user

class Client(AbstractBaseUser):
    login = models.CharField(_('login'), max_length=100, unique=True)
    first_name = models.CharField(_('imię'), max_length=100)
    last_name = models.CharField(_('nazwisko'), max_length=100)
    date_of_birth = models.DateField(_('data urodzenia'), null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_employee = models.BooleanField(default=False)
    is_trainer = models.BooleanField(default=False)

    objects = ClientManager()

    USERNAME_FIELD = 'login'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.login
    
    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin

# Model karnetu
class Membership(models.Model):
    MEMBERSHIP_CHOICES = [
        ('Normal', _('Normal')),
        ('Premium', _('Premium')),
    ]

    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    activation_date = models.DateField()
    expiration_date = models.DateField()
    membership_type = models.CharField(
        max_length=10,
        choices=MEMBERSHIP_CHOICES,
        default='Normal',
    )

    def __str__(self):
        return f"{self.get_membership_type_display()} - {self.client.login}"

# Model wydarzenia
class Event(models.Model):
    date = models.DateTimeField()
    trainer = models.ForeignKey(Client, on_delete=models.SET_NULL, null=True, blank=True, related_name='trainer_events')
    EVENT_TYPE_CHOICES = [
        ('group', 'Trening grupowy'),
        ('personal', 'Trening personalny'),
    ]
    event_type = models.CharField(max_length=20, choices=EVENT_TYPE_CHOICES)
    max_clients = models.PositiveIntegerField(default=1)
    clients_list = models.ManyToManyField('Client', blank=True, related_name='client_events')

    def get_current_registered_clients_count(self):
        return self.eventregistration_set.count()

    

# Model zapisów na wydarzenia
class EventRegistration(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)

