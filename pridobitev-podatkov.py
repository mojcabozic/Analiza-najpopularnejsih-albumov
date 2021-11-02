import re
import requests
import os
import csv

frontpage_url = "https://rateyourmusic.com/charts/top/album/all-time/"

'''
def nalozi_stran_v_niz(url):
    try:
        response_object = requests.get(url)

    except requests.exceptions.ConnectionError:

        print("Napaka pri povezovanju do:", url)
        return ""

    if response_object.status_code == requests.codes.ok:
        return response_object.text
    else:
        raise requests.HTTPError(f"Ni ok: {response_object.status_code}")

def shrani_niz_v_datoteko(directory, filename):
    text = nalozi_stran_v_niz(frontpage_url)

    os.makedirs(directory, exist_ok=True)
    path = os.path.join(directory, filename)
    with open(path, 'w', encoding='utf-8') as file_out:
        file_out.write(text)

    return None

'''

def naredi_seznam_blokov():
    with open("i-got-ip-blocked.html") as dat:
        text = dat.read() 

    vzorec_bloka = re.compile(
        r'<div class="topcharts_item_art_crop"  style="padding-bottom:calc( 100% / (1));">'
        r'(.*?)<div class="topcharts_item_medialinkbox">',
        re.DOTALL)

    seznam_blokov = vzorec_bloka.search(text)

    return seznam_blokov

def naredi_slovar_za_album(seznam_blokov):

    vzorec_albuma = re.compile(
        r'title= (?P<album_name>.*?)">'
        r'class="artist">(?P<artist_name>.*?)</a></div>'
        r'<div class="topcharts_item_releasedate">(?P<release_date>.*?)</div>'
        r'<span class="topcharts_stat_category_mobile">Avg: </span>.*?<span class="topcharts_stat topcharts_avg_rating_stat"(?P<rating>.*?)</span>'
        r'<span class="topcharts_stat_category_mobile">Ratings: </span>.*?<span class="topcharts_stat topcharts_ratings_stat">(?P<nr_of_ratings>.*?)</span>'
        r'<div class="topcharts_item_genres_container">(?P<genres>.*?).*?<div class="topcharts_item_descriptors_container">'
        r'<div class="topcharts_item_descriptors_container">(?P<descriptive_words>.*?).*?</div>.*?</div>',
        re.DOTALL)

    seznam_albumov = []

    for blok in seznam_blokov:
        album = vzorec_albuma.search(blok.group(0)).groupdict()
        seznam_albumov += album
        album["genres"] = []
        album["descriptive_words"] = []

    vzorec_zanra = re.compile(
        r'<span class=""><a class="genre topcharts_item_genres" href="/.*?/">(?P<genre>.*?)</a>'
    )
    vzorec_opisovalnih_besed = re.compile(
        r'<span class="topcharts_item_descriptors">(?P<descriptive_word>.*?), </span>'
    )
    
    for album in seznam_albumov:
        for match in re.finditer(vzorec_zanra, album["genres"]):
            album["genres"] += match.group["genre"]

        for match in re.finditer(vzorec_opisovalnih_besed, album["descriptive_words"]):
            album["descriptive_words"] += match.group["descriptive_word"]

    return seznam_albumov

print(naredi_seznam_blokov())