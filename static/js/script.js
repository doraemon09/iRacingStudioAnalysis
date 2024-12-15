// Global var
const ms_to_kph = 3.6;
const ms_to_mph = 2.237;
const gravity = 9.81;
const m_to_mm = 1000;
const kPa_to_psi = 0.14503773773;

const sensor_sections = ['Timing', 'Vehicle', 'Garage', 'Pitstop', 'Positioning', 'Session', 'Weather', 'Radio', 'Replay', 'Camera', 'Miscellaneous', 'CarIdx', 'Undocumented'];
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
        document.getElementById(section).classList.add('d-none');
    });
};

// Show spinner for button
function showSpinner(button) {
    let this_spinner = document.getElementById(button + '-spinner');

    this_spinner.classList.remove('d-none'); // Removes `display:none`

    setTimeout(() => {
        this_spinner.classList.add('d-none'); // Adds `display:none`
    }, 800); // set in milliseconds
};

// Sensor section
function showSensorData() {
    document.getElementById('sensor_data').classList.remove('d-none');

    // Check if exists
    if(document.getElementById('static_data')) {
        document.getElementById('static_data').classList.add('d-none');
    };

    if(document.getElementById('telemetry_data')) {
        document.getElementById('telemetry_data').classList.add('d-none');
    };

    // Hide all static sections
    hideSections(sensor_sections)

    const default_section = document.getElementById(sensor_sections[0]);
    default_section.classList.remove('d-none');
};

// Sensor buttons
function showSensorSection(section) {
    // Hide all static sections
    hideSections(sensor_sections)

    // Show selected section
    const this_section = document.getElementById(section);
    this_section.classList.remove('d-none');
};


// Static Info section
function showStaticData() {
    document.getElementById('static_data').classList.remove('d-none');

    // Check if exists
    if(document.getElementById('sensor_data')) {
        document.getElementById('sensor_data').classList.add('d-none');
    };

    if(document.getElementById('telemetry_data')) {
        document.getElementById('telemetry_data').classList.add('d-none');
    };

    // Hide all static sections
    hideSections(static_sections)

    const default_section = document.getElementById(static_sections[0]);
    default_section.classList.remove('d-none');
};

// Static Info buttons
function showStaticSection(section) {
    // Hide all static sections
    hideSections(static_sections)

    // Show selected section
    const this_section = document.getElementById(section);
    this_section.classList.remove('d-none');
};

// Telemetry Info section
function showTelemetryData() {
    document.getElementById('telemetry_data').classList.remove('d-none');

    // Check if exists
    if(document.getElementById('sensor_data')) {
        document.getElementById('sensor_data').classList.add('d-none');
    };

    if(document.getElementById('static_data')) {
        document.getElementById('static_data').classList.add('d-none');
    };

    // Hide all telemetry sections
    hideSections(telemetry_sections)

    // Show spinner for button
    showSpinner(telemetry_sections[0])

    const default_section = document.getElementById(telemetry_sections[0]);
    default_section.classList.remove('d-none');
};

// Telemetry Info buttons
function showTelemetrySection(section) {
    // Hide all telemetry sections
    hideSections(telemetry_sections)

    // Show selected section
    const this_section = document.getElementById(section);
    this_section.classList.remove('d-none');

    // Show spinner for button
    showSpinner(section)

    if(section === 'Chart') {
        chartHoverSync();

        const this_charts = ['chartDeltaLapTime', 'chartDeltaSpeed', 'chartBrakeThrottle', 'chartSpeedGear', 'chartLatAccelYaw', 'chartSteeringAngleTorque'];

        this_charts.forEach(chart => {
            Plotly.relayout(chart, {
                'xaxis.autorange': true,
                'yaxis.autorange': true,
            });
        });
    };

    if(section === 'TrackMap') {
        const this_maps = ['mapSectors', 'mapAltLatLon', 'mapRideHeight', 'mapShockDeflection', 'mapShockVelocity', 'mapTirePressure', 'mapTireTemperature', 'mapSpeed'];

        let this_width;
        let this_height;
        this_maps.forEach(map => {
            this_width = document.getElementById('mapSectors').offsetWidth;
            this_height = document.getElementById('mapSectors').offsetWidth * 0.75;

            Plotly.relayout(map, {
                'width': this_width,
                'height': this_height,
            });

        });
    };
};

// Check if user is on mobile
function checkMobile() {
    document.getElementById('mobile-warning').classList.add('d-none');

    is_mobile = /Mobi|Android|iPhone|iPad|iPod|BlackBerry|Windows Phone|IEMobile|Opera Mini/i.test(navigator.userAgent);

    if(is_mobile) {
        document.getElementById('mobile-warning').classList.remove('d-none');
    };
};

// Check orientation on mobile
function checkOrientation() {
    document.getElementById('orientation-warning').classList.add('d-none');

    // Width < Height = Landscape
    if(window.innerWidth < window.innerHeight) {
        document.getElementById('orientation-warning').classList.remove('d-none');
    };
};

// Format lap time
function lapTimeFormat(laptime_seconds) {
    const minutes = Math.floor(laptime_seconds / 60);
    const seconds = Math.floor(laptime_seconds % 60);
    const milliseconds = Math.round((laptime_seconds % 1) * 1000);

    return `${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}.${milliseconds.toString().padStart(3, '0')}`;
};

// Prepend positive number with + sign
function formatWithPlus(value) {
    return value > 0 ? `+${value}` : value;
}

// radian to degree
function radian2Degree(radian) {
    return radian * (180 / Math.PI);
}


