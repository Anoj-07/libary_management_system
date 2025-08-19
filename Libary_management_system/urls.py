"""
URL configuration for Libary_management_system project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from rest_framework.routers import DefaultRouter
from baseApp.views import GenreApiViewSet, BookAPiViewSet, BorrowRecordViewSet, UserApiView

router = DefaultRouter()
router.register(r'genres', GenreApiViewSet, basename='genre')
router.register(r'books', BookAPiViewSet, basename='book')
router.register(r'borrow-records', BorrowRecordViewSet, basename='borrowrecord')

urlpatterns = [
    path('admin/', admin.site.urls),

     # Custom routes for BorrowRecord
    path('borrow-records/<int:pk>/return/', 
         BorrowRecordViewSet.as_view({'post': 'mark_as_returned'}), 
         name='borrowrecord-mark-as-returned'),

    path('borrow-records/<int:pk>/overdue/', 
         BorrowRecordViewSet.as_view({'post': 'mark_as_overdue'}), 
         name='borrowrecord-mark-as-overdue'),

    path('borrow-records/overdue/', 
         BorrowRecordViewSet.as_view({'get': 'overdue'}), 
         name='borrowrecord-overdue-list'),

    path('register/', UserApiView.as_view({'post': 'register'}))
] + router.urls
