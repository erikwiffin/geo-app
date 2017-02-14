'use strict';

import $ from 'jquery';
import _ from 'underscore';


window.initMap = function initMap() {
    var dests = $('.destination').map(function (ix, el) {
        return $(el).data();
    }).get();

    var map = new google.maps.Map(document.getElementById('map'), {
        zoom: 9,
        center: dests[0],
    });

    $.each(dests, function (ix, dest) {
        var marker = new google.maps.Marker({
            position: dest,
            map: map,
            title: dest.name,
        });
    });
}
