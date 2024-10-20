import requests
import sys
from bs4 import BeautifulSoup


url = sys.argv[1]
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
response = requests.get(url, headers=headers)
if response.status_code == 200:
    soup = BeautifulSoup(response.content, 'html.parser')
    print(soup.prettify())
else:
    print(f"Errod code: {response.status_code}")
