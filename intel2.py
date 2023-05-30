import cv2
import numpy as np
from openvino.inference_engine import IECore
import sys

# Load the road sign detection model
model_xml = 'path/to/road_sign_detection_model.xml'
model_bin = 'path/to/road_sign_detection_model.bin'
ie = IECore()
net = ie.read_network(model=model_xml, weights=model_bin)
exec_net = ie.load_network(network=net, device_name='CPU')

# Define the classes corresponding to road signs
classes = ['Speed_limit_20_km/h'
,'Speed_limit_30_km/h'
,'Speed_limit__50_km/h'
,'Speed_limit_60_km/h'
,'Speed_limit_70_km/h'
,'Speed_limit_80_km/h'
,'End_of_speed_limit_(80 km/h)'
,'Speed_limit_100_km/h'
,'Speed_limit_120_km/h'
,'No_passing'
,'No_passing for vehicles over 3.5 metric tons'
,'Right-of-way_at_the next_intersection'
,'Priority_road'
,'Yield'
,'Stop'
,'No_vehicles'
,'Vehicles_over_3.5_metric_tons_prohibited'
,'No_entry'
,'General_caution'
,'Dangerous_curve_to_the_left'
,'Dangerous_curve-to_the_right'
,'Double_curve'
,'Bumpy_road'
,'Slippery_road'
,'Road_narrows_on_the_right'
,'Construction_zone'
,'Traffic_signal_ahead'
,'Pedestrian_crossing'
,'School_zone'
,'Bicycles_crossing'
,'Beware_of_ice/snow'
,'Wild_animals_crossing'
,'End_of_all_speed_and_passing_limits'
,'Turn_right_ahead'
,'Turn_left_ahead'
,'Ahead_only'
,'Go_straight_or_right'
,'Go_straight_or_left'
,'Keep_right'
,'Keep_left'
,'Roundabout_mandatory'
,'End_of_no_passing'
,'End_of_no_passing_by_vehicles_over_3.5_metric _tons']

# Initialize video capture
cap = cv2.VideoCapture(0)

while True:
    # Read frame from camera
    ret, frame = cap.read()
    if not ret:
        break

    # Preprocess the frame
    input_blob = cv2.dnn.blobFromImage(frame, size=(300, 300), ddepth=cv2.CV_8U)
    input_blob = np.transpose(input_blob, (0, 3, 1, 2))
    
    # Perform inference
    outputs = exec_net.infer(inputs={net.input_info['data'].input_name: input_blob})
    detections = outputs[net.output_info['detection_out'].output_name][0][0]

    # Process the detections
    for detection in detections:
        confidence = detection[2]
        if confidence > 0.5:
            class_id = int(detection[1])
            class_name = classes[class_id]
            
            # Get the coordinates of the detected road sign
            x1 = int(detection[3] * frame.shape[1])
            y1 = int(detection[4] * frame.shape[0])
            x2 = int(detection[5] * frame.shape[1])
            y2 = int(detection[6] * frame.shape[0])
            
            # Draw bounding box and label
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(frame, class_name, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

    # Display the frame
    cv2.imshow('Road Sign Detection', frame)
    
    # Exit if 'q' is pressed
    if cv2.waitKey(1) == ord('q'):
        break

# Release resources
cap.release()
cv2.destroyAllWindows()
