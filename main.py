"""Real-Time Weather Detection  Application"""
#Author: Busi Indu
#TODO: Flipkart Internship Task
import requests # To call OpenWeatherMap API
import os
import csv 
from datetime import datetime 

class WeatherApp:# To fetch and display weather
   
    def request_weather(city):
        """Request weather from OpenWeatherMap and return parsed JSON on success.

        Returns the JSON dict on success, or None on error. Prints a helpful message on failure.
        """
        my_api_key = "68fac3c9f89baf92f3af70102fb296c2"   # API key for OpenWeatherMap
        url = "https://api.openweathermap.org/data/2.5/weather"  # Base URL for fetching weather data

        values = {                             # These are the values we send to the API in the URL — like city name, API key, and units.
                "q": city,
                "appid": my_api_key,
                "units": "metric",
        }

        try:
            resp = requests.get(url, params=values)
        except Exception as e:                 # Handle any kind of  error to prevent the program from crashing
            print("\n Error contacting OpenWeather:", e)
            return None

        if resp.status_code == 200:# Successful API response
            try:
                return resp.json() # Return data in JSON format
            except Exception as e:
                print("\n Error parsing response:", e)
                return None
        elif resp.status_code == 404:
            print("\n City not found")
        elif resp.status_code == 500:  # OpenWeatherMap server error
            print("\n Server error at OpenWeatherMap")
        else:
            print("\n City not found or API error")
        return None

    def weather_info(city):
        """Print human-readable weather info for city using the shared request method."""
        data = WeatherApp.request_weather(city)
        if not data:
            return
        print(f"\nWeather in {city.title()}:")  # Displays the city name
        print(f" Temperature: {data['main']['temp']}°C")  # Displays temperature
        print(f" Feels Like: {data['main']['feels_like']}°C")  # Displays feels like temperature 
        print(f" Condition: {data['weather'][0]['description'].capitalize()}")   # Displays weather condition
        print(f" Humidity: {data['main']['humidity']}%")  # Displays humidity
        print(f" Wind Speed: {data['wind']['speed']} m/s")   # Displays wind speed

class Storage:
        # Storing Weather data in CSV file
    def store_weather_data(city):
        try:
            data = WeatherApp.request_weather(city)
            if not data:
                return

            city_name = data["name"]    # Get the city name from the response
            country = data["sys"]["country"]   # Get the country code from the response
            temperature = data["main"]["temp"]    # Get the temperature from the response
            feels_like = data["main"]["feels_like"]   # Get the 'feels like' temperature from the response
            humidity = data["main"]["humidity"]    # Get the humidity value from the response
            condition = data["weather"][0]["description"].capitalize()    # Get the weather condition from the response
            wind_speed = data["wind"]["speed"]    # Get the wind speed from the response


            filename = "weather_data.csv"    # Name of the CSV file used to save weather data
            file_exists = os.path.isfile(filename)    # Check whether the CSV file already exists
            with open(filename, mode="a", newline="", encoding='utf-8') as file:    # Open file for adding data
                writer = csv.writer(file)    # Create a CSV writer to add data into the file
                if not file_exists:    # If the file doesn't exist, write the header
                    writer.writerow(
                        [
                            "Timestamp",
                            "City",
                            "Country",
                            "Temperature (°C)",
                            "Feels Like (°C)",
                            "Humidity (%)",
                            "Condition",
                            "Wind Speed (m/s)"
                            ]
                            )   # Insert the header row into the CSV file
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                writer.writerow([timestamp, city_name, country, temperature, feels_like, humidity, condition, wind_speed])  # Write the fetched weather data to the CSV file


            print(f"\n Weather data for {city_name} stored in {filename}")
        except Exception as e:
            print("\n Error:", str(e))
        
def main():
    city = input("Enter City: ") # Get city name from user
    WeatherApp.weather_info(city) # Call the function to get weather
    Storage.store_weather_data(city)   # Call the function to save the weather data to the CSV file

if __name__ == "__main__":
    main()