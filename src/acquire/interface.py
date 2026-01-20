"""Module interface.py"""
import sys

import pandas as pd

import src.acquire.gauges
import src.elements.s3_parameters as s3p
import src.elements.service as sr
import src.functions.cache


class Interface:
    """
    Notes<br>
    ------<br>

    Reads-in the codes of all assets in-focus.
    """

    def __init__(self, service: sr.Service, s3_parameters: s3p.S3Parameters, arguments: dict):
        """

        :param service: A suite of services for interacting with Amazon Web Services.
        :param s3_parameters: The overarching S3 parameters settings of this
                              project, e.g., region code name, buckets, etc.
        :param arguments: A set of arguments vis-à-vis calculation & storage objectives.
        """

        self.__service = service
        self.__s3_parameters = s3_parameters
        self.__arguments = arguments

    def exc(self) -> pd.DataFrame:
        """

        :return:
        """

        # The gauges
        gauges = src.acquire.gauges.Gauges(
            service=self.__service, s3_parameters=self.__s3_parameters, arguments=self.__arguments).exc()
        if gauges.empty:
            src.functions.cache.Cache().exc()
            sys.exit('There are no data sets.')

        return gauges[['catchment_id', 'ts_id']].drop_duplicates()
