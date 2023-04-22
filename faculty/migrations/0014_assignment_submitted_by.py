# Generated by Django 4.1.7 on 2023-04-22 12:50

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("faculty", "0013_alter_assignment_title"),
    ]

    operations = [
        migrations.AddField(
            model_name="assignment",
            name="submitted_by",
            field=models.ForeignKey(
                default=2,
                limit_choices_to={"groups__name": "student"},
                on_delete=django.db.models.deletion.CASCADE,
                to=settings.AUTH_USER_MODEL,
            ),
            preserve_default=False,
        ),
    ]
