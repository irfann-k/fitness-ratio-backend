# ratios/urls.py

from django.urls import path
from .views import calculate_ratios

urlpatterns = [
    path('calculate/', calculate_ratios, name="calculate_ratios"),
]
