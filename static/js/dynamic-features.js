/**
 * Dynamic Features & Theme Management
 * Hostel Management System
 */

// Initialize all dynamic features
document.addEventListener('DOMContentLoaded', function() {
    initializeAnimations();
    initializeInteractiveElements();
    initializeScrollEffects();
    initializeCardAnimations();
    initializeButtonEffects();
});

/**
 * Card Animation Effects
 */
function initializeCardAnimations() {
    const cards = document.querySelectorAll('.card');
    
    cards.forEach((card, index) => {
        // Stagger animation
        card.style.animationDelay = `${index * 0.1}s`;
        
        // Add ripple effect on hover
        card.addEventListener('mouseenter', function() {
            const ripple = document.createElement('span');
            ripple.classList.add('ripple');
            this.appendChild(ripple);
            
            setTimeout(() => ripple.remove(), 600);
        });
        
        // Interactive glow effect
        card.addEventListener('mousemove', function(e) {
            const rect = this.getBoundingClientRect();
            const x = e.clientX - rect.left;
            const y = e.clientY - rect.top;
            
            const bgGradient = `radial-gradient(circle at ${x}px ${y}px, rgba(52, 152, 219, 0.1), transparent)`;
            this.style.backgroundImage = bgGradient;
        });
        
        card.addEventListener('mouseleave', function() {
            this.style.backgroundImage = 'none';
        });
    });
}

/**
 * Button Effects
 */
function initializeButtonEffects() {
    const buttons = document.querySelectorAll('button, .btn');
    
    buttons.forEach(button => {
        button.addEventListener('click', function(e) {
            // Ripple effect
            const ripple = document.createElement('span');
            ripple.classList.add('button-ripple');
            
            const rect = this.getBoundingClientRect();
            const x = e.clientX - rect.left;
            const y = e.clientY - rect.top;
            
            ripple.style.left = x + 'px';
            ripple.style.top = y + 'px';
            
            this.appendChild(ripple);
            
            setTimeout(() => ripple.remove(), 600);
        });
    });
}

/**
 * Scroll Effects
 */
function initializeScrollEffects() {
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -100px 0px'
    };
    
    const observer = new IntersectionObserver(function(entries) {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('animate-in');
                observer.unobserve(entry.target);
            }
        });
    }, observerOptions);
    
    // Observe all cards and sections
    document.querySelectorAll('.card, .stat-card, .alert').forEach(el => {
        observer.observe(el);
    });
}

/**
 * Navbar Effects on Scroll
 */
function initializeScrollNavbarEffect() {
    const navbar = document.querySelector('.navbar');
    let lastScrollTop = 0;
    
    window.addEventListener('scroll', function() {
        const scrollTop = window.pageYOffset || document.documentElement.scrollTop;
        
        if (scrollTop > 100) {
            navbar.style.boxShadow = '0 4px 20px rgba(0, 0, 0, 0.3)';
        } else {
            navbar.style.boxShadow = '0 2px 12px rgba(0, 0, 0, 0.2)';
        }
        
        lastScrollTop = scrollTop;
    });
}

/**
 * Table Row Animations
 */
function initializeTableRowAnimations() {
    const tables = document.querySelectorAll('.table');
    
    tables.forEach(table => {
        const rows = table.querySelectorAll('tbody tr');
        
        rows.forEach((row, index) => {
            row.style.animationDelay = `${index * 0.05}s`;
            
            row.addEventListener('mouseenter', function() {
                this.style.backgroundColor = 'rgba(52, 152, 219, 0.1)';
                this.style.boxShadow = '0 2px 8px rgba(52, 152, 219, 0.2)';
            });
            
            row.addEventListener('mouseleave', function() {
                this.style.backgroundColor = '';
                this.style.boxShadow = '';
            });
        });
    });
}

/**
 * Interactive Elements
 */
function initializeInteractiveElements() {
    // Dropdown animations
    const dropdowns = document.querySelectorAll('.dropdown-toggle');
    
    dropdowns.forEach(dropdown => {
        dropdown.addEventListener('click', function() {
            this.style.transform = 'rotate(180deg)';
        });
    });
    
    // Form focus effects
    const formControls = document.querySelectorAll('.form-control, .form-select');
    
    formControls.forEach(control => {
        control.addEventListener('focus', function() {
            this.style.borderColor = '#3498db';
            this.style.boxShadow = '0 0 0 0.2rem rgba(52, 152, 219, 0.25)';
        });
        
        control.addEventListener('blur', function() {
            this.style.borderColor = '';
            this.style.boxShadow = '';
        });
    });
    
    // Alert close animations
    const alertCloseButtons = document.querySelectorAll('.alert .btn-close');
    
    alertCloseButtons.forEach(btn => {
        btn.addEventListener('click', function(e) {
            const alert = this.closest('.alert');
            if (alert) {
                alert.style.animation = 'slideUp 0.3s ease forwards';
                setTimeout(() => alert.remove(), 300);
            }
        });
    });
}

