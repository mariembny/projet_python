const chatMessages = document.getElementById('chat-messages');
const userInput = document.getElementById('user-input');
const sendBtn = document.getElementById('send-btn');

function scrollToBottom() {
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

function formatBotMessage(text) {
    // Convert markdown-like syntax to HTML
    return text
        .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
        .replace(/\*(.*?)\*/g, '<em>$1</em>')
        .replace(/\n\n/g, '</p><p>')
        .replace(/\n/g, '<br>')
        .replace(/^(.+)$/, '<p>$1</p>');
}

function addMessage(content, isUser = false) {
    const msg = document.createElement('div');
    msg.className = `message ${isUser ? 'message-user' : 'message-bot'}`;
    msg.innerHTML = `
        <div class="message-avatar">${isUser ? '👤' : '🤖'}</div>
        <div class="message-bubble">${isUser ? content : formatBotMessage(content)}</div>
    `;
    chatMessages.appendChild(msg);
    scrollToBottom();
}

function addTypingIndicator() {
    const typing = document.createElement('div');
    typing.className = 'message message-bot';
    typing.id = 'typing-indicator';
    typing.innerHTML = `
        <div class="message-avatar">🤖</div>
        <div class="message-bubble">
            <div class="typing-indicator">
                <div class="typing-dot"></div>
                <div class="typing-dot"></div>
                <div class="typing-dot"></div>
            </div>
        </div>
    `;
    chatMessages.appendChild(typing);
    scrollToBottom();
}

function removeTypingIndicator() {
    const t = document.getElementById('typing-indicator');
    if (t) t.remove();
}

async function sendMessage() {
    const message = userInput.value.trim();
    if (!message) return;

    addMessage(message, true);
    userInput.value = '';
    userInput.style.height = 'auto';
    sendBtn.disabled = true;
    addTypingIndicator();

    try {
        const response = await fetch('/api/chat', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ message })
        });
        const data = await response.json();
        removeTypingIndicator();
        addMessage(data.response || data.error || 'Erreur inconnue.');
    } catch (err) {
        removeTypingIndicator();
        addMessage('❌ Erreur de connexion. Vérifiez que le serveur est en marche.');
    } finally {
        sendBtn.disabled = false;
        userInput.focus();
    }
}

function sendSuggestion(btn) {
    userInput.value = btn.textContent;
    sendMessage();
}

function handleKeydown(e) {
    if (e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault();
        sendMessage();
    }
}

// Auto-resize textarea
userInput.addEventListener('input', function() {
    this.style.height = 'auto';
    this.style.height = Math.min(this.scrollHeight, 120) + 'px';
});
