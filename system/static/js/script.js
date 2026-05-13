/**
 * EmotionAI - Client-Side JavaScript
 * Handles navigation, file upload, and interactive elements
 */

document.addEventListener('DOMContentLoaded', function() {
    // Initialize navigation
    initializeNavigation();
    
    // Initialize upload functionality if on service page
    const uploadArea = document.getElementById('uploadArea');
    const imageInput = document.getElementById('imageInput');
    
    if (imageInput && uploadArea) {
        initializeUpload();
    }
    
    // Auto-dismiss flash messages
    initializeFlashMessages();
});

/**
 * Initialize navigation interactions
 */
function initializeNavigation() {
    const mobileMenuBtn = document.getElementById('mobileMenuBtn');
    const navMenu = document.getElementById('navMenu');
    
    if (mobileMenuBtn && navMenu) {
        mobileMenuBtn.addEventListener('click', function() {
            navMenu.classList.toggle('active');
        });
    }
    
    // Close mobile menu when clicking outside
    document.addEventListener('click', function(e) {
        if (navMenu && !e.target.closest('.nav-container')) {
            navMenu.classList.remove('active');
        }
    });
}

/**
 * Initialize flash message auto-dismiss
 */
function initializeFlashMessages() {
    const flashMessages = document.querySelectorAll('.flash-message');
    
    flashMessages.forEach(function(message) {
        setTimeout(function() {
            message.style.animation = 'slideOutRight 0.3s ease';
            setTimeout(function() {
                message.remove();
            }, 300);
        }, 5000);
    });
}

// Add slideOutRight animation
const style = document.createElement('style');
style.textContent = `
    @keyframes slideOutRight {
        from {
            transform: translateX(0);
            opacity: 1;
        }
        to {
            transform: translateX(100%);
            opacity: 0;
        }
    }
`;
document.head.appendChild(style);

/**
 * Initialize file upload functionality
 */
function initializeUpload() {
    const uploadArea = document.getElementById('uploadArea');
    const imageInput = document.getElementById('imageInput');
    const uploadForm = document.getElementById('uploadForm');

    // File input change event
    imageInput.addEventListener('change', function(e) {
        handleFileSelect(e.target.files);
    });

    // Drag and drop events
    uploadArea.addEventListener('dragover', function(e) {
        e.preventDefault();
        e.stopPropagation();
        uploadArea.classList.add('drag-over');
    });

    uploadArea.addEventListener('dragleave', function(e) {
        e.preventDefault();
        e.stopPropagation();
        uploadArea.classList.remove('drag-over');
    });

    uploadArea.addEventListener('drop', function(e) {
        e.preventDefault();
        e.stopPropagation();
        uploadArea.classList.remove('drag-over');
        
        const files = e.dataTransfer.files;
        if (files.length > 0) {
            imageInput.files = files;
            handleFileSelect(files);
        }
    });

    // Form submission
    uploadForm.addEventListener('submit', function(e) {
        const submitBtn = document.getElementById('submitBtn');
        const btnText = submitBtn.querySelector('.btn-text');
        const btnLoader = submitBtn.querySelector('.btn-loader');

        // Show loading state
        btnText.style.display = 'none';
        btnLoader.style.display = 'inline';
        submitBtn.disabled = true;
    });
}

/**
 * Handle file selection
 * @param {FileList} files - Selected files
 */
function handleFileSelect(files) {
    if (files.length === 0) {
        return;
    }

    const file = files[0];
    const uploadArea = document.getElementById('uploadArea');
    const previewContainer = document.getElementById('preview');
    const previewImage = document.getElementById('previewImage');

    // Validate file type
    const validTypes = ['image/jpeg', 'image/jpg', 'image/png'];
    if (!validTypes.includes(file.type)) {
        alert('Invalid file type. Please select a JPEG or PNG image.');
        return;
    }

    // Validate file size (10MB)
    const maxSize = 10 * 1024 * 1024;
    if (file.size > maxSize) {
        alert('File size too large. Maximum size is 10MB.');
        return;
    }

    // Read and display preview
    const reader = new FileReader();
    reader.onload = function(e) {
        previewImage.src = e.target.result;
        uploadArea.style.display = 'none';
        previewContainer.style.display = 'block';
    };
    reader.readAsDataURL(file);
}

/**
 * Remove selected image
 */
function removeImage() {
    const uploadArea = document.getElementById('uploadArea');
    const previewContainer = document.getElementById('preview');
    const imageInput = document.getElementById('imageInput');

    imageInput.value = '';
    uploadArea.style.display = 'block';
    previewContainer.style.display = 'none';
}

/**
 * Format file size for display
 * @param {number} bytes - File size in bytes
 * @returns {string} Formatted file size
 */
function formatFileSize(bytes) {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return Math.round(bytes / Math.pow(k, i) * 100) / 100 + ' ' + sizes[i];
}

/**
 * Client-side image validation
 * @param {File} file - Image file
 * @returns {boolean} Whether file is valid
 */
function validateImage(file) {
    // Check file type
    const validTypes = ['image/jpeg', 'image/jpg', 'image/png'];
    if (!validTypes.includes(file.type)) {
        return false;
    }

    // Check file size
    const maxSize = 10 * 1024 * 1024; // 10MB
    if (file.size > maxSize) {
        return false;
    }

    return true;
}
