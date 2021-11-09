import json
import csv

with open("albumi.json") as dat:
    albumi = json.load(dat)


#funkcija preveri, ce ta izvajalec ze obstaja v seznamu
def is_duplicated(array, key, name):
    for dictionary in array:
        if dictionary[key] == name:
            return True

    return False
        
#list vseh izvajalcev, zanrov, besed

list_of_dict_for_artists = []
list_of_dict_for_genres = []
list_of_dict_for_desc_words = []
next_id_artists = 1
next_id_genres = 1
next_id_desc_words = 1

for album in albumi:
    current_artist = album["artist_name"] 
    if not is_duplicated(list_of_dict_for_artists, "artist_name", current_artist):
        list_of_dict_for_artists.append({"id_artist": next_id_artists, "artist_name": current_artist})
        next_id_artists += 1   

    for genre in album["genres"]:
        if not is_duplicated(list_of_dict_for_genres, "genre", genre):
            list_of_dict_for_genres.append({"id_genre": next_id_genres, "genre": genre})
            next_id_genres += 1

    for descriptive_word in album["descriptive_words"]:
        if not is_duplicated(list_of_dict_for_desc_words, "descriptive_word", descriptive_word):
            list_of_dict_for_desc_words.append({"id_descriptive_word": next_id_desc_words, "descriptive_word": descriptive_word})
            next_id_desc_words += 1

with open("artists.csv", "w") as dat:
    writer = csv.DictWriter(dat, fieldnames=["id_artist", "artist_name"])
    writer.writeheader()
    for data in list_of_dict_for_artists:
        writer.writerow(data)

with open("genres.csv", "w") as dat:
    writer = csv.DictWriter(dat, fieldnames=["id_genre", "genre"])
    writer.writeheader()
    for data in list_of_dict_for_genres:
        writer.writerow(data)

with open("descriptive_words.csv", "w") as dat:
    writer = csv.DictWriter(dat, fieldnames=["id_descriptive_word", "descriptive_word"])
    writer.writeheader()
    for data in list_of_dict_for_desc_words:
        writer.writerow(data)


#csv datoteka z ostalimi podatki:
for album in albumi:
    del album["genres"]
    del album["descriptive_words"]

top_row = list(albumi[0].keys())

with open("albumi.csv", "w") as dat:
    writer = csv.DictWriter(dat, fieldnames=top_row)
    writer.writeheader()
    for data in albumi:
        writer.writerow(data)

