import os
from openai import OpenAI
from django.conf import settings

# Initialize the OpenAI client with the API key
client = OpenAI(api_key=settings.OPENAPI_KEY)

def get_exercise_recommendation(exercise_data):
    exercise = exercise_data.get("exercise")
    actual_weight = exercise_data.get("actual_weight")
    ideal_weight = exercise_data.get("ideal_weight")
    percent_difference = exercise_data.get("percent_difference")

    input_prompt = (
        f"For the exercise '{exercise}', the user lifts {actual_weight} kg, "
        f"with an ideal target of {ideal_weight} kg, representing a "
        f"{percent_difference:.2f}% difference in strength. Recommend exercises, "
        "target weights, and an estimated duration it will take to achieve it. Give a short summary as exercise name, weights, no of sets, how many times per week."
        "Give in a json format, key-value in a dictionary as I am serving via api"
    )

    try:
        # Use the chat completions endpoint
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "system", 
                    "content": "You are a helpful fitness trainer."
                },
                {
                    "role": "user", 
                    "content": input_prompt
                }
            ],
            model="gpt-4",  # You can also use "gpt-4" if you have access
        )
        print(chat_completion)
        # Return the generated response
        return chat_completion.choices[0].message.content.strip()
    except Exception as e:
        return str(e)
