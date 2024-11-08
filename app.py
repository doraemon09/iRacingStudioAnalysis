from flask import Flask, render_template, request, redirect, url_for
import os
import string
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
            processed_data = process_binary_file(filepath)
            return render_template('display.html', data=processed_data)

    return render_template('index.html')


# Function to process IBT / binary file
def process_binary_file(filepath):
    try:
        # Use IBT class for reading telemetry file
        ibt = irsdk.IBT()

        # Open uploaded file
        ibt.open(filepath)

        return ibt
    except Exception as err:
        return f"Error reading file: {err}"


if __name__ == "__main__":
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    app.run(debug=True)
