import requests
import sys
import pprint
from bs4 import BeautifulSoup


headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}


def clean_value(str_value):
    if " cm3" in str_value or " km" in str_value or " KM" in str_value or str_value.isnumeric():
        clean_str = str_value.replace(" km", "").replace(" cm3", "").replace(" KM", "").replace(" ", "")
        return int(clean_str)
    return str_value


def get_otomoto_data(url):
    if "osobowe" not in url[0:40]:
        raise Exception("Tylko samochody osobowe.")
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        car_data = {}
        car_data["Portal aukcyjny"] = "OTOMOTO"
        content = BeautifulSoup(response.content, 'html.parser')
        car_data["Marka"] = content.find_all("h1", {"class": "ooa-1dueukt"})[0].get_text().split(" ")[0]
        properties = content.find_all("p", {"class": "e1ho6mkz3 ooa-rlgnr er34gjf0"})
        values = content.find_all("p", {"class": "e1ho6mkz2 ooa-1rcllto er34gjf0"})
        for property, value in zip(properties, values):
            property = property.get_text().strip()
            value = value.get_text().strip()
            if property != "Typ nadwozia":
                car_data[property] = clean_value(value)
        properties = content.find_all("p", {"class": "eizxi837 ooa-y26jp er34gjf0"})
        values = content.find_all("p", {"class": "eizxi838 ooa-17xeqrd er34gjf0"})
        for property, value in zip(properties, values):
            property = property.get_text().strip()
            value = value.get_text().strip()
            if property in ["Rok produkcji", "Model pojazdu"]:
                if property == "Model pojazdu":
                    property = "Model"
                car_data[property] = clean_value(value)

        return dict(sorted(car_data.items()))
    elif response.status_code == 404:
        raise Exception(f"Status code: {response.status_code}. Błędny link.")


def get_olx_data(url):
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        content = BeautifulSoup(response.content, 'html.parser')
        is_passenger_car = False
        for category in content.find_all("a", {"class": "css-tyi2d1"}):
            if category.get_text() == "Samochody osobowe":
                is_passenger_car = True
                break
        if not is_passenger_car:
            raise Exception("Tylko samochody osobowe.")
        properties_values = content.find_all("p", {"class": "css-b5m1rv"})
        if len(properties_values) == 0:
            raise Exception("Brak danych. Prawdopodobnie błędny link.")
        car_data = {}
        car_data["Marka"] = content.find_all("h4", {"class": "css-1kc83jo"})[0].get_text().split(" ")[0]
        car_data["Portal aukcyjny"] = "OLX"
        for property_value in properties_values:
            property_value = property_value.get_text()
            if ":" in property_value:
                property = property_value[0:property_value.find(":")].strip()
                value = property_value[property_value.find(":")+2:].strip()
                if property in ["Model", "Rok produkcji", "Przebieg", "Paliwo", "Poj. silnika", "Moc silnika", "Skrzynia biegów"]:
                    if property == "Moc silnika":
                        property = "Moc"
                    if property == "Paliwo":
                        property = "Rodzaj paliwa"
                    if property == "Poj. silnika":
                        property = "Pojemność skokowa"
                        value = value[:-1] + "3"
                    car_data[property] = clean_value(value)
        return dict(sorted(car_data.items()))


def get_comparison_data(url_1, url_2):
    comparison_dictionary = {}
    for i in [1, 2]:
        car_number = f"car_{i}"
        url = url_1 if i == 1 else url_2
        if "otomoto" in url[0:40]:
            comparison_dictionary[car_number] = get_otomoto_data(url)
        elif "olx" in url[0:40]:
            comparison_dictionary[car_number] = get_olx_data(url)
    return comparison_dictionary


if __name__ == "__main__":
    if len(sys.argv) != 3:
        pprint.pprint("Usage: python get_data.py <url_1> <url_2>")
    else:
        pprint.pprint(get_comparison_data(sys.argv[1], sys.argv[2]))
