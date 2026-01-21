
class Metadata:

    def __init__(self):
        pass

    def __call__(self) -> str:
        """
        About a gauge station and its vicinity.

        :return:
        """

        return """
                function(feature, layer) {
                    layer.bindTooltip(
                        '<b>' + feature.properties.station_name + '</b><br>' +
                        'Gauge Datum: ' + feature.properties.gauge_datum.toFixed(4) + ' metres<br>' +
                        'River/Water: ' + feature.properties.river_name + '<br>' +
                        'Catchment: ' + feature.properties.catchment_name + '<br>' +
                        feature.properties.railway
                    );
                    
                    layer.bindPopup(
                        '<b>' + feature.properties.station_name + '</b><br>' +
                        'Gauge Datum: ' + feature.properties.gauge_datum.toFixed(4) + ' metres<br>' +
                        'River/Water: ' + feature.properties.river_name + '<br>' +
                        'Catchment: ' + feature.properties.catchment_name + '<br>' +
                        feature.properties.railway
                    );
                }
                """
