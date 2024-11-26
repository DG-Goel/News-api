import speech_recognition as sr
import time

# Initialize the recognizer
recognizer = sr.Recognizer()

# Function to listen to the microphone and recognize speech
def recognize_speech_from_mic():
    """
    Listens to the microphone and converts speech to text using Google Web Speech API.
    """
    with sr.Microphone() as source:
        print("Adjusting for ambient noise... Please wait.")
        recognizer.adjust_for_ambient_noise(source)  # Adjust for ambient noise
        print("Listening... Please speak now.")
        audio = recognizer.listen(source)

    try:
        # Recognize speech using Google's Web Speech API
        print("Recognizing...")
        text = recognizer.recognize_google(audio)
        print(f"Recognized text: {text}")
        return text
    except sr.UnknownValueError:
        # If speech is unintelligible
        print("Sorry, I could not understand the audio.")
        return None
    except sr.RequestError as e:
        # If there is an issue with the API
        print(f"Error with the speech recognition service: {e}")
        return None

# Function to process speech command
def process_command(command):
    """
    Process the voice command to determine the task (e.g., weather, news).
    """
    if command:
        command = command.lower()

        # Check for specific commands
        if "weather" in command:
            print("You asked for weather information.")
            # Add weather-related functionality here (e.g., fetch weather data)
            return "weather"
        elif "news" in command:
            print("You asked for news information.")
            # Add news-related functionality here (e.g., fetch news articles)
            return "news"
        elif "zoom" in command:
            print("You asked to zoom on a location.")
            # Add functionality for zooming on a map
            return "zoom"
        elif "exit" in command or "quit" in command:
            print("Exiting the voice assistant.")
            return "exit"  # Exit the program
        else:
            print(f"Unrecognized command: {command}")
            return "unrecognized"
    return "empty"  # Case where the command is empty

# Function to run the voice assistant
def run_voice_assistant():
    """
    Continuously listen for commands and process them.
    """
    print("Voice Assistant is now running. Say 'exit' or 'quit' to stop.")
    
    while True:
        command = recognize_speech_from_mic()

        # Process the command
        result = process_command(command)

        if result == "exit":
            print("Goodbye!")
            break  # Exit the loop if the command is to exit
        elif result == "weather":
            print("Fetching weather information...")
            # Call the weather function here
        elif result == "news":
            print("Fetching news information...")
            # Call the news function here
        elif result == "zoom":
            print("Zooming into the location...")
            # Call the zoom function here
        elif result == "unrecognized":
            print("Sorry, I couldn't recognize the command. Please try again.")
        elif result == "empty":
            print("No command received. Please try again.")
        
        # Optional: Add a delay before the next command is listened for
        time.sleep(1)

if __name__ == "__main__":
    # Start the voice assistant
    run_voice_assistant()
