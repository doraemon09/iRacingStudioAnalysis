// Global var
const sensor_sections = ['Timing', 'Vehicle', 'Garage', 'Pitstop', 'Positioning', 'Session', 'Weather', 'Radio', 'Replay', 'Camera', 'Miscellaneous', 'CarIdx', 'Unlisted'];
const static_sections = ['WeekendInfo', 'SessionInfo', 'QualifyResultsInfo', 'SplitTimeInfo', 'CarSetup', 'DriverInfo', 'RadioInfo', 'CameraInfo'];
const telemetry_sections = ['Lap', 'Chart', 'TrackMap'];

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

// Sensor section
function showSensorData() {
    document.getElementById('sensor_data').style.display = 'block';

    // Check if exists
    if(document.getElementById('static_data')) {
        document.getElementById('static_data').style.display = 'none';
    };

    if(document.getElementById('telemetry_data')) {
        document.getElementById('telemetry_data').style.display = 'none';
    };

    // Hide all static sections
    hideSections(sensor_sections)

    const default_section = document.getElementById(sensor_sections[0]);
    default_section.style.display = 'block';
};

// Sensor buttons
function showSensorSection(section) {
    // Hide all static sections
    hideSections(sensor_sections)

    // Show selected section
    const this_section = document.getElementById(section);
    this_section.style.display = 'block';
};


// Static Info section
function showStaticData() {
    document.getElementById('static_data').style.display = 'block';

    // Check if exists
    if(document.getElementById('sensor_data')) {
        document.getElementById('sensor_data').style.display = 'none';
    };

    if(document.getElementById('telemetry_data')) {
        document.getElementById('telemetry_data').style.display = 'none';
    };

    // Hide all static sections
    hideSections(static_sections)

    const default_section = document.getElementById(static_sections[0]);
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
    if(document.getElementById('sensor_data')) {
        document.getElementById('sensor_data').style.display = 'none';
    };

    if(document.getElementById('static_data')) {
        document.getElementById('static_data').style.display = 'none';
    };

    // Hide all telemetry sections
    hideSections(telemetry_sections)

    const default_section = document.getElementById(telemetry_sections[0]);
    default_section.style.display = 'block';
};

// Telemetry Info buttons
function showTelemetrySection(section) {
    // Hide all telemetry sections
    hideSections(telemetry_sections)

    // Show selected section
    const this_section = document.getElementById(section);
    this_section.style.display = 'block';

    if(section === 'Chart') {
        chart_hover_sync();

        const this_charts = ['chartDeltaLapTime', 'chartDeltaSpeed', 'chartBrakeThrottle', 'chartSpeedGear', 'chartSpeedFuelUsage', 'chartSteeringAngleTorque'];

        this_charts.forEach(chart => {
            Plotly.relayout(chart, {
                'xaxis.autorange': true,
                'yaxis.autorange': true,
            });
        });
    };

    if(section === 'TrackMap') {
        const this_maps = ['mapSectors'];

        this_maps.forEach(map => {
            var this_width = document.getElementById('mapSectors').offsetWidth;
            var this_height = document.getElementById('mapSectors').offsetWidth * 0.75;

            Plotly.relayout(map, {
                'width': this_width,
                'height': this_height,
            });

        });
    };
};

