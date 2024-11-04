# ratios/urls.py

from django.urls import path
from .views import calculate_ratios, calculate_weakness_view

urlpatterns = [
    path('calculate/strength/', calculate_ratios, name="calculate_ratios"),
    path('calculate/weakness/', calculate_weakness_view , name="calculate_weakness"),
]
