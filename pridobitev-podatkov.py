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
        r'class="artist">(?P<artist_name>[\w\d\s\.]*).*?</a></div>.*?'
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


test =  '''<div id="pos1" style="z-index:calc(200 - 1);" class="topcharts_itembox chart_item_release">
                        <div class="topcharts_item_artbox">
                                 
                                     <div class="topcharts_item_art_crop"  style="padding-bottom:calc( 100% / (1));">
                                       <a href="/release/album/radiohead/ok-computer/" title="OK Computer">
                                          <img alt="OK Computer - Cover art" class="topcharts_item_art" src="//e.snmc.io/i/300/w/a370a7b92c4cf2f24d8225696215fb5c/8862252" />
                                          
                                       </a>
                                     </div>
                        </div>
                        <div class="topcharts_position">1<span class="topcharts_position_desktop">.</span></div>
                        <div class="topcharts_textbox_top">
                           
                           <div class="topcharts_item_title"><a href="/release/album/radiohead/ok-computer/" class="release" title="[Album45]">OK Computer</a></div>
                           
                           <div class="topcharts_item_artist_newmusicpage topcharts_item_artist"><a   href="/artist/radiohead" class="artist">Radiohead</a></div>
                        
                           
                           <div class="topcharts_item_releasedate">16 June 1997
                     
                     
                     
                           </div>
                          
                        </div>
                        <div class="topcharts_item_statsbox">
                           <span class="topcharts_stat_category_mobile">Avg: </span>
                              <span class="topcharts_stat topcharts_avg_rating_stat">4.23</span>
                     
                           <span class="topcharts_stat_category_mobile">Ratings: </span>
                              <span class="topcharts_stat topcharts_ratings_stat">70,888</span>
                     
                           <span class="topcharts_stat_category_mobile">Reviews: </span>
                              <span class="topcharts_stat topcharts_reviews_stat">1537</span>
                      
                        </div>

                        <div class="topcharts_textbox_bottom"> 
                           <div class="topcharts_item_genres_container">
                              <span class=""><a class="genre topcharts_item_genres" href="/genre/alternative-rock/">Alternative Rock</a>, </span> 
                     
                              <span class=""><a class="genre topcharts_item_genres" href="/genre/art-rock/">Art Rock</a></span> 
                           </div>

                           <div class="topcharts_item_secondarygenres_container">     
                     
                                 <span class=""><a class="genre topcharts_item_secondarygenres" href="/genre/space-rock-revival/">Space Rock Revival</a></span> 
                           </div>

                           <div class="topcharts_item_descriptors_container">
                                 <span class="topcharts_item_descriptors">melancholic, </span> 
                                 <span class="topcharts_item_descriptors">anxious, </span> 
                                 <span class="topcharts_item_descriptors">futuristic, </span> 
                                 <span class="topcharts_item_descriptors">male vocals, </span> 
                                 <span class="topcharts_item_descriptors">existential, </span> 
                                 <span class="topcharts_item_descriptors">alienation, </span> 
                                 <span class="topcharts_item_descriptors">atmospheric, </span> 
                                 <span class="topcharts_item_descriptors">lonely, </span> 
                                 <span class="topcharts_item_descriptors">cold, </span> 
                     
                                 <span class="topcharts_item_descriptors">pessimistic</span> 
                           </div>
                        </div>

                        <div class="topcharts_item_medialinkbox">'''

vzorec_albuma = re.compile(
        r'title="(?P<album_name>.*?)">.*?'
        r'class="artist">(?P<artist_name>.*?)</a></div>.*?'
        r'<div class="topcharts_item_releasedate">(?P<release_date>\d+ \w+ \d{4}).*?</div>.*?',
        #r'<span class="topcharts_stat_category_mobile">Avg: </span>.*?<span class="topcharts_stat topcharts_avg_rating_stat">(?P<rating>.*?)</span>.*?'
        #r'<span class="topcharts_stat_category_mobile">Ratings: </span>.*?<span class="topcharts_stat topcharts_ratings_stat">(?P<nr_of_ratings>.*?)</span>.*?'
        #r'<div class="topcharts_item_genres_container">(?P<genres_raw>.*?)'
        #r'<div class="topcharts_item_descriptors_container">(?P<descriptive_words_raw>.*?)</div>.*?</div>',
        re.DOTALL)

