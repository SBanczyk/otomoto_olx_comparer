import requests
import sys
import pprint
from bs4 import BeautifulSoup


headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}


def get_otomoto_data(url):
    if "osobowe" not in url[0:40]:
        raise Exception("Tylko samochody osobowe.")
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        content = BeautifulSoup(response.content, 'html.parser')
        keys = content.find_all("p", {"class": "e1ho6mkz3 ooa-rlgnr er34gjf0"})
        values = content.find_all("p", {"class": "e1ho6mkz2 ooa-1rcllto er34gjf0"})
        car_data = {}
        car_data["Marka"] = content.find_all("h1", {"class": "ooa-1dueukt"})[0].get_text().split(" ")[0]
        car_data["Portal aukcyjny"] = "OTOMOTO"
        for key, value in zip(keys, values):
            key = key.get_text().strip()
            value = value.get_text().strip()
            if key != "Typ nadwozia":
                car_data[key] = value
        keys = content.find_all("p", {"class": "eizxi837 ooa-y26jp er34gjf0"})
        values = content.find_all("p", {"class": "eizxi838 ooa-17xeqrd er34gjf0"})
        for key, value in zip(keys, values):
            key = key.get_text().strip()
            value = value.get_text().strip()
            if key in ["Rok produkcji", "Model pojazdu"]:
                if key == "Model pojazdu":
                    key = "Model"
                car_data[key] = value

        return dict(sorted(car_data.items()))
    elif response.status_code == 404:
        raise Exception(f"Status code: {response.status_code}. Błędny link.")


def get_olx_data(url):
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        content = BeautifulSoup(response.content, 'html.parser')
        categories = []
        for category in content.find_all("a", {"class": "css-tyi2d1"}):
            categories.append(category.get_text())
        if "Samochody osobowe" not in categories:
            raise Exception("Tylko samochody osobowe.")
        keys_values = content.find_all("p", {"class": "css-b5m1rv"})
        if len(keys_values) == 0:
            raise Exception("Brak danych. Prawdopodobnie błędny link.")
        car_data = {}
        car_data["Marka"] = content.find_all("h4", {"class": "css-1kc83jo"})[0].get_text().split(" ")[0]
        car_data["Portal aukcyjny"] = "OLX"
        for key_value in keys_values:
            key_value = key_value.get_text()
            if ":" in key_value:
                key = key_value[0:key_value.find(":")].strip()
                value = key_value[key_value.find(":")+2:].strip()
                if key in ["Model", "Rok produkcji", "Przebieg", "Paliwo", "Poj. silnika", "Moc silnika", "Skrzynia biegów"]:
                    if key == "Moc silnika":
                        key = "Moc"
                    if key == "Paliwo":
                        key = "Rodzaj paliwa"
                    if key == "Poj. silnika":
                        key = "Pojemność skokowa"
                        value = value[:-1] + "3"
                    car_data[key] = value
        return dict(sorted(car_data.items()))


if __name__ == "__main__":
    comparison_dict = {}
    for i in [1, 2]:
        key = f"car_{i}"
        if "otomoto" in sys.argv[i][0:40]:
            comparison_dict[key] = get_otomoto_data(sys.argv[i])
        elif "olx" in sys.argv[i][0:40]:
            comparison_dict[key] = get_olx_data(sys.argv[i])
    pprint.pprint(comparison_dict)