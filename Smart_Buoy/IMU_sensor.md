import board
import busio
import time
import adafruit_lsm9ds1

try:
    i2c = board.I2C()
    sensor = adafruit_lsm9ds1.LSM9DS1_I2C(i2c)
except Exception as e:
    print(f"Error initializing sensor: {e}")
    exit(1)

try:
    while True:
        try:
            accel_x, accel_y, accel_z = sensor.acceleration
            mag_x, mag_y, mag_z = sensor.magnetic
            gyro_x, gyro_y, gyro_z = sensor.gyro
            temp = sensor.temperature
        except (ValueError, AttributeError) as e:
            print(f"Error reading sensor data: {e}")
            continue
        
        print("Acceleration (m/s^2): ({0:0.3f}, {1:0.3f}, {2:0.3f})".format(accel_x, accel_y, accel_z))
        print("Magnetometer (gauss): ({0:0.3f}, {1:0.3f}, {2:0.3f})".format(mag_x, mag_y, mag_z))
        print("Gyroscope (dps): ({0:0.3f}, {1:0.3f}, {2:0.3f})".format(gyro_x, gyro_y, gyro_z))
        print("Temperature: {0:0.3f}C".format(temp))
        time.sleep(1.0)

except KeyboardInterrupt:
    print("\nExiting gracefully...")
finally:
    # Clean up resources, if necessary
    pass

    
