import copy
from flask import Flask, render_template, request, redirect, url_for
import irsdk
import numpy as np
import os
import pandas as pd
import sqlite3
import sys
import yaml
import werkzeug.utils


# Initialize Flash app
app = Flask(__name__)

# Load YAML with utf-8 encoding
with open('config/parameters.yaml', 'r', encoding='utf-8') as yaml_file:
    yaml_data = yaml.safe_load(yaml_file)

# Set file folders
app.config['UPLOAD_FOLDER'] = yaml_data['Config']['Upload']['Folder']
#DEMO_FILES_DIR = yaml_data['Config']['Demo']['Folder']

# SQLite db
DATABASE = yaml_data['Config']['Database']['Path']

# Set allowed file extensions
ALLOWED_FILE_EXTENSIONS = { yaml_data['Config']['Upload']['Extensions'] }


# Check for file extension on uploaded file
def allowed_file(filename):
    if '.' not in filename:
        return False
    return filename.rsplit('.', 1)[1].lower() in ALLOWED_FILE_EXTENSIONS


# Route for upload form
@app.route('/', methods=['GET', 'POST'])
def upload_file():
    # Check if user is on local machine
    is_localhost = request.host == '127.0.0.1:5001'

    if request.method == 'POST':
        # 1 = Upload
        if is_localhost:
            # Process upload file
            if 'upload_file' not in request.files:
                return "No file uploaded!"

            # Assign to file variable
            this_file_name = request.files['upload_file'].filename
            this_folder_path = app.config['UPLOAD_FOLDER']
        # 0 = Demo
        else:
            # Assign to file variables
            this_file_name = request.form.get('demo_file')
            #this_folder_path = DEMO_FILES_DIR

        # Check allowed file on localhost
        # Demo files are pre-defined therefore can be bypassed
        if (is_localhost and allowed_file(this_file_name)) or not is_localhost:
            if is_localhost:
                # Clean up file name
                this_file_name = werkzeug.utils.secure_filename(this_file_name)

                # Set file path
                this_file_path = os.path.join(this_folder_path, this_file_name)

            try:
                if is_localhost:
                    # Save upload file to directory
                    request.files['upload_file'].save(this_file_path)

                    # Static Info | gets dict
                    static_data = get_static_data(this_file_path)

                    # Telemetry Info | gets dataframe
                    telemetry_data = get_telemetry_data(this_file_path)

                    # Process selected lap related data | gets dict
                    session_data = process_session_data(telemetry_data)

                    # Sector data | gets dict
                    sector_data = process_sectors_data(static_data, session_data)

                    """
                    # Dump data into txt file
                    this_charts_data = this_file_name.rsplit('.', 1)[0] + '_charts_data.txt'
                    this_laps_data = this_file_name.rsplit('.', 1)[0] + '_laps_data.txt'
                    this_laps_report_data = this_file_name.rsplit('.', 1)[0] + '_laps_report_data.txt'
                    this_reference_lap_data = this_file_name.rsplit('.', 1)[0] + '_reference_lap_data.txt'
                    this_sector_times_data = this_file_name.rsplit('.', 1)[0] + '_sector_times_data.txt'
                    this_sectors_data = this_file_name.rsplit('.', 1)[0] + '_sectors_data.txt'
                    this_sectors_report_data = this_file_name.rsplit('.', 1)[0] + '_sectors_report_data.txt'
                    this_static_data = this_file_name.rsplit('.', 1)[0] + '_static_data.txt'

                    with open(this_charts_data, "w") as txt_file:
                        txt_file.write(repr(session_data['charts_data']))
                    with open(this_laps_data, "w") as txt_file:
                        txt_file.write(repr(session_data['laps_data']))
                    with open(this_laps_report_data, "w") as txt_file:
                        txt_file.write(repr(session_data['laps_report_data']))
                    with open(this_reference_lap_data, "w") as txt_file:
                        txt_file.write(repr(session_data['reference_lap_data']))
                    with open(this_sector_times_data, "w") as txt_file:
                        txt_file.write(repr(sector_data['sector_times_data']))
                    with open(this_sectors_data, "w") as txt_file:
                        txt_file.write(repr(sector_data['sectors_data']))
                    with open(this_sectors_report_data, "w") as txt_file:
                        txt_file.write(repr(sector_data['sectors_report_data']))
                    with open(this_static_data, "w") as txt_file:
                        txt_file.write(repr(static_data))
                    """
                else:
                    # Connect to SQLite
                    this_db = sqlite3.connect(DATABASE)

                    # Convert rows into dictionary-like objects
                    this_db.row_factory = sqlite3.Row

                    # Interact with db via cursor() object
                    cursor = this_db.cursor()
                    cursor.execute('SELECT * FROM telemetry WHERE name = ?', (this_file_name,))

                    this_demo = cursor.fetchone()

                    # Assign with eval() to convert str to dict
                    session_data = {
                        'charts_data': eval(this_demo['charts_data']),
                        'laps_data': eval(this_demo['laps_data']),
                        'laps_report_data': eval(this_demo['laps_report_data']),
                        'reference_lap_data': eval(this_demo['reference_lap_data']),
                    }
                    sector_data = {
                        'sector_times_data': eval(this_demo['sector_times_data']),
                        'sectors_data': eval(this_demo['sectors_data']),
                        'sectors_report_data': eval(this_demo['sectors_report_data']),
                    }
                    static_data = eval(this_demo['static_data'])

                    this_db.close()

                return render_template(
                    'display.html',
                    charts_info=session_data['charts_data'],
                    laps_info=session_data['laps_data'],
                    laps_report_info=session_data['laps_report_data'],
                    reference_lap_info=session_data['reference_lap_data'],
                    sector_times_info=sector_data['sector_times_data'],
                    sectors_info=sector_data['sectors_data'],
                    sectors_report_info=sector_data['sectors_report_data'],
                    static_info=static_data,
                    yaml_info=yaml_data,
                )
            except Exception as err:
                return f"Error processing file: {err}"
        else:
            return "Invalid file extension. iRacing telemetry (.ibt) file only!"
    """
        Else
    """
    demo_files = []

    if not is_localhost:
        #demo_files = os.listdir(DEMO_FILES_DIR)

        # Connect to db for demo name list
        this_db = sqlite3.connect(DATABASE)
        cursor = this_db.cursor()
        cursor.execute('SELECT name FROM telemetry')

        demo_files = [row[0] for row in cursor.fetchall()]

        this_db.close()

    return render_template(
        'index.html',
        is_localhost=is_localhost,
        demo_files=sorted(demo_files),
        yaml_info=yaml_data,
    )


