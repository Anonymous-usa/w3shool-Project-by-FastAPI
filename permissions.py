from fastapi import Depends, HTTPException

from auth.utils import get_current_user

def has_permission(permission):
    def checker(current_user = Depends(get_current_user)):
        user_permissions = [perm.name for perm in current_user.permissions]
        for role in current_user.roles:
            for perm in role.permissions:
                user_permissions.append(perm.name)
        if permission not in user_permissions:
            raise ValueError("Access denied!")
        return True
    return checker



def has_role(role_n: list):
    def checker(current_user = Depends(get_current_user)):
        user_roles = [role.name for role in current_user.roles]
        if not any(role in user_roles for role in role_n):
            raise HTTPException(status_code=403, detail="Access denied: role required")
        return True
    return checker
