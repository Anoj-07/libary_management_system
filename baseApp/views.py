from django.shortcuts import render
from .models import Genre, Book, BorrowRecord
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework import status
from rest_framework.response import Response
from .serializers import GenreSerializer, BookSerializer, BorrowRecordSerializer, UserSerializer
from django.utils import timezone

from django.contrib.auth.models import User


class GenreApiViewSet(ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class BookAPiViewSet(ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

class BorrowRecordViewSet(ModelViewSet):
    """
    API endpoint to manage borrowing records.
    - Provides default CRUD operations (list, retrieve, create, update, delete)
    - Includes custom actions for:
        1. Marking a record as returned
        2. Marking a record as overdue
        3. Listing all overdue records
    """

    # Use select_related for performance (avoid multiple queries for book & member)
    queryset = BorrowRecord.objects.all().select_related("book")

    # The serializer responsible for converting model instances to JSON and vice versa
    serializer_class = BorrowRecordSerializer

    # ---------------- Custom Actions ---------------- #

    def mark_as_returned(self, request, pk=None):
        """
        Custom endpoint: POST /borrow-records/{id}/mark_as_returned/
        Marks the specific borrow record as returned:
        - Updates status = RETURNED
        - Sets return_date = today
        - Increases book.available_copies by 1
        """
        record = self.get_object()  # fetch the BorrowRecord by id
        record.mark_as_returned()   # call model method
        serializer = self.get_serializer(record)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def mark_as_overdue(self, request, pk=None):
        """
        Custom endpoint: POST /borrow-records/{id}/mark_as_overdue/
        Marks the specific borrow record as overdue (if past due_date):
        - Updates status = OVERDUE
        """
        record = self.get_object()
        record.mark_as_overdue()
        serializer = self.get_serializer(record)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def overdue(self, request):
        """
        Custom endpoint: GET /borrow-records/overdue/
        Fetches all borrow records where status = OVERDUE
        Useful for librarians/admins to track pending books.
        """
        today = timezone.now().date()
        overdue_records = BorrowRecord.objects.filter(status="OVERDUE")
        serializer = self.get_serializer(overdue_records, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

# Model for Auhthentication
class UserApiView(GenreApiViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    permission_classes = ([])  # No authentication required for this view and from setting above all views require authentication

    def register(self, request):
        """
        Custom endpoint: POST /register/
        Registers a new user:
        - Accepts username, password, email, first_name, last_name
        - Hashes the password before saving
        """
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
