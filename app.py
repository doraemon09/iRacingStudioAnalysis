from flask import Flask, render_template, request, redirect, url_for
import werkzeug.utils
import os
import yaml
import pandas as pd
import numpy as np
import irsdk


# Initialize Flash app
app = Flask(__name__)

# Set upload and demo file folders
app.config['UPLOAD_FOLDER'] = 'uploads'
DEMO_FILES_DIR = 'static/demo_files'

# Load YAML with utf-8 encoding for Japanese characters
with open('config/parameters.yaml', 'r', encoding='utf-8') as yaml_file:
    yaml_data = yaml.safe_load(yaml_file)

# Set allowed file extensions
ALLOWED_FILE_EXTENSIONS = {'ibt'}


# Check for file extension on uploaded file
def allowed_file(filename):
    if '.' not in filename:
        return False
    return filename.rsplit('.', 1)[1].lower() in ALLOWED_FILE_EXTENSIONS


# Route for upload form
@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # demo / upload flags
        is_demo_file = 0
        is_upload_file = 0

        # Check if demo file was used
        demofile = request.form.get('demofile')

        if demofile:
            is_demo_file = 1
            is_upload_file = 0

            # Assign to file variables
            this_file_name = demofile
            this_folder_path = DEMO_FILES_DIR

        if not is_demo_file:
            is_demo_file = 0
            is_upload_file = 1

            # Process upload file
            if 'uploadfile' not in request.files:
                return "No file uploaded!"

            # Assign to file variable
            this_file_name = request.files['uploadfile'].filename
            this_folder_path = app.config['UPLOAD_FOLDER']

        if allowed_file(this_file_name):
            # Clean up file name
            this_file_name = werkzeug.utils.secure_filename(this_file_name)

            # Set file path
            this_file_path = os.path.join(this_folder_path, this_file_name)

            try:
                if is_upload_file:
                    request.files['uploadfile'].save(this_file_path)

                # Session Info | gets obj
                session_data = get_session_data(this_file_path)

                # Telemetry Info | gets dataframe
                telemetry_data = get_telemetry_data(this_file_path)

                # Process selected lap related data | gets dictionary
                lap_data = process_lap_data(telemetry_data)

                # Split sector data
                sector_data = process_sector_data(session_data, lap_data)

                return render_template(
                    'display.html',
                    session_info=session_data,
                    # telemetry_info=telemetry_data.to_dict(orient='records'),
                    lap_info=lap_data['lap_data'],
                    chart_info=lap_data['chart_data'],
                    split_sector_info=sector_data['split_sector_data'],
                    split_time_info=sector_data['split_time_data'],
                    yaml_info=yaml_data,
                )
            except Exception as err:
                return f"Error processing file: {err}"
        else:
            return "Invalid file extension. iRacing telemetry (.ibt) file only!"
    """
        Else
    """
    # Grab demo files folder content
    demo_files = os.listdir(DEMO_FILES_DIR)

    # Manual flag
    # is_localhost = request.remote_addr == '127.0.0.1'
    is_localhost = 1

    return render_template(
        'index.html',
        is_localhost=is_localhost,
        demo_files=demo_files,
        yaml_info=yaml_data,
    )


