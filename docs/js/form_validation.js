/**
 * Form validation for trading cues subscription
 */
document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('subscription-form');
    
    if (form) {
        form.addEventListener('submit', function(event) {
            // Get form values
            const email = document.getElementById('email').value.trim();
            const slackId = document.getElementById('slack_id').value.trim();
            
            // Check if at least one contact method is provided
            if (!email && !slackId) {
                event.preventDefault();
                showError('Please provide either an email address or Slack ID');
                return;
            }
            
            // Validate email if provided
            if (email && !isValidEmail(email)) {
                event.preventDefault();
                showError('Please enter a valid email address');
                return;
            }
            
            // Check if at least one trading cue is selected
            const checkboxes = form.querySelectorAll('input[type="checkbox"]:checked');
            if (checkboxes.length === 0) {
                event.preventDefault();
                showError('Please select at least one trading cue');
                return;
            }
        });
    }
    
    /**
     * Validates an email address
     * @param {string} email - The email to validate
     * @returns {boolean} - Whether the email is valid
     */
    function isValidEmail(email) {
        const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        return emailPattern.test(email);
    }
    
    /**
     * Displays an error message on the form
     * @param {string} message - The error message to display
     */
    function showError(message) {
        // Remove any existing alerts
        const existingAlerts = document.querySelectorAll('.alert');
        existingAlerts.forEach(alert => alert.remove());
        
        // Create a new alert
        const alertEl = document.createElement('div');
        alertEl.className = 'alert alert-danger alert-dismissible fade show mt-3';
        alertEl.role = 'alert';
        alertEl.innerHTML = `
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
        `;
        
        // Insert at the top of the form
        form.insertBefore(alertEl, form.firstChild);
        
        // Scroll to the alert
        alertEl.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }
});
