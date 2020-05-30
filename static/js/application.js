$(document).ready(function () {

    var modal = $('.modal');
    //connect to the socket server.
    var socket = io.connect('http://' + document.domain + ':' + location.port + '/test');
    var numbers_received = [];

    //receive details from server
    socket.on('newUdp', function (msg) {
        console.log("Received number" + msg.number);
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
        if (msg.number == 1) {
            modal.hide();
            numbers_string = 'Chế độ điều khiển bằng tay';
            status = 'LED Base_Station  OFF + LED Manual_Mode ON';
            $('#mode').html(numbers_string);
            $('.robot-info').html(status);
        } else if (msg.number == 2) {
            numbers_string = 'Chế độ điều khiển bằng tay';
            status = "LED Base_Station ON + LED Manual_Mode ON";
            $('#mode').html(numbers_string);
            $('.robot-info').html(status);
            modal.hide();
            if (msg.status == 1) {
                setTimeout(function () {
                    modal.show();
                }, 1000)
            }
        } else if (msg.number == 3) {
            numbers_string = 'Chế độ điều khiển tự động';
            status = 'LED Base_Station ON + LED Manual_Mode ON';
            $('#mode').html(numbers_string);
            $('.robot-info').html(status);
            modal.hide();
            if (msg.status == 1) {
                setTimeout(function () {
                    modal.show();
                }, 1000)
            }
        } else if (msg.number == 4) {
            numbers_string = 'Chế độ tự động bấm vạch từ';
            status = 'LED Base_Station ON + LED Auto_Following_Line_Mode ON';
            $('#mode').html(numbers_string);
            $('.robot-info').html(status);
            modal.hide();
            if (msg.status == 1) {
                setTimeout(function () {
                    modal.show();
                }, 1000)
            }
        }
    });

});