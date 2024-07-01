import os
import random
import pandas as pd
import tensorflow as tf
from tensorflow.keras import models   # Add this line
from tensorflow.keras import layers
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout

# Obtenez le chemin du répertoire courant
current_directory = os.getcwd()

# Définir les chemins des dossiers d'images
train_data_dir = os.path.join(current_directory, "dataset", "train")
test_data_dir = os.path.join(current_directory, "dataset", "validation")
train_data_dir_logo = os.path.join(train_data_dir, "class_1")
train_data_dir_no_logo = os.path.join(train_data_dir, "class_2")
test_data_dir_logo = os.path.join(test_data_dir, "class_1")
test_data_dir_no_logo = os.path.join(test_data_dir, "class_2")

# Fonction pour charger les images
def load_images_from_directory(directory):
    images = []
    labels = []
    for subdir, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.jpg') or file.endswith('.png'):
                images.append(os.path.join(subdir, file))
                labels.append(1 if "class_1" in subdir else 0)  # Assuming class_1 is logo, class_2 is no logo
    return images, labels

# Charger les images d'entraînement et de validation
train_images, train_labels = load_images_from_directory(train_data_dir)
test_images, test_labels = load_images_from_directory(test_data_dir)

# Créer un DataFrame pandas pour les données d'entraînement et de validation
train_df = pd.DataFrame({'filename': train_images, 'label': train_labels})
test_df = pd.DataFrame({'filename': test_images, 'label': test_labels})

# Convertir les valeurs des étiquettes en chaînes de caractères
train_df['label'] = train_df['label'].astype(str)
test_df['label'] = test_df['label'].astype(str)

# Créer des générateurs de données pour l'entraînement et la validation
batch_size = 64
train_datagen = tf.keras.preprocessing.image.ImageDataGenerator(rescale=1./255)
train_generator = train_datagen.flow_from_dataframe(
    train_df,
    x_col='filename',
    y_col='label',
    target_size=(100, 100),
    batch_size=batch_size,
    class_mode='binary',
    shuffle=True
)

test_datagen = tf.keras.preprocessing.image.ImageDataGenerator(rescale=1./255)
test_generator = test_datagen.flow_from_dataframe(
    test_df,
    x_col='filename',
    y_col='label',
    target_size=(100, 100),
    batch_size=batch_size,
    class_mode='binary',
    shuffle=False
)

# Créer un modèle CNN simple et continuer avec l'entraînement...

'''
# Créer un modèle CNN simple
model = Sequential([
    Conv2D(32, (3, 3), activation='relu', input_shape=(100, 100, 3)),
    MaxPooling2D((2, 2)),
    Conv2D(64, (3, 3), activation='relu'),
    MaxPooling2D((2, 2)),
    Conv2D(128, (3, 3), activation='relu'),
    MaxPooling2D((2, 2)),
    Flatten(),
    Dense(128, activation='relu'),
    Dense(1, activation='sigmoid')
])
'''
input_shape = (100, 100, 3)  # Assuming RGB images with size 100x100 pixels

# Créer un modèle CNN complexe
model = models.Sequential([
    layers.Conv2D(32, (3, 3), activation='relu', input_shape=input_shape),
    layers.MaxPooling2D((2, 2)),
    layers.Conv2D(64, (3, 3), activation='relu'),
    layers.MaxPooling2D((2, 2)),
    layers.Conv2D(128, (3, 3), activation='relu'),
    layers.MaxPooling2D((2, 2)),
    layers.Conv2D(256, (3, 3), activation='relu'),
    layers.MaxPooling2D((2, 2)),
    layers.Flatten(),
    layers.Dense(512, activation='relu'),
    layers.Dropout(0.5),
    layers.Dense(256, activation='relu'),
    layers.Dropout(0.5),
    layers.Dense(1, activation='sigmoid')
])

# Compiler le modèle
model.compile(optimizer='adam',
              loss='binary_crossentropy',
              metrics=['accuracy'])

# Entraîner le modèle
history = model.fit(
    train_generator,
    steps_per_epoch=train_generator.samples // batch_size,
    epochs=20,
    validation_data=test_generator,
    validation_steps=test_generator.samples // batch_size
)

# Sauvegarder le modèle
model.save("logo_detection_model.h5")

print("Entraînement terminé. Modèle sauvegardé sous 'logo_detection_model.h5'.")