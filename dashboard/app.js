// Main application logic

let currentLayout = 'grid';
let currentCategory = 'all';

// Initialize the dashboard
function init() {
    updateDaysRemaining();
    renderQuestions();
    setupEventListeners();
    updateLastUpdateTime();

    // Auto-refresh every 5 minutes
    setInterval(() => {
        refreshAllIframes();
        updateLastUpdateTime();
    }, 5 * 60 * 1000);
}

// Update days remaining counter
function updateDaysRemaining() {
    const days = calculateDaysRemaining();
    document.getElementById('days-remaining').textContent = days;
}

// Render questions based on current filters
function renderQuestions() {
    const grid = document.getElementById('questions-grid');
    grid.innerHTML = '';

    const filteredQuestions = filterQuestions();

    filteredQuestions.forEach(question => {
        const card = createQuestionCard(question);
        grid.appendChild(card);
    });

    // Update visible count
    document.getElementById('visible-questions').textContent = filteredQuestions.length;

    // Apply layout
    applyLayout();
}

// Filter questions based on category
function filterQuestions() {
    if (currentCategory === 'all') {
        return questions;
    }
    return questions.filter(q => q.category === currentCategory);
}

// Create a question card
function createQuestionCard(question) {
    const card = document.createElement('div');
    card.className = 'card';
    card.dataset.questionId = question.id;

    const categoryColors = {
        tech: '#667eea',
        geopolitics: '#f56565',
        economics: '#48bb78',
        entertainment: '#ed8936'
    };

    const categoryColor = categoryColors[question.category] || '#667eea';

    card.innerHTML = `
        <div class="card-body">
            <div class="loading">
                <div class="spinner"></div>
                Loading forecast data...
            </div>
            <iframe
                src="https://www.metaculus.com/questions/embed/${question.questionId}/"
                loading="lazy"
                sandbox="allow-scripts allow-same-origin allow-popups allow-forms"
                onload="this.previousElementSibling.style.display='none'"
            ></iframe>
        </div>
    `;

    return card;
}

// Format date for display
function formatDate(dateString) {
    const date = new Date(dateString);
    const options = { month: 'short', day: 'numeric' };
    return date.toLocaleDateString('en-US', options);
}

// Adjust color brightness
function adjustColor(color, percent) {
    const num = parseInt(color.replace("#", ""), 16);
    const amt = Math.round(2.55 * percent);
    const R = (num >> 16) + amt;
    const G = (num >> 8 & 0x00FF) + amt;
    const B = (num & 0x0000FF) + amt;
    return "#" + (0x1000000 + (R < 255 ? R < 1 ? 0 : R : 255) * 0x10000 +
        (G < 255 ? G < 1 ? 0 : G : 255) * 0x100 +
        (B < 255 ? B < 1 ? 0 : B : 255))
        .toString(16).slice(1);
}

// Apply layout style
function applyLayout() {
    const grid = document.getElementById('questions-grid');
    if (currentLayout === 'single') {
        grid.style.gridTemplateColumns = '1fr';
    } else {
        grid.style.gridTemplateColumns = 'repeat(auto-fit, minmax(500px, 1fr))';
    }
}

// Setup event listeners
function setupEventListeners() {
    // Layout selector
    document.getElementById('layout').addEventListener('change', (e) => {
        currentLayout = e.target.value;
        applyLayout();
    });

    // Category filter
    document.getElementById('category').addEventListener('change', (e) => {
        currentCategory = e.target.value;
        renderQuestions();
    });

    // Refresh button
    document.getElementById('refresh-all').addEventListener('click', () => {
        refreshAllIframes();
        showRefreshNotification();
    });

    // Fullscreen toggle
    document.getElementById('fullscreen').addEventListener('click', toggleFullscreen);
}

// Refresh all iframes
function refreshAllIframes() {
    const iframes = document.querySelectorAll('iframe');
    iframes.forEach(iframe => {
        const src = iframe.src;
        iframe.src = '';
        setTimeout(() => {
            iframe.src = src;
        }, 100);
    });
}

// Show refresh notification
function showRefreshNotification() {
    const button = document.getElementById('refresh-all');
    const originalText = button.textContent;
    button.textContent = '✓ Refreshed!';
    button.style.background = '#48bb78';

    setTimeout(() => {
        button.textContent = originalText;
        button.style.background = '';
    }, 2000);
}

// Toggle fullscreen
function toggleFullscreen() {
    if (!document.fullscreenElement) {
        document.documentElement.requestFullscreen().catch(err => {
            console.log('Fullscreen error:', err);
        });
    } else {
        if (document.exitFullscreen) {
            document.exitFullscreen();
        }
    }
}

// Update last update time
function updateLastUpdateTime() {
    const now = new Date();
    const timeString = now.toLocaleString('en-US', {
        month: 'short',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit',
        second: '2-digit'
    });
    document.getElementById('last-update-time').textContent = timeString;
}

// Keyboard shortcuts
document.addEventListener('keydown', (e) => {
    // R key to refresh
    if (e.key === 'r' && !e.ctrlKey && !e.metaKey) {
        refreshAllIframes();
        showRefreshNotification();
    }

    // F key for fullscreen
    if (e.key === 'f' && !e.ctrlKey && !e.metaKey) {
        toggleFullscreen();
    }

    // Number keys to filter categories
    if (e.key === '1') {
        document.getElementById('category').value = 'all';
        currentCategory = 'all';
        renderQuestions();
    }
    if (e.key === '2') {
        document.getElementById('category').value = 'tech';
        currentCategory = 'tech';
        renderQuestions();
    }
    if (e.key === '3') {
        document.getElementById('category').value = 'geopolitics';
        currentCategory = 'geopolitics';
        renderQuestions();
    }
    if (e.key === '4') {
        document.getElementById('category').value = 'economics';
        currentCategory = 'economics';
        renderQuestions();
    }
    if (e.key === '5') {
        document.getElementById('category').value = 'entertainment';
        currentCategory = 'entertainment';
        renderQuestions();
    }
});

// Initialize when DOM is ready
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
} else {
    init();
}
