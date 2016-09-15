$(document).ready(function() {
    var socket = io.connect('http://' + document.domain + ':' + location.port + '/jousty');

    socket.on('test', function(payload) {
        console.log('got message');
        console.log(payload);
    });
});