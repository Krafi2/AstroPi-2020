from logzero import logger, logfile
from sense_hat import SenseHat
from ephem import readtle, degree
from datetime import datetime, timedelta
from time import sleep
import numpy
import random
from pathlib import Path
import csv



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

def get_latlon():
    """Return the current latitude and longitude, in degrees"""
    iss.compute() # Get the lat/long values from ephem
    return (iss.sublat / degree, iss.sublong / degree)


def main():
    dir_path = Path(__file__).parent.resolve()

    # Set a logfile name
    logfile(dir_path/"kgang.log")

    data_file = dir_path/"data.csv"

    create_csv_file(data_file)

    start_time = datetime.now()
    now_time = datetime.now()
    sh = SenseHat()
    name = "ISS (ZARYA)"
    line1 = "1 25544U 98067A   21013.52860115  .00001434  00000-0  33837-4 0  9995"
    line2 = "2 25544  51.6460  27.6964 0000416 223.1682 273.8476 15.49286819264623"
    iss = readtle(name, line1, line2)
    
    red = [200, 0, 0]
    white = [200, 200, 200]
    blue = [0, 0, 200]
    black = [0, 0, 0]
    yellow = [200, 200, 0]
    
    flag = [
    blue, white, white, white, white, white, white, white,
    blue, blue, white, white, white, white, white, white,
    blue, blue, blue, white, white, white, white, white,
    blue, blue, blue, blue, white, white, white, white,
    blue, blue, blue, blue, red, red, red, red,
    blue, blue, blue, red, red, red, red, red,
    blue, blue, red, red, red, red, red, red,
    blue, red, red, red, red, red, red, red
    ]
    
    smile = [
    yellow, yellow, yellow, yellow, yellow, yellow, yellow, yellow,
    yellow, yellow, black, yellow, yellow, black, yellow, yellow,
    yellow, yellow, yellow, yellow, yellow, yellow, yellow, yellow,
    yellow, yellow, yellow, yellow, yellow, yellow, yellow, yellow,
    yellow, black, yellow, yellow, yellow, yellow, black, yellow,
    yellow, yellow, black, yellow, yellow, black, yellow, yellow,
    yellow, yellow, yellow, black, black, yellow, yellow, yellow,
    yellow, yellow, yellow, yellow, yellow, yellow, yellow, yellow
    ]


    while (now_time < start_time + timedelta(minutes=178)):
        try:
            magnetometer = sh.get_compass()
            accelerometer = sh.get_accelerometer()
            gyroscope = sh.get_gyroscope()
    
  
            # get latitude and longitude
            latitude, longitude = get_latlon()
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
            # update the current time
            now_time = datetime.now()
        except Exception as e:
            logger.error('{}: {})'.format(e.__class__.__name__, e))

if __name__ == "__main__":
    main()
