from flask import Flask
from flask import Flask, jsonify
from flask import abort
from flask import request

import yaml
import json
import sys
import os
sys.path.append("..")

from apps.utils import run, PredictionCase
from detectron2.data.datasets.builtin_meta import COCO_CATEGORIES

app = Flask(__name__)
app_config = {"host": "127.0.0.1", "port": "5000"}

imgs = []

with open(sys.path[0] + "/../configs/Global-Config.yaml", 'r') as fp:
    global_cfg = yaml.load(fp.read(), Loader=yaml.Loader)

model = global_cfg["model_path"]
dataset_path = global_cfg["dataset_path"]
config_file = global_cfg["config_file"]

# model = sys.path[0] + "/../models/model_final34.pth"
# dataset_path = sys.path[0] + "/../detectron2/tools/datasets/coco/test_train/"
# config_file = sys.path[0] + "/../configs/COCO-Detection/faster_rcnn_R_34_FPN_3x.yaml"

def getpoints(points):
    p0 = points[0]
    p3 = points[1]
    p1 = [points[0][0], points[1][1]]
    p2 = [points[1][0], points[0][1]]
    return [p0, p1, p2, p3]

def getpath(url):
    photo = url.split("/")[-1]
    photo = photo.split(".")[0]
    photo_json = dataset_path + photo + '.json'
    return photo_json

@app.route('/post', methods=['POST'])  # results returned from the front-end
def postData():
    data = request.get_json()
    updated_data = json.loads(data["data"])  # image options updated by client
    print(updated_data)
    url = updated_data["url"]
    annotations = updated_data["annotation"]
    print("url: ", url)
    print("annotations:", annotations)

    photo_json = getpath(url)

    retdata = {
        "version": "4.5.9",
        "flags": {},
        "shapes": [],
        "imagePath": url.split("/")[-1],
        "imageData": "Encoded",
        "imageHeight": 0,
        "imageWidth": 0,
        "lineColor": [0, 255, 0, 128],
        "fillColor": [255, 0, 0, 128]
        }

    for anno in annotations:
        if anno["confidence"] == -100:
            retdata["imageWidth"] = anno["bbox"][2]
            retdata["imageHeight"] = anno["bbox"][3]
            continue

        shape = {
            "line_color": None,
            "fill_color": None,
            "label": anno["category"],
            "points": [[anno["bbox"][0], anno["bbox"][1]], [anno["bbox"][2], anno["bbox"][3]]],
            "group_id": None,
            "shape_type": "rectangle",
            "flags": {}
            }
        retdata["shapes"].append(shape)

    with open(photo_json, 'w', encoding='UTF-8') as fp:
        json.dump(retdata, fp, indent=2)

    return jsonify(retdata)


@app.route('/get', methods=['GET'])  # get image detetion results from model
def getData():
    url = request.args.get("url")  # image url uploaded by
    # print(request.get_json())
    # print(url)
    # annos = []
    # data = request.get_json()
    imgs = []
    imgs.append(url)

    cases = run(imgs, model, config_file)

    case_dict = {"url": url, "annotation": [], "height": 0, "width": 0}

    for case in cases[0]:
        anno = {}
        anno["category"] = COCO_CATEGORIES[case.category]["name"]
        anno["bbox"] = case.bbox
        anno["confidence"] = case.confidence
        case_dict["url"] = case.url
        case_dict["annotation"].append(anno)
        case_dict["height"] = case.height
        case_dict["width"] = case.width
    print(case_dict)

    return jsonify(case_dict)


@app.route('/train', methods=['GET'])
def train():
    """train()

    return jsonify(train done)"""
    pass

@app.route('/add', methods=['GET'])
def addPicture():
    """add(picture)

    return jsonify(load_dict)"""
    pass


if __name__ == '__main__':
    app.run(**app_config)