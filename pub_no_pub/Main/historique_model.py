import numpy as np
import matplotlib.pyplot as plt

# Chargement du fichier d'historique
history_filepath = 'history_split_20.npy'
history = np.load(history_filepath, allow_pickle=True).item()

# Tracer les courbes d'apprentissage
plt.plot(history['accuracy'], label='Training Accuracy')
plt.plot(history['val_accuracy'], label='Validation Accuracy')

# Ajouter des titres et des légendes
plt.title('Training and Validation Accuracy')
plt.xlabel('Epoch')
plt.ylabel('Accuracy')
plt.legend()
plt.show()
