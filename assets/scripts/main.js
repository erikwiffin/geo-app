'use strict';

import $ from 'jquery';
import _ from 'underscore';


window.initMap = function initMap() {
    var dests = JSON.parse($('#destinations-data').html());

    var map = new google.maps.Map(document.getElementById('map'), {
        zoom: 9,
        center: dests[0],
    });

    $.each(dests, function (ix, dest) {
        var infoHtml = '<h3>' + dest.name + '</h3>';
        var infoWindow = new google.maps.InfoWindow({
            content: infoHtml,
        });
        var marker = new google.maps.Marker({
            position: dest,
            map: map,
            title: dest.name,
        });
        marker.addListener('click', function() {
            infoWindow.open(map, marker);
        });
        map.addListener('click', function() {
            infoWindow.close();
        });
    });

    navigator.geolocation.getCurrentPosition(function (position) {
        var origin = new google.maps.LatLng(position.coords.latitude,
                                            position.coords.longitude);
        var destinations = _.map(dests, function (dest) {
            return new google.maps.LatLng(dest.lat, dest.lng);
        });

        var service = new google.maps.DistanceMatrixService();

        service.getDistanceMatrix({
            origins: [origin],
            destinations: destinations,
            travelMode: 'DRIVING',
        }, function (response, status) {
            var elements = response.rows[0].elements;
            $('.destination').each(function (ix, el) {
                $(el).append('<p>' + elements[ix].duration.text + '</p>');
            });
        });
    });
}
