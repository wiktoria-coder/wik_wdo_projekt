import requests
from bs4 import BeautifulSoup
import re

class CoordinateFetcher:
    def __init__(self, location: str):
        self.location = location

    def get_coordinates(self) -> list:
        """
        Pobiera współrzędne geograficzne (szerokość i długość) dla lokalizacji
        z polskiej Wikipedii. Obsługuje format dziesiętny oraz DMS.
        """
        address_url: str = f"https://pl.wikipedia.org/wiki/{self.location}"
        try:
            response = requests.get(address_url, timeout=5).text
            response_html = BeautifulSoup(response, "html.parser")

            lat_tags = response_html.select(".latitude")
            lon_tags = response_html.select(".longitude")

            if not lat_tags or not lon_tags:
                raise Exception("Brak współrzędnych na stronie.")

            latitude_raw = lat_tags[-1].text  # ostatni zestaw (najbardziej szczegółowy)
            longitude_raw = lon_tags[-1].text

            latitude = self._convert_to_float(latitude_raw)
            longitude = self._convert_to_float(longitude_raw)

            return [latitude, longitude]
        except Exception as e:
            print(f"Błąd pobierania współrzędnych dla '{self.location}': {e}")
            return None

    def _convert_to_float(self, value: str) -> float:
        """
        Konwertuje wartość współrzędnej z formatu dziesiętnego lub DMS na float.
        """
        # Próbuj konwersji dziesiętnej
        try:
            return float(value.replace(",", "."))
        except ValueError:
            pass

        # Jeśli się nie udało – spróbuj z formatu DMS (np. 52°13′56″N)
        match = re.match(r"(\d+)°(\d+)′(\d+)″([NSEW])", value)
        if not match:
            raise ValueError("Niepoprawny format współrzędnej: " + value)

        degrees, minutes, seconds, direction = match.groups()
        decimal = float(degrees) + float(minutes) / 60 + float(seconds) / 3600
        if direction in ['S', 'W']:
            decimal *= -1
        return decimal
