// Mobile check-in server
// Set up RethinkDB, Express app and modules
var r = require('rethinkdb')
var express = require('express')
var app = express();
var server = require('http').Server(app);
var bodyParser = require('body-parser');
var coro = require('bluebird').coroutine;

// Parse responses from the form
app.use(bodyParser.json())
    .use(express.static(__dirname + '/static'));

// Collect a check-in from the form
app.post('/checkin', coro(function *(req, res) {
    // Establish a RethinkDB connection for the new client
    conn = yield r.connect({host: 'localhost', port: 28015});

    // Insert the check-in into the database
    yield r.db('meetup').table('checkins').insert({
        event_name: req.body.event_name,
        lat: req.body.lat,
        lon: req.body.lon,
    }).run(conn);

    return res.send(200);
}));

// Serve static files 
app.get('/', function(req, res) {
    res.sendfile(__dirname + '/index.html');
});

// Start the app
server.listen(3002);
