import mysql.connector
from mysql.connector import Error
import random
from datetime import datetime, timedelta

from get_info_csv import get_random_adresse
from random_old_date import generate_random_dates

# Fonction pour se connecter à la base de données
def connect():
    try:
        connection = mysql.connector.connect(
            host='192.168.20.24', # 192.168.20.24
            database='batiment_intelligent',
            user='jimmy', # jimmy
            password='jimmy' # jimmy
        )
        if connection.is_connected():
            print('Connecté à la base de données')
            return connection
    except Error as e:
        print(f"Erreur de connexion à la base de données: {e}")
        return None

# Fonction pour insérer des données aléatoires dans la table 'maison'
def insert_random_maison(connection, num_rows):
    try:
        cursor = connection.cursor()

        for _ in range(num_rows):
            liste = get_random_adresse()  
            adresse = f'{liste["numero"][0]}  {liste["voie_nom"][0]} , {liste["commune_nom"][0]}'
            adresse = adresse[:250]
            lattitude_maison = liste["lat"][0]
            longitude_maison = liste["long"][0]
            nb_zones_maison = random.randint(1, 10)

            query = "INSERT INTO maison (adresse_maison, lattitude_maison, longitude_maison, nb_zones_maison) " \
                    "VALUES (%s, %s, %s, %s)"
            values = (adresse, lattitude_maison, longitude_maison, nb_zones_maison)
            cursor.execute(query, values)

            # Récupération de l'id clé primaire
            last_row_id = cursor.lastrowid
            insert_random_zones(connection, last_row_id , random.randint(1, 13))

        connection.commit()
        print(f'{num_rows} lignes insérées dans la table "maison"')

    except Error as e:
        print(f"Erreur lors de l'insertion des données dans la table 'maison': {e}")

# Vous pouvez ajouter des fonctions similaires pour d'autres tables


def insert_random_zones(connection, id_maison , num_rows):
    try:
        cursor = connection.cursor()

        for _ in range(num_rows):

            room_type = ['salle_a_manger','cuisine','salon','couloir','chambre','bureau','sdb','wc','garage','cave','gernier','combles','sous_sol']
            
            designation_zone = random.choice(room_type)
            superficie_zone =  random.uniform(10, 50)
            nom_zone = f'{designation_zone} {count_in_zones(connection, designation_zone ,id_maison) + 1 }'
            nom_zone = nom_zone[:50]

            id_unite =  random_unite(connection  , nom_zone )

            id_capteur =  random_capteurs(connection , nom_zone )


            query = "INSERT INTO zones (designation_zone, superficie_zone, nom_zone, id_maison , id_unite , id_capteur) " \
                    "VALUES (%s, %s, %s, %s, %s, %s)"
            values = (designation_zone, superficie_zone, nom_zone, id_maison , id_unite , id_capteur)

            cursor.execute(query, values)

        connection.commit()
        print(f'{num_rows} lignes insérées dans la table "Zones"')

    except Error as e:
        print(f"Erreur lors de l'insertion des données dans la table 'Zones': {e}")


def count_in_zones(connection,designation_zone,id_maison):
    try:
        cursor = connection.cursor()

        # Exécuter la requête SQL
        query = f"SELECT id_maison, designation_zone, COUNT(*) AS nombre_zones FROM zones WHERE id_maison = {id_maison} AND designation_zone = '{designation_zone}' GROUP BY id_maison, designation_zone"
        cursor.execute(query)

        # Récupérer un seul résultat
        result = cursor.fetchone()

        # Vérifier si le résultat existe
        if result:
            id_maison, designation_zone, nombre_zones = result
            return nombre_zones
        else:
            return 0
        
    except Error as e:
        return ""



def random_unite(connection  , nom_zone ) :
    try:
        cursor = connection.cursor()
        puissance_unite = random.randint(50, 5000)
        thermostat_unite = random.choice(['Aucun','manuel','numérique'])
        type_unite = random.choice(['PAC_reversible','PAC_chauffage','PAC_clim','Convecteur','Chauffage_au_sol','radiateur_bain_huile','radiateur_classique'])
        designation_unite =  type_unite  + nom_zone
        designation_unite = designation_unite[:50]

        query = "INSERT INTO unites (designation_unite, puissance_unite, thermostat_unite, type_unite) " \
                "VALUES (%s, %s, %s, %s)"
        values = (designation_unite, puissance_unite, thermostat_unite, type_unite)

        cursor.execute(query, values)
        last_row_id = cursor.lastrowid

        connection.commit()
        print(f'1 lignes insérées dans la table "unites"')


        insert_random_etats_unites(connection, last_row_id , random.randint(1, 200 ))

        return last_row_id

    except Error as e:
        print(f"Erreur lors de Selection des données dans la table 'unites': {e}")
        return ""


