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


def calculate_weakness(exercise_weights, equipment="barbell", gender=None, age=None):
    """
    Parameters:
    - exercise_weights: a dictionary of actual weights for each exercise, e.g., {"chest": 40, "back": 50, ...}
    - equipment: type of equipment ("barbell" or "dumbbell")
    - gender: gender of the user ("male" or "female")
    - age: age of the user
    
    Returns:
    - A dictionary containing ideal weights, percentage differences, and information about the strongest part.
    """
    
    # Initialize filters with equipment and optional criteria
    filters = {"equipment_type": equipment}
    if gender:
        filters["gender"] = gender
    if age:
        filters["min_age__lte"] = age
        filters["max_age__gte"] = age

    # Retrieve all strength ratios for the specified criteria
    ratios = StrengthRatio.objects.filter(**filters)
    
    if not ratios.exists():
        return {"error": "No matching records for the criteria"}
    
    # Convert the QuerySet to a dictionary with exercise as key and ratio as value
    ratio_dict = {ratio.exercise: ratio.ratio for ratio in ratios}

#Will need to find baseline weight for each exercise and compare on that
    base_wt = {}

    for keys in exercise_weights:
        if keys in ratio_dict:
            base_wt[keys] = exercise_weights[keys] / ratio_dict[keys]

    # Find the strongest exercise by actual weight
    strongest_exercise = max(base_wt, key=base_wt.get)
    #print(strongest_exercise)
    strongest_weight = base_wt[strongest_exercise]
    #print(strongest_weight)
    # Find the ratio for the strongest exercise
    try:
        strongest_ratio = ratios.get(exercise=strongest_exercise).ratio
    except StrengthRatio.DoesNotExist:
        return {"error": f"No ratio found for exercise {strongest_exercise} with the given criteria"}

    # Calculate the baseline weight using the strongest exercise
    baseline_weight = strongest_weight

    # Calculate ideal weights based on the strongest exercise's baseline
    comparison = {}
    for ratio in ratios:
        exercise = ratio.exercise
        ideal_weight = baseline_weight * ratio.ratio
        actual_weight = exercise_weights.get(exercise, 0)
        percent_diff = (actual_weight - ideal_weight) / ideal_weight * 100 if ideal_weight else 0
        
        comparison[exercise] = {
            "actual_weight": actual_weight,
            "ideal_weight": ideal_weight,
            "percent_difference": percent_diff
        }

    # Return the results, including the strongest part information
    return {
        "strongest_exercise": strongest_exercise,
        "strongest_ratio": strongest_ratio,
        "ideal_weights": {exercise: data["ideal_weight"] for exercise, data in comparison.items()},
        "comparison": comparison
    }
