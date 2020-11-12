import logging
from flask import Flask, jsonify
from flask import request, jsonify
from flask_restx import Resource
from rest_api_demo.api.restplus import api
import time
import pandas as pd
from pymongo import MongoClient
from rest_api_demo import settings

log = logging.getLogger(__name__)

ns = api.namespace('image', description='Operations related plants')

client = MongoClient()
mydb = client['imgdb']
collection = mydb['img_150']


@ns.route('/insert')
class load_insert_on_mgdb(Resource):

    def get(self):
        df_img = pd.read_csv(settings.CSV_IMG_DATA).iloc[:, 0:151]
        df_img.reset_index(inplace=True)
        data_dict = df_img.to_dict("records")

        collection.insert_many(data_dict)
        return ''


@ns.route('/')
@api.doc(params={'depth_min': '', 'depth_max': ''})
class get_frm_by_depth_min_max(Resource):

    def get(self):

        if request.args:
            if request.args.get('depth_min'):
                depth_min = request.args.get('depth_min')
            if request.args.get('depth_max'):
                depth_max = request.args.get('depth_max')

        print(float(depth_max), float(depth_min))
        query = {'depth': {"$lt": float(depth_max), "$gt": float(depth_min)}}
        result = collection.find(query, {'_id': 0})
        df = pd.DataFrame(list(result))

        return df.to_json()
