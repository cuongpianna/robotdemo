$(document).ready(function () {

    var e = 0;
    const robot_code = $('body').attr('data-robot');
    const videoCallUrl = $('body').attr('data-call');
    const wsFrom = $('body').attr('data-wsfrom');
    const wsDownloadMedia = $('body').attr('data-wsmedia');

    console.log(wsFrom);

    var modal = $('.modal');
    //connect to the socket server.
    var socket = io.connect('https://' + document.domain + ':' + location.port, {
        'reconnection': true,
        'reconnectionDelay': 500,
        'reconnectionAttemps': 10
    });


    // receive details from server
    socket.on('newUdp', function (msg) {
        // console.log("Received number" + msg.number);
        // console.log(msg)
        //maintain a list of ten numbers
        var numbers_string = '';
        var status = '';
        e = msg.status;

        if (msg.number == 1) {
            modal.hide();
            numbers_string = 'Chế độ điều khiển bằng tay';
            $('#mode').html(numbers_string);
            $('iframe').attr('src', '');

        } else if (msg.number == 2) {
            numbers_string = 'Chế độ điều khiển tự động';
            $('#mode').html(numbers_string);

            if (msg.status == 1) {
                setTimeout(function () {
                    var src = $('iframe').attr('src');
                    if (src == '' || src == undefined)
                        $('iframe').attr('src', videoCallUrl);
                    modal.show();
                }, 7000)
            } else {
                modal.hide();
            }
        }
    });

    function connect2() {
    var socket2 = new WebSocket(wsFrom)
    socket2.onopen = function () {
        console.log('Connected.')
    }

    socket2.onclose = function (event) {
        setTimeout(function () {
        connect2();
        }, 1000)
        if (event.wasClean) {
            console.log('Disconnected.')
        } else {
            console.log('Connection lost.')
        }
        console.log('Code: ' + event.code + '. Reason: ' + event.reason)
    }

    socket2.onmessage = function (event) {
        // @2#16#2#1.5#&_R70448
        var message = event.data
        console.log('Data received: ' + message)
        var robotNo = message.split("&_");
        if (robotNo[1] != undefined && robotNo[1] == robot_code) {
            socket.emit('leave', {value: robotNo[0]});
        }
    }}

    function connectMedia() {
        var socketMedia = new WebSocket(wsDownloadMedia)
    socketMedia.onopen = function () {
        console.log('Connected.')
    }

    socketMedia.onclose = function (event) {
        setTimeout(function () {
        connectMedia();
        socketMedia.onopen = function () {
        console.log('Connected.')
    }
        }, 1000)


        if (event.wasClean) {
            console.log('Disconnected.')
        } else {
            console.log('Connection lost.')
        }
        console.log('Code: ' + event.code + '. Reason: ' + event.reason)
    }

    socketMedia.onmessage = function (event) {
        // @2#16#2#1.5#&_R70448
        var message = event.data
        var messageSend = JSON.parse(JSON.stringify(event.data))
        if (message.includes('DownloadMedia')) {
            console.log('Data received: ' + message)
            var robotNo = message.split("_");
            console.log(robotNo)
            console.log(robotNo[1])
            if (robotNo[1] != undefined && robotNo[1] == robot_code) {
                socket.emit('download', {value: messageSend});
                console.log(robot_code)
                // location.reload()
            }
        }
    }
    }

    connect2();
    connectMedia();

});
