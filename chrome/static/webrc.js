var client = 'undefied' === typeof client? client: {};
(function(client){

    client.login = function(nick, password, channel) {
        socket.emit('login', {'nick': nick, 'password': password, 'channel': channel},
            function(data){
                if (data == 'success'){
                    $('#login_frame').hide();
                    $('#chat_frame').show();
                    $('#send_msg').click(function(){
                        msg = $('#msg').val();
                        if (msg.length) {
                            client.sendmsg(msg);
                        }

                    })
                }
            });
    }

    client.sendmsg = function(msg){
        socket.send(msg);
    }
}
)(client)

$(function(){
        var socket = io.connect('http://localhost:8001');

        socket.on('connect', function(){
            $('#login').click(function(){
                var nickname = $('#nickname').val();
                if (nickname.length){
                    client.login(nickname, '', 'test');
                }
            })
        })


        socket.on('message', function(data){
            _.each(data.split('\r\n'), function(line){
                values = line.split(' ');
                switch(values[1]) {
                    case 'JOIN':
                        $('#msgbox').append(values[0]+':'+line.substr(line.indexOf(values[2]+' :', line.length))+'</br>');
                        break;
                    case 'PRIVMSG':
                        $('#msgbox').append(values[0]+':'+line.substr(line.indexOf(values[2]+' :'), line.length)+'</br>');
                        break;
                    default:
                        console.log(values[1]);
                        break;
                }

                $('#msgbox').scrollTop(1000000);
            })
        })

        socket.on('disconnect', function(){
            //socket = io.connect('http://localhost:8001');
            console.log('disconnect')
        })
})
