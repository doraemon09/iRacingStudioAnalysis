from flask import Flask, render_template, request, redirect, url_for
import os
import irsdk


app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'


# Route for upload form
@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            return "No file uploaded!"

        # file
        file = request.files['file']

        if file.filename == '':
            return "No file selected!"

        if file:
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(filepath)

            # Process binary file and display result
            session_data = get_session_info(filepath)

            return render_template('display.html', session_info=session_data)

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
