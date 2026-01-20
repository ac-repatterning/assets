"""Module cartography/points.py"""
import geopandas
import pandas as pd


class Points:
    """
    Data
    """

    def __init__(self, care: geopandas.GeoDataFrame, schools: geopandas.GeoDataFrame, reference: geopandas.GeoDataFrame):
        """

        :param care: Care home frame
        :param schools: Schools
        :param reference: Of gauges
        """

        self.__care = care
        self.__schools = schools
        self.__reference = reference

    def __get_care(self) -> geopandas.GeoDataFrame:
        """

        :return:
        """

        __f_care = ['catchment_id', 'catchment_name', 'focus', 'latitude', 'longitude', 'organisation',
                    'town', 'local_authority', 'geometry']

        care = self.__care.copy()
        care['latitude'] = care.geometry.apply(lambda k: k.y)
        care['longitude'] = care.geometry.apply(lambda k: k.x)
        care['focus'] = 'elders'

        return care[__f_care]

    def __get_schools(self) -> geopandas.GeoDataFrame:
        """

        :return:
        """

        __f_schools = ['catchment_id', 'catchment_name', 'focus', 'latitude', 'longitude', 'school_name',
                       'level', 'local_authority', 'geometry']

        schools = self.__schools.copy()
        schools['latitude'] = schools.geometry.apply(lambda k: k.y)
        schools['longitude'] = schools.geometry.apply(lambda k: k.x)
        schools['focus'] = 'schools'

        return schools[__f_schools]

    def __get_reference(self) -> geopandas.GeoDataFrame:
        """

        :return:
        """

        __f_reference = ['catchment_id', 'catchment_name', 'focus', 'station_id', 'latitude', 'longitude',
                         'station_name', 'ts_name', 'river_name', 'gauge_datum', 'geometry']

        reference = self.__reference.copy()
        reference['focus'] = 'gauge'

        return reference[__f_reference]

    def exc(self) -> geopandas.GeoDataFrame:
        """

        :return:
        """

        care = self.__get_care()
        schools = self.__get_schools()
        reference = self.__get_reference()

        # Concatenating
        data = pd.concat([care, schools, reference], axis=0, ignore_index=True)

        return data
