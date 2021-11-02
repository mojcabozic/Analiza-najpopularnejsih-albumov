import os

with open("skupna-datoteka.html", "w") as dat:

    for i in range(1, 126):
        with open(f"html-files/{i}.html") as cdat:
            text = cdat.read()
            dat.write(text)
            