// Check if user is on mobile
function checkMobile() {
    document.getElementById('mobile-warning').style.display = 'none';

    is_mobile = /Mobi|Android|iPhone|iPad|iPod|BlackBerry|Windows Phone|IEMobile|Opera Mini/i.test(navigator.userAgent);

    if(is_mobile) {
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

// Sync charts on hover
function chart_hover_sync() {
    /*
        =========================
        Sync hover on Lap Time & Speed delta charts
        =========================
    */
    var chartDeltaLapTime = document.getElementById('chartDeltaLapTime');
    var chartDeltaSpeed = document.getElementById('chartDeltaSpeed');

    chartDeltaLapTime.on('plotly_hover', function(data) {
        var { curveNumber, pointIndex } = data.points[0];

        Plotly.Fx.hover('chartDeltaSpeed', [{
            curveNumber: curveNumber, // match lap trace
            pointNumber: pointIndex, // match point within the lap trace
        }]);
    });

    chartDeltaLapTime.on('plotly_unhover', function(data) {
        Plotly.Fx.unhover('chartDeltaSpeed');
    });

    chartDeltaSpeed.on('plotly_hover', function(data) {
        var { curveNumber, pointIndex } = data.points[0];

        Plotly.Fx.hover('chartDeltaLapTime', [{
            curveNumber: curveNumber,   // match trace
            pointNumber: pointIndex,    // match point within the trace
        }]);
    });

    chartDeltaSpeed.on('plotly_unhover', function(data) {
        Plotly.Fx.unhover('chartDeltaLapTime');
    });

    /*
        =========================
        Sync hover on Brake/Throttle & Speed/Gear & Speed/Fuel Usage & Steering Angle/Torque
        =========================
    */
    var chartBrakeThrottle = document.getElementById('chartBrakeThrottle');
    var chartSpeedFuelUsage = document.getElementById('chartSpeedFuelUsage');
    var chartSpeedGear = document.getElementById('chartSpeedGear');
    var chartSteeringAngleTorque = document.getElementById('chartSteeringAngleTorque');

    // chartBrakeThrottle
    chartBrakeThrottle.on('plotly_hover', function(data) {
        var { curveNumber, pointIndex } = data.points[0];

        const connect_charts = ['chartSpeedFuelUsage', 'chartSpeedGear', 'chartSteeringAngleTorque']

        connect_charts.forEach(chart => {
            Plotly.Fx.hover(chart, [{
                curveNumber: curveNumber,   // match trace
                pointNumber: pointIndex,    // match point within the trace
            }]);
        });
    });

    chartBrakeThrottle.on('plotly_unhover', function(data) {
        const connect_charts = ['chartSpeedFuelUsage', 'chartSpeedGear', 'chartSteeringAngleTorque']

        connect_charts.forEach(chart => {
            Plotly.Fx.unhover(chart);
        });
    });

    // chartSpeedFuelUsage
    chartSpeedFuelUsage.on('plotly_hover', function(data) {
        var { curveNumber, pointIndex } = data.points[0];

        const connect_charts = ['chartBrakeThrottle', 'chartSpeedGear', 'chartSteeringAngleTorque']

        connect_charts.forEach(chart => {
            Plotly.Fx.hover(chart, [{
                curveNumber: curveNumber,   // match trace
                pointNumber: pointIndex,    // match point within the trace
            }]);
        });
    });

    chartSpeedFuelUsage.on('plotly_unhover', function(data) {
        const connect_charts = ['chartBrakeThrottle', 'chartSpeedGear', 'chartSteeringAngleTorque']

        connect_charts.forEach(chart => {
            Plotly.Fx.unhover(chart);
        });
    });

    // chartSpeedGear
    chartSpeedGear.on('plotly_hover', function(data) {
        var { curveNumber, pointIndex } = data.points[0];

        const connect_charts = ['chartBrakeThrottle', 'chartSpeedFuelUsage', 'chartSteeringAngleTorque']

        connect_charts.forEach(chart => {
            Plotly.Fx.hover(chart, [{
                curveNumber: curveNumber,   // match trace
                pointNumber: pointIndex,    // match point within the trace
            }]);
        });
    });

    chartSpeedGear.on('plotly_unhover', function(data) {
        const connect_charts = ['chartBrakeThrottle', 'chartSpeedFuelUsage', 'chartSteeringAngleTorque']

        connect_charts.forEach(chart => {
            Plotly.Fx.unhover(chart);
        });
    });

    // chartSteeringAngleTorque
    chartSteeringAngleTorque.on('plotly_hover', function(data) {
        var { curveNumber, pointIndex } = data.points[0];

        const connect_charts = ['chartBrakeThrottle', 'chartSpeedFuelUsage', 'chartSpeedGear']

        connect_charts.forEach(chart => {
            Plotly.Fx.hover(chart, [{
                curveNumber: curveNumber,   // match trace
                pointNumber: pointIndex,    // match point within the trace
            }]);
        });
    });

    chartSteeringAngleTorque.on('plotly_unhover', function(data) {
        const connect_charts = ['chartBrakeThrottle', 'chartSpeedFuelUsage', 'chartSpeedGear']

        connect_charts.forEach(chart => {
            Plotly.Fx.unhover(chart);
        });
    });
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
            'order': [], // Disable default sort onload
        });
    };
});

// On resize
window.addEventListener('resize', () => {
    checkOrientation();
});
