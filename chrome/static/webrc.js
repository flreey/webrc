var irc = 'undefied' === typeof irc? irc: {};
var socket = io.connect('http://localhost:8001');

(function(irc){

    irc.login = function(nick, password, channel) {
        socket.emit('login', {'nick': nick, 'password': password, 'channel': channel},
            function(data){
                if (data == 'success'){
                    $('#login_frame').hide();
                    $('#chat_frame').show();
                    $('#send_msg').click(function(){
                        msg = $('#msg').val();
                        if (msg.length) {
                            irc.sendmsg(msg);
                        }

                    })
                }
            });
    }

    irc.sendmsg = function(msg){
        socket.send(msg);
    }

    socket.on('message', function(data){
        $('#msgbox').append(data+'</br>');
        $('#msgbox').scrollTop(1000000);
    })
}
)(irc)

$(function(){
        socket.on('connect', function(){
            $('#login').click(function(){
                var nickname = $('#nickname').val();
                if (nickname.length){
                    irc.login(nickname, '', 'test');
                }
            })
        })
})
