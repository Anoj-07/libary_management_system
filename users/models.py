from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    """
    Custom User model extending Django's AbstractUser.
    This model adds a 'role' field to differentiate between
    Admin and Member roles for role-based authentication.

    Why use AbstractUser?
    ---------------------
    - Allows adding custom fields (phone, address, etc.) easily.
    - Avoids complex migrations later if extra fields are needed.
    - Role-based access can be implemented directly using the 'role' field.
    """

    # Role choices for the user
    ADMIN = 'ADMIN'
    MEMBER = 'MEMBER'
    ROLE_CHOICES = [
        (ADMIN, 'Admin'),
        (MEMBER, 'Member'),
    ]

    role = models.CharField(
        max_length=10,
        choices=ROLE_CHOICES,
        default=MEMBER,
        help_text="Defines the role of the user in the system (Admin or Member)."
    )

    email = models.EmailField( unique=True, help_text="Email address of the user. Must be unique.")

    # Additional fields can be added here in the future:
    # phone_number = models.CharField(max_length=15, blank=True, null=True)
    # address = models.TextField(blank=True, null=True)

    def __str__(self):
        """
        String representation of the User object.
        Shows username and role for clarity.
        """
        return f"{self.username} ({self.role})"

    @property
    def is_admin(self):
        """
        Checks if the user has the Admin role.
        Returns:
            bool: True if user is Admin, else False.
        """
        return self.role == self.ADMIN

    @property
    def is_member(self):
        """
        Checks if the user has the Member role.
        Returns:
            bool: True if user is Member, else False.
        """
        return self.role == self.MEMBER
