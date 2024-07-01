import insightface_paddle_face as face
import logging
import cv2
import time

logging.basicConfig(level=logging.INFO)

parser = face.parser()
args = parser.parse_args()

args.det = True
args.rec = True
args.index = "./dataset/index.bin"
args.output = "./output/online"


# Capture an image from the camera
cap = cv2.VideoCapture(0)  # Open the default camera (0)
if not cap.isOpened():
    print("Error: Could not open camera.")
    exit()

ret, frame = cap.read()
cap.release()  # Release the camera

if not ret:
    print("Error: Could not read frame from camera.")
    exit()

# Convert the image from BGR (OpenCV format) to RGB
img = frame#[:, :, ::-1]

# Initialize the InsightFace predictor
predictor = face.InsightFace(args)

# Perform the prediction
res = predictor.predict(img, print_info=True)

# Manually draw the bounding boxes to avoid the issue
def draw_boxes(image, box_list, labels):
    for i, dt in enumerate(box_list):
        bbox, score = dt[2:], dt[1]
        label = labels[i]
        color = (0, 255, 0)  # Green color for bounding boxes
        
        x0, y0, x1, y1 = bbox
        # Ensure x1 >= x0 and y1 >= y0
        if x1 >= x0 and y1 >= y0:
            cv2.rectangle(image, (int(x0), int(y0)), (int(x1), int(y1)), color, 2)
            cv2.putText(image, f"{label} {score:.4f}", (int(x0), int(y0)-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
        else:
            print(f"Invalid box coordinates skipped: {bbox}")

# Process the results manually
for detection in res:
    try:
        bbox_list = detection['box_list']
        print("bbox_list : " , bbox_list)
        labels = detection['labels']
        print(labels)
        draw_boxes(frame, bbox_list, labels)
    except Exception as e:
        print(f"Error processing detection: {e}")

