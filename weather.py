#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from api_key import API_KEY

import argparse
import datetime
import json
import requests

parser = argparse.ArgumentParser(
    description='Get weather information for a city'
)
parser.add_argument('city_name', type=str, help='Specify the city name')
parser.add_argument('--country_code',
                    type=str,
                    help='Use this if the country code is incorrect')

args = parser.parse_args()

if not args.country_code:
    url = f'http://api.openweathermap.org/data/2.5/weather?q={args.city_name}&APPID={API_KEY}&units=metric'  # noqa: E501
else:
    url = f'http://api.openweathermap.org/data/2.5/weather?q={args.city_name},{args.country_code}&APPID={API_KEY}&units=metric'  # noqa: E501
req = requests.get(url)

dumps = json.loads(req.text)

desc = dumps['weather'][0]['description']
temp = dumps['main']['temp']
temp_min = dumps['main']['temp_min']
temp_max = dumps['main']['temp_max']
city = dumps['name'].lower()
country = dumps['sys']['country'].lower()
wind = dumps['wind']['speed']

_, sunrise = str(
    datetime.datetime.fromtimestamp(int(dumps['sys']['sunrise']))
).split(' ')

_, sunset = str(
    datetime.datetime.fromtimestamp(int(dumps['sys']['sunset']))
).split(' ')

print(
    f" {city}, {country}\n\n"
    f" {temp} °C ({temp_min} - {temp_max} °C)\n"
    f" {wind} m/s\n"
    f" {desc}\n\n"
    f" sunrise: {sunrise[:-3]}\n"
    f" sunset:  {sunset[:-3]}\n"
)
