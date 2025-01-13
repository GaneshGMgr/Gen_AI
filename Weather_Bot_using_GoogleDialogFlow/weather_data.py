from app_logger.logger import logger
from dialogflow import create_query_result 
from app_exception.exception import AppException
import pyowm  # Used for fetching weather data from the OpenWeatherMap API.
import sys
from dotenv import load_dotenv
import os
import pytz
from datetime import datetime, timedelta 
import requests
import time

load_dotenv()
OpenWeatherMap = os.getenv("WEATHER_API_KEY")

class WeatherData:
    def __init__(self):
        self.owmapikey = OpenWeatherMap  # OpenWeatherMap API key
        self.owm = pyowm.OWM(self.owmapikey)

    def processRequest(self, req):
        try:
            city_name = req.get("city", "")

            if not city_name:
                raise ValueError("City name is required")
            
            query_result = create_query_result(city_name)

            self.result = query_result.get("queryResult")
            self.parameters = self.result.get("parameters")
            self.city = self.parameters.get("city_name")  # City name input by the user

            # Fetch weather data for the city
            weather_manager = self.owm.weather_manager()
            self.observation = weather_manager.weather_at_place(str(self.city))  # Get weather data for the city
            weather = self.observation.weather  # Access weather details directly
            self.latlon_res = self.observation.location  # Latitude and Longitude of the city

            # Fetch and store additional weather details
            self.weather_condition = weather.status  # Weather condition (e.g., Clear, Rainy)
            self.cloudiness = str(weather.clouds)  # Cloud coverage in percentage
            self.pressure = str(weather.pressure['press'])  # Atmospheric pressure (hPa)
            self.rain = weather.rain  # Rainfall in the last hour (mm)
            self.snow = weather.snow  # Snowfall in the last hour (mm)
            obs = weather_manager.weather_at_place(str(self.city))
            self.visibility = obs.weather.visibility()  # Visibility (in  kilometers)
            self.icon = weather.weather_icon_name  # Weather icon (e.g., sun, clouds)
            self.wind_speed = str(weather.wind()['speed'])  # Wind speed (km/h)
            self.feels_like_temp = str(weather.temperature('celsius')['feels_like'])  # Feels like temperature (°C)
            self.temp_min = str(weather.temperature('celsius')['temp_min'])  # Min temperature (°C)
            self.temp_max = str(weather.temperature('celsius')['temp_max'])  # Max temperature (°C)

            # Get latitude and longitude of the city
            latitude = self.latlon_res.lat
            longitude = self.latlon_res.lon

            # Fetch the timezone data using OpenWeatherMap's Timezone API
            timezone_url = f"http://api.openweathermap.org/data/2.5/timezone?lat={latitude}&lon={longitude}&appid={self.owmapikey}"
            timezone_response = requests.get(timezone_url)
            timezone_data = timezone_response.json()
            timezone_offset = timezone_data.get("offset", 0)  # Timezone offset in seconds from UTC

            # Fetch current time based on city timezone offset
            current_time_utc = datetime.utcnow()
            city_time = current_time_utc + timedelta(seconds=timezone_offset)

            # Format the city time and date
            city_time_str = city_time.strftime('%Y-%m-%d %H:%M:%S')

            # Fetch sunrise and sunset time from the weather object (in Unix timestamp)
            sunrise_time = weather.sunrise_time()  # Sunrise time (Unix timestamp)
            sunset_time = weather.sunset_time()  # Sunset time (Unix timestamp)

            # Convert sunrise and sunset from Unix timestamp to human-readable format
            sunrise_time = time.strftime('%H:%M:%S', time.gmtime(int(sunrise_time)))
            sunset_time = time.strftime('%H:%M:%S', time.gmtime(int(sunset_time)))

            # Gracefully handle the cases where there is no rain or snow
            rain_info = self.rain.get('1h', 'No rain') if self.rain else 'No rain'
            snow_info = self.snow.get('1h', 'No snow') if self.snow else 'No snow'

            # Prepare the speech response
            speech = (
                f"Here's the weather update for {self.city}: "
                f"Currently, it's {self.weather_condition} with {self.cloudiness}% cloud cover. "
                f"The pressure is {self.pressure} hPa, and the wind is at {self.wind_speed} km/h. "
                f"It feels like {self.feels_like_temp}°C, and visibility is {self.visibility} meters. "
                f"Sunrise was at {sunrise_time}, and sunset will be at {sunset_time}. "
                f"We've had {rain_info} rain and {snow_info} snow. "
                f"The temperature ranges from {self.temp_min}°C to {self.temp_max}°C. "
                f"The current date and time in {self.city} is {city_time_str}."
            )

            # Now include all this information in the return dictionary as well
            return {
                "fulfillmentText": speech,  # Text response for speech
                "displayText": speech,     # Display text response
                "city": self.city,
                "latitude": latitude,
                "longitude": longitude,
                "weather_condition": self.weather_condition,
                "cloudiness": self.cloudiness,
                "pressure": self.pressure,
                "wind_speed": self.wind_speed,
                "temperature": self.feels_like_temp,
                "visibility": self.visibility,
                "temp_min": self.temp_min,
                "temp_max": self.temp_max,
                "sunrise": sunrise_time,
                "sunset": sunset_time,
                "rain": rain_info,
                "snow": snow_info,
                "icon": f"http://openweathermap.org/img/wn/{self.icon}.png",  # Icon URL for frontend
                "city_time": city_time_str,  # Add the city time in the response
                "speech": speech
            }

        except Exception as e:
            raise AppException(e, sys) from e