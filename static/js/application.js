$(document).ready(function () {

    var e = 0;

    var modal = $('.modal');
    //connect to the socket server.
    var socket = io.connect('http://' + document.domain + ':' + location.port);

    var numbers_received = [];

    var connectionNetwork = -1;

    socket.on('tt', function (msg) {
        var connection = msg.connection;
        if (connectionNetwork != connection) {
            connectionNetwork = connection;
            if (connection == 0) { // khong ket noi mang
                modal.hide()
            } else {
                modal.show();
            }
        }

    })

    setInterval(function () {
        socket.emit('connection2');
    }, 1000)

    // receive details from server
    socket.on('newUdp', function (msg) {
        console.log("Received number" + msg.number);
        socket.emit('status', msg.number);
        //maintain a list of ten numbers
        if (numbers_received.length >= 10) {
            numbers_received.shift()
        }
        numbers_received.push(msg.number);
        var numbers_string = '';
        var status = '';
        for (var i = 0; i < numbers_received.length; i++) {
            numbers_string = numbers_string + '<p>' + numbers_received[i].toString() + '</p>';
        }

        e = msg.status;

        if (msg.number == 1) {
            modal.hide();
            numbers_string = 'Chế độ điều khiển bằng tay';
            status = 'LED Base_Station  OFF + LED Manual_Mode ON';
            $('#mode').html(numbers_string);
            $('.robot-info').html(status);
            $('iframe').attr('src', '');

        } else if (msg.number == 2) {
            numbers_string = 'Chế độ điều khiển bằng tay';
            status = "LED Base_Station ON + LED Manual_Mode ON";
            $('#mode').html(numbers_string);
            $('.robot-info').html(status);
            var src = $('iframe').attr('src');
            if (src == '')
                $('iframe').attr('src', 'https://157.230.245.8/f');

            if (msg.status == 1) {
                setTimeout(function () {
                    modal.show();
                }, 4000)
            }

        } else if (msg.number == 3) {
            numbers_string = 'Chế độ điều khiển tự động';
            status = 'LED Base_Station ON + LED Manual_Mode ON';
            $('#mode').html(numbers_string);
            $('.robot-info').html(status);
            // modal.hide();

            var src = $('iframe').attr('src');
            if (src == '')
                $('iframe').attr('src', 'https://157.230.245.8/f');

            if (msg.status == 1) {
                setTimeout(function () {
                    modal.show();
                }, 4000)
            }
        } else if (msg.number == 4) {
            numbers_string = 'Chế độ tự động bấm vạch từ';
            status = 'LED Base_Station ON + LED Auto_Following_Line_Mode ON';
            $('#mode').html(numbers_string);
            $('.robot-info').html(status);

            var src = $('iframe').attr('src');
            if (src == '')
                $('iframe').attr('src', 'https://157.230.245.8/f');
            // modal.hide();
            if (msg.status == 1) {
                setTimeout(function () {
                    modal.show();
                }, 4000)
            }
        }
    });

});
