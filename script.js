// ===== Application State =====
const state = {
    apiUrl: '',
    apiKey: '',
    sessionId: null,
    conversationHistory: [],
    messageCount: 0,
    responseTimes: [],
    intelligence: {
        upiIds: new Set(),
        phoneNumbers: new Set(),
        accountNumbers: new Set(),
        phishingLinks: new Set(),
        ifscCodes: new Set()
    }
};

// ===== Helper Functions =====
function generateSessionId() {
    return `test-session-${Math.random().toString(36).substring(2, 10)}`;
}

function formatTime(date) {
    return date.toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit' });
}

function updateStats() {
    document.getElementById('messageCount').textContent = state.messageCount;
    
    if (state.responseTimes.length > 0) {
        const avg = state.responseTimes.reduce((a, b) => a + b, 0) / state.responseTimes.length;
        document.getElementById('avgResponse').textContent = `${avg.toFixed(0)}ms`;
    }
}

function updateIntelligence() {
    document.getElementById('upiCount').textContent = state.intelligence.upiIds.size;
    document.getElementById('phoneCount').textContent = state.intelligence.phoneNumbers.size;
    document.getElementById('accountCount').textContent = state.intelligence.accountNumbers.size;
    document.getElementById('linkCount').textContent = state.intelligence.phishingLinks.size;
    document.getElementById('ifscCount').textContent = state.intelligence.ifscCodes.size;
    
    // Update details
    const details = document.getElementById('intelligenceDetails');
    let html = '';
    
    if (state.intelligence.upiIds.size > 0) {
        html += `<div><strong>UPI IDs:</strong> ${Array.from(state.intelligence.upiIds).join(', ')}</div>`;
    }
    if (state.intelligence.phoneNumbers.size > 0) {
        html += `<div><strong>Phone Numbers:</strong> ${Array.from(state.intelligence.phoneNumbers).join(', ')}</div>`;
    }
    if (state.intelligence.accountNumbers.size > 0) {
        html += `<div><strong>Account Numbers:</strong> ${Array.from(state.intelligence.accountNumbers).join(', ')}</div>`;
    }
    if (state.intelligence.phishingLinks.size > 0) {
        html += `<div><strong>Phishing Links:</strong> ${Array.from(state.intelligence.phishingLinks).join(', ')}</div>`;
    }
    if (state.intelligence.ifscCodes.size > 0) {
        html += `<div><strong>IFSC Codes:</strong> ${Array.from(state.intelligence.ifscCodes).join(', ')}</div>`;
    }
    
    details.innerHTML = html;
}

function extractIntelligence(text) {
    // UPI IDs (pattern: username@provider)
    const upiPattern = /[\w.-]+@[\w.-]+/g;
    const upis = text.match(upiPattern);
    if (upis) upis.forEach(upi => state.intelligence.upiIds.add(upi));
    
    // Phone numbers (10 digits)
    const phonePattern = /\b\d{10}\b/g;
    const phones = text.match(phonePattern);
    if (phones) phones.forEach(phone => state.intelligence.phoneNumbers.add(phone));
    
    // Account numbers (10-16 digits)
    const accountPattern = /\b\d{10,16}\b/g;
    const accounts = text.match(accountPattern);
    if (accounts) accounts.forEach(acc => state.intelligence.accountNumbers.add(acc));
    
    // IFSC codes
    const ifscPattern = /[A-Z]{4}0[A-Z0-9]{6}/g;
    const ifscs = text.match(ifscPattern);
    if (ifscs) ifscs.forEach(ifsc => state.intelligence.ifscCodes.add(ifsc));
    
    // URLs/Links
    const urlPattern = /https?:\/\/[^\s]+/g;
    const urls = text.match(urlPattern);
    if (urls) urls.forEach(url => state.intelligence.phishingLinks.add(url));
    
    updateIntelligence();
}

// ===== Message Display Functions =====
function clearEmptyState() {
    const emptyState = document.querySelector('.empty-state');
    if (emptyState) {
        emptyState.remove();
    }
}

