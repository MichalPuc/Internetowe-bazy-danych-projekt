# Generated by Django 4.2.7 on 2023-12-02 17:08

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('silownia_app', '0002_delete_employee_remove_event_trainer_id_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='clients_list',
            field=models.ManyToManyField(blank=True, related_name='client_events', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='event',
            name='max_clients',
            field=models.PositiveIntegerField(default=1),
        ),
        migrations.AlterField(
            model_name='event',
            name='event_type',
            field=models.CharField(choices=[('group', 'Trening grupowy'), ('personal', 'Trening personalny')], max_length=20),
        ),
        migrations.AlterField(
            model_name='event',
            name='trainer',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='trainer_events', to=settings.AUTH_USER_MODEL),
        ),
    ]