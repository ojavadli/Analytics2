// hAIpClub Custom JavaScript

document.addEventListener('DOMContentLoaded', function() {
    // Initialize tooltips
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Initialize popovers
    var popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    var popoverList = popoverTriggerList.map(function (popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl);
    });

    // Auto-dismiss alerts after 5 seconds
    setTimeout(function() {
        var alerts = document.querySelectorAll('.alert');
        alerts.forEach(function(alert) {
            var bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        });
    }, 5000);

    // Instagram username fetch functionality
    const instagramInput = document.getElementById('id_instagram_username');
    const fetchButton = document.getElementById('fetch-instagram-data');
    const loadingSpinner = document.getElementById('instagram-loading');
    
    if (instagramInput && fetchButton) {
        fetchButton.addEventListener('click', function() {
            const username = instagramInput.value.trim();
            if (!username) {
                showAlert('Please enter an Instagram username', 'warning');
                return;
            }
            
            fetchInstagramData(username);
        });
        
        // Auto-fetch on username input (with debounce)
        let timeout;
        instagramInput.addEventListener('input', function() {
            clearTimeout(timeout);
            timeout = setTimeout(() => {
                const username = this.value.trim();
                if (username.length >= 3) {
                    fetchInstagramData(username);
                }
            }, 1500);
        });
    }

    // Content analysis functionality
    const contentTextarea = document.getElementById('id_caption_text');
    const analyzeButton = document.getElementById('analyze-content');
    const analysisResult = document.getElementById('analysis-result');
    
    if (contentTextarea && analyzeButton) {
        analyzeButton.addEventListener('click', function() {
            const content = contentTextarea.value.trim();
            if (!content) {
                showAlert('Please enter content to analyze', 'warning');
                return;
            }
            
            analyzeContent(content);
        });
    }

    // File upload preview
    const fileInputs = document.querySelectorAll('input[type="file"]');
    fileInputs.forEach(function(input) {
        input.addEventListener('change', function() {
            previewFile(this);
        });
    });

    // Claim offer functionality
    const claimButtons = document.querySelectorAll('.claim-offer-btn');
    claimButtons.forEach(function(button) {
        button.addEventListener('click', function() {
            const offerId = this.dataset.offerId;
            claimOffer(offerId);
        });
    });

    // Redeem offer functionality
    const redeemButtons = document.querySelectorAll('.redeem-offer-btn');
    redeemButtons.forEach(function(button) {
        button.addEventListener('click', function() {
            const claimId = this.dataset.claimId;
            const redeemCode = this.dataset.redeemCode;
            showRedeemModal(claimId, redeemCode);
        });
    });
});

// Fetch Instagram data via AJAX
function fetchInstagramData(username) {
    const loadingSpinner = document.getElementById('instagram-loading');
    const fetchButton = document.getElementById('fetch-instagram-data');
    
    if (loadingSpinner) loadingSpinner.style.display = 'block';
    if (fetchButton) fetchButton.disabled = true;
    
    fetch('/dashboard/ajax/fetch-instagram-data/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken')
        },
        body: JSON.stringify({
            username: username
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            updateInstagramFields(data.data);
            showAlert('Instagram data fetched successfully!', 'success');
        } else {
            showAlert(data.message || 'Failed to fetch Instagram data', 'danger');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        showAlert('An error occurred while fetching Instagram data', 'danger');
    })
    .finally(() => {
        if (loadingSpinner) loadingSpinner.style.display = 'none';
        if (fetchButton) fetchButton.disabled = false;
    });
}

// Update form fields with Instagram data
function updateInstagramFields(data) {
    const fields = [
        'follower_count',
        'following_count',
        'post_count',
        'engagement_rate',
        'bio'
    ];
    
    fields.forEach(field => {
        const input = document.getElementById(`id_${field}`);
        if (input && data[field] !== undefined) {
            input.value = data[field];
        }
    });
    
    // Update profile picture preview if available
    if (data.profile_pic_url) {
        const preview = document.getElementById('profile-pic-preview');
        if (preview) {
            preview.src = data.profile_pic_url;
            preview.style.display = 'block';
        }
    }
}

// Analyze content via AJAX
function analyzeContent(content) {
    const analysisResult = document.getElementById('analysis-result');
    const analyzeButton = document.getElementById('analyze-content');
    
    if (analyzeButton) analyzeButton.disabled = true;
    if (analysisResult) {
        analysisResult.innerHTML = '<div class="loading-spinner"></div>';
        analysisResult.style.display = 'block';
    }
    
    fetch('/dashboard/ajax/analyze-content/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken')
        },
        body: JSON.stringify({
            content: content
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            displayAnalysisResult(data.analysis);
        } else {
            showAlert(data.message || 'Failed to analyze content', 'danger');
            if (analysisResult) analysisResult.style.display = 'none';
        }
    })
    .catch(error => {
        console.error('Error:', error);
        showAlert('An error occurred during content analysis', 'danger');
        if (analysisResult) analysisResult.style.display = 'none';
    })
    .finally(() => {
        if (analyzeButton) analyzeButton.disabled = false;
    });
}

