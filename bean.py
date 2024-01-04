import streamlit as st
import time
import random
import serial

# Global variable for the power data
power_data = []

# Function to simulate power measurements
def generate_power_data():
    return random.randint(50, 100)

# Function to get current configuration from serial
def get_configuration_from_serial():
    # Replace the following line with your logic to read the configuration from the serial port
    # For now, let's assume the device sends back a string in the format "Timeout:X,Power:Y"
    response_str = ser.readline().decode().strip()
    
    # Extract timeout and power values from the response
    timeout_str, power_str = response_str.split(',')
    timeout_value = int(timeout_str.split(':')[1])
    power_value = int(power_str.split(':')[1])
    
    return timeout_value, power_value

# UI Layout
st.title("Power Measurement Dashboard")

# Placeholder for live graph
graph_placeholder = st.line_chart({"Power": power_data})

# Configuration section
st.sidebar.title("Configuration")
timeout_options = [1, 2, 3]
power_options = [50, 75, 100]

# Timeout configuration
timeout = st.sidebar.selectbox("Timeout (minutes)", timeout_options)

# Power configuration
power = st.sidebar.selectbox("Power (%)", power_options)

# Set and Get buttons arranged horizontally
col1, col2 = st.sidebar.columns(2)
set_button = col1.button("Set Configuration")
get_button = col2.button("Get Configuration")

# Placeholder for configuration feedback
config_feedback = st.sidebar.empty()

# Serial communication setup
ser = serial.Serial("COM3", 9600, timeout=1)

# Function to update the live graph
def update_graph():
    global power_data
    while True:
        time.sleep(1)
        power_measurement = generate_power_data()
        power_data.append(power_measurement)
        if len(power_data) > 10:
            power_data = power_data[-10:]
        graph_placeholder.line_chart({"Power": power_data})
        if st.session_state.stop_update:
            break

# Start the live graph update in the main thread
if "stop_update" not in st.session_state:
    st.session_state.stop_update = False

if not st.session_state.stop_update:
    update_graph()

# Handle Set Configuration button click
if set_button:
    # Perform set configuration logic here
    config_feedback.success(f"Configuration set - Timeout: {timeout} minutes, Power: {power}%")

    # Send configuration over serial
    config_str = f"Timeout:{timeout},Power:{power}"
    ser.write(config_str.encode())

# Handle Get Configuration button click
if get_button:
    # Perform get configuration logic here
    current_timeout, current_power = get_configuration_from_serial()
    config_feedback.info(f"Current Configuration - Timeout: {current_timeout} minutes, Power: {current_power}%")

# Close the serial connection
ser.close()