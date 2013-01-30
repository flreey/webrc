
//var websocket = '';
//var connect = function() {
    ////var wsServer = 'ws://192.168.1.171:1337';
    //var wsServer = 'ws://192.168.1.124:8000';
    //websocket = new WebSocket(wsServer); 
    //websocket.onopen = function (evt) { onOpen(evt) }; 
    //websocket.onclose = function (evt) { onClose(evt) }; 
    //websocket.onmessage = function (evt) { onMessage(evt) }; 
    //websocket.onerror = function (evt) { onError(evt) }; 
    //var name = 'test'+parseInt(Math.random() * 10000) + '';
    //function onOpen(evt) { 
        //console.log("Connected to WebSocket server."); 
        //websocket.send('CAP LS\r\n');
        //websocket.send('NICK '+name+'\r\nUSER '+name + ' ' + name + ' 127.0.0.1 :'+name+'\r\n');
        //setInterval(function(){websocket.send('PING LAG2029982703\r\n')}, 10000);
    //} 
    //function onClose(evt) { 
        //console.log("Disconnected"); 
    //} 
    //var firstJoin = true;

    //function onMessage(evt) { 
        //console.log(evt.data);
        //if (evt.data.substr(0, name.length) == ':'+name){
            //websocket.send('PING LAG2029982703\r\n');
            //if (firstJoin) {
                //websocket.send('JOIN #testc\r\n');
                //firstJoin = false;
            //}
        //} else {
            //var content = document.getElementById('content')
            //content.innerText = content.innerText + '\n' + evt.data;
        //}
    //} 
    //function onError(evt) { 
        //console.log('Error occured: ' + evt.data); 
    //} 
//}

//var sendMsg = function() {
    //var msg = document.getElementById('msg');
    //if (msg.value.length > 0){
        //websocket.send(msg.value);
        //console.log('send msg:' + msg.value); 
        //msg.value = '';
    //}
//}
//// Run our kitten generation script as soon as the document's DOM is ready.
//document.addEventListener('DOMContentLoaded', function () {
    //connect();
    //document.getElementById('send').addEventListener('click',
        //function(){
            //sendMsg();
        //}
    //)
//});
