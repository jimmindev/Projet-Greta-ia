import insightface_paddle_face as face
import logging
from tqdm import tqdm
import cv2

logging.basicConfig(level=logging.INFO)

parser = face.parser()
args = parser.parse_args()

args.det = True
args.output = "./output"

def video_crop(input_path) :
    # Ouvrir la vidéo avec OpenCV pour obtenir le nombre total de frames
    cap = cv2.VideoCapture(input_path)
    if not cap.isOpened():
        print("Erreur : Impossible d'ouvrir la vidéo")
        exit()
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    cap.release()

    # Prédiction des visages
    Logs = False
    predictor = face.InsightFace(args,Logs)
    res = predictor.predict(input_path)

    with tqdm(total=total_frames, desc="Detection progress", unit="frames") as pbar:
        for result in res:
            pbar.update(1)  # Mettre à jour d'une frame à la fois
            
    return 1