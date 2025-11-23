// Main JavaScript functionality for StudyEco

// Update subject selection
function updateSubject() {
    const subject = document.getElementById('subjectSelect').value;
    
    fetch('/update_subject', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: `subject=${encodeURIComponent(subject)}`
    })
    .then(response => {
        if (response.ok) {
            // Update UI to reflect new subject
            console.log('Subject updated to:', subject);
        }
    })
    .catch(error => {
        console.error('Error updating subject:', error);
    });
}

// Notification handling
document.addEventListener('DOMContentLoaded', function() {
    // Initialize notification dropdown
    const notificationItem = document.querySelector('.notifications');
    if (notificationItem) {
        notificationItem.addEventListener('click', function(e) {
            e.stopPropagation();
        });
    }
    
    // Close notification dropdown when clicking outside
    document.addEventListener('click', function() {
        const dropdown = document.querySelector('.notification-dropdown');
        if (dropdown) {
            dropdown.style.opacity = '0';
            dropdown.style.visibility = 'hidden';
        }
    });
});

// Sidebar functionality
function toggleSidebar() {
    const sidebar = document.querySelector('.sidebar');
    sidebar.classList.toggle('open');
}

// Mobile responsiveness
function handleResize() {
    const sidebar = document.querySelector('.sidebar');
    const mainContent = document.querySelector('.main-content');
    
    if (window.innerWidth <= 768) {
        sidebar.classList.add('mobile');
        mainContent.classList.add('mobile');
    } else {
        sidebar.classList.remove('mobile');
        mainContent.classList.remove('mobile');
    }
}

// Initialize on page load
window.addEventListener('load', function() {
    handleResize();
});

// Handle window resize
window.addEventListener('resize', handleResize);

// Utility functions
function showNotification(message, type = 'info') {
    // Create notification element
    const notification = document.createElement('div');
    notification.className = `notification notification-${type}`;
    notification.innerHTML = `
        <i class="fas fa-${type === 'success' ? 'check-circle' : type === 'error' ? 'exclamation-circle' : 'info-circle'}"></i>
        <span>${message}</span>
    `;
    
    // Add to page
    document.body.appendChild(notification);
    
    // Show notification
    setTimeout(() => {
        notification.classList.add('show');
    }, 100);
    
    // Remove notification after 3 seconds
    setTimeout(() => {
        notification.classList.remove('show');
        setTimeout(() => {
            document.body.removeChild(notification);
        }, 300);
    }, 3000);
}

// Form validation
function validateForm(formId) {
    const form = document.getElementById(formId);
    if (!form) return false;
    
    const requiredFields = form.querySelectorAll('[required]');
    let isValid = true;
    
    requiredFields.forEach(field => {
        if (!field.value.trim()) {
            field.classList.add('error');
            isValid = false;
        } else {
            field.classList.remove('error');
        }
    });
    
    return isValid;
}

// Loading states
function showLoading(elementId) {
    const element = document.getElementById(elementId);
    if (element) {
        element.innerHTML = '<div class="loading"><i class="fas fa-spinner fa-spin"></i> Loading...</div>';
    }
}

function hideLoading(elementId, content) {
    const element = document.getElementById(elementId);
    if (element) {
        element.innerHTML = content;
    }
}

// Audio player functionality
class AudioPlayer {
    constructor() {
        this.audio = null;
        this.currentTrack = null;
        this.isPlaying = false;
    }
    
    loadTrack(src) {
        if (this.audio) {
            this.audio.pause();
        }
        
        this.audio = new Audio(src);
        this.currentTrack = src;
        this.isPlaying = false;
    }
    
    play() {
        if (this.audio) {
            this.audio.play();
            this.isPlaying = true;
        }
    }
    
    pause() {
        if (this.audio) {
            this.audio.pause();
            this.isPlaying = false;
        }
    }
    
    setVolume(volume) {
        if (this.audio) {
            this.audio.volume = volume / 100;
        }
    }
}

// Initialize global audio player
window.audioPlayer = new AudioPlayer();

// Search functionality
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

// Create debounced search functions
const debouncedBookSearch = debounce(searchBooks, 500);
const debouncedResearchSearch = debounce(searchResearch, 500);

// Keyboard shortcuts
document.addEventListener('keydown', function(e) {
    // Ctrl/Cmd + K for search
    if ((e.ctrlKey || e.metaKey) && e.key === 'k') {
        e.preventDefault();
        const searchInput = document.querySelector('input[type="text"]');
        if (searchInput) {
            searchInput.focus();
        }
    }
    
    // Escape to close modals/dropdowns
    if (e.key === 'Escape') {
        const dropdowns = document.querySelectorAll('.notification-dropdown');
        dropdowns.forEach(dropdown => {
            dropdown.style.opacity = '0';
            dropdown.style.visibility = 'hidden';
        });
    }
});

// Progress tracking
function updateStudyProgress(minutes) {
    const progressBar = document.querySelector('.progress-fill');
    const progressText = document.querySelector('.goal-progress p');
    
    if (progressBar && progressText) {
        const currentMinutes = parseInt(progressText.textContent.split(' ')[0]);
        const totalMinutes = parseInt(progressText.textContent.split(' ')[2]);
        const newMinutes = currentMinutes + minutes;
        
        const percentage = Math.min((newMinutes / totalMinutes) * 100, 100);
        progressBar.style.width = percentage + '%';
        
        progressText.textContent = `${newMinutes} / ${totalMinutes} minutes completed`;
        
        if (newMinutes >= totalMinutes) {
            showNotification('Congratulations! You\'ve completed your daily study goal!', 'success');
        }
    }
}

// Theme management
function toggleTheme() {
    const body = document.body;
    body.classList.toggle('light-theme');
    
    const theme = body.classList.contains('light-theme') ? 'light' : 'dark';
    localStorage.setItem('theme', theme);
}

// Load saved theme
document.addEventListener('DOMContentLoaded', function() {
    const savedTheme = localStorage.getItem('theme');
    if (savedTheme === 'light') {
        document.body.classList.add('light-theme');
    }
});

// Export functions for global use
window.updateSubject = updateSubject;
window.toggleSidebar = toggleSidebar;
window.showNotification = showNotification;
window.validateForm = validateForm;
window.showLoading = showLoading;
window.hideLoading = hideLoading;
window.updateStudyProgress = updateStudyProgress;
window.toggleTheme = toggleTheme;
