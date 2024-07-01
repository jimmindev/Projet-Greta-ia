# -*- coding: utf-8 -*-
import mysql.connector

# Informations de connexion à la base de données
config = {
    'user': 'jimmy',
    'password': '',
    'host': '192.168.20.24',  # ou l'adresse IP du serveur MariaDB
    'database': 'collecte_donnees',  # Remplacez par le nom de votre base de données
    'raise_on_warnings': True
}

def insert_sql(horodatage,temperature_capteur,humidite_capteur,temperature_donnerMeteo,humidite_donnerMeteo,rasp_id):
    try:
        # Connexion à la base de données
        conn = mysql.connector.connect(**config)
        cursor = conn.cursor()
        # Exécution de la requête INSERT
        cursor.execute("INSERT INTO donnee (timestamp, temperature_ext, humidity_ext, temperature_int, humidity_int, raspi_id) VALUES (%s, %s, %s, %s, %s, %s)", (horodatage, temperature_capteur, humidite_capteur,temperature_donnerMeteo,humidite_donnerMeteo,rasp_id,))
        # Valider la transaction
        conn.commit()
    except mysql.connector.Error as err:
        print(f"Erreur lors de l'insertion dans la table 'capteurs': {err}")
    finally:
        # Fermeture de la connexion
        if conn.is_connected():
            cursor.close()
            conn.close()
