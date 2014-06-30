var meetups = [];
window.meetups = meetups;
var sort_list_timer;

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
}
