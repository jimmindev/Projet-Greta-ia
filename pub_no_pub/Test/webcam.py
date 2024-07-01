import cv2
import numpy as np
from tensorflow import keras

# Charger le modèle Keras pré-entraîné
model_path = 'model_data_set_jim.h5'  # Remplacez par le chemin de votre modèle
model = keras.models.load_model(model_path)

# Définir la taille cible des images
target_size = (128, 128)

# Fonction pour effectuer une prédiction sur une image
def predict_image(image):
    # Redimensionner l'image à la taille cible
    image = cv2.resize(image, target_size)
    image = np.expand_dims(image, axis=0)  # Ajouter une dimension pour obtenir un lot (batch)
    
    # Effectuer la prédiction
    prediction = model.predict(image)
    probability = prediction[0][0]  # Récupérer la probabilité de classe positive (ou négative)
    
    return prediction, probability

# Capturer la vidéo depuis la webcam
cap = cv2.VideoCapture(0)  # 0 indique la première webcam, changez-le si nécessaire

while True:
    ret, frame = cap.read()  # Lire une image de la webcam
    
    if not ret:
        break  # Quitter la boucle si la capture échoue
    
    # Effectuer une prédiction sur l'image
    prediction, probability = predict_image(frame)
    
    # Afficher la prédiction et la probabilité en direct sur l'image
    if probability >= 0.4:
        result = "C'est une publicite"
    else:
        result = "Ce n'est pas une publicite"
    
    cv2.putText(frame, result, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    cv2.putText(frame, f"Probabilité : {probability:.2%}", (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
    
    # Afficher l'image en direct
    cv2.imshow("Webcam", frame)
    
    # Quitter la boucle en appuyant sur la touche 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Libérer la webcam et fermer les fenêtres OpenCV
cap.release()
cv2.destroyAllWindows()