import requests
from bs4 import BeautifulSoup
import pandas as pd


# contenu = requests.get("https://www.marocannonces.com/categorie/309/Emploi/Offres-emploi.html")
# soup = BeautifulSoup(contenu.text, "html.parser")

# # Récupérer toutes les annonces
# liste_annonces = soup.find_all("li")  # chaque annonce est dans un <li>

# for annonce in liste_annonces:
#     # Titre
#     titre = annonce.find("h3")
#     if titre:
#         titre = titre.get_text(strip=True)
#     else:
#         titre = "-"
    
#     # Description ou info complémentaire
#     description = annonce.find("p")
#     if description:
#         description = description.get_text(strip=True)
#     else:
#         description = "-"
    
#     # Salaire
#     salaire = annonce.find("div", class_="salary")
#     if salaire:
#         salaire = salaire.get_text(strip=True)
#     else:
#         salaire = "-"
    
#     print("Titre :", titre)
#     print("Description :", description)
#     print("Salaire :", salaire)

#     print("\n########################################################\n")


# URL = "https://www.bkam.ma/Marches/Principaux-indicateurs/Marche-monetaire/Taux-de-reference-du-marche-interbancaire"

# content = requests.get(URL)
# print(content.text)

url = "https://www.bkam.ma/Marches/Principaux-indicateurs/Marche-monetaire/Indice-monia-moroccan-overnight-index-average"
r = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
soup = BeautifulSoup(r.text, "lxml")
# print(soup.text)


# breakpoint()

tables = soup.find_all("table")
frames = [pd.read_html(str(t))[0] for t in tables]
df = pd.concat(frames, ignore_index=True)
df.to_csv("monia.csv", index=False)
