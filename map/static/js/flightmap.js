
var host = '188.166.19.186'

// Create Map
var map = L.map('map').fitBounds([[-20,-135],[60,45]]);

// Create icons
var planeicon = L.icon({iconUrl: 'res/plane.png', iconSize: [16,16], iconAnchor: [8,8]});
var planegreen = L.icon({iconUrl: 'res/plane_green.png', iconSize: [16,16], iconAnchor: [8,8]});
var planered = L.icon({iconUrl: 'res/plane_red.png', iconSize: [16,16], iconAnchor: [8,8]});

// Create realtime leaflet layer
var now = L.realtime({
    url: 'http://' + host + ':5000/now',
    crossOrigin: true,
    type: 'json',
}, {
    interval: 60 * 1000,
    pointToLayer: function (geoJsonPoint, latlng) {
        // Set icon to green or red for onground and atrisk aircraft, respectively
        var i = planeicon
        if (geoJsonPoint.properties.onground) {
            i = planegreen;
        }
        // Create Marker
        m = L.marker(latlng, {icon: i, rotationAngle: geoJsonPoint.properties.heading});
        m.bindPopup("Callsign: " + geoJsonPoint.properties.callsign + "</br>"
        + "Country of origin: " + geoJsonPoint.properties.country + "</br>"
        + "Altitude: " + geoJsonPoint.properties.altitude.toString(), {});
        return m;
    },
    style: function(geoJsonFeature) {
        return {weight: 0.5}
    },
    onEachFeature: function(feature, layer) {
        // Highlight flightpath at mouseover
        layer.on('mouseover', function(e) {
            layer.setStyle({
                weight: 2
            });
        });
        layer.on('mouseout', function(e) {
            layer.setStyle({
                weight: 0.5
            });
        });
    }
}).addTo(map);
// Disabled, data too large to display
/*var airways = L.realtime({
    url: 'http://' + host + ':5000/airways',
    crossOrigin: true,
    type: 'json'
}, {
    interval: 3600 * 1000
});*/

// Create OSM tile layer
L.tileLayer('http://{s}.tile.osm.org/{z}/{x}/{y}.png', {
    attribution: '&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors'
}).addTo(map);

/* Disabled, data too large to display
function setNow() {
    map.removeLayer(airways);
    now.addTo(map)
}

function setAirways() {
    map.removeLayer(now)
    airways.addTo(map)
}*/
