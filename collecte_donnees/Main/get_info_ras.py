# -*- coding: utf-8 -*-
import requests
import subprocess
import mysql.connector

import message_to_discord
import gestion_erreurs

def recuperer_informations(url):
    # Envoie de la requête HTTP pour récupérer les données de la page PHP
    reponse = requests.get(url)
    
    # Vérification du code de statut de la réponse
    if reponse.status_code == 200:
        # Analyse du contenu JSON
        donnees_json = reponse.json()
        
        # Retourne les données sous forme de dictionnaire
        return donnees_json
    else:
        # Affiche un message d'erreur si la requête échoue
        print("Erreur {}: Impossible de récupérer les données.".format(reponse.status_code))
        return None


def get_info_rasp(Timezone , rasp_ip ):
    # URL de la page PHP
    url_page_php = "http://"+rasp_ip+"/modulesGrove.php?all"
    # Appel de la fonction pour récupérer les informations
    informations = recuperer_informations(url_page_php)
    print(informations)

    # Vérification si des informations ont été récupérées avec succès
    if informations is None:
        # 1: "Erreur API rasp !"
        log = gestion_erreurs.gerer_erreur(1)
        message_to_discord.send_message_to_discord(log)
        return ""

    # Informations de connexion à la base de données
    config = {
        'user': 'jimmy',
        'password': '',
        'host': '192.168.20.24',  # ou l'adresse IP du serveur MariaDB
        'database': 'collecte_donnees',  # Remplacez par le nom de votre base de données
        'raise_on_warnings': True
    }

    try:
        # Connexion à la base de données
        conn = mysql.connector.connect(**config)
        cursor = conn.cursor()
        # Exécution de la requête INSERT
        cursor.execute("INSERT INTO donnee_rasp (timestamp, temperature_int, humidity_int, rasp_ip) VALUES (%s, %s, %s, %s)", 
                       (Timezone, informations["temperature"], informations["humidite"],rasp_ip ))
        # Valider la transaction
        conn.commit()
    except mysql.connector.Error as err:
        # 2: "Erreur API rasp Insertion SQL !"
        log = gestion_erreurs.gerer_erreur(2)
        message_to_discord.send_message_to_discord(log)
    finally:
        # Fermeture de la connexion
        if conn.is_connected():
            cursor.close()
            conn.close()

    temperature = informations["temperature"]
    humidite    = informations["humidite"]
    text = f"Rasp_IP : {rasp_ip} \nTemperature : {temperature} \nHumidite : {humidite} \n\n"
    return text