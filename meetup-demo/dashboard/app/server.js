// Set up Express app and modules
var express = require('express')
var app = express();
var server = require('http').Server(app);
var io = require('socket.io')(server);
app.use(express.static(__dirname + '/static'));

// Create a RethinkDB connection
var r = require('rethinkdb')
var connection = r.connect({ host: 'localhost', port: 28015});

// Send static files
app.get('/', function(req, res) {
    res.sendfile(__dirname + '/index.html');
});

// Maintain a list of SocketIO clients whenever a client connects or disconnects
var clients = [];
io.on('connection', function (socket) {
    clients.push(socket);

    socket.on('disconnect', function() {
        clients.splice(clients.indexOf(socket),1);
    });
});

// Follows a changefeed of check-ins
connection.then(function(conn) {
    return r.db('meetup').table('checkins').changes().run(conn).error(console.log);
})
    .then(function(changefeed) {
        // Push all new values in the feed to each SocketIO client
        changefeed.each(function(err, change) {
            if (change.new_val) {
                clients.forEach(function(client) {
                    client.emit('checkin', change.new_val);
                });
            }
        });
    });

// Start the app
server.listen(3001);
