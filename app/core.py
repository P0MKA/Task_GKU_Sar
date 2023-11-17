import os
import json
from typing import List

import requests
import pandas as pd
from bs4 import BeautifulSoup
from dotenv import load_dotenv

from app.writers import DBWriter, ExcelWriter
from app.consts import CITIES_COUNT

load_dotenv()

API_KEY = os.getenv('API_KEY')


class Parser:
    def __init__(self):
        self.cities = []
        self.data = pd.DataFrame()

    def get_cities(self) -> list[str]:
        url = 'https://www.worldatlas.com/cities/10-largest-cities-in-the-world.html'
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        cities = [city.select('td')[1].text.strip() for city in soup.select('tr')[1:1 + CITIES_COUNT]]
        self.cities = cities
        return cities

    def get_weather_data(self, city: str) -> None:
        location_url = f'http://api.openweathermap.org/geo/1.0/direct?q={city}&limit=1&appid={API_KEY}'

        try:
            location_response = requests.get(location_url)
            location = json.loads(location_response.text)[0]
        except Exception as e:
            print(f'Не удалось получить координаты города {city}\n{e}')
        else:
            weather_url = (f'https://api.openweathermap.org/data/2.5/forecast?'
                           f'lat={location.get("lat")}&lon={location.get("lon")}&'
                           f'lang=ru&cnt=24&units=metric&appid={API_KEY}')
            try:
                response = requests.get(weather_url)
                raw_weather_data = json.loads(response.text).get('list')[::8]
            except Exception as e:
                print(f'Не удалось получить данные о погоде для города {city}\n{e}')
            else:
                self._clean_weather_data(raw_weather_data, city)

    def _clean_weather_data(self, weather_data: List[dict], city: str) -> None:
        for chunk in weather_data:
            item = {
                'Город': [city],
                'Температура': [chunk['main']['temp']],
                'Влажность': [chunk['main']['humidity']],
                'Давление': [chunk['main']['pressure']],
                'Погода': [chunk['weather'][0]['description']],
                'Скорость ветра': [chunk['wind']['speed']],
                'Дата': [chunk['dt_txt']],
            }
            df = pd.DataFrame(item)
            if not self.data.empty:
                self.data = pd.concat([self.data, df])
            else:
                self.data = df

    def get_weather(self):
        for city in self.get_cities():
            self.get_weather_data(city)


class WeatherForecast(Parser):
    def __init__(self):
        super().__init__()
        self.writers = [DBWriter, ExcelWriter]

    def save_weather_data(self):
        for writer in self.writers:
            if not self.data.empty:
                writer.save_weather(self.data)


if __name__ == '__main__':
    parser = WeatherForecast()
    parser.get_weather()
    parser.save_weather_data()