import os
import sys

from flask import Flask, Blueprint
from controller.AccountAPI import account_api
from flask import request, session
from flask import Flask, jsonify
from flask import request
from dao import db
from entity.User import User
import json

from apps.utils import run, PredictionCase
from detectron2.data.datasets.builtin_meta import COCO_CATEGORIES

from dao import app


getData_api = Blueprint('getData_api', __name__)
app.register_blueprint(getData_api)


@app.route('/get', methods=['GET']) 
def getData():
    name = session['user']
    user = User.query.filter_by(name=name).first()
    url = request.args.get("url")  # image url uploaded by
    imgs = []
    imgs.append(url)

    model = sys.path[0] + "/../" + user.model_path
    config_file = sys.path[0] + "/../" + user.config_path
    cases = run(imgs, model, config_file, name)

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
