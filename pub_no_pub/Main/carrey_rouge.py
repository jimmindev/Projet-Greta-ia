import cv2

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

while True:
    # Lire le flux vidéo H.264
    ret, frame = cap.read()

    if not ret:
        print("Impossible de lire la trame vidéo.")
        break

    # Dessiner les boîtes rouges
    for box in boxes:
        box_x, box_y, box_width, box_height = box
        cv2.rectangle(frame, (box_x, box_y), (box_x + box_width, box_y + box_height), (0, 0, 255), 2)

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
