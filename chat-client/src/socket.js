import openSocket from 'socket.io-client';
const socket = openSocket('http://localhost:8080');

function subscribeToMessage(fetchFunc) {
    socket.on('fetch', () => fetchFunc());
}

export { subscribeToMessage };