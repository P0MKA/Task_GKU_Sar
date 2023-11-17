import requests
from bs4 import BeautifulSoup


class Parser:
    CITIES_COUNT = 20

    def __init__(self):
        self.cities = []

    def get_cities(self):
        url = 'https://www.worldatlas.com/cities/10-largest-cities-in-the-world.html'
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        cities = [city.select('td')[1].text.strip() for city in soup.select('tr')[1:1 + self.CITIES_COUNT]]
        self.cities = cities

    def get_weather(self):
        pass


class ExcelWriter(Parser):
    def save_weather(self):
        pass


if __name__ == '__main__':
    parser = Parser()
    parser.get_cities()