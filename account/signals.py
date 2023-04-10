from django.contrib.auth.models import Group
from django.db.models.signals import post_migrate
from django.dispatch import receiver

@receiver(post_migrate)
def create_groups(sender, **kwargs):
    groups_to_create = ['student', 'teacher', 'admin']
    for group_name in groups_to_create:
        if not Group.objects.filter(name=group_name).exists():
            Group.objects.create(name=group_name)
