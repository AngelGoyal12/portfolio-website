// Contact form AJAX submission with redirect to home
const contactForm = document.getElementById('contact-form');
const submitBtn = document.getElementById('submit-btn');
const successMessage = document.getElementById('success-message');
const errorMessage = document.getElementById('error-message');

if (contactForm) {
    contactForm.addEventListener('submit', async function(e) {
        e.preventDefault();
        
        // Disable button and show loading state
        submitBtn.textContent = 'Sending...';
        submitBtn.disabled = true;
        
        // Hide any previous messages
        successMessage.style.display = 'none';
        errorMessage.style.display = 'none';
        
        // Get form data
        const formData = new FormData(contactForm);
        
        try {
            // Submit to Formspree
            const response = await fetch(contactForm.action, {
                method: 'POST',
                body: formData,
                headers: {
                    'Accept': 'application/json'
                }
            });
            
            if (response.ok) {
                // Success! Show message briefly, then redirect
                successMessage.style.display = 'block';
                contactForm.reset();
                
                // Scroll to top to see message
                window.scrollTo({ top: 0, behavior: 'smooth' });
                
                // Redirect to home page after 2 seconds
                setTimeout(() => {
                    window.location.href = '/?message=success';
                }, 5000);
                
            } else {
                // Error response from server
                throw new Error('Server error');
            }
            
        } catch (error) {
            // Show error message
            errorMessage.style.display = 'block';
            submitBtn.textContent = 'Send Message';
            submitBtn.disabled = false;
            
            // Scroll to top to see error
            window.scrollTo({ top: 0, behavior: 'smooth' });
        }
    });
}

// Check if redirected from contact form (show flash message on home page)
window.addEventListener('DOMContentLoaded', function() {
    const urlParams = new URLSearchParams(window.location.search);
    const messageType = urlParams.get('message');
    
    if (messageType === 'success') {
        // Create and show flash message
        const flashMessage = document.createElement('div');
        flashMessage.className = 'flash-message flash-success';
        flashMessage.innerHTML = '✅ Thank you for your message! I will get back to you soon.';
        document.body.appendChild(flashMessage);
        
        // Show with animation
        setTimeout(() => {
            flashMessage.classList.add('show');
        }, 100);
        
        // Remove after 5 seconds
        setTimeout(() => {
            flashMessage.classList.remove('show');
            setTimeout(() => {
                flashMessage.remove();
            }, 300);
        }, 5000);
        
        // Clean URL (remove ?message=success)
        window.history.replaceState({}, document.title, window.location.pathname);
    }
});