/**
 * General Animations
 */
function initializeAnimations() {
    // Add CSS for animations
    const style = document.createElement('style');
    style.textContent = `
        @keyframes slideUp {
            to {
                opacity: 0;
                transform: translateY(-20px);
            }
        }
        
        @keyframes fadeInUp {
            from {
                opacity: 0;
                transform: translateY(30px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }
        
        @keyframes ripple {
            to {
                transform: scale(4);
                opacity: 0;
            }
        }
        
        @keyframes buttonRipple {
            to {
                transform: scale(4);
                opacity: 0;
            }
        }
        
        .ripple {
            position: absolute;
            border-radius: 50%;
            background: rgba(52, 152, 219, 0.6);
            transform: scale(0);
            animation: ripple 0.6s ease-out;
            pointer-events: none;
        }
        
        .button-ripple {
            position: absolute;
            border-radius: 50%;
            background: rgba(255, 255, 255, 0.6);
            width: 20px;
            height: 20px;
            transform: scale(0);
            animation: buttonRipple 0.6s ease-out;
            pointer-events: none;
        }
        
        .animate-in {
            animation: fadeInUp 0.5s ease forwards !important;
        }
    `;
    document.head.appendChild(style);
    
    // Initialize scroll navbar effect
    initializeScrollNavbarEffect();
    
    // Initialize table row animations
    initializeTableRowAnimations();
    
    // Animate stat cards
    const statCards = document.querySelectorAll('.stat-card');
    statCards.forEach((card, index) => {
        card.style.animationDelay = `${index * 0.15}s`;
    });
}

/**
 * Count Animation for Stat Cards
 */
function animateCountUp(element, target, duration = 2000) {
    const start = 0;
    const increment = target / (duration / 16);
    let current = start;
    
    const timer = setInterval(() => {
        current += increment;
        if (current >= target) {
            element.textContent = target;
            clearInterval(timer);
        } else {
            element.textContent = Math.floor(current);
        }
    }, 16);
}

/**
 * Initialize count-up animation for stat cards
 */
function initializeStatCardCountUp() {
    const statCards = document.querySelectorAll('.stat-card h3');
    
    const observer = new IntersectionObserver(entries => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const value = parseInt(entry.target.textContent);
                if (!isNaN(value)) {
                    entry.target.textContent = '0';
                    animateCountUp(entry.target, value);
                }
                observer.unobserve(entry.target);
            }
        });
    }, { threshold: 0.5 });
    
    statCards.forEach(card => observer.observe(card));
}

// Initialize count-up when DOM is ready
document.addEventListener('DOMContentLoaded', initializeStatCardCountUp);

/**
 * Parallax Effect for Hero Section
 */
function initializeParallaxEffect() {
    const heroSection = document.querySelector('.hero-section');
    
    if (heroSection) {
        window.addEventListener('scroll', function() {
            const scrollPosition = window.pageYOffset;
            heroSection.style.backgroundPosition = `center ${scrollPosition * 0.5}px`;
        });
    }
}

document.addEventListener('DOMContentLoaded', initializeParallaxEffect);

/**
 * Tooltip Initialization (Bootstrap tooltips)
 */
function initializeTooltips() {
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
}

document.addEventListener('DOMContentLoaded', initializeTooltips);

/**
 * Add animations to newly added elements (for dynamically loaded content)
 */
function observeNewElements(selector = '.card') {
    const observer = new MutationObserver(function(mutations) {
        mutations.forEach(function(mutation) {
            if (mutation.addedNodes.length) {
                mutation.addedNodes.forEach(function(node) {
                    if (node.nodeType === 1) { // Element node
                        const elements = node.querySelectorAll(selector);
                        if (node.matches(selector)) {
                            initializeCardAnimations();
                        }
                        elements.forEach(el => {
                            el.style.animationDelay = '0s';
                        });
                    }
                });
            }
        });
    });
    
    observer.observe(document.body, {
        childList: true,
        subtree: true
    });
}

document.addEventListener('DOMContentLoaded', observeNewElements);

/**
 * Export functions for use in other scripts
 */
window.HostelDynamicFeatures = {
    initializeCardAnimations,
    initializeButtonEffects,
    initializeScrollEffects,
    animateCountUp,
    initializeParallaxEffect,
    initializeTooltips
};
