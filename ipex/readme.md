## Yolov7 Model Training with IPEX

### Software/Hardware Requirements
- Linux OS or Docker Image on Windows ```docker pull intel/intel-optimized-pytorch:latest```
- Install PyTorch CPU ```python -m pip install torch torchvision```
- Install IPEX (Same version as PyTorch) ``` python -m pip install intel_extension_for_pytorch -f https://developer.intel.com/ipex-whl-stable-cpu ```

### Training
- ``` python train.py --workers 8 --device cpu --batch-size 32 --epoch 10 --data data/custom_data.yaml --hyp data/hyp.scratch.custom.yaml --img 640 640 --cfg cfg/training/yolov7-custom.yaml --weights yolov7.pt --name yolov7-custom ```

### Inference
- ``` python detect.py --weights yolov7.pt --conf 0.25 --img-size 640 --source oneAPI_ODAV_APP/TEST_VIDEO/Visual_Pollution.mp4 ```
