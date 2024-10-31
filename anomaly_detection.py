# anomaly_detection.py

import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import numpy as np
import os
import csv

# Initialize the Dash app
app = dash.Dash(__name__)
app.title = "Real-Time Data Stream with Anomaly Detection and Alerts"

# File to log anomalies
ANOMALY_LOG_FILE = "anomalies.csv"

# Remove existing anomaly log file if it exists
if os.path.exists(ANOMALY_LOG_FILE):
    os.remove(ANOMALY_LOG_FILE)


def log_anomaly_to_csv(time_step, value):
    """
    Logs detected anomaly to a CSV file.

    Parameters:
    - time_step (int): The time step at which the anomaly was detected.
    - value (float): The anomalous data value.
    """
    file_exists = os.path.isfile(ANOMALY_LOG_FILE)
    with open(ANOMALY_LOG_FILE, mode='a', newline='') as file:
        writer = csv.writer(file)
        if not file_exists:
            # Write header if file does not exist
            writer.writerow(["Time Step", "Anomaly Value"])
        writer.writerow([time_step, value])


# Global variables for data
data_stream = []  # List of tuples (time_step, value)
data_stream_viz = []
anomalies = []    # List of tuples (time_step, value)
detected_anomalies_vals = []  # list of values to exclude from data stream window
window_size = 20
threshold = 3.0
time_step = 0     # Initialize time step


def generate_data_point():
    """
    Simulates a new data point with seasonal and random noise.

    Returns:
    - value (float): The simulated data value.
    """
    base_pattern = np.sin(np.linspace(0, 2 * np.pi, 5))
    value = np.random.choice(base_pattern) + np.random.normal(0, 0.1)
    # print(base_pattern)
    # print(value)

    # Introduce anomalies with a 5% probability
    if np.random.rand() < 0.05:
        if np.random.rand() > 0.5:
            value += np.random.normal(9, 0.5)
        else:
            value -= np.random.normal(9, 0.5)
    return value


def detect_anomaly(value, data_window):
    """
    Detects if the current value is an anomaly based on a rolling Z-Score.

    Parameters:
    - value (float): The current data point to analyze.
    - data_window (list): List of recent data points (tuples of time_step and value).

    Returns:
    - bool: True if an anomaly is detected, False otherwise.
    """
    if len(data_window) < 2:
        return False  # Not enough data to calculate statistics
    # Extract only the values from the data_window
    values = [v for _, v in data_window if v not in detected_anomalies_vals]
    mean = np.mean(values)
    std_dev = np.std(values)
    # Calculate the Z-Score
    z_score = (value - mean) / std_dev
    return abs(z_score) > threshold


# Define the layout of the app
app.layout = html.Div([
    html.H1("Real-Time Data Stream with Anomaly Detection"),
    html.Div(id='anomaly-alert', style={'color': 'red', 'fontWeight': 'bold'}),
    dcc.Graph(id='live-graph', config={'displayModeBar': False}),
    # Interval component to update the graph periodically
    dcc.Interval(id='interval-component', interval=500,
                 n_intervals=0)  # Update every 500ms
])

# Callback function to update the graph and anomaly alert


@app.callback(
    [Output('live-graph', 'figure'), Output('anomaly-alert', 'children')],
    [Input('interval-component', 'n_intervals')]
)
def update_graph(n):
    """
    Updates the graph and anomaly alert message.

    Parameters:
    - n (int): Number of intervals that have passed (not used directly).

    Returns:
    - figure (dict): The updated figure for the graph.
    - alert_message (str): The alert message to display.
    """
    global data_stream, anomalies, detected_anomalies_vals, time_step, data_stream_viz

    # Generate new data point and increment time step
    new_value = generate_data_point()
    time_step += 1
    data_stream.append((time_step, new_value))
    data_stream_viz.append((time_step, new_value))

    # Maintain a fixed window size for the data stream
    if len(data_stream) > window_size:
        data_stream.pop(0)  # Remove the oldest data point

    # Detect anomalies using the rolling window
    alert_message = ""
    if detect_anomaly(new_value, data_stream[-window_size:]):
        anomalies.append((time_step, new_value))
        detected_anomalies_vals.append(new_value)
        alert_message = f"Anomaly detected at time step {time_step}!"
        # Log the anomaly to the CSV file
        log_anomaly_to_csv(time_step, new_value)

    # Prepare data for plotting
    times = [t for t, _ in data_stream_viz]
    values = [v for _, v in data_stream_viz]
    anomaly_times = [t for t, _ in anomalies]
    anomaly_values = [v for _, v in anomalies]

    # Create the data traces for the graph
    trace_data = go.Scatter(
        x=times,
        y=values,
        mode='lines+markers',
        name='Data Stream'
    )
    trace_anomalies = go.Scatter(
        x=anomaly_times,
        y=anomaly_values,
        mode='markers',
        marker=dict(color='red', size=10),
        name='Anomalies'
    )

    # Define the layout of the graph
    layout = go.Layout(
        xaxis=dict(range=[max(0, time_step - 100), time_step + 1]),
        yaxis=dict(range=[min(values) - 1, max(values) + 1]),
        title='Real-Time Data Stream with Anomaly Detection',
    )

    # Return the updated figure and alert message
    return {'data': [trace_data, trace_anomalies], 'layout': layout}, alert_message


# Run the app
if __name__ == '__main__':
    try:
        app.run_server(debug=False, dev_tools_ui=False,
                       dev_tools_props_check=False)
    except:
        pass
