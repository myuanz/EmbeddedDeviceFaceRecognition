import io from 'socket.io-client';

const socket = io.connect('http://192.168.1.156:8000/test');
socket.on('connect', function () {
    socket.emit('my event', {data: 'I\'m connected!'});
});

function subscribeToTimer(cb) {
    socket.on('timer', timestamp => {
            cb(null, new Date(timestamp.timestamp * 1000).toLocaleString())
        }
    );

    // socket.emit('subscribeToTimer', 1000);
}

function send_message_to_device(type, param) {
    socket.emit('send_message_to_device', type, param);
}

function register_recv_callback(recv_callback) {
    register_event_callback('recv_callback', recv_callback);
}

function register_event_callback(event_name, recv_callback) {
    socket.on(event_name, recv_callback);
}
function emit(type, ...args) {
    socket.emit(type, ...args);
}

export {
    subscribeToTimer,
    register_recv_callback,
    send_message_to_device,
    register_event_callback,
    emit,
};
