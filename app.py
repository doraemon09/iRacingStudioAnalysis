from flask import Flask, render_template, request, redirect, url_for
import werkzeug.utils
import os
import yaml
import pandas as pd
import irsdk


# Initialize Flash app
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'

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
        if 'file' not in request.files:
            return "No file uploaded!"

        # Assign to file variable
        file = request.files['file']

        if file.filename == '':
            return "No file selected!"

        if file and allowed_file(file.filename):
            # Clean up file name
            file.filename = werkzeug.utils.secure_filename(file.filename)

            filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)

            try:
                file.save(filepath)

                # Session Info | gets obj
                session_data = get_session_info(filepath)

                # Telemetry Info | gets dataframe
                telemetry_data = get_telemetry_info(filepath)

                # Process selected lap related data | gets dataframe
                lap_data = process_lap_info(telemetry_data)

                return render_template(
                    'display.html',
                    session_info=session_data,
                    telemetry_info=telemetry_data.to_dict(orient='records'),
                    lap_info=lap_data.to_dict(orient='records'),
                    yaml_info=yaml_data,
                )
            except Exception as err:
                return f"Error processing file: {err}"
        else:
            return "Invalid file extension. iRacing telemetry (.ibt) file only!"
    # Else
    return render_template('index.html', yaml_info=yaml_data)


# Retrieve session info, ie: Weather and Car Set up
def get_session_info(filepath):
    try:
        # Use IRSDK class for session info
        ibt_session_info = irsdk.IRSDK()

        # Read uploaded file
        ibt_session_info.startup(test_file=filepath)

        return ibt_session_info
    except Exception as err:
        return f"Error reading file: {err}"


# Retrieve telemetry info, ie: Lap time and Throttle
def get_telemetry_info(filepath):
    try:
        # Use IBT class for telemetry info
        ibt_telemetry_info = irsdk.IBT()

        # Read uploaded file
        ibt_telemetry_info.open(filepath)

        # Store data into a dataframe
        telemetry_info = process_ibt_telemetry_info(ibt_telemetry_info)

        return telemetry_info
    except Exception as err:
        return f"Error reading file: {err}"


# Process telemetry data into dataframe
def process_ibt_telemetry_info(ibt_telemetry_info):
    try:
        # Initialize new dictionary
        telemetry_dict = {}

        # Loop header with get_all() to retrieve data (list)
        for header in ibt_telemetry_info.var_headers_names:
            try:
                # Assigned retrieved data set
                telemetry_dict[header] = ibt_telemetry_info.get_all(header)
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
def process_lap_info(ibt_telemetry_info):
    try:
        fields_to_process = ['Lap', 'LapDist', 'Speed']

        lap_dict = {}

        for header in fields_to_process:
            try:
                # Assigned retrieved data set
                lap_dict[header] = ibt_telemetry_info[header]
            except Exception as err:
                # Set to empty if header is not found in ibt_telemetry_info
                # Which should not happen to begine with
                lap_dict[header] = []
                print(f"Error retrieving data for {header}: {err}")

        # Create dataframe with lap_dict
        lap_dataframe = pd.DataFrame(lap_dict)

        # Calculate time based on the 60Hz sampling frequency (1/60 seconds between each sample)
        lap_dataframe['Time'] = lap_dataframe.groupby('Lap').cumcount() / 60

        # Calculate lap times by subtracting the first time value in each lap group from the last
        lap_times = lap_dataframe.groupby('Lap')['Time'].max() - lap_dataframe.groupby('Lap')['Time'].min()

        speed_max = lap_dataframe.groupby('Lap')['Time'].max()
        speed_avg = lap_dataframe.groupby('Lap')['Time'].mean()

        # Calculate total lap distance by taking the maximum distance value within each lap
        lap_distances = lap_dataframe.groupby('Lap')['LapDist'].max()

        # Build dataframe with lap time and other lap info
        lap_data = pd.DataFrame({
            'Lap': lap_times.index,
            'LapTime': lap_times.values,
            'LapDist': lap_distances.values,
            'SpeedMax': speed_max.values,
            'SpeedAvg': speed_avg.values,
        })

        # Replace missing data values (NaN) with 0
        lap_data.fillna(0, inplace=True)

        # Exclude the first and last laps for best lap calculation
        laps_to_consider = lap_data['Lap'].iloc[1:-1]  # Excluding the first and last lap
        lap_times_considered = lap_data[lap_data['Lap'].isin(laps_to_consider)]

        # Find best/worst lap
        lap_time_best = lap_times_considered['LapTime'].min()
        lap_time_worst = lap_times_considered['LapTime'].max()

        # Find shortest/longest distance
        lap_distance_shortest = lap_times_considered['LapDist'].min()
        lap_distance_longest = lap_times_considered['LapDist'].max()

        # Find higest/lowest on both max and avg speed
        speed_max_highest = lap_times_considered['SpeedMax'].max()
        speed_max_lowest = lap_times_considered['SpeedMax'].min()
        speed_avg_highest = lap_times_considered['SpeedAvg'].max()
        speed_avg_lowest = lap_times_considered['SpeedAvg'].min()

        # Returns 0/1
        lap_data['IsBestLap'] = lap_data['LapTime'].apply(lambda x: 1 if x == lap_time_best else 0)
        lap_data['IsWorstLap'] = lap_data['LapTime'].apply(lambda x: 1 if x == lap_time_worst else 0)
        lap_data['IsShortestLapDist'] = lap_data['LapDist'].apply(lambda x: 1 if x == lap_distance_shortest else 0)
        lap_data['IsLongestLapDist'] = lap_data['LapDist'].apply(lambda x: 1 if x == lap_distance_longest else 0)
        lap_data['IsBestMaxSpeed'] = lap_data['SpeedMax'].apply(lambda x: 1 if x == speed_max_highest else 0)
        lap_data['IsWorstMaxSpeed'] = lap_data['SpeedMax'].apply(lambda x: 1 if x == speed_max_lowest else 0)
        lap_data['IsBestAvgSpeed'] = lap_data['SpeedAvg'].apply(lambda x: 1 if x == speed_avg_highest else 0)
        lap_data['IsWorstAvgSpeed'] = lap_data['SpeedAvg'].apply(lambda x: 1 if x == speed_avg_lowest else 0)

        # Find delta to best lap
        lap_data['DeltaToBestLap'] = lap_data['LapTime'] - lap_time_best
        lap_data['DeltaToBestLapPercent'] = ((lap_data['LapTime'] - lap_time_best) / lap_time_best) * 100

        # Second run of replace missing data values (NaN) with 0
        lap_data.fillna(0, inplace=True)

        return lap_data
    except Exception as err:
        print(f"Error processing telemetry info: {err}")
        return []


# Custom jinja2 filter
@app.template_filter('timeformat')
def timeformat(seconds):
    mins = int(seconds // 60)
    secs = seconds % 60

    return f"{mins}:{secs:05.3f}"


# Custom jinja2 filter
@app.template_filter('to_km')
def to_km(meters):
    return round(meters / 1000, 5)


# Custom jinja2 filter
def round_filter(value, decimals=2):
    try:
        return round(value, decimals)
    except Exception as err:
        return value


# Register filter with jinja2
app.jinja_env.filters['round'] = round_filter


# ====================
if __name__ == "__main__":
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    app.run(debug=True)
