import torch

def AI_POTHOLES_DETECTION(source="0", model_weights="../Model/potholes_detector.pt"):

    from pathlib import Path
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
        view_img = check_imshow()
        cudnn.benchmark = True  # set True to speed up constant image size inference
        dataset = LoadStreams(source, img_size=imgsz, stride=stride)
    else:
        dataset = LoadImages(source, img_size=imgsz, stride=stride)

    # Get names and colors
    names = model.module.names if hasattr(model, 'module') else model.names
    # colors = [[random.randint(0, 255) for _ in range(3)] for _ in names]
    colors = [(0, 255, 0), (0, 255, 255), (0, 0, 255)]

    # Run inference
    if device.type != 'cpu':
        model(torch.zeros(1, 3, imgsz, imgsz).to(device).type_as(next(model.parameters())))  # run once
    old_img_w = old_img_h = imgsz
    old_img_b = 1

    pot_holes = 0
    high = 0
    medium = 0
    low = 0
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

        # Inference
        t1 = time_synchronized()
        with torch.no_grad():  # Calculating gradients would cause a GPU memory leak
            pred = model(img)[0]
        t2 = time_synchronized()

        # Apply NMS
        pred = non_max_suppression(pred, conf_thres, iou_thres)
        t3 = time_synchronized()

        # Process detections
        current_frame_potholes = 0
        for i, det in enumerate(pred):  # detections per image

            if webcam:  # batch_size >= 1
                p, s, im0, frame = path[i], '%g: ' % i, im0s[i].copy(), dataset.count
            else:
                p, s, im0, frame = path, '', im0s, getattr(dataset, 'frame', 0)

            im0 = cv2.resize(im0, (640, 480))

            gn = torch.tensor(im0.shape)[[1, 0, 1, 0]]  # normalization gain whwh
            if len(det):
                # Rescale boxes from img_size to im0 size
                det[:, :4] = scale_coords(img.shape[2:], det[:, :4], im0.shape).round()

                # Print results
                for c in det[:, -1].unique():
                    n = (det[:, -1] == c).sum()  # detections per class
                    s += f"{n} {names[int(c)]}{'s' * (n > 1)}, "  # add to string

                # Write results
                for *xyxy, conf, cls in reversed(det):
                    label = f'{names[int(cls)]} {conf:.2f}'
                    print(xyxy)
                    pot_holes += 1
                    current_frame_potholes += 1
                    mul = (int(xyxy[2])*int(xyxy[3]))
                    print("sumx", mul)
                    if mul <= 40000:
                        plot_one_box(xyxy, im0, label=label, color=colors[0], line_thickness=1)
                        low += 1
                    elif mul > 40000 and mul < 70000:
                        plot_one_box(xyxy, im0, label=label, color=colors[1], line_thickness=1)
                        medium += 1
                    else:
                        plot_one_box(xyxy, im0, label=label, color=colors[2], line_thickness=1)
                        high += 1





            (H, W) = im0.shape[:2]

            print(H, W)

            cv2.putText(im0, "Neom (PotHoles Detection System)", (110, 40),
                        font, 0.7 * 1, (255, 255, 255), 2)
            cv2.rectangle(im0, (20, 50), (W - 20, 15), (255, 255, 255), 2)

            cv2.putText(im0, "RISK ANALYSIS", (30, 85),
                        font, 0.4 * 1, (255, 255, 255), 1)
            cv2.putText(im0, "-- GREEN : SAFE", (H-20, 85),
                        font, 0.4 * 1, (0, 255, 0), 1)
            cv2.putText(im0, "-- YELLOW : Drive Slowly ", (H - 200, 85),
                        font, 0.4 * 1, (0, 255, 255), 1)
            cv2.putText(im0, "-- RED: UNSAFE", (H-320, 85),
                        font, 0.4 * 1, (0, 0, 255), 1)

            tot_str = "Total Potholes Detected: " + str(pot_holes)
            high_str = "Risky Potholes Detected: " + str(high)
            med_str = "Unsafe Pothole Detected: " + str(medium)
            safe_str = "Safe Pothole Detected: " + str(low)


            sub_img = im0[H - 100: H, 0:260]
            black_rect = np.ones(sub_img.shape, dtype=np.uint8) * 0

            res = cv2.addWeighted(sub_img, 0.8, black_rect, 0.2, 1.0)

            im0[H - 100:H + 40, 0:260] = res


            cv2.putText(im0, tot_str, (10, H - 80),
                        font, 0.5 * 1, (255, 255, 255), 1)
            cv2.putText(im0, high_str, (10, H - 55),
                        font, 0.5 * 1, (0, 255, 0), 1)
            cv2.putText(im0, med_str, (10, H - 30),
                        font, 0.5 * 1, (0, 120, 255), 1)
            cv2.putText(im0, safe_str, (10, H - 5),
                        font, 0.5 * 1, (0, 0, 150), 1)

            cv2.putText(im0, str("CURRENT FRAME: " + str(current_frame_potholes)), (W - 225, H - 35),
                        font, 0.7 * 1, (0, 0, 255), 2)

            now = datetime.now()

            timex = str(now.strftime("%d/%m/%Y %H:%M:%S"))
            cv2.putText(im0, timex, (W - 200, H - 10),
                        font, 0.5 * 1, (255, 255, 255), 1)

            cv2.namedWindow("Output", cv2.WINDOW_NORMAL)
            cv2.setWindowProperty("Output", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
            cv2.imshow("Output", im0)

            if (cv2.waitKey(1) & 0xFF == ord('q')):
                break

    cv2.destroyAllWindows()

# if __name__ == '__main__':
#     with torch.no_grad():
#         AI_POTHOLES_DETECTION("../TEST_VIDEO/potholes.mp4")