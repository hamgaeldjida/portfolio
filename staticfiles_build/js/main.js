// Wait for the DOM to be fully loaded
document.addEventListener('DOMContentLoaded', function() {
    // Add a typing effect to the welcome message
    const welcomeText = document.querySelector('h1');
    const originalText = welcomeText.textContent;
    welcomeText.textContent = '';
    
    let i = 0;
    function typeWriter() {
        if (i < originalText.length) {
            welcomeText.textContent += originalText.charAt(i);
            i++;
            setTimeout(typeWriter, 100);
        }
    }
    
    // Start the typing effect
    typeWriter();

    // Add hover effect to the container
    const container = document.querySelector('.container');
    container.addEventListener('mouseenter', function() {
        this.style.transform = 'scale(1.02)';
        this.style.transition = 'transform 0.3s ease';
    });

    container.addEventListener('mouseleave', function() {
        this.style.transform = 'scale(1)';
    });
}); 