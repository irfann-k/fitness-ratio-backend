# ratios/urls.py

from django.urls import path
from .views import calculate_ratios, calculate_weakness_view

urlpatterns = [
    path('strength/', calculate_ratios, name="calculate_ratios"),
    path('weakness/', calculate_weakness_view , name="calculate_weakness"),
]
