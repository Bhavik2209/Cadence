# myapp/urls.py
from django.urls import path
from .views import process_data_view

urlpatterns = [
    path('processdata', process_data_view , name='process_data'),
]
