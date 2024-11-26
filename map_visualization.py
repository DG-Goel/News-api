import folium
from geopy.geocoders import Nominatim
import webbrowser
import os
import time

# Function to get coordinates from location name
def get_location_coordinates(location_name):
    geolocator = Nominatim(user_agent="news_weather_app")
    location = geolocator.geocode(location_name)
    if location:
        return (location.latitude, location.longitude)
    else:
        print(f"Could not find coordinates for {location_name}")
        return None

# Function to create and display the map (instead of saving it as a file)
def create_map(location_name, weather_data=None, zoom_start=12):
    coordinates = get_location_coordinates(location_name)
    
    if coordinates:
        location_map = folium.Map(location=coordinates, zoom_start=zoom_start)

        # Create popup content
        popup_content = f"<b>{location_name}</b><br>"
        if weather_data:
            popup_content += f"Temperature: {weather_data['temperature']}°C<br>"
            popup_content += f"Condition: {weather_data['condition']}<br>"
            popup_content += f"Humidity: {weather_data['humidity']}%<br>"
            popup_content += f"Wind Speed: {weather_data['wind_speed']} m/s"
        
        # Add a marker at the location with weather info in the popup
        folium.Marker(location=coordinates, popup=popup_content).add_to(location_map)

        # Save the map as an HTML file in a temporary location
        temp_file = "temp_map.html"
        location_map.save(temp_file)
        
        # Wait a bit to ensure the file is saved before opening
        time.sleep(1)

        # Check if the map file exists
        if os.path.exists(temp_file):
            # Open the map in the default web browser
            print(f"Opening map for {location_name}...")
            webbrowser.open('file://' + os.path.realpath(temp_file))
        else:
            print("Error: Could not create the map file.")
    else:
        print("Could not create map due to location fetch error.")

# Wrapper function to be called from main.py
def show_map(location_name, weather_data=None):
    create_map(location_name, weather_data)
