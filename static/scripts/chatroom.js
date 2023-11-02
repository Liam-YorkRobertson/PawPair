const socket = io();
const messagesContainer = document.getElementById('messages');
const messageInput = document.getElementById('message-input');
const sendButton = document.getElementById('send-button');

// Get the username from the query string
const urlParams = new URLSearchParams(window.location.search);
const username = urlParams.get('username');

// Event listener for send button click
sendButton.addEventListener('click', () => {
    const message = messageInput.value.trim();
    if (message) {
        socket.emit('chatMessage', { message, username });
        messageInput.value = '';
    }
});

// Event listener for 'chatMessage' event from the server
socket.on('chatMessage', (data) => {
    const { message, sender } = data;
    const messageElement = document.createElement('div');
    messageElement.textContent = `${sender}: ${message}`;
    messagesContainer.appendChild(messageElement);
});