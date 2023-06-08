import os
import sys
from pathlib import Path
import warnings
import argparse
from openvino.inference_engine import IECore
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
warnings.filterwarnings("ignore")

MODEL_PATH = './model'
model_meta_index = Path("./model/Medical_Diagnosis_CNN.meta") and Path("./model/Medical_Diagnosis_CNN.index")
dir = os.path.dirname(os.path.realpath(__file__))

def freeze_graph(model_dir, output_node_names):
    if not os.path.exists(model_dir):
        raise AssertionError("Export directory doesn't exist. Please specify an export directory: %s" % model_dir)

    if not output_node_names:
        print("You need to supply the name of a node to --output_node_names.")
        return -1

    model_xml = os.path.join(model_dir, 'model.xml')
    model_bin = os.path.join(model_dir, 'model.bin')
    output_model = os.path.join(model_dir, 'updated_model.xml')

    ie = IECore()
    net = ie.read_network(model=model_xml, weights=model_bin)
    exec_net = ie.load_network(network=net, device_name='CPU')

    exec_net.export(output_model)

    print("Model exported successfully.")

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--model_dir", type=str, default="./model/", help="Model folder to export")
    parser.add_argument("--output_node_names", type=str, default="Softmax", help="The name of the output nodes, comma separated.")
    args = parser.parse_args()

    freeze_graph(args.model_dir, args.output_node_names)
