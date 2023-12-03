
const express = require('express');
const app = express();
const server = require('http').createServer(app);
const WebSocket = require('ws');

const wss = new WebSocket.Server({ server: server });
const PORT = process.env.PORT || 3000;

wss.on('connection', function connection(ws, req) {
    console.log('A new client connected: ' + req.socket.remoteAddress);
    ws.send(JSON.stringify({ connection: 'Connection Established with Intermediate Server' }));
    ws.on('message', function incoming(message) {
        console.log('received: %s', message);
        wss.clients.forEach(function each(client) {
            if (client !== ws && client.readyState === WebSocket.OPEN) {
                client.send(message.toString());
            }
        });
    });
})

app.get('/alive', (req, res) => {
    console.log('Alive called..');
    res.json({ status: 'alive' });
})

server.listen(PORT, () => console.log(`Server is now listening on port ${PORT}`));


