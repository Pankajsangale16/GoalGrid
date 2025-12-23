document.addEventListener('DOMContentLoaded', function() {
    // Initialize all circular progress bars
    initializeProgressBars();
    
    // Mobile optimizations
    setupMobileOptimizations();
});

function setupMobileOptimizations() {
    // Prevent double-tap zoom on buttons
    const buttons = document.querySelectorAll('button, .btn-new-client, .btn-submit, .btn-cancel, .btn-add-task-small, .btn-delete-client, .btn-delete-task');
    buttons.forEach(button => {
        let lastTap = 0;
        button.addEventListener('touchend', function(e) {
            const currentTime = new Date().getTime();
            const tapLength = currentTime - lastTap;
            if (tapLength < 300 && tapLength > 0) {
                e.preventDefault();
            }
            lastTap = currentTime;
        });
    });
    
    // Improve input focus on mobile
    const inputs = document.querySelectorAll('input[type="text"], input[type="range"]');
    inputs.forEach(input => {
        input.addEventListener('focus', function() {
            // Scroll input into view on mobile
            setTimeout(() => {
                input.scrollIntoView({ behavior: 'smooth', block: 'center' });
            }, 300);
        });
    });
    
    // Prevent zoom on input focus (iOS)
    const textInputs = document.querySelectorAll('input[type="text"]');
    textInputs.forEach(input => {
        if (input.style.fontSize !== '16px') {
            input.style.fontSize = '16px';
        }
    });
    
    // Improve touch scrolling
    const scrollableElements = document.querySelectorAll('.tasks-list');
    scrollableElements.forEach(element => {
        element.style.webkitOverflowScrolling = 'touch';
    });
    
    // Search input focus handling
    const searchInput = document.getElementById('client-search-input');
    if (searchInput) {
        searchInput.addEventListener('focus', function() {
            // Scroll search into view on mobile
            setTimeout(() => {
                this.scrollIntoView({ behavior: 'smooth', block: 'center' });
            }, 300);
        });
    }
}

function initializeProgressBars() {
    const progressBars = document.querySelectorAll('.circular-progress-global, .circular-progress-client');
    
    progressBars.forEach(function(progressBar) {
        const percentage = parseFloat(progressBar.getAttribute('data-percentage')) || 0;
        const color = progressBar.getAttribute('data-color') || 'neon-green';
        const circle = progressBar.querySelector('.progress-ring-circle');
        
        if (circle) {
            const radius = circle.r.baseVal.value;
            const circumference = radius * 2 * Math.PI;
            
            // Set stroke color based on data-color attribute
            if (color === 'neon-green') {
                circle.style.stroke = '#00ff88';
            } else if (color === 'vivid-orange') {
                circle.style.stroke = '#ff6b35';
            }
            
            // Set stroke-dasharray and stroke-dashoffset
            circle.style.strokeDasharray = `${circumference} ${circumference}`;
            circle.style.strokeDashoffset = circumference;
            
            // Calculate offset based on percentage
            const offset = circumference - (percentage / 100) * circumference;
            
            // Animate the progress bar
            setTimeout(function() {
                circle.style.strokeDashoffset = offset;
            }, 100);
        }
    });
}

// Function to update progress bar (used by AJAX)
function updateProgressBar(selector, percentage) {
    const progressBar = document.querySelector(selector);
    if (!progressBar) return;
    
    const circle = progressBar.querySelector('.progress-ring-circle');
    if (!circle) return;
    
    const radius = circle.r.baseVal.value;
    const circumference = radius * 2 * Math.PI;
    const offset = circumference - (percentage / 100) * circumference;
    
    // Smoothly animate to new value
    circle.style.transition = 'stroke-dashoffset 0.8s cubic-bezier(0.4, 0, 0.2, 1)';
    circle.style.strokeDashoffset = offset;
}

// Function to animate number counting
function animateValue(id, start, end, duration = 500) {
    const element = document.getElementById(id);
    if (!element) return;
    
    const startTime = performance.now();
    
    function update(currentTime) {
        const elapsed = currentTime - startTime;
        const progress = Math.min(elapsed / duration, 1);
        // Easing function for smooth animation
        const easeOutCubic = 1 - Math.pow(1 - progress, 3);
        const current = Math.round(start + (end - start) * easeOutCubic);
        element.textContent = current;
        
        if (progress < 1) {
            requestAnimationFrame(update);
        } else {
            element.textContent = end; // Ensure final value is exact
        }
    }
    
    requestAnimationFrame(update);
}
