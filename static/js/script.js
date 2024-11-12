// Languages
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
    document.getElementById('session_data').style.display = 'block';
    document.getElementById('telemetry_data').style.display = 'none';

    const default_section = document.getElementById('WeatherInfo');
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

// Telemetry Info section
function showTelemetryData() {
    document.getElementById('telemetry_data').style.display = 'block';
    document.getElementById('session_data').style.display = 'none';

    //const default_section = document.getElementById('LapTime');
    //default_section.style.display = 'block';
};

// Telemetry Info buttons
function showTelemetrySection(section) {
    const this_section = document.getElementById(section);

    // Show selected section
    this_section.style.display = 'block';
};

// Load preferred language on page load
document.addEventListener('DOMContentLoaded', () => {
    const preferredLanguage = localStorage.getItem('preferredLanguage') || 'en';
    switchLanguage(preferredLanguage);

    // Look for spinner which only exists post file upload
    const spinner = document.getElementById('spinner-container');

    if (spinner) {
        spinner.style.display = 'none';

        // Show session section on load by default
        showSessionData();
    };

    // Turn the table into a DataTable
    $('table').DataTable({
        lengthMenu: [ 5, 10, 15, 20, 25 ],
        pageLength: 15,
    });
});
