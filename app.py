from flask import Flask, render_template, request, redirect, url_for
import werkzeug.utils
import os
import irsdk


# Initialize Flash app
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'


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

                # Process ibt file and display result
                session_data = get_session_info(filepath)

                return render_template('display.html', session_info=session_data)
            except Exception as err:
                return f"Error processing file: {err}"
        else:
            return "Invalid file extension. iRacing telemetry (.ibt) file only!"

    return render_template('index.html')


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


if __name__ == "__main__":
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    app.run(debug=True)
