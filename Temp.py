#!/usr/bin/env python3
import os
import time

# Define a mapping of sensor IDs to descriptive names
SENSOR_LABELS = {
    '28-fd6fb00a6461': 'Temperature Sensor 1 (Air)',
    '28-b613bc0a6461': 'Temperature Sensor 2 (Ocean Surface)',
    '28-7896b10a6461': 'Temperature Sensor 3 (1 Meter Below Sea Level)',
}

def get_sensors():
    # List all devices in the 1-Wire bus and filter for DS18B20 sensors
    sensors = [i for i in os.listdir('/sys/bus/w1/devices') if i.startswith('28-')]
    if not sensors:
        raise RuntimeError("No DS18B20 sensors found")
    return sensors

def read_temperature(sensor_id):
    # Read temperature data from the DS18B20 sensor
    location = f'/sys/bus/w1/devices/{sensor_id}/w1_slave'
    with open(location) as tfile:
        text = tfile.read()
    secondline = text.split("\n")[1]
    temperaturedata = secondline.split(" ")[9]
    temperature = float(temperaturedata[2:])
    celsius = temperature / 1000
    fahrenheit = (celsius * 1.8) + 32
    return celsius, fahrenheit

def loop():
    # Continuously read and print the temperature from all sensors
    while True:
        sensors = get_sensors()
        for sensor_id in sensors:
            celsius, fahrenheit = read_temperature(sensor_id)
            # Get the descriptive label for the sensor
            label = SENSOR_LABELS.get(sensor_id, f"Unknown Sensor ({sensor_id})")
            print(f"{label} - Current temperature: {celsius:0.3f} C")
            print(f"{label} - Current temperature: {fahrenheit:0.3f} F")
        print("-" * 40)  # Separator line for readability
        time.sleep(1)  # Wait for 1 second before reading again

def cleanup():
    # Placeholder for any cleanup code if needed
    pass

if __name__ == '__main__':
    try:
        loop()
    except KeyboardInterrupt:
        cleanup()
        print("Program terminated by user")
