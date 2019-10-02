import io from 'socket.io-client';

const socket = io.connect('http://127.0.0.1:8000/test');
socket.on('connect', function() {
  socket.emit('my event', {data: 'I\'m connected!'});
});

function subscribeToTimer(cb) {
  socket.on('timer', timestamp => {
      cb(null, new Date(timestamp.timestamp*1000).toLocaleString())
    }
  );
  
    socket.emit('subscribeToTimer', 1000);
}

export { subscribeToTimer };
