function switchLanguage(language) {
    // Save selected preference
    localStorage.setItem('preferredLanguage', language);

    // Update content display per selected language
    const elements = document.querySelectorAll('[data-en][data-jp]');
    elements.forEach(element => {
        if (element.tagName.toLowerCase() === 'input' && element.type.toLowerCase() === 'submit') {
            element.value = element.getAttribute(`data-${language}`);
        } else {
            element.textContent = element.getAttribute(`data-${language}`);
        };
    });
};

// Load preferred language on page load
document.addEventListener('DOMContentLoaded', () => {
    const preferredLanguage = localStorage.getItem('preferredLanguage') || 'en';
    switchLanguage(preferredLanguage);
});
