# Programme de data-scrapping Parcoursup, session 2024.
# Modules requis non-natifs : requests

import requests
from datetime import datetime

try:
    # Ensemble du jeu de données Parcoursup
    url = "https://data.education.gouv.fr/api/explore/v2.1/catalog/datasets/fr-esr-parcoursup/records"
    # Paramètres de requête, limite à 100 (car maximum possible) et refine pour récupérer uniquement les données où fil_lib_voe_acc = "MP2I"
    params = {
        "limit": 100,
        "refine": 'fil_lib_voe_acc:"MP2I"'
    }

    # Requête HTTP GET pour récupérer les données
    response = requests.get(url, params=params)
    response.raise_for_status()
    # Le résultat est une réponse JSON
    data = response.json()

    records = data.get("results", [])

    # On initialise différentes variables pour compter les éléments que nous recherchons
    total_places = 0
    voeux_total = 0
    propositions_total = 0
    rang_total = 0
    taux_total = 0

    count_voeux = 0
    count_prop = 0
    count_rang = 0
    count_taux = 0

    # On boucle à travers les données en récupérant les différents champs qui nous intéresse. 
    # La méthodologie est disponible ici pour mieux comprendre : https://data.education.gouv.fr/api/explore/v2.1/catalog/datasets/fr-esr-parcoursup/attachments/methodologie_opendata_2024_pdf
    for rec in records:
        if rec.get("capa_fin") is not None:
            total_places += rec["capa_fin"]
        if rec.get("voe_tot") is not None:
            voeux_total += rec["voe_tot"]
            count_voeux += 1
        if rec.get("prop_tot") is not None:
            propositions_total += rec["prop_tot"]
            count_prop += 1
        if rec.get("ran_grp1") is not None:
            rang_total += rec["ran_grp1"]
            count_rang += 1
        if rec.get("taux_acces_ens") is not None:
            taux_total += rec["taux_acces_ens"]
            count_taux += 1

    # On calcule les moyennes puisque nos 4 dernières informations sont des moyennes.
    moyenne_voeux = round(voeux_total / count_voeux) if count_voeux else 0
    moyenne_prop = round(propositions_total / count_prop) if count_prop else 0
    moyenne_rang = round(rang_total / count_rang) if count_rang else 0
    moyenne_taux = round(taux_total / count_taux, 1) if count_taux else 0


    # On fini par afficher les données tel que nécessaire pour simplement les copier/coller sur la page Markdown du site (filiere.md)
    print(f"""Voici les chiffres cumulés pour l'année {datetime.now().year - 1} : 

- Nombre de places : {total_places}
- Nombre moyen de voeux formulés par établissement : {moyenne_voeux}
- Nombre moyen de propositions d'admission envoyées : {moyenne_prop}
- Rang moyen du dernier admis : {moyenne_rang}
- Taux d'admission moyen : {moyenne_taux}%
""")

except requests.RequestException as e:
    print("Erreur de chargement :", e)