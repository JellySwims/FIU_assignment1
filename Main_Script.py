#!/usr/bin/env python3

import os
import subprocess
import time
import signal
import sys

# Define the scripts and their paths
SCRIPTS = {
    'temp3.py': '/home/pi/Temperature/temp3.py',
    's3.py': '/home/pi/wind/s3.py',
    'w4.py': '/home/pi/wind/w5.py',
}

IMU_CALIBRATION_CMD = 'RTIMULibCal'
IMU_LOG_FILE = '/home/pi/log/imu_calibration.log'

LOG_DIR = '/home/pi/log'

# Create log directory if it does not exist
if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)

def start_script(script_name, script_path):
    """Start a script and return the process."""
    stdout_log = os.path.join(LOG_DIR, f"{script_name}_stdout.log")
    stderr_log = os.path.join(LOG_DIR, f"{script_name}_stderr.log")

    with open(stdout_log, 'w') as stdout_file, open(stderr_log, 'w') as stderr_file:
        print(f"Starting {script_name}...")
        process = subprocess.Popen(
            ['python3', script_path],
            stdout=stdout_file,
            stderr=stderr_file,
            bufsize=1,
            universal_newlines=True
        )
        return process

def start_imu_calibration():
    """Start the IMU calibration tool and handle interactive input."""    
    stdout_log = IMU_LOG_FILE
    print(f"Starting IMU calibration...")

    # Change directory to where the IMU calibration tool is located
    os.chdir('/home/pi/RTEllipsoidFit')

    # Start the calibration tool
    process = subprocess.Popen(
        [IMU_CALIBRATION_CMD],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        bufsize=1,
        universal_newlines=True
    )

    with open(stdout_log, 'w') as log_file:
        try:
            # Loop to process output
            while True:
                stdout_line = process.stdout.readline()
                stderr_line = process.stderr.readline()

                if stdout_line:
                    log_file.write(stdout_line)
                    log_file.flush()  # Ensure the output is written to the file immediately
                if stderr_line:
                    log_file.write(stderr_line)
                    log_file.flush()  # Ensure the output is written to the file immediately

                # Exit if no more output
                if process.poll() is not None and not stdout_line and not stderr_line:
                    break

        except KeyboardInterrupt:
            print("Keyboard interrupt detected. Exiting IMU calibration...")
            try:
                process.stdin.write('x\n')  # Send 'x' to exit
                process.stdin.flush()
                process.terminate()  # Try to terminate the process gracefully
                process.wait(timeout=10)  # Wait for the process to terminate
            except subprocess.TimeoutExpired:               
                process.kill()  # Force kill if not terminated gracefully
            finally:
                log_file.write("IMU calibration exited due to user interrupt.\n")
                log_file.flush()
                print("IMU calibration process terminated.")

    return process

def monitor_process(process, script_name):
    """Monitor the given process and handle interruptions."""
    stdout_log = os.path.join(LOG_DIR, f"{script_name}_stdout.log")
    stderr_log = os.path.join(LOG_DIR, f"{script_name}_stderr.log")

    with open(stdout_log, 'a') as stdout_file, open(stderr_log, 'a') as stderr_file:
        try:
            while process.poll() is None:
                stdout_line = process.stdout.readline()
                stderr_line = process.stderr.readline()

                if stdout_line:
                    stdout_file.write(stdout_line)
                    stdout_file.flush()  # Ensure the output is written to the file immediate>                
                if stderr_line:
                    stderr_file.write(stderr_line)
                    stderr_file.flush()  # Ensure the output is written to the file immediate>
                time.sleep(1)
        except Exception as e:
            print(f"Error monitoring {script_name}: {e}", file=sys.stderr)
            stderr_file.write(f"Monitoring error: {e}\n")

def stop_script(process):
    """Terminate a process."""
    if process:
        process.terminate()
        try:
            process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            process.kill()
        print(f"Process {process.pid} terminated.")

def main():
    processes = {}

    # Start each script and store the process
    for script_name, script_path in SCRIPTS.items():
        if os.path.isfile(script_path):
            process = start_script(script_name, script_path)
            processes[script_name] = process
        else:
            print(f"Script {script_path} does not exist.", file=sys.stderr)

    # Start the IMU calibration process
    imu_process = start_imu_calibration()

    # Handle termination and cleanup
    try:
        while True:
            time.sleep(10)
    except KeyboardInterrupt:
        print("Main script interrupted. Terminating all processes...")
        for script_name, process in processes.items():
            print(f"Stopping {script_name}...")
            stop_script(process)
        print("Stopping IMU calibration...")
        stop_script(imu_process)
        print("All processes terminated. Exiting...")
        sys.exit(0)

if __name__ == '__main__':
    main()
