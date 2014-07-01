// Set up RethinkDB, Express app and modules
var r = require('rethinkdb')
var express = require('express')
var app = express();
var server = require('http').Server(app);
var io = require('socket.io')(server);
var coro = require('bluebird').coroutine;

// Maintain a SocketIO connection to the client
io.on('connection', coro(function *(socket) {
    // Establish a RethinkDB connection for the new client
    conn = yield r.connect({host: 'localhost', port: 28015});

    // Follow a changefeed of check-ins
    feed = yield r.db('meetup').table('checkins').changes().run(conn);

    // For each change in the feed, notify the browser
    feed.each(function(err, change) {
        if (change.new_val) {
            socket.emit('checkin', change.new_val);
        }
    });

    // Close the RethinkDB connection when the browser disconnects
    socket.on('disconnect', function() {
        conn.close();
    });
}));

// Serve static files
app.use(express.static(__dirname + '/static'));
app.get('/', function(req, res) {
    res.sendfile(__dirname + '/index.html');
});

// Start the app
server.listen(3001);
