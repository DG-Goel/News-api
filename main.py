import time
import threading
from voice_recognition import recognize_speech_from_mic
from data_fetcher import fetch_weather_data
from map_visualization import show_map  # Import show_map to display the map
from nlp_processor import process_text_command
from params_with_topic import fetch_news_datatopic
from params_without_topic import fetch_news_data

# Function to handle weather, news, and map based on voice commands
def handle_voice_command(command):
    """
    Process and handle the voice command based on user input.
    """
    # Process the text command to extract task, location, and other details
    processed_command = process_text_command(command)

    if not isinstance(processed_command, dict):
        print(f"Error processing command: {command}")
        return True  # Continue listening

    task = processed_command.get("task")
    location = processed_command.get("location")
    topic = processed_command.get("topic")

    if task == "weather":
        if location:
            print(f"Fetching weather for {location}...")
            weather_data = fetch_weather_data(command, process_text_command).get("weather")
            if weather_data:
                print(f"Weather in {location}: {weather_data}")
                show_map(location, weather_data)  # Optionally, display the map with weather info
            else:
                print(f"Could not fetch weather for {location}.")
        else:
            print("Location not specified for weather.")

    elif task == "news":
        if location:
            if topic:
                print(f"Fetching news about '{topic}' for '{location}'...")
                news_data = fetch_news_datatopic(location, topic)  # Call the correct function
            else:
                print(f"Fetching top news for '{location}'...")
                news_data = fetch_news_data(location)  # Call the correct function

            if news_data:
                print(f"News for {location}:")
                for article in news_data:
                    print(f"- {article.get('title', 'No Title')} (URL: {article.get('url', 'No URL')})")
                    print(f"Translated Text: {article.get('translated_text', 'No Translation Available')}")
                show_map(location)  # Optionally, display the map for this location
            else:
                print(f"No news articles found for {location}.")
        else:
            print("Location not specified for news.")

    elif "zoom" in command:
        if location:
            print(f"Zooming into {location} on the map...")
            show_map(location)  # Show the map with zoom for the specific location
        else:
            print("Location not specified for zoom.")

    elif "exit" in command or "quit" in command:
        print("Exiting the application...")
        return False  # Stop the loop and exit the program

    else:
        print(f"Command '{command}' not recognized. Please try again.")

    return True  # Continue listening

# Main loop to continuously listen for voice commands and process them
def start_voice_assistant():
    print("Voice Assistant is running. Speak a command...")
    while True:
        # Recognize speech from the microphone
        command = recognize_speech_from_mic()

        # If a valid command is recognized, process it
        if command:
            print(f"Received command: {command}")
            should_continue = handle_voice_command(command)

            # Exit if the command is "exit" or "quit"
            if not should_continue:
                break

        # Small delay to avoid overloading the system with too many requests
        time.sleep(1)

if __name__ == "__main__":
    # Start the voice assistant in a separate thread so that other tasks can run
    assistant_thread = threading.Thread(target=start_voice_assistant)
    assistant_thread.start()
