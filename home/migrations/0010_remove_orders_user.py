# Generated by Django 4.2.7 on 2023-11-06 13:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0009_orders_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='orders',
            name='user',
        ),
    ]
