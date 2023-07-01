import cv2
import supervision as sv
import torch
import pytorch_lightning as pl
from transformers import DetrForObjectDetection, DetrImageProcessor
from PIL import Image
import numpy as np
from torchvision.utils import draw_bounding_boxes





DEVICE = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')
CHECKPOINT = 'facebook/detr-resnet-50'
CONFIDENCE_TRESHOLD = 0.5
IOU_TRESHOLD = 0.8
image_processor = DetrImageProcessor.from_pretrained(CHECKPOINT, ignore_mismatched_sizes  = True )
model = DetrForObjectDetection.from_pretrained(CHECKPOINT, ignore_mismatched_sizes  = True)


model.load_state_dict(torch.load("vehicle_det.pth", map_location = DEVICE), strict = False)


categories = {0: {'id': 0, 'name': 'cars', 'supercategory': 'none'},
 1: {'id': 1, 'name': 'biker', 'supercategory': 'cars'},
 2: {'id': 2, 'name': 'pedestrian', 'supercategory': 'cars'},
 3: {'id': 3, 'name': 'car', 'supercategory': 'cars'},
 4: {'id': 4, 'name': 'trafficLight', 'supercategory': 'cars'}}

id2label = {k: v['name'] for k,v in categories.items()}
label2id = {v['name']: k for k,v in categories.items()}
box_annotator = sv.BoxAnnotator()



def predict():
    image = np.asarray(Image.open("static/inputImage.jpg"))


    with torch.no_grad():

        # load image and predict
        inputs = image_processor(images=image, return_tensors='pt')
        outputs = model(**inputs)

        # post-process
        target_sizes = torch.tensor([image.shape[:2]])
        results = image_processor.post_process_object_detection(
            outputs=outputs, 
            threshold=CONFIDENCE_TRESHOLD, 
            target_sizes=target_sizes
        )[0]

    # annotate
    detections = sv.Detections.from_transformers(transformers_results=results).with_nms(threshold=0.5)
    print(detections[0])
    labels = [f"{id2label[class_id]} {confidence:.2f}" for _, mask, confidence, class_id, _ in detections if class_id <= 4]
    xys = [xyxy for xyxy, mask, confidence, class_id, _ in detections if class_id <= 4]
    print(labels)
    palette = ["orange", "blue", "green", "pink", "black"]
    colors = [palette[label2id[_.split()[0]]] for _ in labels]
    for i in range(len(labels)):
        print(xys[i][0])
        cv2.rectangle(image, (int(xys[i][0]), int(xys[i][1])), (int(xys[i][2]), int(xys[i][3])), (0, 255, 0), 2)
        cv2.putText(image, labels[i], (int(xys[i][0]), int(xys[i][1])), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2, cv2.LINE_AA)
    # frame = box_annotator.annotate(scene=image.copy(), detections=detections, labels=labels )
    cv2.imwrite("static/output.jpg", cv2.cvtColor(image, cv2.COLOR_RGB2BGR))