# Retrieve static info, ie: Weather and Car Set up
def get_static_data(filepath):
    try:
        # Use IRSDK class for static info
        ibt_static_data = irsdk.IRSDK()

        # Read uploaded file
        ibt_static_data.startup(test_file=filepath)

        # Parse into readable data
        info_to_process = ['WeekendInfo', 'SessionInfo', 'QualifyResultsInfo', 'SplitTimeInfo', 'CarSetup', 'DriverInfo', 'RadioInfo', 'CameraInfo']

        info_dict = {}

        for header in info_to_process:
            try:
                # Assigned retrieved data set
                info_dict[header] = ibt_static_data[header]
            except Exception as err:
                # Set to empty if header is not found in ibt_static_data
                # Which should not happen to begine with
                info_dict[header] = {}
                print(f"Error retrieving data for {header}: {err}")

        return info_dict
    except Exception as err:
        return f"Error reading file: {err}"


# Retrieve telemetry info, ie: Lap time and Throttle
def get_telemetry_data(filepath):
    try:
        # Use IBT class for telemetry info
        ibt_telemetry_data = irsdk.IBT()

        # Read uploaded file
        ibt_telemetry_data.open(filepath)

        # Store data into a dataframe
        telemetry_info = process_ibt_telemetry_data(ibt_telemetry_data)

        return telemetry_info
    except Exception as err:
        return f"Error reading file: {err}"


