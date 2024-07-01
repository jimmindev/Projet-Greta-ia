import insightface_paddle_face as face
import logging
from tqdm import tqdm
import cv2

import os
import subprocess
from datetime import timedelta

logging.basicConfig(level=logging.INFO)

parser = face.parser()
args = parser.parse_args()

args.det = True
args.output = "./output"
input_path = "./demo/friends/query/ant.mp4"

# Ouvrir la vidéo avec OpenCV pour obtenir le nombre total de frames
cap = cv2.VideoCapture(input_path)
if not cap.isOpened():
    print("Erreur : Impossible d'ouvrir la vidéo")
    exit()
total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
fps_video = cap.get(cv2.CAP_PROP_FPS)

cap.release()

print(f"total_frames = {total_frames}" )
print(f"fps_video = {fps_video}" )

# Calculer le temps de chargement en secondes en utilisant 30 FPS
loading_time = total_frames / 3
# Convertir le temps de chargement en heures, minutes et secondes
loading_time_hms = str(timedelta(seconds=int(loading_time)))


# Prédiction des visages
Logs = False
predictor = face.InsightFace(args,Logs)
res = predictor.predict(input_path)

print("")
print(f"Temps de chargement estimé : {loading_time_hms}")

if input("Detecter le visage de l'employé :") == 'y' :
    # Affichage de la barre de progression
    with tqdm(total=total_frames, desc="Detection progress", unit="frames") as pbar:
        for result in res:
            # Mise à jour de la barre de progression
            pbar.update(1)  # Mettre à jour d'une frame à la fois

#ici PyQT validation du data Set sinon supprimer des images etc

# Fonction pour ouvrir le dossier
def open_folder(path):
    # Vérifie si le chemin existe
    if os.path.exists(path):
        if os.name == 'nt':  # Vérifie si le système est Windows
            subprocess.run(['explorer', path])
        elif os.name == 'posix':  # Vérifie si le système est Linux ou Mac
            if subprocess.run(['which', 'xdg-open']).returncode == 0:
                subprocess.run(['xdg-open', path])  # Pour Linux
            elif subprocess.run(['which', 'open']).returncode == 0:
                subprocess.run(['open', path])      # Pour Mac
    else:
        print(f"Erreur : Le dossier spécifié '{path}' n'existe pas.")

# Appeler la fonction pour ouvrir le dossier
output_dir = os.path.abspath(args.output+"/detected")
print(output_dir)


print("Les images vous semble correct sinon supprimer les images defectueuse manuellement")
if input("Voir le dossier ? y or n :") == 'y' :
    open_folder(output_dir)
    
print("Entrer le nom de l'employé : ") 
nom = input()
print("Entrer le prenom de l'employé : ") 
prenom = input()

import mysql.connector
from mysql.connector import Error

def connect_to_database(nom , prenom):
    try:
        # Établir la connexion à la base de données
        connection = mysql.connector.connect(
            host='192.168.0.17',
            database='Cam_Auto_Badge',
            user='jimmy',
            password='Ey4@WKIF!3lm)e*y'
        )

        if connection.is_connected():
            db_info = connection.get_server_info()
            print(f"Connected to MySQL Server version {db_info}")
            cursor = connection.cursor()

            # Exécuter la requête SQL INSERT
            insert_query = "INSERT INTO Employes ( nom_employe, prenom_employe) VALUES ( %s, %s)"
            employee_data = ( nom , prenom )
            cursor.execute(insert_query, employee_data)
            connection.commit()  # Valider la transaction

            # Récupérer l'ID de l'employé nouvellement inséré
            employee_id = cursor.lastrowid
            print("Insertion réussie. ID de l'employé :", employee_id)
            return employee_id

    except Error as e:
        print(f"Error while connecting to MySQL: {e}")
    finally:
        if (connection.is_connected()):
            cursor.close()
            connection.close()
            print("MySQL connection is closed")

if input("Enregistrer l'employer dans la base de donnée:") == 'y' :
    id_employe = connect_to_database(nom , prenom)
else :
    id_employe = 1




import os
import shutil

# Chemins des dossiers
source_dir = './output/detected'
destination_base_dir = './dataset'
destination_dir = os.path.abspath(os.path.join(destination_base_dir, f'{id_employe}_{nom}_{prenom}'))
label_file_path = os.path.join(destination_base_dir, 'label.txt')

if input("Transfert dans dataset ? ") == 'y' :
    # Vérifiez si le dossier source existe
    if os.path.exists(source_dir)  :
        # Créez le chemin complet du dossier de destination s'il n'existe pas
        os.makedirs(destination_dir, exist_ok=True)
        
        # Liste des fichiers dans le dossier source
        files = os.listdir(source_dir)
        
        # Ouvrez le fichier label.txt en mode ajout
        with open(label_file_path, 'a') as label_file:
            # Déplacez et renommez chaque fichier
            for index, file_name in enumerate(files):
                # Chemin complet du fichier source
                source_file = os.path.join(source_dir, file_name)
                # Nouveau nom de fichier avec l'incrémentation
                new_file_name = f"{id_employe}_{nom}_{prenom}_{index + 1}{os.path.splitext(file_name)[1]}"
                # Chemin complet du fichier de destination
                destination_file = os.path.join(destination_dir, new_file_name)
                
                # Déplacez et renommez le fichier
                shutil.move(source_file, destination_file)
                
                # Chemin relatif du fichier pour l'entrée dans label.txt
                relative_path = os.path.relpath(destination_file, destination_base_dir).replace("\\", "/")
                # Écrire l'entrée dans label.txt
                label_file.write(f"./{relative_path}\t{id_employe}_{prenom}_{nom}\n")
        
        print("Tous les fichiers ont été déplacés, renommés, et label.txt a été mis à jour avec succès.")
    else:
        print("Le dossier source n'existe pas.")
    
    
    
########## BUILD MODEL BIN

if input("Build Model ? y or n :") == 'y' :
    parser = face.parser()
    args = parser.parse_args()
    args.build_index = "./dataset/index.bin"
    args.img_dir = "./dataset"
    args.label = "./dataset/label.txt"
    predictor = face.InsightFace(args)
    predictor.build_index()

