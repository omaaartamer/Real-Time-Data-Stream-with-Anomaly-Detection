# Real-Time Anomaly Detection in Data Streams

This project implements a real-time anomaly detection system using Python and Dash. It simulates a continuous data stream, detects anomalies using a rolling Z-Score method, and visualizes the data along with detected anomalies on a web interface. Detected anomalies are logged into a CSV file, and real-time alerts are displayed on the web page.

## Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Methodology](#methodology)
- [Customization](#customization)
- [Resources](#resources)
- [License](#license)
- [Contact](#contact)

## Features

- **Real-Time Data Simulation**: Generates a data stream with seasonal patterns, noise, and occasional anomalies.
- **Anomaly Detection**: Implements rolling Z-Score calculation to detect anomalies dynamically.
- **Web Visualization**: Uses Dash to display the data stream and anomalies in real-time on a web interface.
- **Alerts**: Provides real-time alerts on the web page when anomalies are detected.
- **Logging**: Saves detected anomalies into a CSV file for further analysis.

## Installation

### Prerequisites

- Python 3.x installed on your system.
- `pip` package manager.

### Required Libraries

Install the required packages using the following command:

```bash
pip install -r requirements.txt


# Methodology

### Data Stream Simulation

- **Seasonality**: Simulates a sinusoidal pattern to mimic periodic behavior.
- **Noise**: Adds Gaussian noise to the data to represent natural variations.
- **Anomalies**: Introduces anomalies randomly by adding significant deviations to some data points.

### Anomaly Detection Algorithm

- **Rolling Z-Score**:
  - Calculates the mean and standard deviation over a rolling window of recent data points.
  - Computes the Z-Score of the current data point.
  - Flags the point as an anomaly if the absolute Z-Score exceeds a predefined threshold.

### Real-Time Visualization

- **Dash Framework**: Provides a web interface to display the data stream and anomalies.
- **Plotly Graphs**: Visualizes the data using interactive line and scatter plots.
- **Alerts**: Displays messages on the web page when anomalies are detected.

# Customization

- **Threshold Adjustment**: You can adjust the `threshold` variable in the script to make the anomaly detection more or less sensitive.
- **Window Size**: Modify `window_size` to change the number of data points considered in the rolling calculations.
- **Update Interval**: Change the `interval` parameter in `dcc.Interval` to adjust how frequently the data stream updates.

# Resources

- **Dash Documentation**: [https://dash.plotly.com/](https://dash.plotly.com/)
- **Plotly Graph Objects**: [https://plotly.com/python/graph-objects/](https://plotly.com/python/graph-objects/)
- **Anomaly Detection Techniques**:
  - **Rolling Z-Score method**: Used for detecting anomalies in time-series data.
    - Reference: [Anomaly Detection in Time Series Data](https://www.sciencedirect.com/science/article/pii/S1877050917327852)
- **Python CSV Module**: [https://docs.python.org/3/library/csv.html](https://docs.python.org/3/library/csv.html)


### Customization

- **Threshold Adjustment**: You can adjust the `threshold` variable to make the anomaly detection more or less sensitive.
- **Window Size**: Modify `window_size` to change the number of data points considered in the rolling calculations.
- **Update Interval**: Change the `interval` parameter in `dcc.Interval` to adjust how frequently the data stream updates.

### Scalability

- For larger data streams or production environments, consider optimizing the code for performance.
- Integrate with real data sources by replacing the `generate_data_point()` function with actual data ingestion.

### Extending the Project

- **Notifications**: Implement email or SMS notifications when anomalies are detected.
- **Persistent Storage**: Use databases to store data streams and anomalies for long-term analysis.
- **Machine Learning Models**: Integrate advanced anomaly detection models for more complex data patterns.

# Contact

For any questions or suggestions, please contact:

**Omar Tamer**

Email: [omarthetamer@gmail.com](mailto:omarthetamer@gmail.com)
