"""
URL configuration for silownia_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib.auth import views as auth_views
from django.urls import path, include, re_path
from django.contrib import admin
from silownia_app import views
from silownia_app.views import edit_membership, add_event, list_events, user_login, delete_event

urlpatterns = [
    path('', views.index, name='index'),
    path('clients/', views.list_clients, name='list_clients'),
    path('clients/list/', views.list_clients, name='list_clients'),
    path('clients/add/', views.add_client, name='add_client'),
    path('clients/delete/<int:client_id>/', views.delete_client, name='delete_client'),
    path('memberships/list/', views.list_memberships, name='list_memberships'),
    path('memberships/add/', views.add_membership, name='add_membership'),
    path('memberships/delete/<int:membership_id>/', views.delete_membership, name='delete_membership'),
    path('memberships/edit/<int:membership_id>/', edit_membership, name='edit_membership'),
    path('events/add/', add_event, name='add_event'),
    path('events/list/', list_events, name='list_events'),
    path('login/', user_login, name='user_login'),
    path('events/add/', add_event, name='add_event'),
    path('events/add_group/', views.add_group_event, name='add_group_event'),
    path('events/list_group/', views.list_group_events, name='list_group_events'),
    path('events/list_personal_schedules/', views.list_personal_schedules, name='list_personal_schedules'),
    path('enroll_group_event/<int:event_id>/', views.enroll_for_group_event, name='enroll_for_group_event'),
    path('events/delete/<int:event_id>/', delete_event, name='delete_event'),
    path('logout/', views.user_logout, name='user_logout'),
]

