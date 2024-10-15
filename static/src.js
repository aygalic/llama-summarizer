const chatArea = document.getElementById('chat-area');
const chatInput = document.getElementById('chat-input');
const sendBtn = document.getElementById('send-btn');

class ChatHistory {
    constructor() {
        this.history = [];
    }

    addMessage(role, content) {
        this.history.push([role, content]);
    }
}

const chatHistory = new ChatHistory();

function appendMessage(role, content) {
    const messageDiv = document.createElement('div');
    messageDiv.classList.add('chat-message', `${role}-message`);
    messageDiv.textContent = content;
    chatArea.appendChild(messageDiv);
    chatArea.scrollTop = chatArea.scrollHeight;
}

sendBtn.addEventListener('click', async function() {
    const input = chatInput.value.trim();
    if (!input) return;

    appendMessage('user', input);
    chatInput.value = '';

    chatHistory.addMessage('user', input);

    try {
        const response = await fetch('/stream_chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ item: chatHistory.history }),
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const reader = response.body.getReader();
        const decoder = new TextDecoder();
        let modelResponse = '';

        while (true) {
            const { value, done } = await reader.read();
            if (done) break;
            const decodedChunk = decoder.decode(value, { stream: true });
            const lines = decodedChunk.split('\n\n');
            for (const line of lines) {
                if (line.startsWith('data: ')) {
                    const token = line.slice(6);
                    modelResponse += token;
                    // Clear previous model response and update with new one
                    const lastMessage = chatArea.lastElementChild;
                    if (lastMessage && lastMessage.classList.contains('model-message')) {
                        lastMessage.textContent = modelResponse;
                    } else {
                        appendMessage('model', modelResponse);
                    }
                }
            }
        }

        chatHistory.addMessage('assistant', modelResponse);
    } catch (error) {
        console.error('Error:', error);
        appendMessage('model', 'An error occurred while fetching the response.');
    }
});

chatInput.addEventListener('keypress', function(e) {
    if (e.key === 'Enter') {
        sendBtn.click();
    }
});