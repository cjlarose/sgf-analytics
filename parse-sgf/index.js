var pg = require('pg');
var sgf = require('smartgame');
var Promise = require('rsvp').Promise;

function getEvent(client, eventId) {
    return new Promise(function(resolve, reject) {
        var query = "SELECT events.id, events.created_at, events.data " +
                    "FROM events WHERE events.id = $1";
        client.query(query, [eventId], function(err, result) {
            if (err)
                reject(err);
            else {
                resolve(result.rows[0]);
            }
        });
    });
}

function handleNotification(client, msg) {
      var eventId = msg.payload;
      getEvent(client, eventId)
          .then(function(ev) {
              console.log(ev);
              var collection = sgf.parse(ev.data.contents);
              var output = collection.gameTrees[0].nodes;
              console.log(output);
          });
}

function getStreamId(client, streamName) {
    return new Promise(function(resolve, reject) {
        var query = "SELECT id FROM streams WHERE name = $1";
        client.query(query, [streamName], function(err, result) {
            if (err) {
                reject(err)
            } else {
                resolve(result.rows[0].id);
            }
        });
    });
}

var inputStream = 'raw_sgf';
var outputStream = 'parsed_sgf';

pg.connect('postgres://postgres@postgres/postgres', function(err, client) {
    if (err)
        console.log(err);

    client.on('notification', handleNotification.bind(null, client));

    getStreamId(client, inputStream)
        .then(function(streamId) {
          console.log("Listening on channel new_event_%d", streamId);
          client.query('LISTEN new_event_' + streamId);
        });
});
