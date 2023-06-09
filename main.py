import cv2
from ultralyticsplus import YOLO, render_result

# load model
model = YOLO('keremberke/yolov8n-pothole-segmentation')

# set model parameters
model.overrides['conf'] = 0.25  # NMS confidence threshold
model.overrides['iou'] = 0.45  # NMS IoU threshold
model.overrides['agnostic_nms'] = False  # NMS class-agnostic
model.overrides['max_det'] = 1000  # maximum number of detections per image

# Open the default camera
cap = cv2.VideoCapture(0)

# Check if the camera is opened successfully
if not cap.isOpened():
    print("Failed to open the camera")
    exit()

while True:
    # Read frame from the camera
    ret, frame = cap.read()

    # Check if the frame is read successfully
    if not ret:
        print("Failed to capture frame")
        break

    # # Convert the frame to grayscale
    # gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)

    # perform inference
    results = model.predict(frame)
    # observe results
    print(results[0])
    # time.sleep(0.5)

    # Display the grayscale frame
    cv2.imshow("Grayscale Frame", frame)

    # Exit if 'q' is pressed
    if cv2.waitKey(1) == ord('q'):
        break

# Release the camera and close windows
cap.release()
cv2.destroyAllWindows()