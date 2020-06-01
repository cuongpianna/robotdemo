$(document).ready(function () {

    var modal = $('.modal');
    //connect to the socket server.
    var socket = io.connect('http://' + document.domain + ':' + location.port);
    var numbers_received = [];

    // receive details from server
    socket.on('newUdp', function (msg) {
        console.log("Received number" + JSON.stringify(msg));
        socket.emit('status', msg.number);
        var numbers_string = '';

        if (msg.number == 1) {
            modal.hide();
            numbers_string = 'Chế độ điều khiển bằng tay';
            status = 'LED Base_Station  OFF + LED Manual_Mode ON';
            $('#mode').html(numbers_string);
            $('.robot-info').html(status);
        } else if (msg.number == 2) {
            status = "LED Base_Station ON + LED Manual_Mode ON";
            $('.robot-info').html(status);
            if (msg.status == 1) {
                numbers_string = 'Chế độ điều khiển bằng tay';
                $('#mode').html(numbers_string);
                modal.show();
            } else if (msg.status == 0) {
                numbers_string = 'Đang ở Chế độ điều khiển bằng tay nhưng không có kết nối đến server';
                $('#mode').html(numbers_string);
                modal.hide();
                setTimeout(function () {
                    location.reload()
                }, 3000)
            }
        } else if (msg.number == 3) {
            status = 'LED Base_Station ON + LED Auto_Mode ON';
            $('.robot-info').html(status);
            if (msg.status == 1) {
                numbers_string = 'Chế độ điều khiển tự động';
                $('#mode').html(numbers_string);
                modal.show();
            } else {
                numbers_string = 'Đang ở Chế độ điều khiển tự động nhưng không có kết nối đến server';
                $('#mode').html(numbers_string);
                modal.hide();
                setTimeout(function () {
                    location.reload()
                }, 3000)
            }
        } else if (msg.number == 4) {
            status = 'LED Base_Station ON + LED Auto_Following_Line_Mode ON';
            $('.robot-info').html(status);
            if (msg.status == 1) {
                modal.show();
                numbers_string = 'Chế độ tự động bấm vạch từ';
                $('#mode').html(numbers_string);
            } else {
                modal.hide();
                numbers_string = 'Đang ở Chế độ tự động bấm vạch từ nhưng không có kết nối đến server';
                $('#mode').html(numbers_string);
                setTimeout(function () {
                    location.reload();
                }, 3000)
            }
        }
    });

    setInterval(function () {
        socket.emit('connection2');
    }, 1000)

    socket.on('tt', function (msg) {
        var connection = msg.connection;
        if (connection == 0) { // khong ket noi mang
            modal.hide();
            // numbers_string = 'Chế độ điều khiển bằng tay';
            // status = 'LED Base_Station  OFF + LED Manual_Mode ON';
            // $('#mode').html(numbers_string);
            // $('.robot-info').html(status);
            modal.hide()
            setTimeout(function () {
                location.reload();
            }, 3000)
        } else {
            modal.show();
        }
    })

});