def insert_random_etats_unites(connection, id_unite , num_rows):
    try:
        cursor = connection.cursor()
        dates = generate_random_dates(num_rows)

        for date_heure in dates:
            # Convert datetime object to Unix timestamp
            timestamp = int(date_heure.timestamp())
            on_off = random.choice(["ON","OFF"])
            temperature_set_point = random.uniform(1, 5000)

            query = "INSERT INTO etat_unites (date_heure, on_off, temperature_set_point , id_unite) " \
                    "VALUES (FROM_UNIXTIME(%s), %s, %s, %s)"
            values = (timestamp, on_off, temperature_set_point, id_unite)

            cursor.execute(query, values)

        connection.commit()
        print(f'{num_rows} lignes insérées dans la table "etats_unites"')

    except Error as e:
        print(f"Erreur lors de l'insertion des données dans la table 'etats_unites': {e}")






def random_capteurs(connection , nom_zone) :
    try:
        cursor = connection.cursor()


        protocole = random.choice(['z_wave','ip','Zig_bee','LoRa','Bluetooth','Wifi'])
        type_capteur = random.choice(['temperature','humidite','presence','UV','luminosite','temperature_humidite'])
        nom_capteur =  f"{protocole} - {type_capteur} - {nom_zone}"
        nom_capteur = nom_capteur[:50]

        query = "INSERT INTO capteurs (protocole, type_capteur, nom_capteur) " \
                "VALUES (%s, %s, %s)"
        values = (protocole, type_capteur, nom_capteur)

        cursor.execute(query, values)
        last_row_id = cursor.lastrowid

        connection.commit()
        print(f'1 lignes insérées dans la table "capteurs"')


        insert_random_releves_maison(connection, last_row_id , random.randint(1, 200 ))

        return last_row_id

    except Error as e:
        print(f"Erreur lors de Selection des données dans la table 'capteurs': {e}")
        return ""


def insert_random_releves_maison(connection, id_capteur , num_rows):
    try:
        cursor = connection.cursor()
        dates = generate_random_dates(num_rows)

        for date_heure in dates:
            # Convert datetime object to Unix timestamp
            timestamp = int(date_heure.timestamp())

            releve_capteur = random.uniform(1, 5000)
            id_capteur = id_capteur

            id_type_mesure = random_type_mesure(connection)

            query = "INSERT INTO releves_maison (date_heure, releve_capteur, id_capteur , id_type_mesure) " \
                    "VALUES (FROM_UNIXTIME(%s), %s, %s, %s)"
            values = (timestamp, releve_capteur, id_capteur, id_type_mesure)

            cursor.execute(query, values)

        connection.commit()
        print(f'{num_rows} lignes insérées dans la table "releves_maison"')

    except Error as e:
        print(f"Erreur lors de l'insertion des données dans la table 'releves_maison': {e}")


def random_type_mesure(connection):
    try:
        cursor = connection.cursor()

        type_typteur = random.choice(['temperature', 'humidite', 'presence', 'UV', 'luminosite', 'temperature_humidite'])

        # Vérifier si le type existe déjà dans la table
        query_check = "SELECT id_type_mesure FROM type_mesure WHERE type_typteur = %s"
        cursor.execute(query_check, (type_typteur,))
        existing_type_id = cursor.fetchone()

        if existing_type_id:
            # Si le type existe déjà, retourner son ID
            return existing_type_id[0]
        else:
            # Sinon, procéder à l'insertion
            query_insert = "INSERT INTO type_mesure (type_typteur) VALUES (%s)"
            values = (type_typteur,)
            cursor.execute(query_insert, values)
            last_row_id = cursor.lastrowid

            connection.commit()
            print(f'1 ligne insérée dans la table "type_mesure"')
            return last_row_id

    except Error as e:
        print(f"Erreur lors de la sélection des données dans la table 'type_mesure': {e}")
        return ""


# Fonction principale
def main():
    connection = connect()
    


    if connection:

        if 1 == 1 : insert_random_maison(connection, 10) # insert maison + random 1-13 zones + 
        # Fermer la connexion
        connection.close()
        #print('Connexion à la base de données fermée')







if __name__ == "__main__":
    main()