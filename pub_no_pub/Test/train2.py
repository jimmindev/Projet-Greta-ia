import os
import numpy as np
import tensorflow as tf
from tensorflow.keras import layers, models
from tensorflow.keras.preprocessing.image import ImageDataGenerator

# Chemins des dossiers
train_logo_dir = 'dataset_jim/train/'
train_nologo_dir = 'dataset_jim/validation/'

# Paramètres du modèle
img_height, img_width = 128, 128
batch_size = 32

# Prétraitement des données
train_datagen = ImageDataGenerator(rescale=1./255)

train_logo_generator = train_datagen.flow_from_directory(
    train_logo_dir,
    target_size=(img_height, img_width),
    batch_size=batch_size,
    class_mode='binary'
)

train_nologo_generator = train_datagen.flow_from_directory(
    train_nologo_dir,
    target_size=(img_height, img_width),
    batch_size=batch_size,
    class_mode='binary'
)

# Création du modèle CNN
model = models.Sequential()

model.add(layers.Conv2D(32, (3, 3), activation='relu', input_shape=(img_height, img_width, 3)))
model.add(layers.MaxPooling2D((2, 2)))

model.add(layers.Conv2D(64, (3, 3), activation='relu'))
model.add(layers.MaxPooling2D((2, 2)))

model.add(layers.Dropout(0.5))  # Ajout d'une couche de Dropout pour régularisation

model.add(layers.Flatten())
model.add(layers.Dense(64, activation='relu'))
model.add(layers.Dense(1, activation='sigmoid'))  # Binary classification (logo or not)

# Compilation du modèle
model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

# Entraînement du modèle
epochs = 10
history = model.fit(
    train_logo_generator,
    steps_per_epoch=train_logo_generator.samples // batch_size,
    epochs=epochs,
    validation_data=train_nologo_generator,
    validation_steps=train_nologo_generator.samples // batch_size
)

# Sauvegarde du modèle
model.save('model_data_set_jim.h5')
