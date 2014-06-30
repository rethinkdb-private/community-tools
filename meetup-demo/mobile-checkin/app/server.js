// Set up Express app and modules
var express = require('express')
var app = express();
var server = require('http').Server(app);
var bodyParser = require('body-parser');
app.use(bodyParser.json())
    .use(express.static(__dirname + '/static'));

// Create a RethinkDB connection
var r = require('rethinkdb')
var connection = r.connect({ host: 'localhost', port: 28015});

// Send static files
app.get('/', function(req, res) {
    res.sendfile(__dirname + '/index.html');
});

// Collect a check-in from the form
app.post('/checkin', function(req, res) {
    connection.then(function(conn) {
        r.db('meetup').table('checkins').insert(req.body).run(conn).error(console.log);
    }).then(function() { return res.send(200)} );
});

// Start the app
server.listen(3002);
