// Dashboard frontend
$(document).ready(function() {
    // Open the SocketIO connection to the web server
    var socket = io.connect('http://'+document.domain+':'+location.port);

    // When a checkin happens, update the markers and sidebar
    socket.on('checkin', function(checkin) {
        show_meetup_checkin(checkin);
    });
});
