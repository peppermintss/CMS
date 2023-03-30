from django.core.exceptions import PermissionDenied

def verify_admin_access(user):
    
    if user.is_authenticated and user.groups.filter(name='admin').exists():
        return True
    else:
       
        raise PermissionDenied
