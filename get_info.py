import requests
import urllib.parse
import os 
from datetime import date
import time

this_file_path = os.path.realpath(__file__)

weather_location = open(this_file_path[:-11]+'weather/location.info', "r").read()
weather_token    = open(this_file_path[:-11]+"weather/token.info", "r").read()

url_weather = f'https://api.openweathermap.org/data/2.5/weather?q={weather_location}&appid={weather_token}&units=metric'.replace('\n','')
weather = requests.get(url_weather).json()['weather'][0]['main']

if weather == 'Thunderstorm':
    weather = 'Rain'
elif weather == 'Drizzle':
    weather = 'Rain'
elif weather == 'Atmosphere':
    weather = 'Clouds'
    
today = date.today()
day   = today.strftime("%d")
month = today.strftime("%m")
weekdays = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
week  = today.weekday()
hour  = int(time.strftime("%H", time.localtime()))

if   hour >= 3 and hour < 9:
    TOD = '0'
elif hour >= 9 and hour < 13:
    TOD = '1'
elif hour >= 13 and hour < 16:
    TOD = '2'
elif hour >= 16 and hour < 19:
    TOD = '3'
else:
    TOD = '4'

print(day,month,weekdays[week], TOD, weather)
