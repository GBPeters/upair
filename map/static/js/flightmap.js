
var host = '145.100.59.98'

var map = L.map('map').fitBounds([[-20,-135],[60,45]]);
var planeicon = L.icon({iconUrl: 'res/plane.png', iconSize: [24,24], iconAnchor: [12,12]})
var now = L.realtime({
    url: 'http://' + host + ':5000/now',
    crossOrigin: true,
    type: 'json',
}, {
    interval: 60 * 1000,
    pointToLayer: function (geoJsonPoint, latlng) {
        return L.marker(latlng, {icon: planeicon, rotationAngle: geoJsonPoint.properties.heading});
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
