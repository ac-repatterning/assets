"""Module cartography/illustrate.py"""
import os

import branca.colormap
import folium
import folium.plugins
import folium.utilities
import geopandas
import pandas as pd

import config
import src.cartography.centroids
import src.cartography.custom
import src.cartography.parcels
import src.elements.parcel as pcl


class Illustrate:
    """
    Illustrate
    """

    def __init__(self, points: geopandas.GeoDataFrame, coarse: geopandas.GeoDataFrame, codes: pd.DataFrame):
        """

        :param points: A frame of metrics per gauge station, and of care homes.
        :param coarse: The boundaries of the hydrometric catchments
        :param codes: ['catchment_id', 'ts_id']
        """

        self.__points = points
        self.__coarse = coarse

        # Configurations
        self.__configurations = config.Config()

        # Centroid, Parcels
        self.__c_latitude, self.__c_longitude = src.cartography.centroids.Centroids(blob=self.__points).__call__()
        self.__parcels: list[pcl.Parcel] = src.cartography.parcels.Parcels(points=self.__points, codes=codes).exc()

    def __get_focus(self, catchment_id: int, focus: str):
        """

        :param catchment_id:
        :param focus: e.g., care homes `elders`, schools `schools`, gauge stations `gauge`
        :return:
        """

        __focus: geopandas.GeoDataFrame = self.__points.copy().loc[
                (self.__points['catchment_id'] == catchment_id) & (self.__points['focus'] == focus), :]
        __focus.to_crs(epsg=3857, inplace=True)

        return __focus

    # pylint: disable=R0915
    def exc(self, _name: str):
        """

        :param _name: The map file's name
        :return:
        """

        # Colours
        colours: branca.colormap.StepColormap = branca.colormap.LinearColormap(
            ['black', 'brown', 'orange']).to_step(len(self.__parcels))

        # Custom drawing functions
        custom = src.cartography.custom.Custom()

        # Base Layer
        waves = folium.Map(location=[self.__c_latitude, self.__c_longitude], tiles='OpenStreetMap', zoom_start=7)

        folium.GeoJson(
            data=self.__coarse.to_crs(epsg=3857),
            name='Boundaries',
            style_function=lambda feature: {
                "fillColor": "#ffffff", "color": "black", "opacity": 0.35, "weight": 0.85, "dashArray": "5, 2"
            },
            tooltip=folium.GeoJsonTooltip(fields=["catchment_name"], aliases=["Catchment Name"]),
            control=False,
            highlight_function=lambda feature: {
                "fillColor": "#6b8e23", "fillOpacity": 0.10
            }
        ).add_to(waves)

        # Hence
        computations = []
        for parcel in self.__parcels:

            # a parcel, i.e., catchment
            show = parcel.visible
            vector = folium.FeatureGroup(name=parcel.catchment_name, show=show)

            # gauges, care homes, schools
            instances: geopandas.GeoDataFrame = self.__get_focus(catchment_id=parcel.catchment_id, focus='gauge')
            leaves: geopandas.GeoDataFrame = self.__get_focus(catchment_id=parcel.catchment_id, focus='elders')
            schools: geopandas.GeoDataFrame = self.__get_focus(catchment_id=parcel.catchment_id, focus='schools')

            # Gauges
            on_each_feature = folium.utilities.JsCode("""
                function(feature, layer) {
                    layer.bindTooltip(
                        '<b>' + feature.properties.station_name + '</b><br>' +
                        'Gauge Datum: ' + feature.properties.gauge_datum.toFixed(4) + ' metres<br>' +
                        'River/Water: ' + feature.properties.river_name + '<br>' +
                        'Catchment: ' + feature.properties.catchment_name + '<br>'
                    );}""")

            folium.GeoJson(
                instances,
                name=f'{parcel.catchment_name}',
                marker=folium.CircleMarker(
                    radius=22.5, stroke=False, fill=True, fillColor=colours(parcel.decimal), fillOpacity=0.65),
                style_function=lambda feature: {
                    "fillOpacity": custom.f_opacity(feature['properties']['gauge_datum']),
                    "radius": custom.f_radius(feature['properties']['gauge_datum'])
                },
                zoom_on_click=True,
                on_each_feature=on_each_feature
            ).add_to(vector)

            # Care Homes
            for i in range(leaves.shape[0]):
                folium.Marker(
                    location=[leaves.iloc[i]['latitude'], leaves.iloc[i]['longitude']],
                    popup=leaves.iloc[i]['organisation'] + ', ' + leaves.iloc[i]['town'],
                    icon=folium.Icon(prefix='fa', icon='house-flag', icon_size=(0.5,0.5), color='white', icon_color='black')
                ).add_to(vector)

            # Schools
            for i in range(schools.shape[0]):
                folium.Marker(
                    location=[schools.iloc[i]['latitude'], schools.iloc[i]['longitude']],
                    tooltip= schools.iloc[i]['school_name'] + ', ' + schools.iloc[i]['level'],
                    icon=folium.Icon(prefix='fa', icon='school', icon_size=(0.5,0.5), color='white', icon_color='#504f10')
                ).add_to(vector)

            # Finally
            waves.add_child(vector)
            computations.append(vector)

        folium.plugins.GroupedLayerControl(
            groups={'catchment': computations}, exclusive_groups=False, collapsed=True
        ).add_to(waves)

        # Persist
        outfile = os.path.join(self.__configurations.maps_, f'{_name}.html')
        waves.save(outfile=outfile)
