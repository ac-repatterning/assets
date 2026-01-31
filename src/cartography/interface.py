"""Module cartography/interface.py"""
import logging

import boto3
import geopandas
import pandas as pd

import config
import src.acquire.maps
import src.acquire.reference
import src.cartography.illustrate
import src.cartography.points
import src.elements.s3_parameters as s3p
import src.functions.secret
import src.s3.keys


class Interface:
    """
    An interface to the risks programs
    """

    def __init__(self, connector: boto3.session.Session, s3_parameters: s3p.S3Parameters):
        """

        :param connector: An instance of boto3.session.Session
        :param s3_parameters: The overarching S3 parameters settings of this
                              project, e.g., region code name, buckets, etc.<br>
        """

        self.__connector = connector
        self.__s3_parameters = s3_parameters

        # Instances
        self.__maps = src.acquire.maps.Maps(connector=self.__connector, s3_parameters=self.__s3_parameters)

        # A `map tiles` option
        self.__secret = src.functions.secret.Secret(connector=self.__connector)

    def exc(self, codes: pd.DataFrame):
        """
        © Europa Technologies Ltd. Contains Ordnance Survey data © Crown copyright and database

        :param codes: ['catchment_id', 'ts_id']
        :return:
        """

        # Maps
        coarse = self.__maps.exc(key_name='cartography/coarse.geojson')
        care = self.__maps.exc(key_name='cartography/care_and_coarse_catchments.geojson')
        schools = self.__maps.exc(key_name='cartography/sch-catchments.geojson')
        reference = src.acquire.reference.Reference(s3_parameters=self.__s3_parameters).exc()

        # Thus far, points vis-à-vis care homes and gauge stations.
        points: geopandas.GeoDataFrame = src.cartography.points.Points(
            care=care, schools=schools, reference=reference).exc()
        logging.info(points)

        # Draw
        provider = self.__secret.exc(secret_id=config.Config().project_key_name, node='europa-technologies')
        mapping_service = {
            'tiles': 'https://tile.viaeuropa.uk.com/' +  provider + '/m0306/{z}/{x}/{y}.png',
            'attr': '© Europa Technologies Ltd. Contains Ordnance Survey data © Crown copyright and database'
        }
        src.cartography.illustrate.Illustrate(
            points=points, coarse=coarse, codes=codes).exc(_name='assets', mapping_service=mapping_service)
