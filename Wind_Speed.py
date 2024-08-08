import time
import binascii
from pymodbus.client import ModbusSerialClient

# Configuration for Modbus and RS485
SERIAL_PORT = '/dev/ttyUSB0'  # Adjust as per your USB-to-RS485 adapter
BAUD_RATE = 9600
PARITY = 'N'
STOP_BITS = 1
DATA_BITS = 8

# Modbus client setup
client = ModbusSerialClient(
    method='rtu',
    port=SERIAL_PORT,
    baudrate=BAUD_RATE,
    parity=PARITY,
    stopbits=STOP_BITS,
    bytesize=DATA_BITS
)

# Helper function to convert hexadecimal to integer
def hex_to_int(hex_str):
    return int(hex_str, 16)

# Read wind speed from the sensor
def read_wind_speed():
    try:
        if not client.connect():
            raise ConnectionError("Unable to connect to the Modbus client")

        # Read wind speed
        request = client.read_holding_registers(0x0000, 1, unit=0x02)

        if request and request.registers:
            wind_speed_hex = binascii.hexlify(request.registers[0].to_bytes(2, byteorder='big')).>            wind_speed_value = hex_to_int(wind_speed_hex) / 10.0
            return wind_speed_value
        else:
            return None

    except Exception as e:
           print(f"Error reading wind speed: {e}")
        return None

# Read air level from the sensor
def read_air_level():
    try:
        if not client.connect():
            raise ConnectionError("Unable to connect to the Modbus client")

        # Read air level
        request = client.read_holding_registers(0x0001, 1, unit=0x02)

        if request and request.registers:
            air_level_hex = binascii.hexlify(request.registers[0].to_bytes(2, byteorder='big')).d>            air_level_value = hex_to_int(air_level_hex)
            positions = [
                "N", "North by Northeast", "N/E", "East by Northeast", "E", "East by Southeast",
                "S/E", "South by Southeast", "S", "South by Southwest", "S/W", "South by Southwes>                "W", "West by Northwest", "N/W", "North by Northwest"
            ]
            return positions[air_level_value]
        else:
            return None

    except Exception as e:
        print(f"Error reading air level: {e}")
        return None

if __name__ == "__main__":
    try:
        while True:
            wind_speed = read_wind_speed()
            air_level = read_air_level()

            # Print results
            if wind_speed is not None:
                print(f"Wind Speed: {wind_speed:.1f} m/s")
            else:
                print("Failed to read wind speed")

            if air_level is not None:
                print(f"Air Level: {air_level}")
            else:
                print("Failed to read air level")

            # Wait for 4 seconds before the next reading
            time.sleep(4)

    except KeyboardInterrupt:
        print("Interrupted by user. Exiting...")
    finally:
        client.close()
