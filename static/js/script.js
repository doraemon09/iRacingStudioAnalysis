// Global var
let session_sections = ['WeatherInfo', 'SessionInfo', 'QualifyResultsInfo', 'SplitTimeInfo', 'CarSetup', 'DriverInfo', 'RadioInfo', 'CameraInfo'];
let telemetry_sections = ['Charts', 'Laps', 'TrackMaps'];

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
            element.innerHTML = element.getAttribute(`data-${language}`);
        };
    });
};

function hideSections(section_list) {
    section_list.forEach(section => {
        document.getElementById(section).style.display = 'none';
    });
};

// Session Info section
function showSessionData() {
    document.getElementById('session_data').style.display = 'block';
    document.getElementById('telemetry_data').style.display = 'none';

    // Hide all session sections
    hideSections(session_sections)

    const default_section = document.getElementById('WeatherInfo');
    default_section.style.display = 'block';
};

// Session Info buttons
function showSessionSection(section) {
    // Hide all session sections
    hideSections(session_sections)

    // Show selected section
    const this_section = document.getElementById(section);
    this_section.style.display = 'block';
};

// Telemetry Info section
function showTelemetryData() {
    document.getElementById('telemetry_data').style.display = 'block';
    document.getElementById('session_data').style.display = 'none';

    // Hide all telemetry sections
    hideSections(telemetry_sections)

    const default_section = document.getElementById('Charts');
    default_section.style.display = 'block';
};

// Telemetry Info buttons
function showTelemetrySection(section) {
    // Hide all telemetry sections
    hideSections(telemetry_sections)

    // Show selected section
    const this_section = document.getElementById(section);
    this_section.style.display = 'block';
};

// Load preferred language on page load
document.addEventListener('DOMContentLoaded', () => {
    const preferredLanguage = localStorage.getItem('preferredLanguage') || 'en';
    switchLanguage(preferredLanguage);

    // Look for display page
    const display_page = document.getElementById('display');

    if (display_page) {
        // Hide loading spinner
        document.getElementById('spinner-container').style.display = 'none';

        // Show telemetry section on load by default
        showTelemetryData();

        // Turn the table into a DataTable
        $('table').DataTable({
            lengthMenu: [ 5, 10, 15, 20, 25 ],
            pageLength: 15,
            "order": [], // Disable default sort onload
        });
    };
});