# Process telemetry data into dataframe
def process_ibt_telemetry_data(ibt_telemetry_data):
    try:
        # Initialize new dictionary
        telemetry_dict = {}

        # Loop header with get_all() to retrieve data (list)
        for header in ibt_telemetry_data.var_headers_names:
            try:
                # Assigned retrieved data set
                telemetry_dict[header] = ibt_telemetry_data.get_all(header)
            except Exception as err:
                # Set to empty if header is not found in ibt_telemetry_info
                # Which should not happen to begine with
                telemetry_dict[header] = []
                print(f"Error retrieving data for {header}: {err}")

        # Create dataframe with telemetry_dict
        telemetry_dataframe = pd.DataFrame(telemetry_dict)

        # Replace missing data values (NaN) with 0
        telemetry_dataframe.fillna(0, inplace=True)

        return telemetry_dataframe
    except Exception as err:
        print(f"Error processing telemetry info: {err}")
        return []


# Lap data
def process_session_data(ibt_telemetry_data):
    try:
        fields_to_process = ['Brake', 'Gear', 'Lap', 'LapDist', 'Lat', 'Lon', 'RPM', 'Speed', 'Throttle']

        main_dict = {}

        for header in fields_to_process:
            try:
                # Assigned retrieved data set
                main_dict[header] = ibt_telemetry_data[header]
            except Exception as err:
                # Set to empty if header is not found in ibt_telemetry_info
                # Which should not happen to begine with
                main_dict[header] = {}
                print(f"Error retrieving data for {header}: {err}")

        # Create dataframe with lap_dict
        main_dataframe = pd.DataFrame(main_dict)

        # Calculate cumulative lap time based on the 60Hz sampling frequency (1/60 seconds between each sample)
        main_dataframe['Time'] = main_dataframe.groupby('Lap').cumcount() / 60

        # Calculate lap times by subtracting the first time value in each lap group from the last
        lap_times = main_dataframe.groupby('Lap')['Time'].max() - main_dataframe.groupby('Lap')['Time'].min()

        # Calculate total lap distance by taking the maximum distance value within each lap
        lap_distances = main_dataframe.groupby('Lap')['LapDist'].max()

        # Find max and avg speed per lap
        speed_max = main_dataframe.groupby('Lap')['Time'].max()
        speed_avg = main_dataframe.groupby('Lap')['Time'].mean()

        # Build dataframe with lap time and other lap info
        laps_dataframe = pd.DataFrame({
            'LapNum': lap_times.index,
            'LapTime': lap_times.values,
            'LapDistance': lap_distances.values,
            'SpeedMax': speed_max.values,
            'SpeedAvg': speed_avg.values,
        })

        # Replace missing data values (NaN) with 0
        laps_dataframe.fillna(0, inplace=True)

        # Find valid laps if laps are +/- 15% of best lap
        temp_laps_valid_1 = laps_dataframe['LapNum'].iloc[1:-1]  # Excluding the first and last lap
        temp_lap_times_valid_1 = laps_dataframe[laps_dataframe['LapNum'].isin(temp_laps_valid_1)]
        temp_lap_time_best_1 = temp_lap_times_valid_1['LapTime'].min()

        # Set upper/lower
        temp_lower_bound_1 = temp_lap_time_best_1 * 0.85
        temp_upper_bound_1 = temp_lap_time_best_1 * 1.15

        temp_laps_valid_2 = laps_dataframe[
            ((laps_dataframe['LapTime'] >= temp_lower_bound_1) & (laps_dataframe['LapTime'] <= temp_upper_bound_1))
            & (laps_dataframe.index > 0) # Exclude Lap 0 / out lap
        ]

        # Run it again to ensure actual best lap is captured, particularly for test sessions.
        temp_lap_times_valid_2 = laps_dataframe[laps_dataframe['LapNum'].isin(temp_laps_valid_2['LapNum'])]
        temp_lap_time_best_2 = temp_lap_times_valid_2['LapTime'].min()

        # Set upper/lower
        temp_lower_bound_2 = temp_lap_time_best_2 * 0.85
        temp_upper_bound_2 = temp_lap_time_best_2 * 1.15

        temp_laps_valid_2 = laps_dataframe[
            ((laps_dataframe['LapTime'] >= temp_lower_bound_2) & (laps_dataframe['LapTime'] <= temp_upper_bound_2))
            & (laps_dataframe.index > 0) # Exclude Lap 0 / out lap
        ]

        # Valid laps and lap times
        valid_laps = temp_laps_valid_2['LapNum']
        valid_lap_times = laps_dataframe[laps_dataframe['LapNum'].isin(valid_laps)]

        # Find best laps
        lap_nums_to_report = 2

        laps_best = valid_lap_times.nsmallest(lap_nums_to_report,"LapTime") # Fastest N laps
        lap_best = laps_best['LapNum'].iloc[0]
        lap_time_best = laps_best['LapTime'].iloc[0]

        # Find shortest/longest distance
        lap_distance_shortest = valid_lap_times['LapDistance'].min()

        # Find higest/lowest on both max and avg speed
        speed_max_highest = valid_lap_times['SpeedMax'].max()
        speed_avg_highest = valid_lap_times['SpeedAvg'].max()

        # Find delta to best lap
        laps_dataframe['DeltaToBestLap'] = laps_dataframe['LapTime'] - lap_time_best
        laps_dataframe['DeltaToBestLapPercent'] = ((laps_dataframe['LapTime'] - lap_time_best) / lap_time_best) * 100

        # Second run of replace missing data values (NaN) with 0
        laps_dataframe.fillna(0, inplace=True)

        """
        Set up laps report
        """
        laps_report = {
            'ValidLaps': valid_lap_times['LapNum'].values.tolist(),
            'TopLaps': valid_lap_times.nsmallest(lap_nums_to_report,"LapTime")['LapNum'].values.tolist(),
            'TopLapTimes': valid_lap_times.nsmallest(lap_nums_to_report,"LapTime")['LapTime'].values.tolist(),
            'TopLapDistances': valid_lap_times.nsmallest(lap_nums_to_report,"LapDistance")['LapDistance'].values.tolist(),
            'TopMaxSpeeds': valid_lap_times.nlargest(lap_nums_to_report,"SpeedMax")['SpeedMax'].values.tolist(),
            'TopAvgSpeeds': valid_lap_times.nlargest(lap_nums_to_report,"SpeedAvg")['SpeedAvg'].values.tolist(),
        }

        """
        Set up data for charts
        """
        charts_dict = {}

        # Reference lap
        lap_reference_dataframe = main_dataframe[main_dataframe['Lap'] == lap_best][main_dataframe.columns.tolist()]

        reference_lap = {
            'Latitude': lap_reference_dataframe['Lat'].values.tolist(),
            'Longitude': lap_reference_dataframe['Lon'].values.tolist(),
        }

        for lap in laps_best['LapNum'].values.tolist():
            chart_dataframe = main_dataframe[main_dataframe['Lap'] == lap][main_dataframe.columns.tolist()]

            lap_interpolated_speeds = np.interp(
                lap_reference_dataframe['LapDist'].values,
                chart_dataframe['LapDist'].values,
                chart_dataframe['Speed'].values,
            )

            lap_interpolated_laptimes = np.interp(
                lap_reference_dataframe['LapDist'].values,
                chart_dataframe['LapDist'].values,
                chart_dataframe['Time'].values,
            )

            delta_speeds = lap_interpolated_speeds - lap_reference_dataframe['Speed'].values
            delta_laptimes = lap_interpolated_laptimes - lap_reference_dataframe['Time'].values

            charts_dict[lap] = {
                'LapTime': chart_dataframe['Time'].values.tolist(),
                'Brake': chart_dataframe['Brake'].values.tolist(),
                'Throttle': chart_dataframe['Throttle'].values.tolist(),
                'Speed': chart_dataframe['Speed'].values.tolist(),
                'RPM': chart_dataframe['RPM'].values.tolist(),
                'Gear': chart_dataframe['Gear'].values.tolist(),
                'Distance': chart_dataframe['LapDist'].values.tolist(),
                'SpeedDelta': delta_speeds.tolist(),
                'LapTimeDelta': delta_laptimes.tolist(),
                #'DistanceRefLap': lap_reference_dataframe['LapDist'].values.tolist(),
                #'GPSLatitudeRefLap': lap_reference_dataframe['Lat'].values.tolist(),
                #'GPSLongitudeRefLap': lap_reference_dataframe['Lon'].values.tolist(),
            }

        return {
            'charts_data': charts_dict,
            'laps_data': laps_dataframe.to_dict(orient='records'),
            'laps_report_data': laps_report,
            'reference_lap_data': reference_lap,
            'z_dataframe': main_dataframe, # Internal use
        }
    except Exception as err:
        print(f"Error processing lap data: {err}")
        return []


