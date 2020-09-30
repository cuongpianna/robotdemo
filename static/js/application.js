$(document).ready(function () {
    const robot_code = $('body').attr('data-robot');
    const videoCallUrl = $('body').attr('data-call');
    const wsFrom = $('body').attr('data-wsfrom');
    const wsDownloadMedia = $('body').attr('data-wsmedia');
    var e = 0;

    var modal = $('.modal');
    //connect to the socket server.
    var socket = io.connect('http://' + document.domain + ':' + location.port);

    // receive details from server
    socket.on('leave', function (msg) {
        console.log("Received number" + msg.number);
        socket.emit('status', msg.number);

        e = msg.status;

        if (msg.number == 1) {
            modal.hide();
            numbers_string = 'Chế độ điều khiển bằng tay';
            status = 'LED Base_Station  OFF + LED Manual_Mode ON';
            $('#mode').html(numbers_string);
            $('.robot-info').html(status);
            $('iframe').attr('src', '');

        } else if (msg.number == 2) {
            numbers_string = 'Chế độ điều khiển tự động';
            status = "LED Base_Station ON + LED Manual_Mode ON";
            $('#mode').html(numbers_string);
            $('.robot-info').html(status);
            var src = $('iframe').attr('src');
            if (src == '')
                $('iframe').attr('src', videoCallUrl);

            if (msg.status == 1) {
                setTimeout(function () {
                    modal.show();
                }, 4000)
            }

        // } else if (msg.number == 3) {
        //     numbers_string = 'Chế độ điều khiển tự động';
        //     status = 'LED Base_Station ON + LED Manual_Mode ON';
        //     $('#mode').html(numbers_string);
        //     $('.robot-info').html(status);
        //     // modal.hide();
        //
        //     var src = $('iframe').attr('src');
        //     if (src == '')
        //         $('iframe').attr('src', videoCallUrl);
        //
        //     if (msg.status == 1) {
        //         setTimeout(function () {
        //             modal.show();
        //         }, 4000)
        //     }
        // } else if (msg.number == 4) {
        //     numbers_string = 'Chế độ tự động bấm vạch từ';
        //     status = 'LED Base_Station ON + LED Auto_Following_Line_Mode ON';
        //     $('#mode').html(numbers_string);
        //     $('.robot-info').html(status);
        //
        //     var src = $('iframe').attr('src');
        //     if (src == '')
        //         $('iframe').attr('src', videoCallUrl);
        //     // modal.hide();
        //     if (msg.status == 1) {
        //         setTimeout(function () {
        //             modal.show();
        //         }, 4000)
        //     }
        }
    });

    var socket2 = new WebSocket(wsFrom)
    socket2.onopen = function () {
        console.log('Connected.')
    }

    socket2.onclose = function (event) {
        setTimeout(function () {
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
    }

    console.log(wsDownloadMedia)
    var socketMedia = new WebSocket(wsDownloadMedia)
    socketMedia.onopen = function () {
        console.log('Connected.')
    }

    socketMedia.onclose = function (event) {
        setTimeout(function () {
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
                location.reload()
            }
        }
    }
});
