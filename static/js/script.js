// Global var
let static_sections = ['WeekendInfo', 'SessionInfo', 'QualifyResultsInfo', 'SplitTimeInfo', 'CarSetup', 'DriverInfo', 'RadioInfo', 'CameraInfo'];
let telemetry_sections = ['Laps', 'Charts', 'TrackMaps'];

// Languages
function switchLanguage(language) {
    // Save selected preference
    localStorage.setItem('preferredLanguage', language);

    // Update content display per selected language
    const languages = document.querySelectorAll('[data-en][data-jp]');
    languages.forEach(this_language => {
        if (this_language.tagName.toLowerCase() === 'input' && this_language.type.toLowerCase() === 'submit') {
            this_language.value = this_language.getAttribute(`data-${language}`);
        } else {
            this_language.innerHTML = this_language.getAttribute(`data-${language}`);
        };
    });
};

// Hide sections
function hideSections(section_list) {
    section_list.forEach(section => {
        document.getElementById(section).style.display = 'none';
    });
};

// Static Info section
function showStaticData() {
    document.getElementById('static_data').style.display = 'block';

    // Check if exists
    if(document.getElementById('telemetry_data')) {
        document.getElementById('telemetry_data').style.display = 'none';
    };

    // Hide all static sections
    hideSections(static_sections)

    const default_section = document.getElementById('WeekendInfo');
    default_section.style.display = 'block';
};

// Static Info buttons
function showStaticSection(section) {
    // Hide all static sections
    hideSections(static_sections)

    // Show selected section
    const this_section = document.getElementById(section);
    this_section.style.display = 'block';
};

// Telemetry Info section
function showTelemetryData() {
    document.getElementById('telemetry_data').style.display = 'block';

    // Check if exists
    if(document.getElementById('static_data')) {
        document.getElementById('static_data').style.display = 'none';
    };

    // Hide all telemetry sections
    hideSections(telemetry_sections)

    const default_section = document.getElementById('Laps');
    default_section.style.display = 'block';
};

// Telemetry Info buttons
function showTelemetrySection(section) {
    // Hide all telemetry sections
    hideSections(telemetry_sections)

    // Show selected section
    const this_section = document.getElementById(section);
    this_section.style.display = 'block';

    if(section === 'Charts') {
        const this_charts = ['chartDeltaLapTime', 'chartDeltaSpeed', 'chartBrakeThrottle', 'chartSpeedGear'];

        this_charts.forEach(id => {
            Plotly.relayout(id, {
                'xaxis.autorange': true,
                'yaxis.autorange': true,
            });
        });
    };

    if(section === 'TrackMaps') {
        const this_maps = ['mapSectors'];

        this_maps.forEach(id => {
            Plotly.relayout(id, {
                'xaxis.autorange': true,
                'yaxis.autorange': true,
            });
        });
    };
};

// Check if user is on mobile
function checkMobile() {
    document.getElementById('mobile-warning').style.display = 'none';

    is_Mobile = /Mobi|Android|iPhone|iPad|iPod|BlackBerry|Windows Phone|IEMobile|Opera Mini/i.test(navigator.userAgent);

    if(is_Mobile) {
        document.getElementById('mobile-warning').style.display = 'block';
    };
};

// Check orientation on mobile
function checkOrientation() {
    document.getElementById('orientation-warning').style.display = 'none';

    // Width < Height = Landscape
    if(window.innerWidth < window.innerHeight) {
        document.getElementById('orientation-warning').style.display = 'block';
    };
};

// Format lap time
function lapTimeFormat(laptime_seconds) {
    const minutes = Math.floor(laptime_seconds / 60);
    const seconds = Math.floor(laptime_seconds % 60);
    const milliseconds = Math.round((laptime_seconds % 1) * 1000);

    return `${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}.${milliseconds.toString().padStart(3, '0')}`;
};

// On page load
document.addEventListener('DOMContentLoaded', () => {
    const preferredLanguage = localStorage.getItem('preferredLanguage') || 'en';
    switchLanguage(preferredLanguage);

    checkOrientation();

    checkMobile();

    // Look for index page
    const index_page = document.getElementById('index');

    if (index_page) {
        const this_form = document.getElementById('upload-demo-form');
        const this_submit = document.getElementById('upload-demo-submit');
        const this_spinner = document.getElementById('upload-demo-spinner');

        this_form.addEventListener('submit', function(event) {
            // Disable sbumit button and show the spinner
            this_submit.setAttribute('disabled', true);
            this_spinner.classList.remove('d-none'); // Removes `display:none`

            //event.preventDefault();
        });
    };

    // Look for display page
    const display_page = document.getElementById('display');

    if (display_page) {
        // Hide loading spinner
        document.getElementById('spinner-container').style.display = 'none';

        // If exists, show telemetry section on load by default
        if(document.getElementById('telemetry_data')) {
            showTelemetryData();
        } else {
            showStaticData();
        }

        // Turn the table into a DataTable
        $('table').DataTable({
            lengthMenu: [ 5, 10, 15, 20, 25 ],
            pageLength: 15,
            "order": [], // Disable default sort onload
        });
    };
});

// On resize
window.addEventListener('resize', () => {
    checkOrientation();
});
