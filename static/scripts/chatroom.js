const socket = io.connect();
const messagesContainer = document.getElementById('chat-messages');
const messageInput = document.getElementById('message-input');
const sendButton = document.getElementById('send-button');

// Get the receiver's username from the URL
const receiverUsername = window.location.pathname.split('/').pop();

// Event listener for send button click
sendButton.addEventListener('click', () => {
    sendMessage();
});

// Event listener for 'chatMessage' event from the server
socket.on('chatMessage', (data) => {
    console.log('Received message:', data);
    const { sender, message } = data;
    appendMessage(sender, message);
});

// Event listener for Enter key press
messageInput.addEventListener('keyup', (event) => {
    if (event.key === 'Enter') {
        sendMessage();
    }
});

// Event listener for 'chatHistory' event from the server
socket.on('chatHistory', (messages) => {
    messagesContainer.innerHTML = '';  // Clear existing messages
    messages.forEach((message) => {
        appendMessage(message.sender_username, message.message);
    });
});

function sendMessage() {
    const message = messageInput.value.trim();
    if (message) {
        const senderUsername = sessionStorage.getItem('username');
        socket.emit('chatMessage', { message, sender_username: senderUsername, receiver_username: receiverUsername });
        messageInput.value = '';
        setTimeout(() => {
            window.location.reload();
        }, 250);
    }
}

function appendMessage(sender, message) {
    const messageElement = document.createElement('div');
    messageElement.textContent = `${sender}: ${message}`;
    messagesContainer.appendChild(messageElement);

    // Scroll to the latest message
    messagesContainer.scrollTop = messagesContainer.scrollHeight;
}

const terminateChatroomButton = document.getElementById('terminate-chatroom-btn');
const dogDateButton = document.getElementById('schedule-dog-date-btn');

terminateChatroomButton.addEventListener('click', () => {
    const receiverUsername = window.location.pathname.split('/').pop();
    const confirmation = confirm("You are going to terminate this chatroom, and your chat history will no longer be available to you. Are you sure?");
    if (confirmation) {
        // Send a DELETE request to terminate the chatroom
        fetch(`/terminate_chatroom?receiver_username=${receiverUsername}`, {
            method: 'DELETE',
            headers: {
                'Content-Type': 'application/json'
            }
        })
        .then(response => {
            if (response.ok) {
                // Chatroom terminated successfully, redirect to user_dashboard.html
                window.location.href = '/user_dashboard';
            } else {
                // Handle error (chatroom not terminated)
                console.error('Chatroom not terminated.');
            }
        })
        .catch(error => {
            // Handle network error
            console.error('Network error:', error);
        });
    } else {
        // User clicked 'No', do nothing
    }
});

dogDateButton.addEventListener('click', () => {
    const receiverUsername = window.location.pathname.split('/').pop();
    const confirmation = confirm("You are going to schedule a dog date, and your chat history will no longer be available to you. Are you sure?");
    if (confirmation) {
        // Send a DELETE request to terminate the chatroom
        fetch(`/terminate_chatroom?receiver_username=${receiverUsername}`, {
            method: 'DELETE',
            headers: {
                'Content-Type': 'application/json'
            }
        })
        .then(response => {
            if (response.ok) {
                // Chatroom terminated successfully, redirect to thank_you.html
                window.location.href = '/user_thank_you';
            } else {
                // Handle error (chatroom not terminated)
                console.error('Chatroom not terminated.');
            }
        })
        .catch(error => {
            // Handle network error
            console.error('Network error:', error);
        });
    } else {
        // User clicked 'No', do nothing
    }
});