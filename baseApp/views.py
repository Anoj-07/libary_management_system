from django.shortcuts import render
from .models import Genre, Book
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from .serializers import GenreSerializer, BookSerializer


class GenreApiViewSet(ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class BookAPiViewSet(ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer