import logging
from flask import request, jsonify
from flask_restx import Resource
from api.restplus import api
import pandas as pd
from pymongo import MongoClient
import cv2
import numpy as np
import matplotlib.pyplot as plt

import json

log = logging.getLogger(__name__)

ns = api.namespace('image', description='Operations related plants')

client = MongoClient(host='img_mongodb',
                     port=27017,
                     username='root',
                     password='pass',
                     authSource="admin")
mydb = client['imgdb_notebooks']
collection = mydb['img']


def get_mpl_colormap(cmap_name):
    cmap = plt.get_cmap(cmap_name)
    sm = plt.cm.ScalarMappable(cmap=cmap)
    color_range = sm.to_rgba(np.linspace(0, 1, 256), bytes=True)[:, 2::-1]
    return color_range.reshape(256, 1, 3)


@ns.route('/insert')
class LoadImgTODB(Resource):

    def get(self):
        data = np.genfromtxt('img.csv', delimiter=',', encoding=None, dtype=None)

        np_image = data[1:, 1:]
        depth = data[1:, 0]

        img_height, img_width = np_image.shape
        w_resize_to = 150
        ratio = w_resize_to / img_width
        new_width = int(img_width * ratio)
        new_height = int(img_height * ratio)
        headers = data[0:1, 1:new_width + 1]
        np_image[np_image == ''] = 0

        img_resized_db = cv2.resize(np_image.astype(float), (new_width, new_height), interpolation=cv2.INTER_LINEAR)

        header_col_flat_list = [item for elem in headers.tolist() for item in elem]

        df_img = pd.DataFrame(data=img_resized_db[0:new_height, 0:new_width], index=depth[:new_height],
                              columns=header_col_flat_list)

        df_img_db = pd.DataFrame(data=df_img, index=depth[:new_height], columns=header_col_flat_list)
        df_img_db.index.name = 'depth'
        df_img_db.reset_index(inplace=True)
        try:
            collection.delete_many({})
            records = df_img_db.to_dict('records')

            collection.insert_many(records)
            return True
        except Exception as e:
            log.error("insert exception" + e.__cause__)
            return False


class NumpyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return json.JSONEncoder.default(self, obj)


@ns.route('/')
@api.doc(params={'depth_min': '', 'depth_max': '', 'color_map': ''})
class Depth(Resource):

    def get(self):
        if request.args:
            if request.args.get('depth_min'):
                depth_min = float(request.args.get('depth_min'))
            if request.args.get('depth_max'):
                depth_max = float(request.args.get('depth_max'))

        result = collection.find({}, {'_id': False})

        df_img_db = pd.DataFrame(data=list(result))

        df_img_db = df_img_db.set_index('depth')
        df_img_db['depth'] = df_img_db.index.astype(float)

        np_img = df_img_db.loc[(df_img_db["depth"] > depth_min) &
                               (df_img_db["depth"] < depth_max)]  # load frame by dpeth min and max

        arr8 = np_img.iloc[:, 1:].values.astype(np.uint8)

        if request.args.get('color_map'):
            colors_map = request.args.get('colors_map')
            image_bgr = cv2.applyColorMap(arr8, get_mpl_colormap(colors_map))  # apply color map to frame
            encoded_np = json.dumps(image_bgr, cls=NumpyEncoder)
            return encoded_np
        else:
            img_json = df_img_db.to_dict('list')
            return json.dumps(img_json)


@ns.route('/applyColorMap/')
@api.doc(params={'colors_map': ''})
class ApplyColorMapToImg(Resource):
    _colors_map = 'bwr'

    def get(self):

        if request.args:
            if request.args.get('colors_map'):
                _colors_map = request.args.get('colors_map')

        my_data = list(map(lambda x: list(x.values()), collection.find({}, {"_id": 0, "depth": 0})))
        result = np.array(my_data)

        arr8 = result.astype(np.uint8)
        image_bgr = cv2.applyColorMap(arr8, get_mpl_colormap(self._colors_map))
        encoded_np = json.dumps(image_bgr, cls=NumpyEncoder)
        return encoded_np
