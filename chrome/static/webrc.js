var socket = io.connect('http://localhost:8001');
socket.send('hello');
socket.emit('news', { msg: 'data' });

