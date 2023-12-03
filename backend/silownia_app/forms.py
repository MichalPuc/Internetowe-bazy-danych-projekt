# forms.py w silownia_app

from django import forms
from .models import Client, Membership, Event
from datetime import date, timedelta
from django.contrib.auth.forms import AuthenticationForm
from django import forms
from django.contrib.auth.hashers import make_password
from .models import Client


class ClientForm(forms.ModelForm):
    login = forms.CharField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput)
    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100)
    date_of_birth = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))

    # Dodaj 'client' jako nową opcję z domyślnym zaznaczeniem
    ROLE_CHOICES = [
        ('client', 'Client'),
        ('employee', 'Employee'),
        ('trainer', 'Trainer'),
        ('admin', 'Admin'),
    ]

    role = forms.ChoiceField(label='Role', choices=ROLE_CHOICES, widget=forms.RadioSelect, initial='client')

    class Meta:
        model = Client
        fields = ['login', 'password', 'first_name', 'last_name', 'date_of_birth', 'role']

    def save(self, commit=True):
        instance = super().save(commit=False)

        role = self.cleaned_data.get('role')

        if role == 'admin':
            instance.is_admin = True
            instance.is_employee = False
            instance.is_trainer = False
        elif role == 'employee':
            instance.is_admin = False
            instance.is_employee = True
            instance.is_trainer = False
        elif role == 'trainer':
            instance.is_admin = False
            instance.is_employee = False
            instance.is_trainer = True
        elif role == 'client':  # Nowa opcja
            instance.is_admin = False
            instance.is_employee = False
            instance.is_trainer = False
        else:
            raise ValidationError('Invalid role selection')

        # Ustaw hasło używając make_password
        instance.password = make_password(self.cleaned_data['password'])

        if commit:
            instance.save()

        return instance


class MembershipForm(forms.ModelForm):
    class Meta:
        model = Membership
        fields = ['client', 'activation_date', 'expiration_date', 'membership_type']

        widgets = {
            'activation_date': forms.DateInput(attrs={'type': 'date'}),
            'expiration_date': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super(MembershipForm, self).__init__(*args, **kwargs)
        self.fields['activation_date'].initial = date.today()
        expiration_date_initial = date.today() + timedelta(days=30)
        self.fields['expiration_date'].initial = expiration_date_initial

class MembershipEditForm(forms.ModelForm):
    class Meta:
        model = Membership
        fields = ['activation_date', 'expiration_date', 'membership_type']

        widgets = {
            'activation_date': forms.DateInput(attrs={'type': 'date'}),
            'expiration_date': forms.DateInput(attrs={'type': 'date'}),
        }


class EventForm(forms.ModelForm):
    EVENT_TYPE_CHOICES = [
        ('group', 'Trening grupowy'),
        ('personal', 'Trening personalny'),
    ]
    event_type = forms.ChoiceField(choices=EVENT_TYPE_CHOICES, label='Typ wydarzenia')
    max_clients = forms.IntegerField(label='Maksymalna liczba klientów', min_value=1)

    class Meta:
        model = Event
        fields = ['event_type', 'date', 'max_clients']

        widgets = {
            'date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

    def __init__(self, *args, **kwargs):
        super(EventForm, self).__init__(*args, **kwargs)

        # Ustaw domyślną wartość max_clients w zależności od typu wydarzenia
        self.fields['max_clients'].initial = 15

class GroupEventForm(forms.ModelForm):
    trainer = forms.ModelChoiceField(queryset=Client.objects.filter(is_trainer=True))
    max_clients = forms.IntegerField(label='Maksymalna liczba klientów', min_value=1)

    class Meta:
        model = Event
        fields = ['date', 'trainer', 'max_clients']

        widgets = {
            'date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

    def __init__(self, *args, **kwargs):
        super(GroupEventForm, self).__init__(*args, **kwargs)

        # Ogranicz queryset do użytkowników, którzy są trenerami
        self.fields['trainer'].queryset = Client.objects.filter(is_trainer=True)

        # Ustaw domyślną wartość max_clients w zależności od typu wydarzenia
        self.fields['max_clients'].initial = 15

class ClientAuthenticationForm(AuthenticationForm):
    class Meta:
        model = Client
        fields = ['login', 'password']

class TrainerSelectForm(forms.Form):
    trainer = forms.ModelChoiceField(queryset=Client.objects.filter(is_trainer=True))
