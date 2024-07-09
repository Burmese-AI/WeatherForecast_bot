import os, requests
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()
WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")

def get_weather_forecast(lat, lon, action) -> str|dict:
	params = {
		"lat": lat,
		"lon": lon,
		"appid":WEATHER_API_KEY,
		"units": "imperial"
	}
	if action == "today":
		url = f"https://api.openweathermap.org/data/2.5/weather"
		try:
			response = requests.get(url, params=params)
			if response.status_code == 200:
				data = response.json()

				if data["cod"] != "404":
					weather_info = {
						"city_name": data['name'],
						"timestamp": data['dt'],
						"temp": data['main']['temp'],
						"main": data['weather'][0]["main"],
						"desc": data['weather'][0]['description'],
						"wind_speed": data['wind']['speed']
					}
					return weather_info
				else:
					return " City Not Found! "
		except requests.RequestException as e:
			return f"Error fetching weather API: {e}"
	
	elif action == "forecast":
		url = f"https://api.openweathermap.org/data/2.5/forecast"
		params["cnt"] = 7
		try:
			response = requests.get(url, params=params)
			if response.status_code == 200:
				data = response.json()

				if data["cod"] != "404":
					weather_info = {
						"city_name": data['city']['name'],
						"timezone": data['city']['timezone'],
						'weather_list': data["list"]
					}
					return weather_info
				else:
					return " City Not Found! "
		except requests.RequestException as e:
			return f"Error fection weather API from APP: {e}"
	
	else:
		return "We can't find your Location. Please check your location info and try again!"

def format_weather_info(weather_info)-> str:
	if isinstance(weather_info, str):
		return weather_info
	
	if "weather_list" in weather_info:
		formatted_info = f"Weather Forecast for {weather_info['city_name']}: \n"
		for day in weather_info['weather_list']:
			date = datetime.fromtimestamp(day['dt']).strftime('%d - %m - %Y')
			temp = day['main']['temp']
			weather_main = day['weather'][0]['main']
			weather_desc = day['weather'][0]['description']
			wind_speed = day['wind']['speed']

			formatted_info += (
				f"\nDate: {date}\n"
				f"Temperature: {temp} °F\n"
				f"Weather: {weather_main} - {weather_desc}\n"
				f"Wind Speed: {wind_speed} mph\n"
			)

	else:
		formatted_info = (
			f"Weather Forecast for {weather_info['city_name']}:\n"
			f"\nDate: {datetime.fromtimestamp(weather_info['timestamp']).strftime('%d - %m - %Y')}\n"
			f"Temperature: {weather_info['temp']} °F\n"
			f"Weather: {weather_info['main']} - {weather_info['desc']}\n"
			f"Wind Speed: {weather_info['wind_speed']} mph\n"
		)

	return formatted_info