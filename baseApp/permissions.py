from rest_framework.permissions import BasePermission

class IsAdminUserRole(BasePermission):
     """
    Custom permission to allow only Admin role users to access the view.
    Uses the custom 'is_admin' property from the User model.
    """
     def has_permission(self, request, view):
          return bool(request.user and request.user.is_authenticated and request.user.is_admin)
     

class IsMemberUserRole(BasePermission):
    """
    Custom permission to allow only Member role users to access the view.
    Uses the custom 'is_member' property from the User model.
    """
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.is_member)