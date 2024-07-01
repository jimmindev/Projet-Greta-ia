import numpy as np
import matplotlib.pyplot as plt

# Replace 'your_file.npy' with the actual file path
file_path = 'history_split_40.npy'

# Load the .npy file
data = np.load(file_path, allow_pickle=True).item()

# Plot the training and validation accuracy
plt.plot(data['accuracy'], label='Training Accuracy')
plt.plot(data['val_accuracy'], label='Validation Accuracy')
plt.title('Training and Validation Accuracy')
plt.xlabel('Epoch')
plt.ylabel('Accuracy')
plt.legend()
plt.show()
