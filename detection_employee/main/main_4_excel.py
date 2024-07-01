import mysql.connector
import pandas as pd
import logging
import os
from datetime import datetime

# Configuration de la base de données
config_bdd = {
    'host': '192.168.0.17',
    'database': 'Cam_Auto_Badge',
    'user': 'jimmy',
    'password': 'Ey4@WKIF!3lm)e*y'
}

def get_passages(start_date, end_date):
    try:
        # Connexion à la base de données
        conn = mysql.connector.connect(**config_bdd)
        cursor = conn.cursor(dictionary=True)

        # Requête pour obtenir les données de passage entre deux dates
        query = """
        SELECT p.id_passage, p.horaire_passage, p.entree_sortie_passage, e.id_employe, e.nom_employe, e.prenom_employe
        FROM Passages p
        JOIN Employes e ON p.id_employe = e.id_employe
        WHERE p.horaire_passage BETWEEN %s AND %s
        """
        cursor.execute(query, (start_date, end_date))
        passages = cursor.fetchall()

        # Fermer la connexion à la base de données
        cursor.close()
        conn.close()

        return passages

    except mysql.connector.Error as err:
        logging.error(f"Erreur: {err}")
        return []

def export_to_excel(data, output_file):
    # Convertir les données en DataFrame pandas
    df = pd.DataFrame(data)

    # Créer le répertoire 'excel' s'il n'existe pas
    os.makedirs(os.path.dirname(output_file), exist_ok=True)

    # Exporter le DataFrame en fichier Excel
    df.to_excel(output_file, index=False)

if __name__ == "__main__":
    # Dates de début et de fin pour la requête
    start_date = "2024-05-01"
    end_date = "2024-05-29"

    # Obtenir les données de passage
    passages = get_passages(start_date, end_date)

    # Obtenir la date et l'heure actuelles pour le nom de fichier Excel
    current_datetime = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    output_file = f"./excel/passages_{current_datetime}.xlsx"

    # Exporter les données en fichier Excel
    export_to_excel(passages, output_file)

    print(f"Données exportées avec succès vers {output_file}")
