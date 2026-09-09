/**
 * AWS S3 Assistant - Chat Application
 * An intelligent assistant for AWS S3 storage questions
 */

(function() {
    'use strict';

    // ===================================
    // STATE MANAGEMENT
    // ===================================
    const state = {
        messages: [],
        isLoading: false,
        pendingQuestion: null
    };

    // ===================================
    // DOM ELEMENTS
    // ===================================
    const elements = {
        messagesContainer: document.getElementById('messagesContainer'),
        messageInput: document.getElementById('messageInput'),
        sendButton: document.getElementById('sendButton'),
        clearChat: document.getElementById('clearChat'),
        welcomeMessage: document.getElementById('welcomeMessage'),
        sidebar: document.getElementById('sidebar'),
        sidebarToggle: document.getElementById('sidebarToggle'),
        sidebarOverlay: document.getElementById('sidebarOverlay'),
        sampleChips: document.querySelectorAll('.sample-chip')
    };

    // ===================================
    // INITIALIZATION
    // ===================================
    function init() {
        loadChatHistory();
        setupEventListeners();
        configureMarkdown();

        // Focus input on load
        elements.messageInput.focus();

        // Hide welcome if there's history
        if (state.messages.length > 0 && elements.welcomeMessage) {
            elements.welcomeMessage.style.display = 'none';
        }
    }

    function configureMarkdown() {
        if (typeof marked !== 'undefined') {
            marked.setOptions({
                breaks: true,
                gfm: true,
                highlight: function(code, lang) {
                    if (typeof hljs !== 'undefined' && lang && hljs.getLanguage(lang)) {
                        return hljs.highlight(code, { language: lang }).value;
                    }
                    return code;
                }
            });
        }
    }

    // ===================================
    // EVENT LISTENERS
    // ===================================
    function setupEventListeners() {
        // Send message
        elements.sendButton.addEventListener('click', handleSend);
        elements.messageInput.addEventListener('keydown', handleInputKeydown);

        // Auto-resize textarea
        elements.messageInput.addEventListener('input', handleInputChange);

        // Clear chat
        elements.clearChat.addEventListener('click', clearChat);

        // Sample questions
        elements.sampleChips.forEach(chip => {
            chip.addEventListener('click', () => {
                const question = chip.dataset.question;
                elements.messageInput.value = question;
                handleSend();
                closeSidebar();
            });
        });

        // Mobile sidebar
        elements.sidebarToggle.addEventListener('click', toggleSidebar);
        elements.sidebarOverlay.addEventListener('click', closeSidebar);
    }

    // ===================================
    // INPUT HANDLING
    // ===================================
    function handleInputKeydown(e) {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            handleSend();
        }
    }

    function handleInputChange() {
        // Auto-resize
        elements.messageInput.style.height = 'auto';
        elements.messageInput.style.height = Math.min(elements.messageInput.scrollHeight, 120) + 'px';

        // Update send button state
        elements.sendButton.disabled = elements.messageInput.value.trim().length === 0 || state.isLoading;
    }

    function handleSend() {
        const question = elements.messageInput.value.trim();
        if (!question || state.isLoading) return;

        // Add user message
        addMessage('user', question);

        // Clear input
        elements.messageInput.value = '';
        elements.messageInput.style.height = 'auto';
        elements.sendButton.disabled = true;

        // Show typing indicator and send to API
        showTypingIndicator();
        sendMessageToAPI(question);
    }

    // ===================================
    // API COMMUNICATION
    // ===================================
    async function sendMessageToAPI(question) {
        state.pendingQuestion = question;

        try {
            const response = await fetch(`${API_BASE_URL}/chat`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ question: question })
            });

            hideTypingIndicator();

            if (!response.ok) {
                throw new Error(`Server error: ${response.status}`);
            }

            const data = await response.json();
            addMessage('bot', data.answer);
        } catch (error) {
            hideTypingIndicator();
            state.pendingQuestion = null;
            addMessage('bot', null, error.message);
        }
    }

    // ===================================
    // MESSAGE RENDERING
    // ===================================
    function addMessage(role, content, errorMessage = null) {
        const message = {
            role,
            content,
            error: errorMessage,
            timestamp: new Date().toISOString()
        };

        state.messages.push(message);
        saveChatHistory();
        renderMessage(message);
        scrollToBottom();
    }

    function renderMessage(message) {
        // Hide welcome message
        if (elements.welcomeMessage) {
            elements.welcomeMessage.style.display = 'none';
        }

        const messageEl = document.createElement('div');
        messageEl.className = `message ${message.role}`;

        const avatar = document.createElement('div');
        avatar.className = 'message-avatar';
        avatar.textContent = message.role === 'bot' ? 'AI' : 'You';

        const content = document.createElement('div');
        content.className = 'message-content';

        const bubble = document.createElement('div');
        bubble.className = 'message-bubble';

        if (message.error) {
            bubble.classList.add('error');
            bubble.innerHTML = `
                <div class="error-title">Connection Error</div>
                <div>${escapeHtml(message.error)}</div>
                ${state.pendingQuestion ? `<button class="retry-btn" onclick="window.retryLastMessage()">Try Again</button>` : ''}
            `;
        } else if (message.role === 'bot' && typeof marked !== 'undefined') {
            bubble.innerHTML = marked.parse(message.content);
        } else {
            bubble.textContent = message.content;
        }

        const time = document.createElement('span');
        time.className = 'message-time';
        time.textContent = formatTime(message.timestamp);

        content.appendChild(bubble);
        content.appendChild(time);
        messageEl.appendChild(avatar);
        messageEl.appendChild(content);

        elements.messagesContainer.appendChild(messageEl);
    }

    // ===================================
    // TYPING INDICATOR
    // ===================================
    function showTypingIndicator() {
        state.isLoading = true;
        elements.sendButton.disabled = true;

        const indicator = document.createElement('div');
        indicator.className = 'typing-indicator';
        indicator.id = 'typingIndicator';

        indicator.innerHTML = `
            <div class="message-avatar">AI</div>
            <div class="typing-dots">
                <div class="typing-dot"></div>
                <div class="typing-dot"></div>
                <div class="typing-dot"></div>
            </div>
        `;

        elements.messagesContainer.appendChild(indicator);
        scrollToBottom();
    }

    function hideTypingIndicator() {
        state.isLoading = false;
        elements.sendButton.disabled = false;

        const indicator = document.getElementById('typingIndicator');
        if (indicator) {
            indicator.remove();
        }
    }

    // ===================================
    // RETRY FUNCTIONALITY
    // ===================================
    window.retryLastMessage = function() {
        if (state.pendingQuestion) {
            // Remove the error message
            const errorIndex = state.messages.length - 1;
            if (state.messages[errorIndex]?.error) {
                state.messages.splice(errorIndex, 1);
                const lastMessage = elements.messagesContainer.lastElementChild;
                if (lastMessage) lastMessage.remove();
            }

            showTypingIndicator();
            sendMessageToAPI(state.pendingQuestion);
        }
    };

    // ===================================
    // LOCAL STORAGE
    // ===================================
    function saveChatHistory() {
        try {
            localStorage.setItem('s3_chat_history', JSON.stringify(state.messages));
        } catch (e) {
            // Storage full or unavailable - silent fail
        }
    }

    function loadChatHistory() {
        try {
            const saved = localStorage.getItem('s3_chat_history');
            if (saved) {
                const messages = JSON.parse(saved);
                if (Array.isArray(messages) && messages.length > 0) {
                    state.messages = messages;
                    messages.forEach(msg => renderMessage(msg));
                }
            }
        } catch (e) {
            // Invalid data - start fresh
            state.messages = [];
        }
    }

    // ===================================
    // CLEAR CHAT
    // ===================================
    function clearChat() {
        if (state.messages.length === 0) return;

        if (confirm('Clear all chat history?')) {
            state.messages = [];
            state.pendingQuestion = null;
            localStorage.removeItem('s3_chat_history');

            // Remove all messages from DOM
            const messages = elements.messagesContainer.querySelectorAll('.message, .typing-indicator');
            messages.forEach(el => el.remove());

            // Show welcome message
            if (elements.welcomeMessage) {
                elements.welcomeMessage.style.display = '';
            }
        }
    }

    // ===================================
    // SIDEBAR (MOBILE)
    // ===================================
    function toggleSidebar() {
        elements.sidebar.classList.toggle('open');
        elements.sidebarOverlay.classList.toggle('visible');
    }

    function closeSidebar() {
        elements.sidebar.classList.remove('open');
        elements.sidebarOverlay.classList.remove('visible');
    }

    // ===================================
    // UTILITY FUNCTIONS
    // ===================================
    function scrollToBottom() {
        requestAnimationFrame(() => {
            elements.messagesContainer.scrollTop = elements.messagesContainer.scrollHeight;
        });
    }

    function formatTime(isoString) {
        const date = new Date(isoString);
        return date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
    }

    function escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }

    // ===================================
    // START THE APP
    // ===================================
    document.addEventListener('DOMContentLoaded', init);
})();
