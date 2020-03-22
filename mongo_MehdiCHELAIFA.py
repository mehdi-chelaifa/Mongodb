# Fait par Mehdi CHELAIFA , IF7 Fintech

import pymongo
import requests
import json
import matplotlib.pyplot as plt


from pymongo import MongoClient


#on connecte python à mongodb
cluster = MongoClient('mongodb+srv://Hodor:Bqbyluigi007@cluster0-mcdo3.mongodb.net/test?retryWrites=true&w=majority')

#on ouvre notre collection
db= cluster['Base']
collection = db['collection']

# API : nombre de cas confirmés de coronavirus en France sur les 3 derniers mois
response = requests.get("https://api.covid19api.com/total/country/france/status/confirmed")


# Fonction JPrint qui permet de mieux afficher les données (cascadées)
def jprint(obj):
     # on crée un string avec l'objet Json
    text = json.dumps(obj, sort_keys=True, indent=4)
    print(text)

#jprint(response.json())

#initialisation de la collection
x = collection.delete_many({})

#on insère nos données dans notre base de données.
data=response.text
dictio = json.loads(data)        
collection.insert_many(dictio)

# On va étudier l'évolution du taux de contamination par jour.

resultat = collection.find({})
Liste_Nb_cas=[]
for x in resultat:
    Liste_Nb_cas.append(x["Cases"])
Liste_evolution=[]
for i in range(3,len(Liste_Nb_cas)-1):   #on commence à partir du 3ème jour ( 1er cas)
    Liste_evolution.append(((Liste_Nb_cas[i+1] - Liste_Nb_cas[i]) * 100) / Liste_Nb_cas[i])
#print(Liste_evolution)

# on obtient alors les taux suivants :
#[0.0, 0.0, 33.333333333333336, 25.0, 0.0, 0.0, 20.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 83.33333333333333, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 9.090909090909092, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 16.666666666666668, 28.571428571428573, 111.11111111111111, 50.0, 75.43859649122807, 30.0, 46.92307692307692, 6.806282722513089, 41.1764705882353, 31.944444444444443, 72.63157894736842, 45.88414634146341, 18.495297805642632, 7.319223985890653, 47.24732949876746, 27.790178571428573, 0.0, 60.56768558951965, 22.001631765025838, 0.7579135086937138, 47.323008849557525, 15.617960654752967, 18.262111962592545, 20.230642504118617, 15.392344934685301, 14.241608613046232]
    
#on remarque qu'une donnée est manquante, le nombre de cas de 10 jours plus tôt
# qui ne varie pas ( 2290), on va alors la supprimer de la collection.

collection.delete_one({"Cases" : 2290})

resultat = collection.find({})
Liste_Nb_cas=[]
for x in resultat:
    Liste_Nb_cas.append(x["Cases"])
Liste_evolution=[]
for i in range(3,len(Liste_Nb_cas)-1):   #on commence à partir du 3ème jour ( 1er cas)
    Liste_evolution.append(((Liste_Nb_cas[i+1] - Liste_Nb_cas[i]) * 100) / Liste_Nb_cas[i])
print(Liste_evolution)

#on obtient alors une liste avec des données plus pertitentes, qu'on peut aussi projeter sur une courbe.
plt.plot(Liste_evolution)
plt.show