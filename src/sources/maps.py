"""Module maps.py"""
import io

import boto3
import geopandas

import src.elements.s3_parameters as s3p
import src.s3.unload


class Maps:
    """
    Maps
    """

    def __init__(self, connector: boto3.session.Session, s3_parameters: s3p.S3Parameters):
        """

        :param connector: A boto3 session instance, it retrieves the developer's <default> Amazon
                          Web Services (AWS) profile details, which allows for programmatic interaction with AWS.
        :param s3_parameters: The overarching S3 parameters settings of this project, e.g., region code
                              name, buckets, etc.
        """


        self.__connector = connector
        self.__s3_parameters = s3_parameters

    def __get_spatial_data(self, key_name: str) -> geopandas.GeoDataFrame:
        """

        :param key_name: e.g., 'cartography/coarse.geojson'
        :return:
        """

        __s3_client: boto3.session.Session.client = self.__connector.client(service_name='s3')
        buffer = src.s3.unload.Unload(s3_client=__s3_client).exc(
            bucket_name=self.__s3_parameters.internal, key_name=key_name)
        data = geopandas.read_file(io.StringIO(buffer))

        return data

    def exc(self, key_name: str) -> geopandas.GeoDataFrame:
        """

        :param key_name: e.g., 'cartography/coarse.geojson'
        :return:
        """

        return self.__get_spatial_data(key_name=key_name)
