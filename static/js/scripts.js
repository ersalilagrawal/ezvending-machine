document.addEventListener('DOMContentLoaded', function() {
    const successMessage = document.querySelector('.success');
    if (successMessage) {
        setTimeout(function() {
            window.location.href = '/';
        }, 3000);  // Redirect after 3 seconds
    }
});