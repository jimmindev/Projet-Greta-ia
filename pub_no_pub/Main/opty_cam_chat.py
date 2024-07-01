import cv2
import numpy as np
from tensorflow.keras.models import load_model
import time

# Charger le modèle pré-entraîné
model = load_model('model_data_set_jim.h5')

# Informations de la caméra
# (Assuming you have valid camera credentials)
camera_ip = "192.168.20.37"
camera_port = 88
camera_username = "dev_IA_P3"
camera_password = "dev_IA_P3"

# URL du flux vidéo principal (haute qualité) via RTSP
video_url_main = f"rtsp://{camera_username}:{camera_password}@{camera_ip}:{camera_port}/videoMain"

# Ouvrir le flux vidéo avec OpenCV
cap = cv2.VideoCapture(video_url_main)

if not cap.isOpened():
    print("Impossible d'ouvrir le flux vidéo.")
    exit()

# Liste des coordonnées et tailles de boîtes
boxes = [
    (1340, 50, 155, 155),
    (1340, 555, 155, 155),
    (365, 520, 155, 155),
    (390, 50, 155, 155)
]

# Variables de suivi des prédictions par boîte
prediction_history = {i: [] for i in range(len(boxes))}
history_duration = 5  # Durée en secondes pour la moyenne des prédictions
history_frames = int(cap.get(cv2.CAP_PROP_FPS) * history_duration)

# Variable pour suivre le temps de traitement
last_process_time = time.time()

# Nombre de snapshots à prendre
num_snapshots = 10

# Compteur de logos détectés
logo_counter = 0

while True:
    # Lire le flux vidéo H.264
    ret, frame = cap.read()

    if not ret:
        print("Impossible de lire la trame vidéo.")
        break

    # Prédiction pour chaque boîte
    for i, box in enumerate(boxes):
        box_x, box_y, box_width, box_height = box

        # Extraire la région d'intérêt (ROI) correspondant à chaque boîte
        roi = frame[box_y:box_y + box_height, box_x:box_x + box_width]

        # Prétraitement de l'image pour la détection du logo
        input_image = cv2.resize(roi, (155, 155))  # Ajustez la taille en fonction du modèle
        input_image = np.expand_dims(input_image, axis=0) / 255.0

        # Prédiction avec le modèle
        prediction = model.predict(input_image)[0]

        # Ajouter la prédiction à l'historique
        prediction_history[i].append(prediction)

        # Garder l'historique à la taille spécifiée
        if len(prediction_history[i]) > history_frames:
            prediction_history[i] = prediction_history[i][-history_frames:]

        # Calculer la moyenne des prédictions sur l'historique
        avg_prediction = np.mean(prediction_history[i])

        # Dessiner les boîtes rouges ou vertes en fonction de la prédiction moyenne
        color = (0, 0, 255) if avg_prediction > 0.5 else (0, 255, 0)
        cv2.rectangle(frame, (box_x, box_y), (box_x + box_width, box_y + box_height), color, 2)

        # Afficher le texte "logo" ou "no logo" avec la probabilité moyenne
        proba_text = np.format_float_positional(avg_prediction, precision=2)
        label = f"Box {i + 1} no logo: {proba_text}" if avg_prediction > 0.5 else f"Box {i + 1} logo: {proba_text}"
        label_color = (0, 0, 255) if avg_prediction > 0.5 else (0, 255, 0)
        cv2.putText(frame, label, (box_x, box_y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, label_color, 2)

        # Vérifier si un logo est détecté
        if avg_prediction > 0.5:
            logo_counter += 1

    # Afficher la trame vidéo avec les boîtes
    cv2.imshow("Flux vidéo en direct", frame)

    # Vérifier si une seconde s'est écoulée depuis le dernier traitement
    current_time = time.time()
    if current_time - last_process_time >= 1:
        # Mettre à jour le dernier temps de traitement
        last_process_time = current_time

        # Vérifier si le nombre de snapshots requis a été atteint
        if logo_counter >= num_snapshots:
            print(f"Nombre de logos détectés dans les {history_duration} dernières secondes: {logo_counter}")
            logo_counter = 0  # Réinitialiser le compteur pour le prochain intervalle de temps

    # Attendre 1 milliseconde pour détecter les événements clavier
    key = cv2.waitKey(1)

    # Quitter la boucle si la touche 'q' est enfoncée
    if key == ord('q'):
        break

# Libérer les ressources
cap.release()
cv2.destroyAllWindows()
