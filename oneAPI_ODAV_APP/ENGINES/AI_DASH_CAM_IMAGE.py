import torch

def AI_DASH_CAM_IMAGE(source="0", model_weights="../Model/visual_pollution.pt"):

    import numpy as np
    import cv2
    from datetime import datetime
    import torch
    import torch.backends.cudnn as cudnn

    from models.experimental import attempt_load
    from utils.datasets import LoadStreams, LoadImages
    from utils.general import check_img_size, check_requirements, check_imshow, non_max_suppression, apply_classifier, \
        scale_coords, xyxy2xywh, strip_optimizer, set_logging, increment_path
    from utils.plots import plot_one_box
    from utils.torch_utils import select_device, load_classifier, time_synchronized, TracedModel

    device = 'cuda' if torch.cuda.is_available() else 'cpu'
    weights = model_weights
    img_size = 640
    iou_thres = 0.45
    conf_thres = 0.5

    font = cv2.FONT_HERSHEY_SIMPLEX

    webcam = source.isnumeric()

    # Initialize
    set_logging()
    device = select_device(device)
    half = device.type != 'cpu'  # half precision only supported on CUDA

    # Load model
    model = attempt_load(weights, map_location=device)  # load FP32 model
    stride = int(model.stride.max())  # model stride
    imgsz = check_img_size(img_size, s=stride)  # check img_size

    if half:
        model.half()  # to FP16

    # Set Dataloader
    if webcam:
        cudnn.benchmark = True  # set True to speed up constant image size inference
        dataset = LoadStreams(source, img_size=imgsz, stride=stride)
    else:
        dataset = LoadImages(source, img_size=imgsz, stride=stride)

    # Get names and colors
    names = model.module.names if hasattr(model, 'module') else model.names

    colors = [(255, 255, 255), (255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0), (0, 255, 255), (255, 0, 255)
        , (155, 255, 100), (255, 155, 100), (155, 100, 255), (155, 155, 100)]

    # Run inference
    if device.type != 'cpu':
        model(torch.zeros(1, 3, imgsz, imgsz).to(device).type_as(next(model.parameters())))  # run once
    old_img_w = old_img_h = imgsz
    old_img_b = 1

    TOTAL = 0
    GRAFFITI = 0
    FADED_SIGNAGE = 0
    POTHOLES = 0
    GARBAGE = 0
    CONSTRUCTION_ROAD = 0
    BROKEN_SIGNAGE = 0
    BAD_STREETLIGHT = 0
    BAD_BILLBOARD = 0
    SAND_ON_ROAD = 0
    CLUTTER_SIDEWALK = 0
    UNKEPT_FACADE = 0


    for path, img, im0s, vid_cap in dataset:

        img = torch.from_numpy(img).to(device)
        img = img.half() if half else img.float()  # uint8 to fp16/32
        img /= 255.0  # 0 - 255 to 0.0 - 1.0
        if img.ndimension() == 3:
            img = img.unsqueeze(0)

        # Warmup
        if device.type != 'cpu' and (
                old_img_b != img.shape[0] or old_img_h != img.shape[2] or old_img_w != img.shape[3]):
            old_img_b = img.shape[0]
            old_img_h = img.shape[2]
            old_img_w = img.shape[3]

        with torch.no_grad():  # Calculating gradients would cause a GPU memory leak
            pred = model(img)[0]

        # Apply NMS
        pred = non_max_suppression(pred, conf_thres, iou_thres)

        # Process detections
        current_frame_potholes = 0
        for i, det in enumerate(pred):  # detections per image

            if webcam:  # batch_size >= 1
                p, s, im0, frame = path[i], '%g: ' % i, im0s[i].copy(), dataset.count
            else:
                p, s, im0, frame = path, '', im0s, getattr(dataset, 'frame', 0)

            im0 = cv2.resize(im0, (640, 480))

            if len(det):
                # Rescale boxes from img_size to im0 size
                det[:, :4] = scale_coords(img.shape[2:], det[:, :4], im0.shape).round()

                for c in det[:, -1].unique():
                    n = (det[:, -1] == c).sum()  # detections per class
                    s += f"{n} {names[int(c)]}{'s' * (n > 1)}, "  # add to string

                # Write results
                for *xyxy, conf, cls in reversed(det):
                    label = f'{names[int(cls)]} {conf:.2f}'
                    TOTAL += 1
                    labelx = names[int(cls)]
                    current_frame_potholes += 1
                    if labelx == 'GRAFFITI':
                        plot_one_box(xyxy, im0, label=label, color=colors[0], line_thickness=1)
                        GRAFFITI += 1
                    elif labelx == 'FADED SIGNAGE':
                        plot_one_box(xyxy, im0, label=label, color=colors[1], line_thickness=1)
                        FADED_SIGNAGE += 1
                    elif labelx == 'POTHOLES':
                        plot_one_box(xyxy, im0, label=label, color=colors[2], line_thickness=1)
                        POTHOLES += 1
                    elif labelx == 'GARBAGE':
                        plot_one_box(xyxy, im0, label=label, color=colors[3], line_thickness=1)
                        GARBAGE += 1
                    elif labelx == 'CONSTRUCTION ROAD':
                        plot_one_box(xyxy, im0, label=label, color=colors[4], line_thickness=1)
                        CONSTRUCTION_ROAD += 1
                    elif labelx == 'BROKEN SIGNAGE':
                        plot_one_box(xyxy, im0, label=label, color=colors[5], line_thickness=1)
                        BROKEN_SIGNAGE += 1
                    elif labelx == 'BAD STREETLIGHT':
                        plot_one_box(xyxy, im0, label=label, color=colors[6], line_thickness=1)
                        BAD_STREETLIGHT += 1
                    elif labelx == 'BAD BILLBOARD':
                        plot_one_box(xyxy, im0, label=label, color=colors[7], line_thickness=1)
                        BAD_BILLBOARD += 1
                    elif labelx == 'SAND ON ROAD':
                        plot_one_box(xyxy, im0, label=label, color=colors[8], line_thickness=1)
                        SAND_ON_ROAD += 1
                    elif labelx == 'CLUTTER SIDEWALK':
                        plot_one_box(xyxy, im0, label=label, color=colors[9], line_thickness=1)
                        CLUTTER_SIDEWALK += 1
                    elif labelx == 'UNKEPT FACADE':
                        plot_one_box(xyxy, im0, label=label, color=colors[10], line_thickness=1)
                        UNKEPT_FACADE += 1


            (H, W) = im0.shape[:2]

            print(" ")


            cv2.putText(im0, "Neom (Visual Pollution Detection System)", (110, 40),
                        font, 0.7 * 1, (255, 255, 255), 2)
            cv2.rectangle(im0, (20, 50), (W - 20, 15), (255, 255, 255), 2)




            sub_img = im0[H - 300: H, 0:200]
            black_rect = np.ones(sub_img.shape, dtype=np.uint8) * 0

            res = cv2.addWeighted(sub_img, 0.8, black_rect, 0.2, 1.0)

            im0[H - 300:H + 40, 0:200] = res

            cv2.putText(im0, str("GRAFFITI: " + str(GRAFFITI)), (30, H - 280),
                        font, 0.4 * 1, colors[0], 1)
            cv2.rectangle(im0, (10, H - 280), (20, H-285), colors[0], 7)

            cv2.putText(im0, str("FADED SIGNAGE: " + str(FADED_SIGNAGE)), (30, H - 255),
                        font, 0.4 * 1, colors[1], 1)
            cv2.rectangle(im0, (10, H - 255), (20, H - 260), colors[1], 7)

            cv2.putText(im0, str("POTHOLES: " + str(POTHOLES)), (30, H - 230),
                        font, 0.4 * 1, colors[2], 1)
            cv2.rectangle(im0, (10, H - 230), (20, H - 235), colors[2], 7)

            cv2.putText(im0, str("GARBAGE: " + str(GARBAGE)), (30, H - 205),
                        font, 0.4 * 1, colors[3], 1)
            cv2.rectangle(im0, (10, H - 205), (20, H - 210), colors[3], 7)

            cv2.putText(im0, str("CONSTRUCTION ROAD: " + str(CONSTRUCTION_ROAD)), (30, H - 180),
                        font, 0.4 * 1, colors[4], 1)
            cv2.rectangle(im0, (10, H - 180), (20, H - 185), colors[4], 7)

            cv2.putText(im0, str("BROKEN SIGNAGE: " + str(BROKEN_SIGNAGE)), (30, H - 155),
                        font, 0.4 * 1, colors[5], 1)
            cv2.rectangle(im0, (10, H - 155), (20, H - 160), colors[5], 7)

            cv2.putText(im0, str("BAD STREETLIGHT: " + str(BAD_STREETLIGHT)), (30, H - 130),
                        font, 0.4 * 1, colors[6], 1)
            cv2.rectangle(im0, (10, H - 130), (20, H - 135), colors[6], 7)

            cv2.putText(im0, str("BAD BILLBOARD: " + str(BAD_BILLBOARD)), (30, H - 105),
                        font, 0.4 * 1, colors[7], 1)
            cv2.rectangle(im0, (10, H - 105), (20, H - 100), colors[7], 7)

            cv2.putText(im0, str("SAND ON ROAD: " + str(SAND_ON_ROAD)), (30, H - 80),
                        font, 0.4 * 1, colors[8], 1)
            cv2.rectangle(im0, (10, H - 80), (20, H - 85), colors[8], 7)

            cv2.putText(im0, str("CLUTTER SIDEWALK: " + str(CLUTTER_SIDEWALK)), (30, H - 55),
                        font, 0.4 * 1, colors[9], 1)
            cv2.rectangle(im0, (10, H - 55), (20, H - 60), colors[9], 7)

            cv2.putText(im0, str("UNKEPT FACADE: " + str(UNKEPT_FACADE)), (30, H - 30),
                        font, 0.4 * 1, colors[10], 1)
            cv2.rectangle(im0, (10, H - 30), (20, H - 35), colors[10], 7)

            cv2.putText(im0, str("TOTAL: " + str(TOTAL)), (30, H - 5),
                        font, 0.4 * 1, (0, 0, 0), 1)

            cv2.putText(im0, str("CURRENT FRAME: " + str(current_frame_potholes)), (W - 225, H - 35),
                        font, 0.7 * 1, (0, 0, 255), 2)

            now = datetime.now()

            timex = str(now.strftime("%d/%m/%Y %H:%M:%S"))
            cv2.putText(im0, timex, (W - 200, H - 10),
                        font, 0.5 * 1, (255, 255, 255), 1)

            cv2.namedWindow("Output", cv2.WINDOW_NORMAL)
            cv2.setWindowProperty("Output", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
            cv2.imshow("Output", im0)

            cv2.waitKey(5000)


    cv2.destroyAllWindows()

# if __name__ == '__main__':
#     with torch.no_grad():
#         AI_DASH_CAM_IMAGE("../TEST_VIDEO/test3.png")