// Display content analysis result
function displayAnalysisResult(analysis) {
    const analysisResult = document.getElementById('analysis-result');
    if (!analysisResult) return;
    
    const recommendationClass = analysis.recommendation === 'approve' ? 'success' : 
                               analysis.recommendation === 'reject' ? 'danger' : 'warning';
    
    const html = `
        <div class="card">
            <div class="card-header">
                <h6 class="mb-0"><i class="bi bi-robot"></i> AI Content Analysis</h6>
            </div>
            <div class="card-body">
                <div class="row">
                    <div class="col-md-6">
                        <p><strong>Sentiment:</strong> 
                            <span class="badge bg-${analysis.sentiment === 'positive' ? 'success' : analysis.sentiment === 'negative' ? 'danger' : 'secondary'}">
                                ${analysis.sentiment}
                            </span>
                        </p>
                        <p><strong>Brand Mentioned:</strong> 
                            <span class="badge bg-${analysis.brand_mentioned ? 'success' : 'danger'}">
                                ${analysis.brand_mentioned ? 'Yes' : 'No'}
                            </span>
                        </p>
                    </div>
                    <div class="col-md-6">
                        <p><strong>Quality Score:</strong> ${analysis.quality_score}/10</p>
                        <p><strong>Brand Safe:</strong> 
                            <span class="badge bg-${analysis.brand_safe ? 'success' : 'danger'}">
                                ${analysis.brand_safe ? 'Yes' : 'No'}
                            </span>
                        </p>
                    </div>
                </div>
                <div class="alert alert-${recommendationClass} mt-3">
                    <strong>Recommendation:</strong> ${analysis.recommendation.toUpperCase()}
                </div>
                ${analysis.feedback ? `<p class="text-muted"><strong>Feedback:</strong> ${analysis.feedback}</p>` : ''}
                ${analysis.issues && analysis.issues.length > 0 ? `
                    <div class="mt-2">
                        <strong>Issues:</strong>
                        <ul class="mb-0">
                            ${analysis.issues.map(issue => `<li>${issue}</li>`).join('')}
                        </ul>
                    </div>
                ` : ''}
            </div>
        </div>
    `;
    
    analysisResult.innerHTML = html;
}

// File preview functionality
function previewFile(input) {
    if (input.files && input.files[0]) {
        const file = input.files[0];
        const reader = new FileReader();
        
        reader.onload = function(e) {
            const previewContainer = input.parentNode.querySelector('.file-preview');
            if (previewContainer) {
                if (file.type.startsWith('image/')) {
                    previewContainer.innerHTML = `<img src="${e.target.result}" class="img-fluid rounded" style="max-height: 200px;">`;
                } else if (file.type.startsWith('video/')) {
                    previewContainer.innerHTML = `<video src="${e.target.result}" class="img-fluid rounded" style="max-height: 200px;" controls></video>`;
                } else {
                    previewContainer.innerHTML = `<div class="alert alert-info">File selected: ${file.name}</div>`;
                }
                previewContainer.style.display = 'block';
            }
        };
        
        reader.readAsDataURL(file);
    }
}

// Claim offer functionality
function claimOffer(offerId) {
    if (!confirm('Are you sure you want to claim this offer?')) {
        return;
    }
    
    fetch(`/dashboard/offers/${offerId}/claim/`, {
        method: 'POST',
        headers: {
            'X-CSRFToken': getCookie('csrftoken')
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            showAlert('Offer claimed successfully!', 'success');
            setTimeout(() => {
                window.location.reload();
            }, 1500);
        } else {
            showAlert(data.message || 'Failed to claim offer', 'danger');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        showAlert('An error occurred while claiming the offer', 'danger');
    });
}

// Show redeem modal
function showRedeemModal(claimId, redeemCode) {
    const modal = new bootstrap.Modal(document.getElementById('redeemModal'));
    document.getElementById('redeem-code-display').textContent = redeemCode;
    document.getElementById('confirm-redeem-btn').dataset.claimId = claimId;
    modal.show();
}

// Utility function to get CSRF token
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

// Show alert message
function showAlert(message, type = 'info') {
    const alertContainer = document.getElementById('alert-container') || document.body;
    const alertDiv = document.createElement('div');
    alertDiv.className = `alert alert-${type} alert-dismissible fade show`;
    alertDiv.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    if (alertContainer === document.body) {
        alertDiv.style.position = 'fixed';
        alertDiv.style.top = '20px';
        alertDiv.style.right = '20px';
        alertDiv.style.zIndex = '9999';
        alertDiv.style.maxWidth = '400px';
    }
    
    alertContainer.appendChild(alertDiv);
    
    // Auto-dismiss after 5 seconds
    setTimeout(() => {
        const bsAlert = new bootstrap.Alert(alertDiv);
        bsAlert.close();
    }, 5000);
}

// Format numbers with commas (but respecting user preference for no commas)
function formatNumber(num) {
    // Based on user preference, we'll format without commas
    return num.toString();
}

// Smooth scrolling for anchor links
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            target.scrollIntoView({
                behavior: 'smooth',
                block: 'start'
            });
        }
    });
});

// Copy to clipboard functionality
function copyToClipboard(text) {
    navigator.clipboard.writeText(text).then(function() {
        showAlert('Copied to clipboard!', 'success');
    }, function(err) {
        console.error('Could not copy text: ', err);
        showAlert('Failed to copy to clipboard', 'danger');
    });
} 