import os

def rename_images_with_labels(folder_path):
    # Obtenez la liste des fichiers dans le dossier
    files = os.listdir(folder_path)
    
    # Boucle à travers les fichiers et les renommer avec des étiquettes numériques
    for i, file_name in enumerate(files):
        if file_name.endswith('.png'):
            label = i + 1  # Utilisez i + 1 car les indices commencent à 0
            new_name = f"{label}.png"
            file_path = os.path.join(folder_path, file_name)
            new_path = os.path.join(folder_path, new_name)
            os.rename(file_path, new_path)
            print(f"Renommage de {file_name} à {new_name}")

# Chemins des dossiers "train" et "test"
train_folder_path = 'image_folder_logo/train'
test_folder_path = 'image_folder_logo/test'

# Renommer les images dans les dossiers "train" et "test"
rename_images_with_labels(train_folder_path)
rename_images_with_labels(test_folder_path)

# Chemins des dossiers "train" et "test"
train_folder_path = 'image_folder_no_logo/train'
test_folder_path = 'image_folder_no_logo/test'

# Renommer les images dans les dossiers "train" et "test"
rename_images_with_labels(train_folder_path)
rename_images_with_labels(test_folder_path)