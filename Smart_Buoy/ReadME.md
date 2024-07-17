Here we have a collection of scripts working in unison to create a smart buoy for FIU. The intended sensors for this project include wind RS485 (speed/ direction), IMU (raspberry hat), 3 temperature sensors (air, surface, 1m depth), a pyranometer, and possibly a gps location. 


Hardware
The Sense HAT features an 8x8 RGB LED matrix, a mini joystick and the following sensors:

	Gyroscope
	Accelerometer
	Magnetometer
	Temperature
	Humidity
	Barometric pressure


Documentation
Comprehensive documentation is available at https://sense-hat.readthedocs.io/en/latest/.

Installation

		RTIMULib
  
This is the actual RTIMULib library source. Custom apps only need to include this library.

Linux
This directory contains the embedded Linux demo apps (for Raspberry Pi and Intel Edison) and also the Python interface to RTIMULib.

RTHost
RTHost contains the two apps, RTHost and RTHostGL, that can be used by desktops that don't have direct connection to an IMU (as they don't have I2C or SPI interfaces). An Arduino running RTArduLinkIMU from the RTIMULib-Arduino repo provides the hardware interface and a USB cable provides the connection between the desktop and the Arduino.

		RTEllipsoidFit
  
This contains Octave code used by the ellipsiod fit data generation in RTIMULibCal, RTIMULibDemo, RTIMULibDemoGL, RTHostIMU and RTHostIMUGL. It's important that a copy of this directory is at the same level, or the one above, the app's working directory or ellipsoid fit data generation will fail.
git clone https://github.com/RPi-Distro/RTIMULib.git

In order to work correctly, the Sense HAT requires an up-to-date kernel, I2C to be enabled, and a few libraries to get started.
Ensure your APT package list is up-to-date:

   $ sudo apt update
   
Next, install the sense-hat package, which will ensure the kernel is up to date, enable I2C, and install the necessary libraries and programs:

    $ sudo apt install sense-hat
    
Finally, a reboot may be required if I2C was disabled or the kernel was not up-to-date prior to the install:

    $ sudo reboot
    
Getting started

After installation, example code can be found under /usr/src/sense-hat/examples.

The calibration program displays the following menu:

Options are:

  m - calibrate magnetometer with min/max
  e - calibrate magnetometer with ellipsoid (do min/max first)
  a - calibrate accelerometers
  x - exit

Enter option:
Press lowercase m. The following message will then show. Press any key to start.

    Magnetometer min/max calibration
    --------------------------------
    Waggle the IMU chip around, ensuring that all six axes
    (+x, -x, +y, -y and +z, -z) go through their extrema.
    When all extrema have been achieved, enter 's' to save, 'r' to reset
    or 'x' to abort and discard the data.

    Press any key to start...
After it starts, you should see output similar to the following scrolling up the screen:


 Min x:  51.60  min y:  69.39  min z:  65.91
 Max x:  53.15  max y:  70.97  max z:  67.97

Further reading
You can find more information on how to use the Sense HAT in the Raspberry Pi Press book Experiment with the Sense HAT. Written by The Raspberry Pi Foundation’s Education Team, it is part of the MagPi Essentials series published by Raspberry Pi Press. The book covers the background of the Astro Pi project, and walks you through how to make use of all the Sense HAT features using the Python library.


