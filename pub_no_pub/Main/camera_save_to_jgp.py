import cv2
import os
import time

# Informations de la caméra
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

# Répertoire de sauvegarde
base_save_directory = "C:/dataset2"

# Créer le répertoire de base s'il n'existe pas
os.makedirs(base_save_directory, exist_ok=True)

# Délai entre chaque capture (en secondes)
capture_interval = 1

# Initialiser la variable last_capture_time
last_capture_time = time.time()

# Créer un dossier pour chaque boîte
box_directories = []
for i, box in enumerate(boxes):
    box_save_directory = os.path.join(base_save_directory, f"box_{i+1}")
    os.makedirs(box_save_directory, exist_ok=True)
    box_directories.append(box_save_directory)

# Compteur d'images global
image_counter = 1

while True:
    # Lire le flux vidéo H.264
    ret, frame = cap.read()

    if not ret:
        print("Impossible de lire la trame vidéo.")
        break

    # Dessiner les boîtes rouges
    for i, box in enumerate(boxes):
        box_x, box_y, box_width, box_height = box
        cv2.rectangle(frame, (box_x, box_y), (box_x + box_width, box_y + box_height), (0, 0, 255), 2)

    # Capturer et sauvegarder toutes les boîtes avec un délai constant
    if time.time() - last_capture_time >= capture_interval:
        for i, box in enumerate(boxes):
            box_x, box_y, box_width, box_height = box
            roi = frame[box_y:box_y + box_height, box_x:box_x + box_width]
            box_save_directory = box_directories[i]

            # Enregistrer l'image dans le dossier de la boîte
            save_path = os.path.join(box_save_directory, f"image_{image_counter}.jpg")
            cv2.imwrite(save_path, roi)

        # Incrémenter le compteur d'images global
        image_counter += 1

        # Réinitialiser le temps de capture
        last_capture_time = time.time()

    # Afficher la trame vidéo avec les boîtes
    cv2.imshow("Flux vidéo en direct", frame)

    # Attendre 1 milliseconde pour détecter les événements clavier
    key = cv2.waitKey(1)

    # Quitter la boucle si la touche 'q' est enfoncée
    if key == ord('q'):
        break

# Libérer les ressources
cap.release()
cv2.destroyAllWindows()
