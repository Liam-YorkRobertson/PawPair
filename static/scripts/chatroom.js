// create connection to socket.io server
const socket = io.connect();
const messagesContainer = document.getElementById('chat-messages');
const messageInput = document.getElementById('message-input');
const sendButton = document.getElementById('send-button');
const terminateChatroomButton = document.getElementById('terminate-chatroom-btn');
const dogDateButton = document.getElementById('schedule-dog-date-btn');

// get the receiver's username from the URL
const receiverUsername = window.location.pathname.split('/').pop();

// event listener for send button click
sendButton.addEventListener('click', () => {
    sendMessage();
});

// event listener for 'chatMessage' event from the server
socket.on('chatMessage', (data) => {
    console.log('Received message:', data);
    const { sender, message } = data;
    appendMessage(sender, message);
});

// event listener for enter key press
messageInput.addEventListener('keyup', (event) => {
    if (event.key === 'Enter') {
        sendMessage();
    }
});

// event listener for 'chatHistory' event from the server
socket.on('chatHistory', (messages) => {
    messagesContainer.innerHTML = '';  // Clear existing messages
    messages.forEach((message) => {
        appendMessage(message.sender_username, message.message);
    });
});

// event listener for terminate chatroom button click
terminateChatroomButton.addEventListener('click', () => {
    const receiverUsername = window.location.pathname.split('/').pop();
    const confirmation = confirm("You are going to terminate this chatroom, and your chat history will no longer be available to you. Are you sure?");
    if (confirmation) {
        // send a delete request to terminate the chatroom
        fetch(`/terminate_chatroom?receiver_username=${receiverUsername}`, {
            method: 'DELETE',
            headers: {
                'Content-Type': 'application/json'
            }
        })
        .then(response => {
            if (response.ok) {
                // chatroom terminated successfully, redirect to user_dashboard.html
                window.location.href = '/user_dashboard';
            } else {
                // handle error
                console.error('Chatroom not terminated.');
            }
        })
        .catch(error => {
            // handle network error
            console.error('Network error:', error);
        });
    } else {
        // user clicked 'No', do nothing
    }
});

// event listener for schedule dog date button click
dogDateButton.addEventListener('click', () => {
    const receiverUsername = window.location.pathname.split('/').pop();
    const confirmation = confirm("You are going to schedule a dog date, and your chat history will no longer be available to you. Are you sure?");
    if (confirmation) {
        // send a delete request to terminate the chatroom
        fetch(`/terminate_chatroom?receiver_username=${receiverUsername}`, {
            method: 'DELETE',
            headers: {
                'Content-Type': 'application/json'
            }
        })
        .then(response => {
            if (response.ok) {
                // chatroom terminated successfully, redirect to thank_you.html
                window.location.href = '/user_thank_you';
            } else {
                // handle error
                console.error('Chatroom not terminated.');
            }
        })
        .catch(error => {
            // handle network error
            console.error('Network error:', error);
        });
    } else {
        // user clicked 'No', do nothing
    }
});

// function to send a chat message
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

// function to append a chat message to the messages container
function appendMessage(sender, message) {
    const messageElement = document.createElement('div');
    messageElement.textContent = `${sender}: ${message}`;
    messagesContainer.appendChild(messageElement);
    // scroll to the latest message
    messagesContainer.scrollTop = messagesContainer.scrollHeight;
}