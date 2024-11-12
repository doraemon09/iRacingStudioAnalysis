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

                return render_template(
                    'display.html',
                    session_info=session_data,
                    telemetry_info=telemetry_data.to_dict(orient='records'),
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


# ====================
if __name__ == "__main__":
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    app.run(debug=True)
