import cv2
import supervision as sv
import torch
import pytorch_lightning as pl
from transformers import DetrForObjectDetection


class Detr(pl.LightningModule):

    def __init__(self, lr, lr_backbone, weight_decay):
        super().__init__()
        self.model = DetrForObjectDetection.from_pretrained(
            pretrained_model_name_or_path= "Deployment/ObjectDetectionModel-state.pth", 
            num_labels=len(id2label),
            ignore_mismatched_sizes=True
        )
        
        self.lr = lr
        self.lr_backbone = lr_backbone
        self.weight_decay = weight_decay

    def forward(self, pixel_values, pixel_mask):
        return self.model(pixel_values=pixel_values, pixel_mask=pixel_mask)

    def common_step(self, batch, batch_idx):
        pixel_values = batch["pixel_values"]
        pixel_mask = batch["pixel_mask"]
        labels = [{k: v.to(self.device) for k, v in t.items()} for t in batch["labels"]]

        outputs = self.model(pixel_values=pixel_values, pixel_mask=pixel_mask, labels=labels)

        loss = outputs.loss
        loss_dict = outputs.loss_dict

        return loss, loss_dict

    def training_step(self, batch, batch_idx):
        loss, loss_dict = self.common_step(batch, batch_idx)     
        # logs metrics for each training_step, and the average across the epoch
        self.log("training_loss", loss)
        for k,v in loss_dict.items():
            self.log("train_" + k, v.item())

        return loss

    def validation_step(self, batch, batch_idx):
        loss, loss_dict = self.common_step(batch, batch_idx)     
        self.log("validation/loss", loss)
        for k, v in loss_dict.items():
            self.log("validation_" + k, v.item())
            
        return loss

    def configure_optimizers(self):
        param_dicts = [
            {
                "params": [p for n, p in self.named_parameters() if "backbone" not in n and p.requires_grad]},
            {
                "params": [p for n, p in self.named_parameters() if "backbone" in n and p.requires_grad],
                "lr": self.lr_backbone,
            },
        ]
        return torch.optim.AdamW(param_dicts, lr=self.lr, weight_decay=self.weight_decay)
    

DEVICE = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')
CHECKPOINT = 'facebook/detr-resnet-50'
CONFIDENCE_TRESHOLD = 0.5
IOU_TRESHOLD = 0.8

categories = {0: {'id': 0, 'name': 'cars-trafficlights-pedestrian-', 'supercategory': 'none'},
 1: {'id': 1, 'name': 'biker', 'supercategory': 'cars-trafficlights-pedestrian-'},
 2: {'id': 2, 'name': 'car', 'supercategory': 'cars-trafficlights-pedestrian-'},
 3: {'id': 3, 'name': 'pedestrian', 'supercategory': 'cars-trafficlights-pedestrian-'},
 4: {'id': 4, 'name': 'trafficLight', 'supercategory': 'cars-trafficlights-pedestrian-'},
 5: {'id': 5, 'name': 'trafficLight-Green', 'supercategory': 'cars-trafficlights-pedestrian-'},
 6: {'id': 6, 'name': 'trafficLight-GreenLeft', 'supercategory': 'cars-trafficlights-pedestrian-'},
 7: {'id': 7, 'name': 'trafficLight-Red', 'supercategory': 'cars-trafficlights-pedestrian-'},
 8: {'id': 8, 'name': 'trafficLight-RedLeft', 'supercategory': 'cars-trafficlights-pedestrian-'},
 9: {'id': 9, 'name': 'trafficLight-Yellow', 'supercategory': 'cars-trafficlights-pedestrian-'},
 10: {'id': 10, 'name': 'trafficLight-YellowLeft', 'supercategory': 'cars-trafficlights-pedestrian-'},
 11: {'id': 11, 'name': 'truck', 'supercategory': 'cars-trafficlights-pedestrian-'}}

id2label = {k: v['name'] for k,v in categories.items()}
box_annotator = sv.BoxAnnotator()



image_path = "static/inputImage.jpg"
image = cv2.imread(image_path)



model = Detr(lr=1e-4, lr_backbone=1e-5, weight_decay=1e-4)
model.load_state_dict(torch.load("ObjectDetectionModel-state"))
model.to(DEVICE)




def predict():
    # inference
    with torch.no_grad():

        # load image and predict
        inputs = image_processor(images=image, return_tensors='pt').to(DEVICE)
        outputs = model(**inputs)

        # post-process
        target_sizes = torch.tensor([image.shape[:2]]).to(DEVICE)
        results = image_processor.post_process_object_detection(
            outputs=outputs, 
            threshold=CONFIDENCE_TRESHOLD, 
            target_sizes=target_sizes
        )[0]

    # annotate
    detections = sv.Detections.from_transformers(transformers_results=results).with_nms(threshold=0.5)
    labels = [f"{id2label[class_id]} {confidence:.2f}" for _, confidence, class_id, _ in detections]
    frame = box_annotator.annotate(scene=image.copy(), detections=detections, labels=labels)


    cv2.imsave(frame, "static/output.jpg")