import google.generativeai as genai
import requests
import json
import re
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings

# Configure Gemini API
genai.configure(api_key="your_api_key_here")  # Replace with your actual API key


# Function to fetch weather dynamically
def get_weather(city):
    api_key = settings.WEATHER_API_KEY
    url = f"https://api.weatherapi.com/v1/current.json?key={api_key}&q={city}"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            condition = (
                data.get("current", {}).get("condition", {}).get("text", "No data")
            )
            temp_c = data.get("current", {}).get("temp_c", "No data")
            return f"The weather in {city} is {condition} with a temperature of {temp_c}°C."
        else:
            return "Unable to fetch weather information. Please try again."
    except Exception as e:
        return f"Error retrieving weather data: {str(e)}"


# Extract city name from user query
def extract_city_from_query(query):
    city_pattern = r"(?:weather in|temperature in|climate in)\s*([a-zA-Z\s]+)"
    match = re.search(city_pattern, query, re.IGNORECASE)
    return match.group(1).strip() if match else None


# Function to get response from Gemini API
def get_gemini_response(prompt):
    try:
        genai.configure(api_key="your_api_key_here")  # Replace with your actual API key
        model = genai.GenerativeModel("gemini-1.5-pro")
        response = model.generate_content(
            f"Answer concisely (max 10 lines) while maintaining context of agriculture and weather, if the context is not about the agriculture return 'Out of Context' :\n\n{prompt}"
        )
        if response and hasattr(response, "text"):
            return "\n".join(response.text.split("\n")[:10])  # Limit output to 10 lines

        return "No valid response received from Gemini API."
    except Exception as e:
        return f"Error processing your request: {str(e)}"


# Chatbot API view
@csrf_exempt
def chatbot_query(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            user_query = data.get("query", "").strip()

            if not user_query:
                return JsonResponse({"response": "Please enter a question."})

            # Auto-detect city for weather-related queries
            if "weather" in user_query.lower() or "temperature" in user_query.lower():
                city = extract_city_from_query(user_query)
                if city:
                    return JsonResponse({"response": get_weather(city)})
                else:
                    return JsonResponse(
                        {
                            "response": "Please specify a city to get the weather details."
                        }
                    )

            # Get response from Gemini using existing function
            gemini_response = get_gemini_response(user_query)
            return JsonResponse({"response": gemini_response})

        except Exception as e:
            return JsonResponse({"response": f"Error: {str(e)}"})

    return JsonResponse({"response": "Invalid request."})
