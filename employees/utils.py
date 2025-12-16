def has_role(user, allowed_roles=[]):
    if not user.is_authenticated:
        return False
    if user.is_superuser:
        return True
    try:
        return user.employee.role in allowed_roles
    except:
        return False
