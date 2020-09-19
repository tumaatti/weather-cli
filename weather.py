#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import json
import requests
from api_key import API_KEY

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
print(
    f"{dumps['weather'][0]['description']}, {dumps['main']['temp']} °C in "
    f"{dumps['name']}, {dumps['sys']['country']}"
)
