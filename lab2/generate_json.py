from bs4 import BeautifulSoup
from re import search
from requests import get
import json
TRAM_URL_FILE = 'tramstop_vt_url.json' 
url = 'https://www.vasttrafik.se/reseplanering/hallplatslista/'
avgangstavla = 'https://avgangstavla.vasttrafik.se/?source=vasttrafikse-stopareadetailspage&stopAreaGid='

doc = get(url, verify=False)

soup = BeautifulSoup(doc.text, 'html.parser')

link_list = dict()

for link in soup.find_all('a'):
    if search('/reseplanering/hallplatser/.+', link.get('href')):
        stop = link.text.splitlines()[1].strip()[:-1]

        link_list[stop] = avgangstavla + link.get('href').split('/')[-2]

with open(TRAM_URL_FILE, 'w') as file:
    json.dump(link_list, file, indent=2, ensure_ascii=False)