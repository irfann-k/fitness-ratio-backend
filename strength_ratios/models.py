from django.db import models

# Create your models here.
# ratios/models.py

class StrengthRatio(models.Model):
    EXERCISE_CHOICES = [
        ("chest", "Chest"),
        ("back", "Back"),
        ("shoulders", "Shoulders"),
        ("biceps", "Biceps"),
        ("triceps", "Triceps"),
        ("legs_squat", "Legs (Squat)"),
        ("legs_deadlift", "Legs (Deadlift)"),
    ]
    EQUIPMENT_CHOICES = [
        ("barbell", "Barbell"),
        ("dumbbell", "Dumbbell"),
    ]
    GENDER_CHOICES = [
        ("male", "Male"),
        ("female", "Female"),
    ]

    exercise = models.CharField(max_length=20, choices=EXERCISE_CHOICES)
    ratio = models.FloatField()
    equipment_type = models.CharField(max_length=20, choices=EQUIPMENT_CHOICES, default="barbell")
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, null=True, blank=True)
    min_age = models.IntegerField(null=True, blank=True)
    max_age = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return f"{self.exercise} - {self.ratio} ({self.equipment_type}, {self.gender})"
