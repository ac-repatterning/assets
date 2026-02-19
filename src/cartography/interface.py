"""Module cartography/interface.py"""
import logging

import boto3
import dask
import geopandas
import pandas as pd

import src.cartography.backgrounds
import src.cartography.illustrate
import src.cartography.points
import src.elements.s3_parameters as s3p
import src.s3.keys
import src.sources.maps
import src.sources.reference


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
        self.__maps = src.sources.maps.Maps(connector=self.__connector, s3_parameters=self.__s3_parameters)
        self.__backgrounds = src.cartography.backgrounds.Backgrounds(connector=connector)()
        self.__reference = src.sources.reference.Reference(s3_parameters=self.__s3_parameters).exc()

    def __codes(self) -> pd.DataFrame:
        """

        :return:
            codes: ['catchment_id', 'ts_id']
        """

        codes = self.__reference[['catchment_id', 'ts_id']].drop_duplicates()

        return codes

    def exc(self):
        """
        © Europa Technologies Ltd. Contains Ordnance Survey data © Crown copyright and database

        :return:
        """

        codes = self.__codes()

        # Maps
        coarse = self.__maps.exc(key_name='cartography/coarse.geojson')
        care = self.__maps.exc(key_name='cartography/care_and_coarse_catchments.geojson')
        schools = self.__maps.exc(key_name='cartography/sch-catchments.geojson')

        # Thus far, points vis-à-vis care homes and gauge stations.
        points: geopandas.GeoDataFrame = src.cartography.points.Points(
            care=care, schools=schools, reference=self.__reference).exc()

        # Draw
        __illustrate = dask.delayed(src.cartography.illustrate.Illustrate(
            points=points, coarse=coarse, codes=codes).exc)

        computations = []
        for background in self.__backgrounds:
            message = __illustrate(background=background)
            computations.append(message)
        messages = dask.compute(computations, scheduler='processes')
        logging.info(messages)
