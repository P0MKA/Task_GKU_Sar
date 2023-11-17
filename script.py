from app.core import WeatherForecast


def parse():
    parser = WeatherForecast()
    parser.get_weather()
    parser.save_weather_data()


if __name__ == "__main__":
    parse()
