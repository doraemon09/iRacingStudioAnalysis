# iRacing Studio Analysis

A Flask-based web application designed to process, analyze, and display iRacing telemetry data. The application supports file uploads, telemetry processing, and detailed data visualizations, offering insights into laps, sectors, throttle/brake usage, and more.

## Features

- **Telemetry File Upload**: Accepts iRacing telemetry files (`.ibt`) for processing.
- **Data Visualization**: Provides detailed charts and graphs for lap performance, fuel usage, and more.
- **Sector Analysis**: Breaks down lap times by track sectors with theoretical best lap calculations.
- **Advanced Data Insights**:
  - Throttle, brake, and coast time analysis.
  - Fuel usage reports.
  - Reference lap data with comparisons.
  - Weather conditions and sensor data.
- **Database Integration**: Retrieves preprocessed telemetry data for demonstration purposes.
- **Custom Jinja2 Filters**: Formats lap times, converts distances, and more.

## Demo

A live demo of the application is available at **[http://13.52.127.109/](http://13.52.127.109/)**.  
The demo is hosted on an AWS EC2 instance (Free Tier).

## Installation

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/doraemon09/iRacingStudioAnalysis.git
   cd iRacingStudioAnalysis
   ```
2. **Set Up Virtual Environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. **Install Required Packages**: Install the following Python packages:
   ```bash
   pip install flask irsdk numpy pandas pyyaml sqlite3 werkzeug
   ```
4. **Run the Application**:
   - **Local Mode**:
     ```bash
     python app.py --localhost
     ```
   - **Production Mode**:
     ```bash
     python app.py
     ```

## Usage

1. **Upload Telemetry Files**:
   - Navigate to the root URL (`http://127.0.0.1:5001` for local mode).
   - Upload `.ibt` files for processing.

2. **Explore Data**:
   - View charts, reports, and telemetry details in the web interface.

3. **Demo Mode**:
   - In production, access preloaded demo data from the database.

## Contribution

1. Fork the repository.
2. Create a new branch (`git checkout -b feature-name`).
3. Commit your changes (`git commit -m "Description"`).
4. Push to your branch (`git push origin feature-name`).
5. Submit a pull request.

## Acknowledgments

- This project utilizes the [pyirsdk library](https://github.com/kutu/pyirsdk) to access iRacing telemetry data. Special thanks to the contributors of `pyirsdk` for making this integration possible and enabling efficient telemetry processing.
- Built with [Flask](https://flask.palletsprojects.com/).
- Utilizes libraries like `pandas`, `numpy`, `sqlite3`, and `irsdk`.

## License

This project is licensed under the **Apache License 2.0**. See the `LICENSE` file for details.
