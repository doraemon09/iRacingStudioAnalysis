function switchLanguage(language) {
    // Save selected preference
    localStorage.setItem('preferredLanguage', language);

    // Update content display per selected language
    const elements = document.querySelectorAll('[data-en][data-jp]');
    elements.forEach(element => {
        element.textContent = element.getAttribute(`data-${language}`);
    });
};

// Load preferred language on page load
document.addEventListener('DOMContentLoaded', () => {
    const preferredLanguage = localStorage.getItem('preferredLanguage') || 'en';
    switchLanguage(preferredLanguage);
});
