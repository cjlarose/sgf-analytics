var pg = require('pg');
var sgf = require('smartgame');

pg.connect('postgres://postgres@postgres/postgres', function(err, client) {
    if (err)
      console.log(err);

    client.on('notification', function(msg) {
      console.log(msg);
    });
    client.query('LISTEN new_event');
    console.log('Listening for events');
});
