# Generated by Django 4.1.7 on 2023-03-21 14:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0002_account_phone_number'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='address',
            field=models.CharField(blank=True, max_length=150, null=True),
        ),
    ]
