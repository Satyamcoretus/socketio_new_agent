const chatBox = document.getElementById('chat-box');
const messageInput = document.getElementById('message-input');
const sendButton = document.getElementById('send-button');

// Function to create a chat message element
function createChatMessage(message, isUserMessage) {
  const chatMessage = document.createElement('div');
  chatMessage.classList.add('chat-message');

  if (isUserMessage) {
    chatMessage.classList.add('user-message');
  } else {
    chatMessage.classList.add('bot-message');
  }

  chatMessage.textContent = message;
  return chatMessage;
}

// Function to simulate a bot response (replace with actual logic later)
function simulateBotResponse(message) {
  const response = `You said: "${message}"`;
  const botMessage = createChatMessage(response, false);
  chatBox.appendChild(botMessage);
  chatBox.scrollTop = chatBox.scrollHeight; // Scroll to the bottom
}

// Handle send button click
sendButton.addEventListener('click', () => {
  const userMessage = messageInput.value.trim();
  if (userMessage) {
    const userChatMessage = createChatMessage(userMessage, true);
    chatBox.appendChild(userChatMessage);
    messageInput.value = ''; // Clear the input field

    // Simulate a bot response (replace with actual logic)
    simulateBotResponse(userMessage);
  }
});
