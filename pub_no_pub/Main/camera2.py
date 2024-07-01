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

# Initialiser les coordonnées et la taille de la boîte
box_x, box_y, box_width, box_height = 50, 50, 100, 100

while True:
    # Lire le flux vidéo H.264
    ret, frame = cap.read()

    if not ret:
        print("Impossible de lire la trame vidéo.")
        break

    # Dessiner la boîte rouge
    cv2.rectangle(frame, (box_x, box_y), (box_x + box_width, box_y + box_height), (0, 0, 255), 2)

    # Afficher les coordonnées X et Y au milieu de l'écran
    text = f"X: {box_x}\nY: {box_y}\nbox_width : {box_width}\nbox_height : {box_height}"
    cv2.putText(frame, text, (int(frame.shape[1] / 2) - 100, int(frame.shape[0] / 2) - 50),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)

    # Afficher la trame vidéo avec la boîte
    cv2.imshow("Flux vidéo en direct", frame)

    # Attendre 1 milliseconde pour détecter les événements clavier
    key = cv2.waitKey(1)

    # Déplacer la boîte avec les touches directionnelles
    if key == ord('q'):  # Flèche gauche
        box_x -= 5
    elif key == ord('z'):  # Flèche up
        box_y -= 5
    elif key == ord('d'):  # Flèche droite
        box_x += 5
    elif key == ord('s'):  # Flèche down
        box_y += 5

    # Ajuster la taille de la boîte avec les touches '+' et '-'
    elif key == ord('+'):
        box_width += 5
        box_height += 5
    elif key == ord('-'):
        box_width -= 5
        box_height -= 5

    # Quitter la boucle si la touche 'q' est enfoncée
    elif key == ord('a'):
        break

# Libérer les ressources
cap.release()
cv2.destroyAllWindows()
