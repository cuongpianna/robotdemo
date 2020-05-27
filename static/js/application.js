
$(document).ready(function(){

    var modal = $('.modal');
    //connect to the socket server.
    var socket = io.connect('http://' + document.domain + ':' + location.port + '/test');
    var numbers_received = [];

    //receive details from server
    socket.on('newUdp', function(msg) {
        console.log("Received number" + msg.number);
        //maintain a list of ten numbers
        if (numbers_received.length >= 10){
            numbers_received.shift()
        }
        numbers_received.push(msg.number);
        numbers_string = '';
        for (var i = 0; i < numbers_received.length; i++){
            numbers_string = numbers_string + '<p>' + numbers_received[i].toString() + '</p>';
        }
        if(msg.number == 1) {
            $('.row').removeClass('active');
            $('.row1').addClass('active');
            modal.hide();
            numbers_string = 'Chế độ điều khiển bằng tay';
        }else if(msg.number == 2) {
            modal.hide();
            $('.row').removeClass('active');
            $('.row2').addClass('active');
            if(msg.status == 1) {
                numbers_string = '<div>Chế độ điều khiển bằng tay</div><div>Kết nối trạm điều khiển trung tâm thành công</div>';
            }else {
                numbers_string = '<div>Chế độ điều khiển bằng tay</div><div>Kết nối trạm điều khiển trung tâm thất bại</div>';
            }
        }else if(msg.number == 3) {
            modal.hide();
            $('.row').removeClass('active');
            $('.row3').addClass('active');
            if(msg.status == 1) {
                numbers_string = '<div>Chế độ điều khiển tự động</div><div>Kết nối trạm điều khiển trung tâm thành công</div>';
            }else {
                numbers_string = '<div>Chế độ điều khiển bằng tay</div><div>Kết nối trạm điều khiển trung tâm thất bại</div>';
            }
        }else if(msg.number == 4) {
            $('.row').removeClass('active');
            $('.row4').addClass('active');
            modal.show();
            if(msg.status == 1) {
                numbers_string = '<div>Chế độ tự động bấm vạch từ</div><div>Kết nối trạm điều khiển trung tâm thành công</div>';
            }else {
                numbers_string = '<div>Chế độ điều khiển bằng tay</div><div>Kết nối trạm điều khiển trung tâm thất bại</div>';
            }
        }
        $('#log').html(numbers_string);
    });

});