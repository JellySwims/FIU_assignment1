import time
from pymodbus.client import ModbusSerialClient
from pymodbus.exceptions import ModbusException

# Configuration
SERIAL_PORT = '/dev/ttyUSB0'  # Replace with your USB to RS485 port
BAUD_RATE = 9600
PARITY = 'N'
STOP_BITS = 1
DATA_BITS = 8
SLAVE_ADDRESS = 0x02
UPDATE_INTERVAL = 2  # Interval in seconds between updates

# Create Modbus client
client = ModbusSerialClient(
    method='rtu',
    port=SERIAL_PORT,
    baudrate=BAUD_RATE,
    parity=PARITY,
    stopbits=STOP_BITS,
    bytesize=DATA_BITS
)

# Wind direction mapping dictionary
wind_direction_mapping = {
    0: "South",               # Was North
    1: "South-southwest",     # Was North-northeast
    2: "Southwest",           # Was Northeast
    3: "West-southwest",      # Was East-northeast
    4: "West",                # Was East
    5: "West-northwest",      # Was East-southeast
    6: "Northwest",           # Was Southeast
    7: "North-northwest",     # Was South-southeast
    8: "North",               # Was South
    9: "North-northeast",     # Was South-southwest
    10: "Northeast",          # Was Southwest
    11: "East-northeast",     # Was West-southwest
    12: "East",               # Was West
    13: "East-southeast",     # Was West-northwest
    14: "Southeast",          # Was Northwest
    15: "South-southeast",    # Was North-northwest
    16: "South"               # Was North
 }

def convert_degrees_to_direction(degrees):
    """Convert degrees to wind direction based on ranges."""
    if degrees > 348.75 or degrees <= 11.25:
        return "South"
    elif degrees <= 33.75:
        return "South-southwest"
    elif degrees <= 56.25:
        return "Southwest"
    elif degrees <= 78.75:
        return "West-southwest"
    elif degrees <= 101.25:
        return "West"
    elif degrees <= 123.75:
        return "West-northwest"
    elif degrees <= 146.25:
        return "Northwest"
    elif degrees <= 168.75:
        return "North-northwest"
    elif degrees <= 191.25:
        return "North"
    elif degrees <= 213.75:
        return "North-northeast"
    elif degrees <= 236.25:
        return "Northeast"
    elif degrees <= 258.75:
        return "East-northeast"
    elif degrees <= 281.25:
        return "East"
    elif degrees <= 303.75:
        return "East-southeast"
    elif degrees <= 348.75:
        return "Southeast"
    else:
        return "Unknown"

def read_wind_direction():
    """Read the wind direction (360 degrees) from the sensor."""
    try:
        response = client.read_holding_registers(0x0000, 1, unit=SLAVE_ADDRESS)
        if response.isError():
                print("Error reading wind direction:", response)
        else:
            # Unpack the response
            register_value = response.registers[0]
            wind_direction = register_value / 10.0
            direction = convert_degrees_to_direction(wind_direction)
            print(f"Wind Direction: {wind_direction:.1f} degrees ({direction})")
    except ModbusException as e:
        print("Modbus exception occurred:", e)

def read_16_wind_directions():
    """Read the 16 wind directions from the sensor."""
    try:
        response = client.read_holding_registers(0x0001, 1, unit=SLAVE_ADDRESS)
        if response.isError():
            print("Error reading 16 wind directions:", response)
        else:
            # Unpack the response
            register_value = response.registers[0]
            print(f"16 Wind Directions Value: {register_value}")

            # Use the wind direction mapping dictionary
            direction = wind_direction_mapping.get(register_value, "Unknown")
            print(f"Wind Direction (16-way): {direction}")
    except ModbusException as e:
        print("Modbus exception occurred:", e)

def main():
    try:
        # Connect to the Modbus server
        client.connect()

        while True:
            # Read wind direction
            read_wind_direction()

            # Read 16 wind directions
            read_16_wind_directions()

            # Wait for the next update
            time.sleep(UPDATE_INTERVAL)