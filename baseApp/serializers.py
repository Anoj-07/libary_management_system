from rest_framework import serializers
from .models import Genre, Book, BorrowRecord

class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = '__all__'

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at')
    
    def validate(self, data):
        if data['available_copies'] > data['total_copies']:
            raise serializers.ValidationError("Available copies cannot exceed total copies.")
        return data
    

class BorrowRecordSerializer(serializers.ModelSerializer):
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
            # "member",
            # "member_name",
            "borrow_date",
            "due_date",
            "return_date",
            "status",
        ]
        read_only_fields = ["status", "return_date"]  # prevent direct modification