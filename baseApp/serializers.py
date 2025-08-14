from rest_framework import serializers
from .models import Genre, Book

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
