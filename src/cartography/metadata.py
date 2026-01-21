
class Metadata:

    def __init__(self):
        pass

    def __call__(self) -> str:
        """
        About a gauge station and its vicinity.

        :return:
        """

        firms: str = 'Fire Information for Resource Management System'
        nasa: str = 'National Aeronautics and Space Administration'

        return """
                function(feature, layer) {
                    layer.bindTooltip(
                        '<b>' + feature.properties.station_name + '</b><br>' +
                        'Gauge Datum: ' + feature.properties.gauge_datum.toFixed(4) + ' metres<br>' +
                        'River/Water: ' + feature.properties.river_name + '<br>' +
                        'Catchment: ' + feature.properties.catchment_name + '<br><br>' +
                        'LIVE TRAINS: Inspect live ' + feature.properties.railway + '; by signalbox.io.<br>' +
                        'FIRE TRACKING: A ' + feature.properties.fire + ' information source option; by ' + 
                        '<abbr title="National Aeronautics and Space Administration, United States of America">NASA</abbr> ' +
                        '<abbr title="Fire Information for Resource Management System">FIRMS</abbr> ' + 
                        '[<a href="https://www.earthdata.nasa.gov/data/tools/firms/faq" target="_blank">README</a>].'
                    );
                    
                    layer.bindPopup(
                        '<b>' + feature.properties.station_name + '</b><br>' +
                        'Gauge Datum: ' + feature.properties.gauge_datum.toFixed(4) + ' metres<br>' +
                        'River/Water: ' + feature.properties.river_name + '<br>' +
                        'Catchment: ' + feature.properties.catchment_name + '<br><br>' +
                        'LIVE TRAINS: Inspect live ' + feature.properties.railway + '; by signalbox.io.<br>' +
                        'FIRE TRACKING: A ' + feature.properties.fire + ' information source option; by ' + 
                        '<abbr title="National Aeronautics and Space Administration, United States of America">NASA</abbr> ' +
                        '<abbr title="Fire Information for Resource Management System">FIRMS</abbr> ' + 
                        '[<a href="https://www.earthdata.nasa.gov/data/tools/firms/faq" target="_blank">README</a>].'
                    );
                }
                """
