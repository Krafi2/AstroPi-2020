import csv
import datetime
import numpy as np

"""
This class stores the recorded flight data.
It contains fields `time`, `mag`, `acc`, `orientation`, and `pos`.
date/time, mag_x, mag_y, mag_z, acc_x, acc_y, acc_z, pitch, roll, yaw, latitude, longitude
"""
class Data:
    def __init__(self, file: str):
        with open(file) as f:
            self.time = []
            self.mag = []
            self.acc = []
            self.orientation = [] 
            self.pos = []

            reader = csv.DictReader(f)
            for line in reader:
                self.time.append(datetime.datetime.strptime(line["date/time"], '%Y-%m-%d %H:%M:%S.%f'))
                self.mag.append(np.array([line["mag_x"], line["mag_y"], line["mag_z"]]))
                self.acc.append(np.array([line["acc_x"], line["acc_y"], line["acc_z"]]))
                self.acc.append(np.array([line["pitch"], line["roll"],  line["yaw"]]))
                self.acc.append(np.array([line["latitude"], line["longitude"]]))

