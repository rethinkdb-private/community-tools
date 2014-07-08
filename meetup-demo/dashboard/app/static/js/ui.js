var meetups = [];
window.meetups = meetups;
var sort_list_timer;
var markers = [];

var sort_list = function() {
    meetups.sort(function(a,b) {
        return b.count - a.count;
    });
    var height = $('#list li.event').outerHeight();
    var y = 0;
    for (var i=0; i < meetups.length; i++) {
        $(meetups[i].$item).css("top", y + "px");
        y += height;
    }
}

var show_meetup_checkin = function(checkin) {
    var meetup = null;

    for (var i=0; i < meetups.length; i++) {
        if (meetups[i].name === checkin.event_name) {
            meetup = meetups[i];
        }
    }
    // A meetup is already being tracked
    if(meetup) {
        // Update the meetup check-in count
        meetup.count = meetup.count + 1;
        $('span.count', meetup.$item).text(meetup.count);
    }
    // We need to add the meetup to the list
    else {
        el = [
            "<li data-event='"+checkin.event_name+"' class='event'>",
            "   <p class='name'>"+checkin.event_name+"</p>",
            "   <p class='details'><span class='count'>1</span> meetup attendees</p>",
            "</li>"
        ].join("\n");
        meetup = {
            $item: $(el),
            count: 1,
            name: checkin.event_name
        }
        if (meetups.length == 0) {
            meetup.$item.css('top', 0);
        }
        else {
            height = $('#list li.event').outerHeight();
            meetup.$item.css('top', height * meetups.length);
        }
        meetups.push(meetup);
        $("#list").append(meetup.$item);
    }

    // Update total checkins
    total = 0;
    $.each(meetups, function() {
        total += this.count;
    });
    $('#checkin-count .count').text(total);

    // Sort the list if there's been inactivity for a bit of time
    clearTimeout(sort_list_timer);
    sort_list_timer = setTimeout(sort_list, 500);

    // Update the markers on the map
    m = new L.marker(new L.LatLng(checkin.lat,checkin.lon));
    markers.addLayer(m);
}

$(document).ready(function() {
    // Set up the map, using OpenStreetMap
    var map = L.map('map').setView([37.7820, -122.4100], 15);
    L.tileLayer('http://{s}.tiles.mapbox.com/v3/mglukhovsky.ikf53bk4/{z}/{x}/{y}.png', {
        attribution: 'Map data &copy; <a href="http://openstreetmap.org">OpenStreetMap</a> contributors, <a href="http://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, Imagery © <a href="http://mapbox.com">Mapbox</a>',
        maxZoom: 18
    }).addTo(map);

    // Add a layer to the map to track checkins via colorful markers
    //markers = L.markerClusterGroup({maxClusterRadius: 20});
    markers = new L.MarkerClusterGroup({

        iconCreateFunction: function(cluster) {
            var childCount = cluster.getChildCount();
            var c = ' marker-cluster-';
            if (childCount < 10) {
                c += 'small';
            } else if (childCount < 100) {
                c += 'medium';
            } else {
                c += 'large';
            }

            return new L.DivIcon({
                html: '<div><span>' + childCount + '</span></div>',
                className: 'marker-cluster' + c,
                iconSize: new L.Point(80, 80) 
            });
        }
    });
    map.addLayer(markers);

}); 
