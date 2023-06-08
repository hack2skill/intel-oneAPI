import os
import sys
import argparse
from pathlib import Path
import cv2
import numpy as np
from PIL import Image
import warnings
import logging
from addict import Dict
from compression.api import DataLoader, Metric
from compression.engines.openvino_engine import OpenVINOEngine
from compression.graph import load_model, save_model
from compression.graph.model_utils import compress_model_weights
from openvino.inference_engine import IECore

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
warnings.filterwarnings("ignore")


class ClassificationDataLoader(DataLoader):
    def __init__(self, data_source):
        self.data_source = Path(data_source)
        self.dataset = [p for p in self.data_source.glob("**/*") if p.suffix in (".png", ".jpeg")]
        self.class_names = sorted([item.name for item in self.data_source.iterdir() if item.is_dir()])

    def __len__(self):
        return len(self.dataset)

    def __getitem__(self, index):
        filepath = self.dataset[index]
        annotation = (index, self.class_names.index(filepath.parent.name))
        image = self._read_image(filepath)
        return annotation, image

    def _read_image(self, index):
        image = np.array(Image.open(index))
        image = cv2.resize(image, (300, 300)).astype(np.float32)
        image = image.transpose(2, 0, 1)
        return image


class Accuracy(Metric):
    def __init__(self):
        super().__init__()
        self._name = "accuracy"
        self._matches = []

    @property
    def value(self):
        return {self._name: self._matches[-1]}

    @property
    def avg_value(self):
        num_correct = np.count_nonzero(self._matches)
        return {self._name: num_correct / len(self._matches)}

    def update(self, output, target):
        predict = np.argmax(output[0], axis=1)
        match = predict == target
        self._matches.append(match)

    def reset(self):
        self._matches = []

    def get_attributes(self):
        return {self._name: {"direction": "higher-better", "type": "accuracy"}}


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--datapath', type=str, required=False, default=Path('/home/azureuser/oneAPI-MedicalDiagnosis-DL/data/chest_xray/val'), help='dataset path')
    parser.add_argument('--modelpath', type=str, required=False, default=Path("model/Medical_Diagnosis_CNN.xml"), help='Model path trained')
    FLAGS = parser.parse_args()
    model_xml = Path(FLAGS.modelpath)
    data_dir = Path(FLAGS.datapath)

    if not model_xml.exists():
        logger.info("Not Executing training notebook....")

    model_config = Dict(
        {
            "model_name": "Medical_Diagnosis_CNN",
            "model": str(model_xml),
            "weights": str(model_xml.with_suffix(".bin")),
        }
    )

    engine_config = Dict({"device": "CPU", "stat_requests_number": 2, "eval_requests_number": 2})

    algorithms = [
        {
            "name": "DefaultQuantization",
            "params": {
                "target_device": "CPU",
                "preset": "performance",
                "stat_subset_size": 1000,
            },
        }
    ]

    model = load_model(model_config=model_config)
    original_model = copy.deepcopy(model)

    data_loader = ClassificationDataLoader(data_source=data_dir)

    metric = Accuracy()

    engine = OpenVINOEngine(config=engine_config, data_loader=data_loader, metric=metric)

    pipeline = create_pipeline(algo_config=algorithms, engine=engine)

    compressed_model = pipeline.run(model=model)

    compress_model_weights(model=compressed_model)

    compressed_model_paths = save_model(model=compressed_model, save_path=os.path.join(os.path.curdir, "model/optimized"))
    compressed_model_xml = Path(compressed_model_paths[0]["model"])
    logger.info(f"The quantized model is stored in {compressed_model_xml}")

    original_metric_results = pipeline.evaluate(original_model)
    if original_metric_results:
        print(f"Accuracy of the original model: {next(iter(original_metric_results.values())):.5f}")
        logger.info(f"Accuracy of the original model: {next(iter(original_metric_results.values()))}")

    quantized_metric_results = pipeline.evaluate(compressed_model)
    if quantized_metric_results:
        print(f"Accuracy of the quantized model: {next(iter(quantized_metric_results.values())):.5f}")
        logger.info(f"Accuracy of the quantized model: {next(iter(quantized_metric_results.values()))}")
