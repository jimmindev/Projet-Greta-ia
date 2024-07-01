from flask import Flask, Response
from flask_cors import CORS  # Ajoutez cette ligne pour gérer CORS
import cv2

app = Flask(__name__)
CORS(app)  # Active CORS pour tous les domaines (peut être ajusté en fonction de vos besoins)

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

def generate_frames():
    while True:
        # Lire le flux vidéo H.264
        ret, frame = cap.read()

        if not ret:
            print("Impossible de lire la trame vidéo.")
            break

        # Convertir la trame en format JPEG
        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()

        # Renvoyer la trame en tant que flux binaire
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

@app.route('/video_feed')
def video_feed():
    # Renvoyer le flux vidéo en tant que réponse HTTP avec le bon type MIME
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)

# Libérer les ressources (sera appelé lors de la fermeture de l'application Flask)
@app.teardown_appcontext
def cleanup_camera(exception=None):
    cap.release()
    cv2.destroyAllWindows()
