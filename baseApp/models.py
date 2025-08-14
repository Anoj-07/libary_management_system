from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta


# Create your models here.

# class for genre
class Genre(models.Model):
    """
    Represents a category or type of book.
    This model allows easy filtering/searching by genre.
    Example: Fiction, Non-Fiction, Science, Technology, etc.
    """ 
    name = models.CharField(max_length=100, unique=True, help_text="Name of the genre")
    description = models.TextField(blank=True, null=True, help_text="Description of the genre")

    def __str__(self):
        return self.name

# class for book
class Book(models.Model):
    """
    Represents a book in the library's collection.
    Stores essential information about each book and its availability.
    """
    title = models.CharField(max_length=200, help_text="Title of the book")
    author = models.CharField(max_length=100, help_text="Author of the book")
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE, null=True, help_text="Genre of the book")
    isbn = models.CharField(max_length=20, unique=True, help_text="ISBN number of the book")
    total_copies = models.PositiveIntegerField(help_text="Total number of copies available in the library")
    available_copies = models.PositiveIntegerField(help_text="Number of copies currently available for borrowing")
    created_at = models.DateTimeField(auto_now_add=True, help_text="Time when the book was added")
    updated_at = models.DateTimeField(auto_now=True, help_text="Time when the book record was last updated")

    def __str__(self):
        return f"{self.title} by {self.author}"
    
    def is_available(self):
        """
        Checks if at least one copy of the book is available.
        Returns:
            bool: True if available_copies > 0, else False.
        """
        return self.available_copies > 0

def default_due_date():
    """
    Returns a default due date 14 days from today.
    Django migrations can serialize this function, unlike a lambda.
    """
    return timezone.now().date() + timedelta(days=14)


class BorrowRecord(models.Model):
    """
    Tracks the borrowing history of books.
    Links each borrowed book to the member who borrowed it.
    """
    STATUS_CHOICES = [
        ('BORROWED', 'Borrowed'),
        ('RETURNED', 'Returned'),
        ('OVERDUE', 'Overdue'),
    ]

    book = models.ForeignKey(Book, on_delete=models.CASCADE, help_text="The book being borrowed.")
    member = models.ForeignKey(
        User,  # Custom user model defined in settings.py
        on_delete=models.CASCADE,
        limit_choices_to={'role': 'MEMBER'},
        help_text="The member who borrowed the book."
    )
    borrow_date = models.DateField(default=timezone.now, help_text="Date when the book was borrowed.")
    due_date = models.DateField(
        default=default_due_date,
        help_text="Date when the book should be returned."
    )
    return_date = models.DateField(null=True, blank=True, help_text="Date when the book was actually returned.")
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='BORROWED',
        help_text="Current status of the borrowing record."
    )

    def __str__(self):
        return f"{self.member} borrowed {self.book}"

    def mark_as_returned(self):
        """
        Marks the borrow record as returned and updates the book's available copies.
        """
        if self.status == 'BORROWED':
            self.status = 'RETURNED'
            self.return_date = timezone.now().date()
            self.book.available_copies += 1
            self.book.save()
            self.save()

    def mark_as_overdue(self):
        """
        Marks the borrow record as overdue if past the due date.
        """
        if self.status == 'BORROWED' and timezone.now().date() > self.due_date:
            self.status = 'OVERDUE'
            self.save()