import os
import numpy as np
import tensorflow as tf
from tensorflow.keras import layers, models
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.callbacks import ModelCheckpoint
import matplotlib.pyplot as plt

# Chemin du dossier principal
dataset_dir = 'c:/dataset3/france2'

# Paramètres du modèle
img_height, img_width = 155, 155
batch_size = 32

# Liste des proportions de données de validation
validation_splits = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]

# Variable pour suivre la meilleure précision de validation
best_val_accuracy = 0.0
best_model_checkpoint = ''

# Tracer les courbes d'apprentissage
for validation_split in validation_splits:
    # Prétraitement des données
    datagen = ImageDataGenerator(rescale=1./255, validation_split=validation_split)

    train_generator = datagen.flow_from_directory(
        dataset_dir,
        target_size=(img_height, img_width),
        batch_size=batch_size,
        class_mode='binary',
        subset='training'  # Utiliser la partie d'entraînement
    )

    validation_generator = datagen.flow_from_directory(
        dataset_dir,
        target_size=(img_height, img_width),
        batch_size=batch_size,
        class_mode='binary',
        subset='validation'  # Utiliser la partie validation
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
    model.add(layers.Dense(1, activation='sigmoid'))  # Classification binaire (logo ou non)

    # Compilation du modèle
    model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

    # Définition du callback pour sauvegarder le meilleur modèle
    checkpoint_filepath = f'model_checkpoint_split_{int(validation_split*100)}.h5'
    model_checkpoint_callback = ModelCheckpoint(
        filepath=checkpoint_filepath,
        save_best_only=True,
        monitor='val_accuracy',
        mode='max',
        verbose=1
    )

    # Entraînement du modèle
    epochs = 10
    history = model.fit(
        train_generator,
        steps_per_epoch=train_generator.samples // batch_size,
        epochs=epochs,
        validation_data=validation_generator,
        validation_steps=validation_generator.samples // batch_size,
        callbacks=[model_checkpoint_callback]
    )

    # Check if the current model's validation accuracy is better than the best recorded so far
    if history.history['val_accuracy'][-1] > best_val_accuracy:
        best_val_accuracy = history.history['val_accuracy'][-1]
        best_model_checkpoint = checkpoint_filepath

    # Sauvegarde de l'historique dans un fichier
    history_filepath = f'history_split_{int(validation_split*100)}.npy'
    np.save(history_filepath, history.history)

# Charger et sauvegarder le meilleur modèle à la fin
best_model = tf.keras.models.load_model(best_model_checkpoint)
best_model.save('best_model.h5')

# Tracer les courbes d'apprentissage à la fin
for validation_split in validation_splits:
    history_filepath = f'history_split_{int(validation_split*100)}.npy'
    history = np.load(history_filepath, allow_pickle=True).item()

    plt.plot(history['accuracy'], label=f'Training Accuracy (split={validation_split})')
    plt.plot(history['val_accuracy'], label=f'Validation Accuracy (split={validation_split})')

plt.title('Training and Validation Accuracy')
plt.xlabel('Epoch')
plt.ylabel('Accuracy')
plt.legend()
plt.show()