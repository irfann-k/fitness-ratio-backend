from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .utils import calculate_ideal_weights
from .utils import calculate_weakness

@api_view(['POST'])
def calculate_ratios(request):
    exercise_input = request.data.get("exercise")
    weight_input = request.data.get("weight")
    equipment = request.data.get("equipment", "barbell")
    gender = request.data.get("gender", None)
    age = request.data.get("age", None)

    if not exercise_input or not weight_input:
        return Response({"error": "Both 'exercise' and 'weight' fields are required."}, status=status.HTTP_400_BAD_REQUEST)

    try:
        weight_input = float(weight_input)
        age = int(age) if age else None
    except ValueError:
        return Response({"error": "Weight and age must be valid numbers."}, status=status.HTTP_400_BAD_REQUEST)

    ideal_weights = calculate_ideal_weights(exercise_input, weight_input, equipment, gender, age)
    if "error" in ideal_weights:
        return Response(ideal_weights, status=status.HTTP_404_NOT_FOUND)
    
    return Response(ideal_weights, status=status.HTTP_200_OK)

@api_view(['POST'])
def calculate_weakness_view(request):
    # Get data from request body
    data = request.data
    exercise_weights = data.get("exercise_weights", {})
    equipment = data.get("equipment", "barbell")
    gender = data.get("gender", None)
    age = data.get("age", None)

    # Validate the input data
    if not exercise_weights:
        return JsonResponse({"error": "Exercise weights are required."}, status=400)

    # Call the utility function to calculate weakness
    result = calculate_weakness(
        exercise_weights=exercise_weights,
        equipment=equipment,
        gender=gender,
        age=age
    )

    # Return the result as JSON
    return Response(result, status=status.HTTP_200_OK)
