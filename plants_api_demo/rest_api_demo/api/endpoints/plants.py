import logging
from flask import Flask, jsonify
from flask import request, jsonify, Blueprint
from flask_restx import Resource

import time
import pandas as pd
import settings
import geopandas as gpd
from shapely.geometry import Point, Polygon
from flask_restx import Api

log = logging.getLogger(__name__)

REQUEST_API = Blueprint('plants', __name__)

api = Api(REQUEST_API)

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
        self.df_plants = pd.read_excel(open(settings.EXCEL_DATA_EGRID_URI, 'rb'), sheet_name='PLNT16', header=1)


def load_excel():
    return ApiPlants()


def set_default(obj):
    if isinstance(obj, set):
        return list(obj)
    raise TypeError


def get_blueprint():
    """Return the blueprint for the main app module"""
    return REQUEST_API


@REQUEST_API.route('/<state_code>', methods=['GET'])
@ns.route('/<state_code>')
@api.doc(params={'state_code': 'TX/tx/Tx/tX', 'p1_lat': '', 'p1_lon': '', 'p2_lat': '', 'p2_lon': ''})
class PlaintsByState(Resource):

    def get(self, state_code):
        start = time.time()
        df_plants = load_excel().df_plants
        pl_by_state_df = df_plants.groupby("PSTATABB")
        result = pl_by_state_df.get_group(state_code.upper())
        # state point
        states_filter = gpd.GeoDataFrame(result, geometry=gpd.points_from_xy(result.LON, result.LAT))
        # glob point geo frame
        states = gpd.GeoDataFrame(df_plants, geometry=gpd.points_from_xy(df_plants.LON, df_plants.LAT))

        percentage = result["PSTATABB"].count() / len(df_plants)
        plants_number = result["PSTATABB"].count()

        if request.args:
            if request.args.get('p1_lat') and request.args.get('p1_lon'):
                lat_first_p = float(request.args.get('p1_lat'))
                lon_first_p = float(request.args.get('p1_lon'))

            if request.args.get('p2_lon') and request.args.get('p2_lat'):
                lat_second_p = float(request.args.get('p1_lat'))
                lon_second_p = float(request.args.get('p1_lon'))

                p1 = Point(lat_first_p, lon_first_p)
                p2 = Point(lat_second_p, lon_second_p)
                points = gpd.GeoDataFrame(geometry=[p1, p2])
                points.set_crs(epsg=4326, inplace=True)
                points = points.to_crs("EPSG:3395")
                result_gdf = gpd.sjoin(points, states_filter, how="inner", op='intersects')

                return result_gdf.to_json()

        plants_data_info = {'abs_value': int(plants_number), "percent": "{:.2%}".format(percentage)}

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

        df_sorted = \
            df_plants.sort_values(by=ApiPlants.search_key_defaults["sort_by"], ascending=False, na_position='last')[
                ApiPlants.search_key_defaults["cols"]][:ApiPlants.search_key_defaults["top"]]

        return df_sorted.to_json()
