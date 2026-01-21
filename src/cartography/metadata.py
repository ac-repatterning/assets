"""Module metadata.py"""


class Metadata:
    """
    The popup & tooltip text of the gauge stations.
    """

    def __init__(self):
        pass

    def __call__(self) -> str:
        """
        About a gauge station and its vicinity.

        <ul>
            <li>FIRMS: Fire Information for Resource Management System</li>
            <li>NASA: National Aeronautics and Space Administration</li>
        </ul>

        :return:
        """

        return """
                function(feature, layer) {
                    layer.bindTooltip(
                        '<b>' + feature.properties.station_name + '</b><br>' +
                        'Gauge Datum: ' + feature.properties.gauge_datum.toFixed(4) + ' metres<br>' +
                        'River/Water: ' + feature.properties.river_name + '<br>' +
                        'Catchment: ' + feature.properties.catchment_name + '<br><br>' +
                        '<b>For more about the vicinity of the gauge station <br>' + 
                        '<span style="color: #d54b00;">click on this gauge station&apos;s icon</span></b>; the resulting popup <br>' + 
                        'has links to hubs that outline live trains, fires, <br>' + 
                        'etc., - <b>if applicable/any.</b>'
                    );
                    
                    layer.bindPopup(
                        '<b>' + feature.properties.station_name + '</b><br>' +
                        'Gauge Datum: ' + feature.properties.gauge_datum.toFixed(4) + ' metres<br>' +
                        'River/Water: ' + feature.properties.river_name + '<br>' +
                        'Catchment: ' + feature.properties.catchment_name + '<br><br>' +
                        '<b>LIVE TRAINS:</b> Inspect live ' + feature.properties.railway + 
                        '; by <a href="https://www.signalbox.io" target="_blank">signalbox.io</a>.<br><br>' +
                        '<b>FIRE TRACKING:</b> An area ' + feature.properties.fire + ' information source option; by ' + 
                        '<abbr title="National Aeronautics and Space Administration, United States of America">NASA</abbr> ' +
                        '<abbr title="Fire Information for Resource Management System">FIRMS</abbr> ' + 
                        '[<a href="https://www.earthdata.nasa.gov/data/tools/firms/faq" target="_blank">README</a>].'
                    );
                }
                """
