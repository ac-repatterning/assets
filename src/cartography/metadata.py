
class Metadata:

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
                        'For more about the vicinity of the gauge station click on this icon; ' + 
                        'the resulting popup has links to hubs that outline live trains, fires, etc., - <b>if applicable/any.</b>'
                    );
                    
                    layer.bindPopup(
                        '<b>' + feature.properties.station_name + '</b><br>' +
                        'Gauge Datum: ' + feature.properties.gauge_datum.toFixed(4) + ' metres<br>' +
                        'River/Water: ' + feature.properties.river_name + '<br>' +
                        'Catchment: ' + feature.properties.catchment_name + '<br><br>' +
                        '<b>LIVE TRAINS:</b> Inspect live ' + feature.properties.railway + '; by signalbox.io.<br><br>' +
                        '<b>FIRE TRACKING:</b> A ' + feature.properties.fire + ' information source option; by ' + 
                        '<abbr title="National Aeronautics and Space Administration, United States of America">NASA</abbr> ' +
                        '<abbr title="Fire Information for Resource Management System">FIRMS</abbr> ' + 
                        '[<a href="https://www.earthdata.nasa.gov/data/tools/firms/faq" target="_blank">README</a>].'
                    );
                }
                """
