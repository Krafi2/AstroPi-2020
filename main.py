from logzero import logger, logfile
from sense_hat import SenseHat
from ephem import readtle, degree
from datetime import datetime, timedelta
from time import sleep
import numpy
import random
from pathlib import Path
import csv
from math import sin, sqrt


def create_csv_file(data_file):
    """Create a new CSV file and add the header row"""
    with open(data_file, 'w') as f:
        writer = csv.writer(f)
        header = ("Date/time", "Magnetometer", "Gyroscope", "Accelerometer")
        writer.writerow(header)


def add_csv_data(data_file, data):
    """Add a row of data to the data_file CSV"""
    with open(data_file, 'a') as f:
        writer = csv.writer(f)
        writer.writerow(data)


def get_latlon(iss):
    """Return the current latitude and longitude, in degrees"""
    iss.compute()  # Get the lat/long values from ephem
    return (iss.sublat / degree, iss.sublong / degree)

def delta_t(t1, t2):
    return abs((t2 - t1).microseconds / 10**6)


def main():
    # This is the frequency at which we take measurments
    m_freq = 1.
    # The frequency at which we update the display
    d_freq = 1.
    # The cofficient applied to time when fading the image
    time_k = 1.
    # The acceleration in gs required to trigger the vibration warning
    vib_treshold = 0.1
    # Message to be displayed
    vib_message = "Please be careful. Thank you!"

    dir_path = Path(__file__).parent.resolve()

    # Set a logfile name
    logfile((dir_path / "kgang.log").resolve())

    data_file = dir_path / "data.csv"

    create_csv_file(data_file)

    sh = SenseHat()
    name = "ISS (ZARYA)"
    line1 = "1 25544U 98067A   21013.52860115  .00001434  00000-0  33837-4 0  9995"
    line2 = "2 25544  51.6460  27.6964 0000416 223.1682 273.8476 15.49286819264623"
    iss = readtle(name, line1, line2)

    red = [200, 0, 0]
    white = [200, 200, 200]
    blue = [0, 0, 200]
    
    flag = [
        blue, white, white, white, white, white, white, white,
        blue, blue,  white, white, white, white, white, white,
        blue, blue,  blue,  white, white, white, white, white,
        blue, blue,  blue,  blue,  white, white, white, white,
        blue, blue,  blue,  blue,  red,   red,   red,   red,
        blue, blue,  blue,  red,   red,   red,   red,   red,
        blue, blue,  red,   red,   red,   red,   red,   red,
        blue, red,   red,   red,   red,   red,   red,   red
    ]

    start_time = datetime.now()
    now_time = datetime.now()
    # Time of previous measurement
    prev_m = now_time
    # Time of previous display update
    prev_d = now_time
    
    while (now_time < start_time + timedelta(minutes=178)):
        # Update the display
        if delta_t(prev_d, now_time) > 1 / d_freq:
            prev_d = now_time
            image = [col * sin(time_k * now_time) for col in flag]
            sh.set_pixels(image)    
        
        # Take a measurment
        if delta_t(prev_m, now_time) > 1 / m_freq:
            prev_m = now_time

            magnetometer = sh.get_compass()
            accelerometer = sh.get_accelerometer()
            gyroscope = sh.get_gyroscope()

            # get latitude and longitude
            latitude, longitude = get_latlon(iss)

            # Save the data to the file
            data = (
                datetime.now(),
                magnetometer,
                accelerometer,
                gyroscope,
                latitude,
                longitude
            )
            print(data)
            add_csv_data(data_file, data)
        
        accel = sh.get_accelerometer_raw()
        magnitude = sqrt(accel["x"]**2 + accel["y"]**2 + accel["z"]**2)
        if magnitude > vib_treshold:
            sh.show_message(vib_message)

        # Update the current time
        now_time = datetime.now()
        try:
            pass
        except Exception as e:
            logger.error('{}: {})'.format(e.__class__.__name__, e))


if __name__ == "__main__":
    main()
