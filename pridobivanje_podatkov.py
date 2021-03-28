# pridobivanje podatkov
import requests
import re
from zipfile import ZipFile
import pandas as pd
from urllib.request import urlopen
import os

def pridobivanje_podatkov(url):
    '''funkcija poišče povezavo za json datoteko na podani spletni strani'''
    html = requests.get(url)
    reg_iz = r'/api/3/action(.*)"'
    ujemanje = re.search(reg_iz,html.text)
    json_url = 'https://podatki.gov.si' + ujemanje.group().split()[0][:-1] 
    poisci_json = requests.get(json_url)
    json = poisci_json.json() # dobimo slovar slovarjev s podatki o spletni strani

    pot = json["result"]["resources"][:-1] # predstavlja seznam slovarjev za posamezno leto

    url_slovar = {}
    for leto in pot:
        naslov = leto["description"]
        url_za_leto = leto["url"] # to je URL zip datoteke za posamezno leto
        url_slovar[naslov] = url_za_leto
    
    return url_slovar


def prenos_datotek(url, lokacija):
    odpri = urlopen(url)
    #ustvarimo začasno zip datoteko
    trenutnizip = open('tempfile.zip', "wb")
    #zapišemo vsebino prenesene datoteke v lokalno shrambo
    trenutnizip.write(odpri.read())
    trenutnizip.close()
    #ponovno odpremo zip datoteko
    zip_datoteka = ZipFile('tempfile.zip')
    #prenešene datoteke shranimo v izbrano mapo
    zip_datoteka.extractall(path = os.getcwd() + lokacija)
    zip_datoteka.close()

for url in pridobivanje_podatkov('https://podatki.gov.si/dataset/mnzpprometne-nesrece-od-leta-2009-dalje').values():
    prenos_datotek(url, '/podatki')


