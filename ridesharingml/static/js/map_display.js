let map = L.map('map').setView([51.505, -0.09], 13);
//sk.eyJ1Ijoid29ibmlhciIsImEiOiJjbDBsOHdvNmIwZjR3M2NwZTduZGJudjRyIn0.7T4gYxgezHejOT_iaCYbWw
L.tileLayer('https://api.mapbox.com/styles/v1/{id}/tiles/{z}/{x}/{y}?access_token={accessToken}', {
    attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors, Imagery © <a href="https://www.mapbox.com/">Mapbox</a>',
    maxZoom: 18,
    id: 'mapbox/streets-v11',
    tileSize: 512,
    zoomOffset: -1,
    accessToken: 'sk.eyJ1Ijoid29ibmlhciIsImEiOiJjbDBsOHdvNmIwZjR3M2NwZTduZGJudjRyIn0.7T4gYxgezHejOT_iaCYbWw'
}).addTo(map);
let popup = L.popup();

function onMapClick(e) {
    console.log(e.latlng)
    L.marker([e.latlng["lat"],e.latlng["lng"]], {icon: greenIcon}).addTo(map);
    // popup
    //     .setLatLng(e.latlng)
    //     .setContent("You clicked the map at " + e.latlng.toString())
    //     .openOn(map);
}

map.on('click', onMapClick);
let greenIcon = L.icon({
    iconUrl: './static/img/car2.png',

    iconSize:     [20, 15], // size of the icon
    iconAnchor:   [15, 15], // point of the icon which will correspond to marker's location
    popupAnchor:  [-3, -76] // point from which the popup should open relative to the iconAnchor
});
