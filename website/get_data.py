import requests
import sys
import os
from bs4 import BeautifulSoup
from dotenv import load_dotenv


load_dotenv()
headers = {'User-Agent': os.getenv('USER-AGENT')}


def clean_value(str_value):
    if " cm3" in str_value or " km" in str_value or " KM" in str_value or str_value.replace(" ", "").isnumeric():
        clean_str = str_value.replace(" km", "").replace(" cm3", "").replace(" KM", "").replace(" ", "")
        return int(clean_str)
    return str_value


def get_otomoto_data(url):
    if "osobowe" not in url[0:40]:
        raise ValueError
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        car_data = {}
        car_data['website'] = "OTOMOTO"
        content = BeautifulSoup(response.content, 'html.parser')
        car_data['price'] = clean_value(content.find_all("h3", {"class": "ooa-1kdys7g"})[0].get_text())
        car_data['currency'] = content.find_all("p", {"class": "ooa-m6bn4u"})[0].get_text()
        car_data['brand'] = content.find_all("h1", {"class": "ooa-1dueukt"})[0].get_text().split(" ")[0]
        properties = content.find_all("p", {"class": "ee3fiwr3 ooa-rlgnr er34gjf0"})
        values = content.find_all("p", {"class": "ee3fiwr2 ooa-1rcllto er34gjf0"})
        for property, value in zip(properties, values):
            property = property.get_text().strip()
            value = value.get_text().strip()
            if property != "Typ nadwozia":
                if property == "Moc":
                    car_data['power'] = clean_value(value)
                elif property == "Pojemność skokowa":
                    car_data['engine_size'] = clean_value(value)
                elif property == "Przebieg":
                    car_data['mileage'] = clean_value(value)
                elif property == "Rodzaj paliwa":
                    car_data['fuel'] = clean_value(value)
                elif property == "Skrzynia biegów":
                    car_data['gearbox'] = clean_value(value)

                
        properties = content.find_all("p", {"class": "eim4snj7 ooa-y26jp er34gjf0"})
        values = content.find_all("p", {"class": "eim4snj8 ooa-17xeqrd er34gjf0"})
        for property, value in zip(properties, values):
            property = property.get_text().strip()
            value = value.get_text().strip()
            if property in ["Rok produkcji", "Model pojazdu"]:
                if property == "Model pojazdu":
                    car_data['model'] = clean_value(value)
                if property == "Rok produkcji":
                    car_data['year'] = clean_value(value)
        order = ['brand', 'model', 'year', 'fuel', 'engine_size', 'power', 'gearbox', 'mileage', 'price', 'currency', 'website']
        return {key: car_data[key] for key in order}
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
            raise ValueError
        properties_values = content.find_all("p", {"class": "css-b5m1rv"})
        if len(properties_values) == 0:
            raise Exception("No data.")
        car_data = {}
        car_data['website'] = "OLX"
        car_data['price'] = clean_value(content.find_all("h3", {"class": "css-90xrc0"})[0].get_text()[:-3])
        car_data['currency'] = content.find_all("h3", {"class": "css-90xrc0"})[0].get_text()[-2:]
        car_data['brand'] = content.find_all("h4", {"class": "css-1kc83jo"})[0].get_text().split(" ")[0]
        for property_value in properties_values:
            property_value = property_value.get_text()
            if ":" in property_value:
                property = property_value[0:property_value.find(":")].strip()
                value = property_value[property_value.find(":")+2:].strip()
                if property in ["Model", "Rok produkcji", "Przebieg", "Paliwo", "Poj. silnika", "Moc silnika", "Skrzynia biegów"]:
                    if property == "Moc silnika":
                        car_data['power'] = clean_value(value)
                    elif property == "Model":
                        car_data['model'] = clean_value(value)
                    elif property == "Paliwo":
                        car_data['fuel'] = clean_value(value)
                    elif property == "Poj. silnika":
                        value = value[:-1] + "3"
                        car_data['engine_size'] = clean_value(value)
                    elif property == "Przebieg":
                        car_data['mileage'] = clean_value(value)
                    elif property == "Rok produkcji":
                        car_data['year'] = clean_value(value)
                    elif property == "Skrzynia biegów":
                        car_data['gearbox'] = clean_value(value)

        order = ['brand', 'model', 'year', 'fuel', 'engine_size', 'power', 'gearbox', 'mileage', 'price', 'currency', 'website']
        return {key: car_data[key] for key in order}


def get_comparison_data(url_1, url_2):
    comparison_dictionary = {}
    for i in [1, 2]:
        car_number = f"car_{i}"
        url = url_1 if i == 1 else url_2
        if "otomoto" in url[0:40]:
            comparison_dictionary[car_number] = get_otomoto_data(url)
        elif "olx" in url[0:40]:
            comparison_dictionary[car_number] = get_olx_data(url)
    if 'car_1' in comparison_dictionary and 'car_2' in comparison_dictionary:
        return comparison_dictionary
    else:
        raise ValueError


if __name__ == "__main__":
    print(get_comparison_data(sys.argv[1], sys.argv[2]))
