from app.core import ExcelWriter


def parse():
    writer = ExcelWriter()
    writer.get_cities()
    writer.save_weather()


if __name__ == "__main__":
    parse()
