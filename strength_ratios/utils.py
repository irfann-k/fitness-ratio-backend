# ratios/utils.py

from .models import StrengthRatio

def calculate_ideal_weights(exercise_input, weight_input, equipment="barbell", gender=None, age=None):
    # Filter ratios based on input criteria
    filters = {"equipment_type": equipment, "exercise": exercise_input}
    if gender:
        filters["gender"] = gender
    if age:
        filters["min_age__lte"] = age
        filters["max_age__gte"] = age

    try:
        baseline_ratio = StrengthRatio.objects.get(**filters).ratio
    except StrengthRatio.DoesNotExist:
        return {"error": "No matching strength ratio found for given criteria."}

    baseline_weight = weight_input / baseline_ratio
    ideal_weights = {}
    ratios = StrengthRatio.objects.filter(equipment_type=equipment, gender=gender, min_age__lte=age, max_age__gte=age)

    for ratio in ratios:
        ideal_weights[ratio.exercise] = baseline_weight * ratio.ratio

    return ideal_weights
