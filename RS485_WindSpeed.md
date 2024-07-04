import serial
import time
import sys
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')
logger = logging.getLogger(__name__)

def open_serial_port(port='/dev/ttyUSB0', baudrate=9600, timeout=1):
    try:
        ser = serial.Serial(
            port=port,
            baudrate=baudrate,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            bytesize=serial.EIGHTBITS,
            timeout=timeout
        )
        logger.info(f'Serial port {port} opened successfully')
        return ser
    except serial.SerialException as e:
        logger.error(f"Failed to open serial port {port}: {e}")
        sys.exit(1)  # Exit the script if serial port opening fails

def read_wind_direction(ser):
    try:
        ser.write(b'DIR\r\n')  # Example command to get wind direction, adjust as per your sensor's protocol
        time.sleep(0.1)        # Wait for stable response time
        response = ser.readline().decode().strip()
        return response
    except serial.SerialException as e:
        logger.error(f"Serial communication error: {e}")
        return None

if __name__ == '__main__':
    ser = open_serial_port()  # Open the serial port
    try:
        while True:
            direction = read_wind_direction(ser)
            if direction:
                print(f"Wind direction: {direction}")
            time.sleep(1)  # Adjust as needed for your application
    except KeyboardInterrupt:
        logger.info("Exiting due to keyboard interrupt...")
    finally:
        if ser:
            ser.close()  # Close the serial port when done
            logger.info("Serial port closed.")
