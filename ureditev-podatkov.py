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
next_id_desc_words = 1

for i, album in enumerate(albumi):
    album["id"] = i + 1
    current_artist = album["artist_name"] 
    if not is_duplicated(list_of_dict_for_artists, "artist_name", current_artist):
        list_of_dict_for_artists.append({"id_artist": next_id_artists, "artist_name": current_artist})
        next_id_artists += 1   

    for genre in album["genres"]:
        list_of_dict_for_genres.append({"id_albuma": album["id"], "genre": genre})

    for descriptive_word in album["descriptive_words"]:
        list_of_dict_for_desc_words.append({"id_albuma": album["id"], "descriptive_word": descriptive_word})
        next_id_desc_words += 1

with open("artists.csv", "w") as dat:
    writer = csv.DictWriter(dat, fieldnames=["id_artist", "artist_name"])
    writer.writeheader()
    for data in list_of_dict_for_artists:
        writer.writerow(data)

with open("genres.csv", "w") as dat:
    writer = csv.DictWriter(dat, fieldnames=["id_albuma", "genre"])
    writer.writeheader()
    for data in list_of_dict_for_genres:
        writer.writerow(data)

with open("descriptive_words.csv", "w") as dat:
    writer = csv.DictWriter(dat, fieldnames=["id_albuma", "descriptive_word"])
    writer.writeheader()
    for data in list_of_dict_for_desc_words:
        writer.writerow(data)


#csv datoteka z ostalimi podatki:
for album in albumi:
    del album["genres"]
    del album["descriptive_words"]

top_row = list(albumi[0].keys()) + ["release_year"]

with open("albumi.csv", "w") as dat:
    writer = csv.DictWriter(dat, fieldnames=top_row)
    writer.writeheader()
    for data in albumi:
        try:
            data["release_year"] = int(data["release_date"].split(" ")[-1])
        except:
            try:
                data["release_year"] = int(data["release_date"])
            except:
                print(data, "is gay")

        writer.writerow(data)


list_of_dict_for_artists_and_albums = []
for artist in list_of_dict_for_artists:
    id_artist = artist["id_artist"]
    for album in albumi:
        if album["artist_name"] == artist["artist_name"]:
            album_name = album["album_name"]
            list_of_dict_for_artists_and_albums.append({"id_artist": f"{id_artist}", "album_name": f"{album_name}"})


with open("artists_and_albums.csv", "w") as dat:
    writer = csv.DictWriter(dat, fieldnames=["id_artist", "album_name"])
    writer.writeheader()
    for data in list_of_dict_for_artists_and_albums:
        writer.writerow(data)