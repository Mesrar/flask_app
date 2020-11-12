import logging
from flask import Flask, jsonify
from flask import request, jsonify
from flask_restx import Resource
from api.restplus import api
import time
import pandas as pd
from rest_api_demo import settings

log = logging.getLogger(__name__)

ns = api.namespace('plants', description='Operations related plants')


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class ApiPlants(metaclass=Singleton):
    search_key_defaults = {"top": 20,
                           "sort_by": "PLNGENAN",
                           "cols": ["ORISPL", "PSTATABB", "PNAME", "LON", "LAT", 'PLNGENAN']}

    def __init__(self):
        print("init")  # never prints
        self.df_plants = pd.read_excel(open(settings.EXCEL_DATA_EGRID_URI, 'rb'), sheet_name='PLNT16',
                                       index_col=settings.EXCEL_DATA_COL_INDEX_NAME, header=1)


def load_excel():
    return ApiPlants()


@ns.route('/<state_code>')
@api.doc(params={'state_code': 'TX/tx/Tx/tX', 'p1': '', 'p2': ''})
@api.response(404, 'plants not found.')
class PlaintsByState(Resource):

    def get(self, state_code):
        start = time.time()
        df_plants = load_excel().df_plants
        df_plants_info = df_plants[df_plants.PSTATABB.str.contains(state_code, case=False)]
        df_plants['LON'] = df_plants['LON'].astype(float)
        df_plants['LAT'] = df_plants['LAT'].astype(float)

        plt_percentage = len(df_plants[df_plants.PSTATABB.str.contains(state_code, case=False)]) / \
                         len(df_plants)

        if request.args:
            if request.args.get('p1'):
                lat = request.args.get('p1')

            if request.args.get('p2'):
                lon = request.args.get('p2')

            df_plant_zoom = df_plants_info.loc[
                (df_plants["LON"] == float(lon)) & (df_plants["LAT"] == float(lat))]

            return df_plant_zoom.to_json()

        plants_data_info = {'abs_value': len(df_plants_info), "percent": "{:.2%}".format(plt_percentage),
                            "response_time": "{}s".format(time.time() - start)}
        return jsonify(plants_data_info)


@ns.route('/', methods=['GET'])
@api.doc(params={'top': '<int:top>', 'sort_by': 'col code default : PLNGENAN', 'cols': 'cols code to show'})
class TOPPlaints(Resource):

    def get(self):
        df_plants = load_excel().df_plants
        if request.args:
            if request.args.get('top'):
                ApiPlants.search_key_defaults["top"] = int(request.args.get('top'))
            if request.args.get('sort_by'):
                ApiPlants.search_key_defaults["sort_by"] = request.args.get('sort_by')
            if request.args.get('cols'):
                ApiPlants.search_key_defaults["cols"] = request.args.get('cols').split(",")
            else:  # if no cols arg show the one sorted by
                ApiPlants.search_key_defaults["cols"] = ApiPlants.search_key_defaults["sort_by"]

        df_sorted = \
            df_plants.sort_values(by=ApiPlants.search_key_defaults["sort_by"], ascending=False, na_position='last')[
                ApiPlants.search_key_defaults["cols"]][:ApiPlants.search_key_defaults["top"]]

        return df_sorted.to_json()
