import re
import requests
import os
import json



def naredi_seznam_blokov():
    with open("skupna-datoteka.html") as dat:
        text = dat.read() 


    vzorec_bloka = re.compile(
        r'<div class="topcharts_item_art_crop" \s*style="padding-bottom:calc\( 100% / \(1\)\);">.*?'
        r'<div class="topcharts_item_medialinkbox">',
        flags=re.DOTALL,
        )

    seznam_blokov = vzorec_bloka.findall(text)

    return seznam_blokov

def naredi_slovar_za_album():
    seznam_blokov = naredi_seznam_blokov()
    vzorec_albuma = re.compile(
        r'title="(?P<album_name>.*?)">.*?'
        r'class="artist">(?P<artist_name>[^<>]*).*?</a></div>.*?'
        r'<div class="topcharts_item_releasedate">(?P<release_date>.*\d{4}).*?</div>.*?'
        r'<span class="topcharts_stat_category_mobile">Avg: </span>.*?<span class="topcharts_stat topcharts_avg_rating_stat">(?P<rating>.*?)</span>.*?'
        r'<span class="topcharts_stat_category_mobile">Ratings: </span>.*?<span class="topcharts_stat topcharts_ratings_stat">(?P<nr_of_ratings>.*?)</span>.*?'
        r'<div class="topcharts_item_genres_container">(?P<genres_raw>.*?)'
        r'<div class="topcharts_item_descriptors_container">(?P<descriptive_words_raw>.*?)</div>.*?</div>',
        re.DOTALL)

    seznam_albumov = []

    for blok in seznam_blokov:
        album = vzorec_albuma.search(blok).groupdict()
        seznam_albumov.append(album)
        album["genres"] = []
        album["descriptive_words"] = []


    vzorec_zanra = re.compile(
        r'<span class=""><a class="genre topcharts_item_genres" href=".*?">(?P<genre>.*?)</a>'
    )
    vzorec_opisovalnih_besed = re.compile(
        r'<span class="topcharts_item_descriptors">(?P<descriptive_word>.*?), </span>'
    )
    
    for album in seznam_albumov:
        for match in re.finditer(vzorec_zanra, album["genres_raw"]):
            album["genres"].append(match.group("genre"))

        for match in re.finditer(vzorec_opisovalnih_besed, album["descriptive_words_raw"]):
            album["descriptive_words"].append(match.group("descriptive_word"))

        del album["genres_raw"]
        del album["descriptive_words_raw"]

        album["nr_of_ratings"] = album["nr_of_ratings"].replace(",", "")

    return seznam_albumov

with open("albumi.json", "w") as dat:
    json.dump(naredi_slovar_za_album(), dat)


