import requests
from datetime import datetime

try:
    url = "https://data.education.gouv.fr/api/explore/v2.1/catalog/datasets/fr-esr-parcoursup/records"
    params = {
        "limit": 100,
        "refine": 'fil_lib_voe_acc:"MP2I"'
    }

    response = requests.get(url, params=params)
    response.raise_for_status()
    data = response.json()

    records = data.get("results", [])

    total_places = 0
    voeux_total = 0
    propositions_total = 0
    rang_total = 0
    taux_total = 0

    count_voeux = 0
    count_prop = 0
    count_rang = 0
    count_taux = 0

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

    moyenne_voeux = round(voeux_total / count_voeux) if count_voeux else 0
    moyenne_prop = round(propositions_total / count_prop) if count_prop else 0
    moyenne_rang = round(rang_total / count_rang) if count_rang else 0
    moyenne_taux = round(taux_total / count_taux, 1) if count_taux else 0


    print(f"""Voici les chiffres cumulés pour l'année {datetime.now().year - 1} : 

- Nombre de places : {total_places}
- Nombre moyen de voeux formulés par établissement : {moyenne_voeux}
- Nombre moyen de propositions d'admission envoyées : {moyenne_prop}
- Rang moyen du dernier admis : {moyenne_rang}
- Taux d'admission moyen : {moyenne_taux}%
""")

except requests.RequestException as e:
    print("Erreur de chargement :", e)