function addMessage(sender, text, metadata = {}) {
    clearEmptyState();
    
    const messagesContainer = document.getElementById('chatMessages');
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${sender}`;
    
    const avatar = sender === 'scammer' ? '🎭' : '🤖';
    const senderLabel = sender === 'scammer' ? 'Test Message' : 'Agent';
    const time = formatTime(new Date());
    
    let metaInfo = '';
    if (metadata.responseTime) {
        metaInfo = `<div class="message-meta">Response time: ${metadata.responseTime}ms</div>`;
    }
    
    messageDiv.innerHTML = `
        <div class="message-avatar">${avatar}</div>
        <div class="message-content">
            <div class="message-header">
                <span class="message-sender">${senderLabel}</span>
                <span class="message-time">${time}</span>
            </div>
            <div class="message-bubble">${text}</div>
            ${metaInfo}
        </div>
    `;
    
    messagesContainer.appendChild(messageDiv);
    messagesContainer.scrollTop = messagesContainer.scrollHeight;
    
    // Extract intelligence from message
    extractIntelligence(text);
}

function showLoading(show) {
    const loader = document.getElementById('loadingIndicator');
    const sendBtn = document.getElementById('sendMessage');
    
    if (show) {
        loader.classList.add('active');
        sendBtn.disabled = true;
    } else {
        loader.classList.remove('active');
        sendBtn.disabled = false;
    }
}

// ===== API Functions =====
async function testConnection() {
    const url = document.getElementById('apiUrl').value;
    const key = document.getElementById('apiKey').value;
    
    if (!url || !key) {
        alert('Please enter both API URL and API Key');
        return;
    }
    
    state.apiUrl = url;
    state.apiKey = key;
    
    const btn = document.getElementById('testConnection');
    const originalText = btn.innerHTML;
    btn.innerHTML = '<span class="btn-icon">⏳</span>Testing...';
    btn.disabled = true;
    
    try {
        const testMessage = "Hello, testing connection";
        const response = await sendToAgent(testMessage);
        
        if (response) {
            // Connection successful
            const statusBadge = document.getElementById('connectionStatus');
            statusBadge.classList.add('connected');
            statusBadge.querySelector('.status-text').textContent = 'Connected';
            
            alert('✅ Connection successful!');
        } else {
            throw new Error('No response received');
        }
    } catch (error) {
        alert('❌ Connection failed: ' + error.message);
    } finally {
        btn.innerHTML = originalText;
        btn.disabled = false;
    }
}

async function sendToAgent(message) {
    if (!state.sessionId) {
        state.sessionId = generateSessionId();
        document.getElementById('sessionId').textContent = `Session: ${state.sessionId}`;
    }
    
    const payload = {
        sessionId: state.sessionId,
        message: {
            sender: 'scammer',
            text: message,
            timestamp: Date.now()
        },
        conversationHistory: state.conversationHistory
    };
    
    const startTime = Date.now();
    
    try {
        const response = await fetch(state.apiUrl, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'x-api-key': state.apiKey
            },
            body: JSON.stringify(payload)
        });
        
        const responseTime = Date.now() - startTime;
        state.responseTimes.push(responseTime);
        
        if (!response.ok) {
            throw new Error(`HTTP ${response.status}: ${response.statusText}`);
        }
        
        const data = await response.json();
        
        if (data.status === 'success' && data.reply) {
            // Update conversation history
            state.conversationHistory.push(
                { sender: 'scammer', text: message, timestamp: Date.now() },
                { sender: 'user', text: data.reply, timestamp: Date.now() }
            );
            
            return { reply: data.reply, responseTime };
        } else {
            throw new Error('Invalid response format');
        }
    } catch (error) {
        console.error('API Error:', error);
        throw error;
    }
}

async function sendMessage(message) {
    if (!message.trim()) return;
    
    if (!state.apiUrl || !state.apiKey) {
        alert('Please configure API settings and test connection first');
        return;
    }
    
    // Add user message
    addMessage('scammer', message);
    state.messageCount++;
    updateStats();
    
    // Show loading
    showLoading(true);
    
    try {
        const response = await sendToAgent(message);
        
        // Add agent response
        addMessage('agent', response.reply, { responseTime: response.responseTime });
        state.messageCount++;
        updateStats();
    } catch (error) {
        addMessage('agent', `❌ Error: ${error.message}`, {});
    } finally {
        showLoading(false);
    }
}

// ===== Event Handlers =====
function initializeEventListeners() {
    // Test connection button
    document.getElementById('testConnection').addEventListener('click', testConnection);
    
    // Send message button
    document.getElementById('sendMessage').addEventListener('click', () => {
        const input = document.getElementById('messageInput');
        sendMessage(input.value);
        input.value = '';
        input.style.height = 'auto';
    });
    
    // Enter key to send
    document.getElementById('messageInput').addEventListener('keydown', (e) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            const input = e.target;
            sendMessage(input.value);
            input.value = '';
            input.style.height = 'auto';
        }
    });
    
    // Auto-resize textarea
    document.getElementById('messageInput').addEventListener('input', (e) => {
        e.target.style.height = 'auto';
        e.target.style.height = e.target.scrollHeight + 'px';
    });
    
    // Scenario buttons
    document.querySelectorAll('.scenario-btn').forEach(btn => {
        btn.addEventListener('click', () => {
            const message = btn.getAttribute('data-message');
            sendMessage(message);
        });
    });
    
    // New session button
    document.getElementById('newSession').addEventListener('click', () => {
        if (confirm('Start a new session? This will reset the conversation but keep intelligence data.')) {
            state.sessionId = null;
            state.conversationHistory = [];
            state.messageCount = 0;
            state.responseTimes = [];
            
            document.getElementById('sessionId').textContent = 'Session: Not Started';
            document.getElementById('chatMessages').innerHTML = `
                <div class="empty-state">
                    <div class="empty-icon">🤖</div>
                    <h3>Ready to Test!</h3>
                    <p>Select a test scenario from the left or type your own message below</p>
                </div>
            `;
            
            updateStats();
        }
    });
    
    // Clear chat button
    document.getElementById('clearChat').addEventListener('click', () => {
        if (confirm('Clear all data including intelligence? This cannot be undone.')) {
            state.sessionId = null;
            state.conversationHistory = [];
            state.messageCount = 0;
            state.responseTimes = [];
            state.intelligence = {
                upiIds: new Set(),
                phoneNumbers: new Set(),
                accountNumbers: new Set(),
                phishingLinks: new Set(),
                ifscCodes: new Set()
            };
            
            document.getElementById('sessionId').textContent = 'Session: Not Started';
            document.getElementById('chatMessages').innerHTML = `
                <div class="empty-state">
                    <div class="empty-icon">🤖</div>
                    <h3>Ready to Test!</h3>
                    <p>Select a test scenario from the left or type your own message below</p>
                </div>
            `;
            
            updateStats();
            updateIntelligence();
        }
    });
}

// ===== Initialize App =====
document.addEventListener('DOMContentLoaded', () => {
    initializeEventListeners();
    
    // Load saved config if exists
    state.apiUrl = document.getElementById('apiUrl').value;
    state.apiKey = document.getElementById('apiKey').value;
    
    console.log('🚀 Honeypot Agent Tester initialized!');
});
