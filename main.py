import requests
import sys
from bs4 import BeautifulSoup


headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}

def get_otomoto_data(url):
    if "osobowe" not in url[0:40]:
        raise Exception("Tylko samochody osobowe.")
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        keys = soup.find_all("p", {"class": "eizxi837 ooa-y26jp er34gjf0"})
        values = soup.find_all("p", {"class": "eizxi838 ooa-17xeqrd er34gjf0"})
        car_data = {}
        for key, value in zip(keys, values):
            car_data[key.get_text()] = value.get_text()
        keys = soup.find_all("p", {"class": "e1ho6mkz3 ooa-rlgnr er34gjf0"})
        values = soup.find_all("p", {"class": "e1ho6mkz2 ooa-1rcllto er34gjf0"})
        for key, value in zip(keys, values):
            car_data[key.get_text()] = value.get_text()
    elif response.status_code == 404:
        raise Exception(f"Status code: {response.status_code}. Błędny link.")
    return car_data


if __name__ == "__main__":
    otomoto_data = get_otomoto_data(sys.argv[1])
    print(otomoto_data)
    