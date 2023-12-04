# views.py w silownia_app

from django.shortcuts import render, redirect, get_object_or_404
from .models import Client, Membership, Event, EventRegistration
from .forms import ClientForm, Membership, MembershipForm, MembershipEditForm, EventForm, GroupEventForm, TrainerSelectForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
import logging
from django.contrib.auth.decorators import user_passes_test, login_required
from .forms import ClientAuthenticationForm
@login_required(login_url='user_login')
def index(request):
    user_role = None

    if request.user.is_authenticated:
        if request.user.is_employee:
            user_role = 'employee'
        elif request.user.is_trainer:
            user_role = 'trainer'
        elif request.user.is_admin:
            user_role = 'admin'

        # Dodaj poniższy kod, aby uzyskać karnety użytkownika
        user_memberships = Membership.objects.filter(client=request.user)
        context = {'user_role': user_role, 'user_memberships': user_memberships}
    else:
        context = {'user_role': user_role}

    return render(request, 'index.html', context)


@user_passes_test(lambda user: user.is_active and (user.is_employee or user.is_admin), login_url='user_login')
def list_clients(request):
    clients = Client.objects.all()
    return render(request, 'clients/list.html', {'clients': clients, 'home_url': 'home'})


@user_passes_test(lambda user: user.is_active and (user.is_employee or user.is_admin), login_url='user_login')
def add_client(request):
    if request.method == 'POST':
        # Pass the user's role to the form
        form = ClientForm(request.POST, user_role='admin' if request.user.is_admin else 'employee')

        if form.is_valid():
            form.save()
            return redirect('list_clients')
    else:
        # Pass the user's role to the form
        form = ClientForm(user_role='admin' if request.user.is_admin else 'employee')

    return render(request, 'clients/add.html', {'form': form, 'home_url': 'home'})

@user_passes_test(lambda user: user.is_active and (user.is_employee or user.is_admin), login_url='login')
def delete_client(request, client_id):
    client = Client.objects.get(id=client_id)
    client.delete()
    return redirect('list_clients')

@user_passes_test(lambda user: user.is_active and (user.is_employee or user.is_admin), login_url='user_login')
def add_membership(request):
    if request.method == 'POST':
        form = MembershipForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('list_memberships')
    else:
        form = MembershipForm()

    return render(request, 'memberships/add.html', {'form': form, 'home_url': 'home'})

@user_passes_test(lambda user: user.is_active and (user.is_employee or user.is_admin), login_url='user_login')
def delete_membership(request, membership_id):
    membership = Membership.objects.get(id=membership_id)
    membership.delete()
    return redirect('list_memberships')

@user_passes_test(lambda user: user.is_active and (user.is_employee or user.is_admin), login_url='user_login')
def list_memberships(request):
    clients_with_memberships = Client.objects.prefetch_related('membership_set').all()
    return render(request, 'memberships/list.html', {'clients': clients_with_memberships})

@user_passes_test(lambda user: user.is_active and (user.is_employee or user.is_admin), login_url='user_login')
def edit_membership(request, membership_id):
    membership = get_object_or_404(Membership, id=membership_id)

    if request.method == 'POST':
        form = MembershipEditForm(request.POST, instance=membership)
        if form.is_valid():
            form.save()
            return redirect('list_memberships')
    else:
        form = MembershipEditForm(instance=membership)

    return render(request, 'memberships/edit.html', {'form': form, 'membership': membership})

@user_passes_test(lambda user: user.is_active and (user.is_trainer or user.is_admin), login_url='user_login')
def add_event(request):
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            event = form.save(commit=False)
            event.trainer = request.user  # Przypisz zalogowanego trenera
            event.save()
            return redirect('list_events')
    else:
        form = EventForm()

    return render(request, 'events/add.html', {'form': form})

@user_passes_test(lambda user: user.is_active and (user.is_employee or user.is_admin), login_url='user_login')
def add_group_event(request):
    if request.method == 'POST':
        form = GroupEventForm(request.POST)
        if form.is_valid():
            event = form.save(commit=False)
            event.event_type = 'group'
            event.save()
            return redirect('list_events')
    else:
        form = GroupEventForm()

    return render(request, 'events/add_group.html', {'form': form})



def list_events(request):
    events = Event.objects.all().order_by('date')  # Sort events by date
    context = {'events': events}
    return render(request, 'events/list.html', context)

def get_group_events():
    group_events = Event.objects.filter(event_type='group').order_by('date')  # Sort group events by date
    return group_events

def list_group_events(request):
    group_events = get_group_events()
    user_is_registered = {event.id: request.user.eventregistration_set.filter(event=event).exists() for event in group_events}
    print(f'{user_is_registered}')
    return render(request, 'events/list_group.html', {'group_events': group_events, 'user_is_registered': user_is_registered})


def list_personal_schedules(request):
    form = TrainerSelectForm(request.GET)

    # Pobierz wszystkich trenerów, aby wyświetlić ich w formularzu
    trainers = Client.objects.filter(is_trainer=True)

    personal_events = Event.objects.filter(event_type='personal')

    if form.is_valid():
        trainer = form.cleaned_data['trainer']
        personal_events = personal_events.filter(trainer=trainer)

    return render(request, 'events/list_personal_schedules.html',
                  {'form': form, 'trainers': trainers, 'personal_events': personal_events})


@user_passes_test(lambda user: user.is_active and (user.is_employee or user.is_admin or user.is_trainer), login_url='user_login')
def delete_event(request, event_id):
    event = Event.objects.get(id=event_id)

    # Check if the user has permission to delete the event
    if not (request.user.is_admin or request.user == event.trainer):
        return redirect('list_events')

    event.delete()
    return redirect('list_events')

def show_user_credentials(request):
    users = Client.objects.all()
    return render(request, 'show_user_credentials.html', {'users': users})


def user_login(request):
    if request.method == 'POST':
        login_value = request.POST['login']
        password = request.POST['password']
        user = authenticate(request, login=login_value, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, 'Login successful')
            return redirect('index')
        else:
            messages.error(request, 'Invalid login credentials')
            logging.error(f'Login failed for user: {login_value}')

    return render(request, 'registration/login.html')

def has_employee_role(user):
    return user.is_authenticated and user.is_employee

def has_trainer_role(user):
    return user.is_authenticated and user.is_trainer

def has_admin_role(user):
    return user.is_authenticated and user.is_admin

def user_logout(request):
    logout(request)
    return redirect('user_login')

@login_required(login_url='user_login')
def enroll_for_group_event(request, event_id):
    event = get_object_or_404(Event, id=event_id, event_type='group')
    client = request.user  # Bezpośrednio używaj request.user jako klienta

    # Sprawdź, czy klient już nie jest zapisany na to wydarzenie
    if EventRegistration.objects.filter(client=client, event=event).exists():
        # Tutaj możesz obsłużyć sytuację, gdy klient już jest zapisany
        # Na przykład przekierować klienta z komunikatem
        messages.warning(request, 'Jesteś już zapisany na te zajęcia.')
        return redirect('list_group_events')

    # Tworzenie nowego wpisu o zapisie klienta na wydarzenie grupowe
    EventRegistration.objects.create(client=client, event=event)

    return redirect('list_group_events')


