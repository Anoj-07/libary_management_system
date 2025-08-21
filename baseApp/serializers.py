from rest_framework import serializers
from .models import Genre, Book, BorrowRecord
from django.contrib.auth.models import User, Group
from django.contrib.auth.hashers import make_password


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = "__all__"


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = "__all__"
        read_only_fields = ("created_at", "updated_at")

    def validate(self, data):
        if data["available_copies"] > data["total_copies"]:
            raise serializers.ValidationError(
                "Available copies cannot exceed total copies."
            )
        return data

class BorrowRecordSerializer(serializers.ModelSerializer):
    """
    Serializer for the BorrowRecord model, representing a record of a book borrowed by a member.
    Fields:
        id (int): Unique identifier for the borrow record.
        book (int): Primary key of the borrowed book.
        book_title (str): Title of the borrowed book (read-only).
        member (int): Primary key of the member who borrowed the book.
        borrow_date (date): Date when the book was borrowed.
        due_date (date): Date by which the book should be returned.
        return_date (date or None): Date when the book was returned (read-only, nullable).
        status (str): Current status of the borrow record (read-only).
    Meta:
        model (BorrowRecord): The model associated with this serializer.
        fields (list): List of fields to be included in the serialized output.
        read_only_fields (list): Fields that are read-only and cannot be modified directly.
    Validation:
        - Ensures that the member belongs to the "member" group before allowing them to borrow books.
    """
    book_title = serializers.CharField(source="book.title", read_only=True)
    # member_name = serializers.CharField(source="member.username", read_only=True)

    # borrow_date = serializers.DateField(format="%Y-%m-%d", read_only=True)
    due_date = serializers.DateField(format="%Y-%m-%d")
    # return_date = serializers.DateField(format="%Y-%m-%d", required=False, allow_null=True)

    class Meta:
        model = BorrowRecord
        fields = [
            "id",
            "book",
            "book_title",
            "member",
            "borrow_date",
            "due_date",
            "return_date",
            "status",
        ]
        read_only_fields = ["status", "return_date"]  # prevent direct modification

        def validate_member(self, value):
            if not value.groups.filter(name="member").exists():
                raise serializers.ValidationError("User must be a Member to borrow books.")
            return value


# Serializer for Authentication
class UserSerializer(serializers.ModelSerializer):
    # password = serializers.CharField(write_only=True) # This field will not be returned in the response
    class Meta:
        model = User
        fields = ['username', 'password', 'groups', 'email', 'first_name', 'last_name']
    
    def create(self, validated_data):
        raw_password = validated_data.pop('password') # remove and assigned password key and value which user sent and validated
        hash_password = make_password(raw_password) # hasing user's password using make_password function
        validated_data['password'] = hash_password # Assigning hashed password as a validated data
        user =  super().create(validated_data) # Passing the validated data to the parent class's create method to save the user instance

        member_group = Group.objects.get(name="member")
        user.groups.add(member_group)

        return user

class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ["id", "name"]

# serializer for Login
class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()


# member
class MemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']

