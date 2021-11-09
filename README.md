# Analiza najbolj popularnih albumov 

Analizirala bom najbolj popularne albume. Podatki so pridobljeni iz spletne strani https://rateyourmusic.com/charts/popular/album/all-time/.

Za vsak album bom zajela:
* ime albuma in izvajalca
* število ocen in povprečno oceno
* žanr albuma in datum izida
* besede, ki opisujejo album


Delovne hipoteze:
* Katera zvrst glasbe ima najboljšo povprečno oceno
* Ali obstaja povezava med določenim izvajalcem in povprečno oceno njegovih/njihovih albumov?
* Ali lahko napovem izvajalca iz besed, ki opisujejo njegov/njihov album?

V datotekah iz mape "html-files" je html iz posamezne strani (npr. 25.html vsebuje html iz 25. strani od 125). Vsebina vseh teh datotek je združena v datoteki "skupna-datoteka.html". Datoteka "albumi.csv" vsebuje podatke o naslovu albuma, izvajalcu, datumu izdaje, oceni in številu glasov. Datoteka "artists.csv" vsebuje podatke o vseh izvajalcih, ki se pojavljajo kot avtorji katerega od albumov. Datoteki "genres.csv" in "descriptive_words.csv" vsebujeta imena zanrov in besed, ki album opisujejo.
Datoteka "artists_and_albums.csv" vsebuje id izvajalca in vse njegove albume.