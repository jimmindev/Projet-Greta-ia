import os

def generate_labels_for_dataset(dataset_path):
    label_file_path = os.path.join(dataset_path, 'label.txt')
    
    with open(label_file_path, 'w') as label_file:
        # Parcourez chaque dossier dans le dataset
        for root, dirs, files in os.walk(dataset_path):
            for dir_name in dirs:
                dir_path = os.path.join(root, dir_name)
                # Vérifiez si le chemin est bien un sous-dossier direct du dataset
                if os.path.abspath(dir_path).startswith(os.path.abspath(dataset_path)) and dir_path != dataset_path:
                    # Parcourez chaque fichier dans le sous-dossier
                    for index, file_name in enumerate(os.listdir(dir_path)):
                        file_path = os.path.join(dir_path, file_name)
                        if os.path.isfile(file_path):
                            # Chemin relatif de l'image
                            relative_path = os.path.relpath(file_path, dataset_path).replace("\\", "/")
                            # Label correspondant
                            label = f"{dir_name}"
                            # Écrire l'entrée dans label.txt
                            label_file.write(f"./{relative_path}\t{label}\n")
    
    print("Le fichier label.txt a été créé et mis à jour avec succès.")

if input("Transfert dans dataset ? ") == 'y':
    dataset_path = './dataset'
    generate_labels_for_dataset(dataset_path)