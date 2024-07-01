import cv2
import os
import numpy as np
import tensorflow as tf

# Charger le modèle de détection d'objets pré-entraîné (exemple avec MobileNetV2)
model = tf.keras.applications.MobileNetV2(weights="imagenet", include_top=True)
model.summary()

# Répertoire contenant les images avec les coins de la télévision
dataset_path = "C:/dataset2"

# Répertoire de sauvegarde pour les résultats
output_path = "C:/results"
os.makedirs(output_path, exist_ok=True)

# Liste des classes (labels) du modèle ImageNet
imagenet_labels = tf.keras.utils.get_file('ImageNetLabels.txt', 'https://storage.googleapis.com/download.tensorflow.org/data/ImageNetLabels.txt')
with open(imagenet_labels) as f:
    classes = [line.strip() for line in f.readlines()]

# Fonction de détection des logos de chaînes TV
def detect_channel_logos(image_path):
    # Charger l'image
    image = cv2.imread(image_path)
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # Redimensionner l'image à la taille attendue par le modèle
    image_resized = cv2.resize(image_rgb, (224, 224))

    # Prétraiter l'image pour le modèle
    input_array = tf.keras.applications.mobilenet_v2.preprocess_input(image_resized[tf.newaxis, ...])

    # Effectuer la prédiction avec le modèle
    predictions = model.predict(input_array)

    # Récupérer la classe prédite et la probabilité maximale
    predicted_class = np.argmax(predictions)
    confidence = predictions[0, predicted_class]

    # Récupérer le label de la classe prédite
    predicted_label = classes[predicted_class]

    # Afficher les résultats
    print(f"Predicted Label: {predicted_label}")
    print(f"Confidence: {confidence:.2f}")

    # Enregistrer une copie de l'image avec la prédiction
    output_image_path = os.path.join(output_path, f"result_{os.path.basename(image_path)}")
    cv2.putText(image, f"Prediction: {predicted_label}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    cv2.imwrite(output_image_path, image)

# Appliquer la détection des logos pour chaque image dans le dataset
for img_file in os.listdir(dataset_path):
    if img_file.endswith(".jpg"):
        image_path = os.path.join(dataset_path, img_file)
        detect_channel_logos(image_path)
