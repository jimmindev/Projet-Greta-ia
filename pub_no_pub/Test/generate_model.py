import os
import numpy as np
import tensorflow as tf
from tensorflow.keras import layers, models
from tensorflow.keras.preprocessing.image import ImageDataGenerator

def build_model(input_shape, dropout_rate=0.5):
    model = models.Sequential()
    model.add(layers.Conv2D(32, (3, 3), activation='relu', input_shape=input_shape))
    model.add(layers.MaxPooling2D((2, 2)))
    model.add(layers.Conv2D(64, (3, 3), activation='relu'))
    model.add(layers.MaxPooling2D((2, 2)))
    model.add(layers.Conv2D(128, (3, 3), activation='relu'))
    model.add(layers.MaxPooling2D((2, 2)))
    model.add(layers.Flatten())
    model.add(layers.Dense(128, activation='relu'))
    model.add(layers.Dropout(dropout_rate))
    model.add(layers.Dense(1, activation='sigmoid'))  # Binary classification

    model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
    return model

def train_model(train_data_dir, validation_data_dir, input_shape=(256, 256, 3), batch_size=32, epochs=10, dropout_rate=0.5):
    train_datagen = ImageDataGenerator(
        rescale=1./255,
        rotation_range=40,
        width_shift_range=0.2,
        height_shift_range=0.2,
        shear_range=0.2,
        zoom_range=0.2,
        horizontal_flip=True,
        fill_mode='nearest'
    )

    validation_datagen = ImageDataGenerator(rescale=1./255)

    train_generator = train_datagen.flow_from_directory(
        train_data_dir,
        target_size=(input_shape[0], input_shape[1]),
        batch_size=batch_size,
        class_mode='binary'
    )

    validation_generator = validation_datagen.flow_from_directory(
        validation_data_dir,
        target_size=(input_shape[0], input_shape[1]),
        batch_size=batch_size,
        class_mode='binary'
    )

    model = build_model(input_shape, dropout_rate)

    model.fit(
        train_generator,
        steps_per_epoch=train_generator.samples // batch_size,
        epochs=epochs,
        validation_data=validation_generator,
        validation_steps=np.ceil(validation_generator.samples / batch_size)
    )

    return model

if __name__ == "__main__":
    train_data_dir = "C:/Users/jimmy.inthalangsy/Documents/GitHub/jimmy.inthalangsy/Projets/pub_no_pub/Nouveau dossier/train/"
    validation_data_dir = "C:/Users/jimmy.inthalangsy/Documents/GitHub/jimmy.inthalangsy/Projets/pub_no_pub/Nouveau dossier/validation/"

    model = train_model(train_data_dir, validation_data_dir, epochs=20, dropout_rate=0.4)

    model.summary()
    
    # Sauvegarder le modèle
    model.save("logo_classification_model.h5")
