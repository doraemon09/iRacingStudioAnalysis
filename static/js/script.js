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

// Session Info section
function showSessionData() {
    const default_section = document.getElementById('WeatherInfo');
    document.getElementById('session_data').style.display = 'block';
    default_section.style.display = 'block';
};

// Session Info buttons
function showSessionSection(section) {
    const this_section = document.getElementById(section);

    // Hide all session sections
    session_sections = ['WeatherInfo', 'SessionInfo', 'QualifyResultsInfo', 'SplitTimeInfo', 'CarSetup', 'DriverInfo', 'RadioInfo', 'CameraInfo'];
    session_sections.forEach(section => {
        document.getElementById(section).style.display = 'none';
    });

    // Show selected section
    this_section.style.display = 'block';
};

// Load preferred language on page load
document.addEventListener('DOMContentLoaded', () => {
    const preferredLanguage = localStorage.getItem('preferredLanguage') || 'en';
    switchLanguage(preferredLanguage);

    // Hide spinner on display.html
    document.getElementById('spinner-container').style.display = 'none';

    // Show session section on load by default
    showSessionData();
});
