from django.shortcuts import render
from .models import Genre
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from .serializers import GenreSerializer


class GenreApiViewSet(ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer