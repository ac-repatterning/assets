"""Module parcels.py"""

import geopandas
import numpy as np
import pandas as pd

import src.elements.parcel as pcl


class Parcels:
    """
    Parcels
    """

    def __init__(self, points: geopandas.GeoDataFrame, codes: pd.DataFrame):
        """

        :param points: The frame of metrics per gauge station.
        :param codes: ['catchment_id', 'ts_id']
        """

        self.__points = points
        self.__codes = codes

        # Seed
        self.__seed = 5
        self.__rng = np.random.default_rng(seed=self.__seed)

    def __get_decimals(self, size: int):
        """

        :param size: The number of required random numbers
        :return:
        """

        return self.__rng.uniform(low=0.05, high=0.80, size=size)

    def __catchments(self) -> pd.DataFrame:
        """

        :return:
        """

        frame = self.__points[['catchment_id', 'catchment_name']].drop_duplicates()
        frame = frame.copy().loc[frame['catchment_id'].isin(self.__codes['catchment_id'].unique()), :]

        # Hence
        frame.sort_values(by='catchment_name', inplace=True)
        frame.reset_index(drop=True, inplace=True)

        return frame

    def __visible(self, data: pd.DataFrame):
        """

        :param data:
        :return:
        """


        indices = self.__rng.choice(np.arange(data.shape[0]), size=5, replace=False)
        sequence = np.arange(data.shape[0])

        return data.assign(
            visible=np.isin(sequence, indices))

    def exc(self) -> list[pcl.Parcel]:
        """

        :return:
        """

        catchments = self.__catchments()
        catchments['decimal'] = self.__get_decimals(size=catchments.shape[0])
        catchments = self.__visible(data=catchments.copy())

        # An iterable for mapping by layer
        values: list[dict] = catchments.to_dict(orient='records')
        parcels = [pcl.Parcel(**value) for value in values]

        return parcels
