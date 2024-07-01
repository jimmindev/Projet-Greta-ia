import os
import cv2
import numpy as np
from keras.preprocessing.image import ImageDataGenerator

def is_rgb(img):
    return len(img.shape) == 3 and img.shape[2] == 3

def load_and_preprocess_image(image_path):
    # Normalize the path
    image_path_normalized = os.path.normpath(image_path)

    # Attempt to read the image
    img = cv2.imread(image_path_normalized)

    if img is None:
        print(f"Error: Unable to load image from {image_path_normalized}")
        return None

    # Check if the image is in RGB format
    if is_rgb(img):
        return img
    else:
        print(f"Error: Image {image_path_normalized} is not in RGB format.")
        return None

def resize_and_save(input_folder, output_folder, target_size=(256, 256)):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    files = os.listdir(input_folder)

    for file in files:
        image_path = os.path.join(input_folder, file)

        if os.path.isfile(image_path) and image_path.lower().endswith(('.png', '.PNG')):
            img = load_and_preprocess_image(image_path)

            if img is not None:
                img_resized = cv2.resize(img, target_size)
                output_path = os.path.join(output_folder, file)
                cv2.imwrite(output_path, img_resized)

def augment_and_save_images(input_folder, output_folder):
    resized_folder = os.path.join(output_folder, 'resized_images')
    resize_and_save(input_folder, resized_folder, target_size=(256, 256))

    datagen = ImageDataGenerator(
        rotation_range=40,
        width_shift_range=0.2,
        height_shift_range=0.2,
        shear_range=0.2,
        zoom_range=0.2,
        horizontal_flip=True,
        fill_mode='nearest'
    )

    files = os.listdir(resized_folder)

    for file in files:
        image_path = os.path.join(resized_folder, file)

        if os.path.isfile(image_path) and image_path.lower().endswith(('.png', '.PNG')):
            img = load_and_preprocess_image(image_path)

            if img is not None:
                # Expand dimensions for batch
                img_batch = np.expand_dims(img, axis=0)

                # Generate augmented images
                it = datagen.flow(img_batch, batch_size=1, save_to_dir=output_folder, save_prefix='aug', save_format='png')

                for _ in range(5):
                    batch = it.next()

if __name__ == "__main__":
    input_folder  = "C:/Users/jimmy.inthalangsy/Documents/GitHub/jimmy.inthalangsy/Projets/pub_no_pub/Nouveau dossier/image_folder/"
    output_folder = "C:/Users/jimmy.inthalangsy/Documents/GitHub/jimmy.inthalangsy/Projets/pub_no_pub/Nouveau dossier/saved_images_logo/"
    augment_and_save_images(input_folder, output_folder)

    input_folder  = "C:/Users/jimmy.inthalangsy/Documents/GitHub/jimmy.inthalangsy/Projets/pub_no_pub/Nouveau dossier/image_folder_no_logo/"
    output_folder = "C:/Users/jimmy.inthalangsy/Documents/GitHub/jimmy.inthalangsy/Projets/pub_no_pub/Nouveau dossier/saved_images_Nologo/"
    augment_and_save_images(input_folder, output_folder)