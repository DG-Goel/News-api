from params_with_topic import fetch_news_datatopic
from params_without_topic import fetch_news_data
import requests

# Constants for Weather API
WEATHER_API_URL = "http://api.openweathermap.org/data/2.5/weather"
WEATHER_API_KEY = "39e1b1ea2b3798a7f1f3f62213768746"  # Replace with your valid API key
'''
# Function to fetch weather data
def fetch_weather_data(location):
    """
    Fetches the current weather data for a given location.
    """
    params = {
        "q": location,
        "appid": WEATHER_API_KEY,
        "units": "metric"
    }

    try:
        response = requests.get(WEATHER_API_URL, params=params)
        response.raise_for_status()
        data = response.json()

        if data.get("cod") != 200:
            print("Error fetching weather:", data.get("message", "Unknown error"))
            return {}

        return {
            "location": location,
            "temperature": data["main"]["temp"],
            "condition": data["weather"][0]["description"],
            "humidity": data["main"]["humidity"],
            "wind_speed": data["wind"]["speed"]
        }

    except requests.RequestException as e:
        print(f"Error fetching weather: {e}")
        return {}'''
def fetch_weather_data(location):
    params = {
        "q": location,
        "appid": WEATHER_API_KEY,
        "units": "metric"
    }

    try:
        response = requests.get(WEATHER_API_URL, params=params)
        response.raise_for_status()
        data = response.json()

        # If the response does not contain valid weather data
        if data.get("cod") != 200:
            print(f"Error fetching weather for {location}: {data.get('message')}")
            return None

        return {
            "location": location,
            "temperature": data["main"]["temp"],
            "condition": data["weather"][0]["description"],
            "humidity": data["main"]["humidity"],
            "wind_speed": data["wind"]["speed"]
        }

    except requests.RequestException as e:
        print(f"Error fetching weather data: {e}")
        return None

# Main Data Fetcher
def data_fetcher(user_input, process_command_function):
    """
    Main function to decide and fetch data based on user input.
    """
    # Use the provided `process_text_command` function to analyze input
    command = process_command_function(user_input)

    task = command["task"]
    location = command["location"]
    topic = command["topic"]

    if task == "weather":
        if location:
            print(f"Fetching weather for {location}")
            return {"weather": fetch_weather_data(location)}
        else:
            print("Location not specified for weather.")
            return {"error": "Please provide a location for weather information."}

    elif task == "news":
        if topic:
            print(f"Fetching news about '{topic}' for '{location}'")
            return {"news": fetch_news_datatopic(location, topic)}
        else:
            print(f"Fetching top news for '{location}'")
            return {"news": fetch_news_data(location)}

    else:
        return {"error": "Unable to determine the task from input."}