// Assign bearing based on degree of angle
function compassBearing(degree) {
    if(337.5 <= degree || degree < 22.5) {
        return "N"
    } else if(22.5 <= degree && degree < 67.5) {
        return "NE"
    } else if(67.5 <= degree && degree < 112.5) {
        return "E"
    } else if(112.5 <= degree && degree < 157.5) {
        return "SE"
    } else if(157.5 <= degree && degree < 202.5) {
        return "S"
    } else if(202.5 <= degree && degree < 247.5) {
        return "SW"
    } else if(247.5 <= degree && degree < 292.5) {
        return "W"
    } else if(292.5 <= degree && degree < 337.5) {
        return "NW"
    }
};

// Sync charts on hover
function chartHoverSync() {
    /*
        =========================
        Lap Time & Speed delta charts
        =========================
    */
    const chartDeltaLapTime = document.getElementById('chartDeltaLapTime');
    const chartDeltaSpeed = document.getElementById('chartDeltaSpeed');

    chartDeltaLapTime.on('plotly_hover', function(data) {
        let { curveNumber, pointIndex } = data.points[0];

        Plotly.Fx.hover('chartDeltaSpeed', [{
            curveNumber: curveNumber, // match lap trace
            pointNumber: pointIndex, // match point within the lap trace
        }]);
    });

    chartDeltaLapTime.on('plotly_unhover', function(data) {
        Plotly.Fx.unhover('chartDeltaSpeed');
    });

    chartDeltaSpeed.on('plotly_hover', function(data) {
        let { curveNumber, pointIndex } = data.points[0];

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
        Brake/Throttle & Speed/Gear & Speed/Fuel Usage & Steering Angle/Torque
        =========================
    */
    const chartBrakeThrottle = document.getElementById('chartBrakeThrottle');
    const chartLatAccelYaw = document.getElementById('chartLatAccelYaw');
    const chartSpeedGear = document.getElementById('chartSpeedGear');
    const chartSteeringAngleTorque = document.getElementById('chartSteeringAngleTorque');

    // chartBrakeThrottle
    chartBrakeThrottle.on('plotly_hover', function(data) {
        let { curveNumber, pointIndex } = data.points[0];

        const connect_charts = ['chartLatAccelYaw', 'chartSpeedGear', 'chartSteeringAngleTorque']

        connect_charts.forEach(chart => {
            Plotly.Fx.hover(chart, [{
                curveNumber: curveNumber,   // match trace
                pointNumber: pointIndex,    // match point within the trace
            }]);
        });
    });

    chartBrakeThrottle.on('plotly_unhover', function(data) {
        const connect_charts = ['chartLatAccelYaw', 'chartSpeedGear', 'chartSteeringAngleTorque']

        connect_charts.forEach(chart => {
            Plotly.Fx.unhover(chart);
        });
    });

    // chartLatAccelYaw
    chartLatAccelYaw.on('plotly_hover', function(data) {
        let { curveNumber, pointIndex } = data.points[0];

        const connect_charts = ['chartBrakeThrottle', 'chartSpeedGear', 'chartSteeringAngleTorque']

        connect_charts.forEach(chart => {
            Plotly.Fx.hover(chart, [{
                curveNumber: curveNumber,   // match trace
                pointNumber: pointIndex,    // match point within the trace
            }]);
        });
    });

    chartLatAccelYaw.on('plotly_unhover', function(data) {
        const connect_charts = ['chartBrakeThrottle', 'chartSpeedGear', 'chartSteeringAngleTorque']

        connect_charts.forEach(chart => {
            Plotly.Fx.unhover(chart);
        });
    });

    // chartSpeedGear
    chartSpeedGear.on('plotly_hover', function(data) {
        let { curveNumber, pointIndex } = data.points[0];

        const connect_charts = ['chartBrakeThrottle', 'chartLatAccelYaw', 'chartSteeringAngleTorque']

        connect_charts.forEach(chart => {
            Plotly.Fx.hover(chart, [{
                curveNumber: curveNumber,   // match trace
                pointNumber: pointIndex,    // match point within the trace
            }]);
        });
    });

    chartSpeedGear.on('plotly_unhover', function(data) {
        const connect_charts = ['chartBrakeThrottle', 'chartLatAccelYaw', 'chartSteeringAngleTorque']

        connect_charts.forEach(chart => {
            Plotly.Fx.unhover(chart);
        });
    });

    // chartSteeringAngleTorque
    chartSteeringAngleTorque.on('plotly_hover', function(data) {
        let { curveNumber, pointIndex } = data.points[0];

        const connect_charts = ['chartBrakeThrottle', 'chartLatAccelYaw', 'chartSpeedGear']

        connect_charts.forEach(chart => {
            Plotly.Fx.hover(chart, [{
                curveNumber: curveNumber,   // match trace
                pointNumber: pointIndex,    // match point within the trace
            }]);
        });
    });

    chartSteeringAngleTorque.on('plotly_unhover', function(data) {
        const connect_charts = ['chartBrakeThrottle', 'chartLatAccelYaw', 'chartSpeedGear']

        connect_charts.forEach(chart => {
            Plotly.Fx.unhover(chart);
        });
    });
};

// On DOM loaded
document.addEventListener('DOMContentLoaded', () => {
    const preferredLanguage = localStorage.getItem('preferredLanguage') || 'en';
    switchLanguage(preferredLanguage);

    checkOrientation();

    checkMobile();
});

// On page load
window.addEventListener('load', () => {
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
        document.getElementById('spinner-container').classList.add('d-none');

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
