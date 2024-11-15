from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .utils import get_exercise_recommendation

class RecommendationView(APIView):
    def post(self, request):
        # Extract the exercise type from the payload
        exercise_data = request.data
        exercise_type = exercise_data.get("exercise")

        # Validate that the necessary keys are present in the request
        if not exercise_type or not all(key in exercise_data for key in ["actual_weight", "ideal_weight", "percent_difference"]):
            return Response(
                {"error": "Invalid data. Please provide 'exercise', 'actual_weight', 'ideal_weight', and 'percent_difference'."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Pass the exercise data to the OpenAI recommendation function
        recommendation = get_exercise_recommendation(exercise_data)

        # Return the recommendation response
        return Response({"recommendation": recommendation}, status=status.HTTP_200_OK)
