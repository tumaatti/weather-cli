#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from api_key import API_KEY

import argparse
import datetime
import json
import httpx


def main():
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

    req = httpx.get(url)
    if req.status_code != 200:
        print(
            "API didn't return anything. Did you type the city name correctly?"
        )
        return 1
    dumps = json.loads(req.text)

    lon = dumps['coord']['lon']
    lat = dumps['coord']['lat']
    desc = dumps['weather'][0]['description']
    temp = dumps['main']['temp']
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
        f"weather in {city}, {country}\n"
        f"  {temp} °C \n"
        f"  {wind} m/s\n"
        f"  {desc}\n\n"
        f"  sunrise: {sunrise[:-3]}\n"
        f"  sunset:  {sunset[:-3]}\n"
    )

    one_call_url = f'https://api.openweathermap.org/data/2.5/onecall?lat={lat}&lon={lon}&exclude=minutely,hourly&appid={API_KEY}&units=metric'  # noqa: E501
    req = httpx.get(one_call_url)
    if req.status_code != 200:
        print(
            "API didn't return anything. Did you type the city name correctly?"
        )
        return 1
    dumps = json.loads(req.text)

    # in daily forecast the 0th day is today
    tomorrow_json = dumps['daily'][0]
    temp_morn = tomorrow_json['temp']['morn']
    temp_day = tomorrow_json['temp']['day']
    temp_eve = tomorrow_json['temp']['eve']
    temp_night = tomorrow_json['temp']['night']
    weather_desc = tomorrow_json['weather'][0]['description']
    wind_speed = tomorrow_json['wind_speed']
    day, sunrise = str(
        datetime.datetime.fromtimestamp(int(tomorrow_json['sunrise']))
    ).split()
    _, sunset = str(
        datetime.datetime.fromtimestamp(int(tomorrow_json['sunset']))
    ).split()

    print(
        f"weather for tomorrow:\n"
        f"  morning:  {temp_morn} °C\n"
        f"  day:      {temp_day} °C\n"
        f"  evening:  {temp_eve} °C\n"
        f"  night:    {temp_night} °C\n\n"
        f" {wind_speed} m/s\n"
        f" {weather_desc}\n\n"
        f" sunrise: {sunrise[:-3]}\n"
        f" sunset:  {sunset[:-3]}\n"
    )


if __name__ == '__main__':
    main()
