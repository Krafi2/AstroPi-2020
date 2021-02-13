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
    """This function returns the time delta in between two datetimes seconds as a float"""
    delta = abs(t2 - t1)
    delta = delta.seconds + delta.microseconds / 10**6
    return delta


def main():
    # This is the frequency at which we take measurments
    m_freq = 20.
    # The frequency at which we update the display
    d_freq = 20.
    # The cofficient applied to time when fading the image
    time_k = 1.
    # The low bound of the color multiplier
    color_l_bound = 0.5
    # The acceleration in gs required to trigger the vibration warning
    vib_treshold = 1.1
    # Message to be displayed
    vib_message = "Please be careful. Thank you!"

    dir_path = Path(__file__).parent.resolve()

    # Set a logfile name
    logfile(dir_path / "kgang.log")

    data_file = dir_path / "data.csv"

    create_csv_file(data_file)

    sh = SenseHat()
    name = "ISS (ZARYA)"
    line1 = "1 25544U 98067A   21013.52860115  .00001434  00000-0  33837-4 0  9995"
    line2 = "2 25544  51.6460  27.6964 0000416 223.1682 273.8476 15.49286819264623"
    iss = readtle(name, line1, line2)

    red = [100, 0, 0]
    white = [100, 100, 100]
    blue = [0, 0, 100]
    yellow = [100, 100, 0]
    black = [0, 0, 0]
    
    """This is a flag of the Czech Republic, which will be displayed by the computer when everything is running correctly.
    In order to communicate that the program isn't stalling, the picture will fade using a sin function."""
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
    

    """This is an image of an angry emoji, which will be displayed when the accelerometr detects acceleration above vib_treshold.
     We used an emoji instead of text, because the execution stalled while displaying text, which interrupted our measurements."""
    angry = [
        yellow, yellow, yellow, yellow, yellow, yellow, yellow, yellow,
        yellow, yellow, black,  yellow, yellow, black,  yellow, yellow,
        yellow, yellow, yellow, yellow, yellow, yellow, yellow, yellow,
        yellow, yellow, yellow, yellow, yellow, yellow, yellow, yellow,
        yellow, yellow, yellow, black,  black,  yellow, yellow, yellow,
        yellow, yellow, black,  yellow, yellow, black,  yellow, yellow,
        yellow, black,  yellow, yellow, yellow, yellow, black,  yellow,
        yellow, yellow, yellow, yellow, yellow, yellow, yellow, yellow
    ]
    

    start_time = datetime.now()
    now_time = start_time
    # Time of previous measurement
    prev_m = now_time
    # Time of previous display update
    prev_d = now_time
    # The program will run for 178 minutes
    while (now_time < start_time + timedelta(minutes=178)):
        try:
            # We're using this function to make screen brighter and darker over time, at some point the disply will turn off and after a few seconds it'll turn on again
            if delta_t(prev_d, now_time) > (1 / d_freq):
                prev_d = now_time
                image = [[int(col * (color_l_bound + (1 - color_l_bound) * (0.5 + 0.5 * sin(time_k * (now_time.second + now_time.microsecond / 10**6))))) for col in rgb] for rgb in flag]
                sh.set_pixels(image)
            
            # Take a measurment
            if delta_t(prev_m, now_time) > (1 / m_freq):
                prev_m = now_time
                # define data, we need raw compass and accelerometer
                magnetometer = sh.get_compass_raw()
                accelerometer = sh.get_accelerometer_raw()
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
                add_csv_data(data_file, data)
            
            # if magnitude is over some level, the display will show angry face
            magnitude = sqrt(accelerometer["x"]**2 + accelerometer["y"]**2 + accelerometer["z"]**2)
            if magnitude > vib_treshold:
                sh.set_pixels(angry)
                # sh.show_message(vib_message)

            # Update the current time
            now_time = datetime.now()
        except Exception as e:
            logger.error('{}: {})'.format(e.__class__.__name__, e))


if __name__ == "__main__":
    main()
