import requests
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from datetime import datetime
import threading
import time

# Replace this URL with your ESP32 temperature endpoint
URL = "http://esp32.local/temperature1?unit=celsius"  # Change to your actual endpoint

# Lists to store the time and temperature data
time_data = []
temperature_data = []

# Lock to safely update shared data from multiple threads
data_lock = threading.Lock()

# Function to get temperature data from the server
def get_temperature():
    try:
        response = requests.get(URL, timeout=5)  # Make GET request to the temperature endpoint
        response.raise_for_status()  # Raise an exception for HTTP errors
        temperature = float(response.text.split()[0])  # Assuming the response is "XX.XX °C" or "XX.XX °F"
        return temperature
    except requests.exceptions.RequestException as e:
        print(f"Error fetching temperature: {e}")
        return None

# Function to fetch temperature data every 1 second
def fetch_data():
    while True:
        temperature = get_temperature()
        if temperature is not None:
            current_time = datetime.now().strftime('%H:%M:%S')
            with data_lock:
                time_data.append(current_time)
                temperature_data.append(temperature)
            print(f"Fetched: {temperature} at {current_time}")
        time.sleep(1)  # Fetch data every 1 second

# Function to update the plot
def update_plot(frame):
    with data_lock:
        # Keep the plot with the last 20 data points
        time_data_to_plot = time_data[-20:]
        temperature_data_to_plot = temperature_data[-20:]

    ax.clear()
    ax.plot(time_data_to_plot, temperature_data_to_plot, marker='o', color='b', linestyle='-')
    ax.set_title('Live Temperature Data')
    ax.set_xlabel('Time')
    ax.set_ylabel('Temperature (°C)')
    plt.xticks(rotation=45, ha='right')

# Start the data fetching thread
data_thread = threading.Thread(target=fetch_data, daemon=True)
data_thread.start()

# Create the plot
fig, ax = plt.subplots()
ani = animation.FuncAnimation(fig, update_plot, interval=250)  # Plot update every 1 second

plt.tight_layout()
plt.show()
