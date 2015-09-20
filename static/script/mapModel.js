function placeMarkers(positions, map) {
    markers = [];
    for (var i = 0; i < positions.length; i++) {
        var pos = positions[i];
        var marker = new google.maps.Marker({
            position: new google.maps.LatLng(pos[0], pos[1]),
            map: map,
            animation: google.maps.Animation.DROP,
        });
        markers.push(marker);
    }
    return markers;
}


function setMapOnAll(markers, map) {
    for (var i = 0; i < markers.length; i++) {
        markers[i].setMap(map);
    }
}

function clearMarkers(markers) {
    for (var i = 0; i < markers.length; i++) {
        markers[i].setMap(null);
    }
}