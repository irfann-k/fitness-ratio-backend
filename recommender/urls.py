from django.urls import path
from .views import RecommendationView

urlpatterns = [
    path('exercises/', RecommendationView.as_view(), name='recommendation'),
]