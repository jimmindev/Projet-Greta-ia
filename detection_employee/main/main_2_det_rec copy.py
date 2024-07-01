import insightface_paddle_face as face
import logging
import cv2
import time
import mysql.connector
import os

logging.basicConfig(level=logging.INFO)

# Parser les arguments
parser = face.parser()
args = parser.parse_args()

# Configuration des paramètres du modèle
args.det = True
args.rec = True
args.index = "./dataset/index.bin"
args.output = "./output/online"

# Initialiser le prédicteur InsightFace
predictor = face.InsightFace(args)

# Configuration de la base de données
config_bdd = {
    'host': '192.168.0.17',
    'database': 'Cam_Auto_Badge',
    'user': 'jimmy',
    'password': 'Ey4@WKIF!3lm)e*y'
}

# Connexion à la base de données
conn = mysql.connector.connect(**config_bdd)
cursor = conn.cursor()

# Assurer l'existence du répertoire de sortie des images
os.makedirs(args.output, exist_ok=True)

# Capturer une image depuis la caméra
cap = cv2.VideoCapture(0)  # Ouvrir la caméra par défaut (0)
if not cap.isOpened():
    logging.error("Impossible d'ouvrir la caméra.")
    exit()

while True:
    ret, frame = cap.read()
    if not ret:
        logging.error("Impossible de lire l'image depuis la caméra.")
        break

    # Convertir l'image de format BGR (OpenCV) en format RGB
    img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Effectuer la prédiction
    res = predictor.predict(img, print_info=True)

    # Dessiner manuellement les boîtes de délimitation pour éviter les problèmes
    def draw_boxes(image, box_list, labels):
        for i, dt in enumerate(box_list):
            bbox, score = dt[2:], dt[1]
            label = labels[i]
            color = (0, 255, 0)  # Couleur verte pour les boîtes de délimitation
            
            x0, y0, x1, y1 = bbox
            # S'assurer que x1 >= x0 et y1 >= y0
            if x1 >= x0 and y1 >= y0:
                cv2.rectangle(image, (int(x0), int(y0)), (int(x1), int(y1)), color, 2)
                cv2.putText(image, f"{label} {score:.4f}", (int(x0), int(y0)-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
            else:
                logging.warning(f"Coordonnées de la boîte non valides : {bbox}")

    # Traiter les résultats manuellement
    for detection in res:
        try:
            bbox_list = detection['box_list']
            labels = detection['labels']
            draw_boxes(frame, bbox_list, labels)

            # Enregistrer la présence et l'image
            timestamp = time.strftime("%Y%m%d-%H%M%S")
            for label in labels:
                parts = label.split('_')
                if len(parts) == 3:
                    employee_id, last_name, first_name = parts
                else:
                    if label != "unknown" :
                        logging.warning(f"Format de libellé non valide : {label}")
                    continue

                # Enregistrer l'image dans le répertoire de l'employé
                employee_dir = os.path.join(args.output, f"{employee_id}_{last_name}_{first_name}")
                os.makedirs(employee_dir, exist_ok=True)
                image_path = os.path.join(employee_dir, f"{label}_{timestamp}.jpg")
                cv2.imwrite(image_path, frame)

                # Obtenir l'heure actuelle
                current_time = time.strftime('%Y-%m-%d %H:%M:%S')

                # Insérer un enregistrement de log dans la table Logs
                cursor.execute("""
                    INSERT INTO Logs (dossier_log, id_version)
                    VALUES (%s, (SELECT id_version FROM versions ORDER BY id_version DESC LIMIT 1))
                """, (image_path,))
                log_id = cursor.lastrowid  # Obtenir le dernier ID inséré

                # Insérer un enregistrement de passage dans la table Passages
                cursor.execute("INSERT INTO Passages (horaire_passage, entree_sortie_passage, id_employe, id_log) VALUES (%s, %s, %s, %s)",
                               (current_time, '0', employee_id, log_id))

                # Valider les modifications dans la base de données
                conn.commit()

                print(f"Présence enregistrée pour {last_name} {first_name} (ID: {employee_id}) à {timestamp} avec l'image {image_path}")

        except Exception as e:
            logging.error(f"Erreur lors du traitement de la détection : {e}")

# Libérer la caméra
cap.release()

# Fermer la connexion à la base de données
conn.close()