# Lap Sectors
def process_sectors_data(static_data, session_data):
    """
    Set up data for sector lap times
    """
    sector_times_dict = {}

    valid_laps = session_data['laps_report_data']['ValidLaps']
    best_lap = valid_laps[0]

    # Use best lap as reference lap to set start/end sector positions
    ref_lap_distance = session_data['z_dataframe'][session_data['z_dataframe']['Lap'] == best_lap]['LapDist']

    # Duplicate dict to be used to set up start/end position values for each sector
    # without affecting the original dict/data
    ref_sectors = copy.deepcopy(static_data['SplitTimeInfo'])

    # Calculate start / end points for each sector based on reference lap distance
    for sector in ref_sectors['Sectors']:
        this_position = round(len(ref_lap_distance) * sector['SectorStartPct'])
        sector['StartPosition'] = ref_lap_distance.iloc[this_position] if this_position > 0 else 0
        sector['EndPosition'] = float('inf')

    for idx in range(len(ref_sectors['Sectors']) - 1):
        current_position = ref_sectors['Sectors'][idx]
        next_position = ref_sectors['Sectors'][idx + 1]
        current_position['EndPosition'] = next_position['StartPosition']

    try:
        for idx in range(len(session_data['laps_data'])):
            # Initialize list with 0 for diff() will be used for calculation
            this_sector_times = [0]

            # Drop the first row in case it starts from 0
            this_lap_dataframe = session_data['z_dataframe'][session_data['z_dataframe']['Lap'] == idx].iloc[1:]

            for sector in ref_sectors['Sectors']:
                # Check if distance value falls between sector start/end positions
                this_sector = this_lap_dataframe[(this_lap_dataframe['LapDist'] >= sector['StartPosition']) & (this_lap_dataframe['LapDist'] < sector['EndPosition'])]

                # Assign 0 if returns empty, else assign last lap time of the sector
                this_lap_time = this_sector['Time'].iloc[-1] if not this_sector.empty else 0

                # Append lap time to list
                this_sector_times.append(this_lap_time)

            # Use diff() to calculate difference between consecutive elements
            # Returns 1 less element
            sector_differences = np.diff(this_sector_times)

            # Convert back to list
            lap_sector_times = sector_differences.tolist()

            sector_times_dict[idx] = {
                'LapNum': session_data['laps_data'][idx]['LapNum'],
                'LapTime': session_data['laps_data'][idx]['LapTime'],
                'LapSectorTimes': lap_sector_times
            }

        # Initialize list with a position infinity value as placeholder
        # then multiplied by number of sectors to complete the list of placeholders
        best_sector_times = [float('inf')] * len(static_data['SplitTimeInfo']['Sectors'])

        for this_lap in sector_times_dict.values():
            if this_lap['LapNum'] in valid_laps:
                sector_times = this_lap['LapSectorTimes']
                for idx in range(len(static_data['SplitTimeInfo']['Sectors'])):
                    best_sector_times[idx] = min(best_sector_times[idx], sector_times[idx])

        theoretical_best_lap = sum(best_sector_times)
        estimated_lap_time = static_data['DriverInfo']['DriverCarEstLapTime']

        sectors_report = {
            'BestSectorTimes': best_sector_times,
            'TheoreticalBestLap': theoretical_best_lap,
            'EstimatedLapTime': estimated_lap_time,
        }
    except Exception as err:
        # Set to empty if error
        sector_times_dict = {}
        print(f"Error retrieving data: {err}")

    """
    Set up sector data for track map
    """
    first_key = next(iter(session_data['charts_data']))

    sector_percents = []
    sector_points = []
    sector_colors = []
    sector_lats = []
    sector_lons = []

    sectors_dict = {}

    colors = [
        'rgb(159, 226, 191)',
        'rgb(255, 127, 80)',
        'rgb(64, 224, 208)',
        'rgb(189, 183, 107)',
        'rgb(204, 204, 255)',
        'rgb(255, 191, 0)',
        'rgb(255, 182, 193)',
        'rgb(100, 149, 237)',
    ]

    try:
        # Gather all the sectors and the percentage values
        for sector in static_data['SplitTimeInfo']['Sectors']:
            sector_percents.append(sector['SectorStartPct'])

        # Find lat/lon estimates by multiplying the list length
        # and use that list position to retrieve the coordinates
        for percent in sector_percents:
            sector_points.append(round(len(session_data['reference_lap_data']['Latitude']) * percent))
            sector_colors.extend(colors)

            sector_lats.append(
                session_data['reference_lap_data']['Latitude']
                [round(len(session_data['reference_lap_data']['Latitude']) * percent)]
            )
            sector_lons.append(
                session_data['reference_lap_data']['Longitude']
                [round(len(session_data['reference_lap_data']['Longitude']) * percent)]
            )

        sectors_dict['Sectors'] = {
            'Percentages': sector_percents,
            'SectorPoints': sector_points,
            'SectorColors': sector_colors[:len(static_data['SplitTimeInfo']['Sectors'])],
            'Latitude': sector_lats,
            'Longitude': sector_lons,
        }

        return {
            'sectors_report_data': sectors_report,
            'sectors_data': sectors_dict,
            'sector_times_data': sector_times_dict,
        }
    except Exception as err:
        print(f"Error processing sector data: {err}")
        return []


"""
    Custom jinja2 filters
"""
@app.template_filter('laptimeformat')
def laptimeformat(seconds):
    mins = int(seconds // 60)
    secs = int(seconds % 60)
    millisecs = round((seconds % 1) * 1000)

    return f"{mins}:{secs:02d}.{millisecs:03d}"


@app.template_filter('to_km')
def to_km(meters):
    return round(meters / 1000, 5)


def round_filter(value, decimals=0):
    try:
        return round(value, decimals)
    except Exception as err:
        return value


"""
    Register filters with jinja2
"""
app.jinja_env.filters['round'] = round_filter


# ====================
if __name__ == "__main__":
    # Must run with the following argument on local machine
    # to distinguish local or remote server
    # ie: `python app.py --localhost`
    is_localhost = '--localhost' in sys.argv

    if is_localhost:
        os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
        app.run(debug=True, port=5001)
    else:
        app.run(host='0.0.0.0', port=5000)
