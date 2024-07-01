import cv2
import numpy as np  # Add this line to import NumPy
import matplotlib.pyplot as plt
from tensorflow.keras.models import load_model

# Load the model
model = load_model('best_model.h5')

# Function to preprocess an image
# Function to preprocess an image
def preprocess_image(image_path):
    img = cv2.imread(image_path)

    # Check if the image is loaded successfully
    if img is None:
        print(f"Error: Unable to load image from {image_path}")
        return None

    img = cv2.resize(img, (155, 155))
    img = np.expand_dims(img, axis=0) / 255.0
    return img


# Function to predict and display the result
# Function to predict and display the result
def predict_and_display(image_path, label):
    test_image = preprocess_image(image_path)
    # Check if the image loading failed
    if test_image is None:
        print(f"Skipping prediction for {image_path}")
        return
    prediction = model.predict(test_image)
    # Extract the scalar value from the NumPy array
    prediction_scalar = prediction[0][0]
    # Read the image for display
    img = cv2.imread(image_path)
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    # Display the image with prediction result
    plt.imshow(img_rgb)
    plt.title(f"Prediction: {label}\nProbability: {prediction_scalar:.2f}")  # Use prediction_scalar here
    plt.axis('off')
    plt.show()


# Example image paths
logo_example_path = 'Z:/jimmy/camera_ip/main/output_crop/cropped_1709045031_1_top_right.jpg'
no_logo_example_path = 'Z:/jimmy/camera_ip/main/output_crop/cropped_1709045032_2_bottom_right.jpg'

# Predict and display example with logo
predict_and_display(logo_example_path, label='Logo')

# Predict and display example with no logo
predict_and_display(no_logo_example_path, label='No Logo')