# Retrieve session info, ie: Weather and Car Set up
def get_session_data(filepath):
    try:
        # Use IRSDK class for session info
        ibt_session_data = irsdk.IRSDK()

        # Read uploaded file
        ibt_session_data.startup(test_file=filepath)

        return ibt_session_data
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
def process_lap_data(ibt_telemetry_data):
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
        lap_dataframe = pd.DataFrame({
            'LapNum': lap_times.index,
            'LapTime': lap_times.values,
            'LapDistance': lap_distances.values,
            'SpeedMax': speed_max.values,
            'SpeedAvg': speed_avg.values,
        })

        # Replace missing data values (NaN) with 0
        lap_dataframe.fillna(0, inplace=True)

        # Exclude the first and last laps for best lap calculation
        laps_valid = lap_dataframe['LapNum'].iloc[1:-1]  # Excluding the first and last lap
        lap_times_valid = lap_dataframe[lap_dataframe['LapNum'].isin(laps_valid)]

        # Find best/worst lap
        lap_best = lap_times_valid['LapTime'].idxmin()
        lap_worst = lap_times_valid['LapTime'].idxmax()

        lap_time_best = lap_times_valid['LapTime'].min()
        lap_time_worst = lap_times_valid['LapTime'].max()

        # Find shortest/longest distance
        lap_distance_shortest = lap_times_valid['LapDistance'].min()
        lap_distance_longest = lap_times_valid['LapDistance'].max()

        # Find higest/lowest on both max and avg speed
        speed_max_highest = lap_times_valid['SpeedMax'].max()
        speed_max_lowest = lap_times_valid['SpeedMax'].min()
        speed_avg_highest = lap_times_valid['SpeedAvg'].max()
        speed_avg_lowest = lap_times_valid['SpeedAvg'].min()

        # Find delta to best lap
        lap_dataframe['DeltaToBestLap'] = lap_dataframe['LapTime'] - lap_time_best
        lap_dataframe['DeltaToBestLapPercent'] = ((lap_dataframe['LapTime'] - lap_time_best) / lap_time_best) * 100

        # Returns 0/1
        lap_dataframe['IsBestLap'] = lap_dataframe['LapTime'].apply(lambda x: 1 if x == lap_time_best else 0)
        lap_dataframe['IsWorstLap'] = lap_dataframe['LapTime'].apply(lambda x: 1 if x == lap_time_worst else 0)
        lap_dataframe['IsBestLapDist'] = lap_dataframe['LapDistance'].apply(lambda x: 1 if x == lap_distance_shortest else 0)
        lap_dataframe['IsWorstLapDist'] = lap_dataframe['LapDistance'].apply(lambda x: 1 if x == lap_distance_longest else 0)
        lap_dataframe['IsBestMaxSpeed'] = lap_dataframe['SpeedMax'].apply(lambda x: 1 if x == speed_max_highest else 0)
        lap_dataframe['IsWorstMaxSpeed'] = lap_dataframe['SpeedMax'].apply(lambda x: 1 if x == speed_max_lowest else 0)
        lap_dataframe['IsBestAvgSpeed'] = lap_dataframe['SpeedAvg'].apply(lambda x: 1 if x == speed_avg_highest else 0)
        lap_dataframe['IsWorstAvgSpeed'] = lap_dataframe['SpeedAvg'].apply(lambda x: 1 if x == speed_avg_lowest else 0)

        # Second run of replace missing data values (NaN) with 0
        lap_dataframe.fillna(0, inplace=True)

        """
        Set up data for charts
        """
        chart_dict = {}

        # Reference lap
        lap_reference_dataframe = main_dataframe[main_dataframe['Lap'] == lap_best][main_dataframe.columns.tolist()]

        for lap in main_dataframe['Lap'].unique():
            if lap == lap_time_best or lap == 0 or lap == main_dataframe['Lap'].max():
               continue # Skipping best + first + last lap
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

            chart_dict[lap] = {
                'LapTime': chart_dataframe['Time'].values.tolist(),
                'Brake': chart_dataframe['Brake'].values.tolist(),
                'Throttle': chart_dataframe['Throttle'].values.tolist(),
                'Speed': chart_dataframe['Speed'].values.tolist(),
                'RPM': chart_dataframe['RPM'].values.tolist(),
                'Gear': chart_dataframe['Gear'].values.tolist(),
                'Distance': chart_dataframe['LapDist'].values.tolist(),
                'SpeedDelta': delta_speeds.tolist(),
                'LapTimeDelta': delta_laptimes.tolist(),
                'LapBest': lap_best.tolist(), # Single value
                'LapWorst': lap_worst.tolist(), # Single value
                'DistanceRefLap': lap_reference_dataframe['LapDist'].values.tolist(),
                'GPSLatitudeRefLap': lap_reference_dataframe['Lat'].values.tolist(),
                'GPSLongitudeRefLap': lap_reference_dataframe['Lon'].values.tolist(),
            }

        return {
            'lap_data': lap_dataframe.to_dict(orient='records'),
            'chart_data': chart_dict,
        }
    except Exception as err:
        print(f"Error processing telemetry info: {err}")
        return []


# Lap Sectors
def process_sector_data(session, lap):
    """
    Set up data for sector/split lap times
    """
    split_time_dict = {}

    for idx in range(len(lap['lap_data'])):
        try:
            # Inline loop to calculate the split time
            lap_sector_times = [
                lap['lap_data'][idx]['LapTime'] * info['SectorStartPct']
                for info in session['SplitTimeInfo']['Sectors']
            ]

            split_time_dict[idx] = {
                'LapNum': lap['lap_data'][idx]['LapNum'],
                'LapTime': lap['lap_data'][idx]['LapTime'],
                'LapSectorTimes': lap_sector_times
            }
        except Exception as err:
            # Set to empty if error
            split_time_dict = {}
            print(f"Error retrieving data: {err}")

    """
    Set up sector data for track map
    """
    split_sector_percents = []
    split_sector_points = []
    split_sector_colors = []
    split_sector_lats = []
    split_sector_lons = []

    split_sector_dict = {}

    colors = [
        'rgb(159, 226, 191)', 'rgb(255, 127, 80)',
        'rgb(64, 224, 208)', 'rgb(189, 183, 107)',
        'rgb(204, 204, 255)', 'rgb(255, 191, 0)',
        'rgb(255, 182, 193)', 'rgb(100, 149, 237)',
    ]

    # Gather all the sectors and the percentage values
    for sector in session['SplitTimeInfo']['Sectors']:
        split_sector_percents.append(sector['SectorStartPct'])

    # Find lat/lon estimates by multiplying the list length
    # and use that list position to retrieve the coordinates
    for percent in split_sector_percents:
        split_sector_points.append(round(len(lap['chart_data'][1]['GPSLatitudeRefLap']) * percent))
        split_sector_colors.extend(colors)

        split_sector_lats.append(
            lap['chart_data'][1]['GPSLatitudeRefLap']
            [round(len(lap['chart_data'][1]['GPSLatitudeRefLap']) * percent)]
        )
        split_sector_lons.append(
            lap['chart_data'][1]['GPSLongitudeRefLap']
            [round(len(lap['chart_data'][1]['GPSLongitudeRefLap']) * percent)]
        )

    split_sector_dict['SplitSectors'] = {
        # 'SectorNum': len(split_sector_percents),
        'Percentages': split_sector_percents,
        'SectorPoints': split_sector_points,
        'SectorColors': split_sector_colors,
        'Latitude': split_sector_lats,
        'Longitude': split_sector_lons,
    }

    return {
        'split_time_data': split_time_dict,
        'split_sector_data': split_sector_dict,
    }


"""
    Custom jinja2 filters
"""
@app.template_filter('timeformat')
def timeformat(seconds):
    mins = int(seconds // 60)
    secs = int(seconds % 60)
    millisecs = round((seconds % 1) * 1000)

    return f"{mins}:{secs:02d}.{millisecs:03d}"


@app.template_filter('to_km')
def to_km(meters):
    return round(meters / 1000, 5)


def round_filter(value, decimals=2):
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
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    app.run(debug=True)
    # app.run(host='0.0.0.0', port=5000)
