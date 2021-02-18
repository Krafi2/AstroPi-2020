from logzero import logger, logfile
from sense_hat import SenseHat
from ephem import readtle, degree
from datetime import datetime, timedelta
from pathlib import Path
import csv
from math import sin, sqrt


def create_csv_file(data_file):
    """Create a new CSV file and add the header row"""
    with open(data_file, 'w') as f:
        writer = csv.writer(f)
        header = ("Date/time", "Magnetometer", "Accelerometer", "Gyroscope", "Latitide", "Longitude")
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

def apply_fade(image, t, time_k, l_bound):
    """This function multiplies the colours of the image by sin(time_k * t) with a low bound
    to achieve a periodic fading effect."""
    k = (l_bound + (1 - l_bound) * (0.5 + 0.5 * sin(time_k * (t.second + t.microsecond / 10**6))))
    return [[int(col * k) for col in rgb] for rgb in image]

def main():
    # This is the frequency at which we take measurments
    m_freq = 20.
    # The frequency at which we update the display
    d_freq = 10.
    # The cofficient applied to time when fading the image
    time_k = 1.
    # The low bound of the color multiplier
    color_l_bound = 0.4
    # The acceleration in gs required to trigger the vibration warning
    # TODO change this to space a compatible value before sending off the program
    vib_treshold = 1.1
    # This message is displayed when acceleration exceeds vib_treshold
    vib_message = "Please be careful. Thank you!"
    # Message duration in seconds
    m_duration = 10.
    # Colour of the message text
    m_colour = [100, 100, 100]
    # Path to program root
    dir_path = Path(__file__).parent.resolve()

    # Setup the logfile
    logfile(dir_path / "kgang.log")
    # File for data collection
    data_file = dir_path / "data.csv"

    create_csv_file(data_file)

    # Initialize state
    sh = SenseHat()
    name = "ISS (ZARYA)"
    line1 = "1 25544U 98067A   21013.52860115  .00001434  00000-0  33837-4 0  9995"
    line2 = "2 25544  51.6460  27.6964 0000416 223.1682 273.8476 15.49286819264623"
    iss = readtle(name, line1, line2)

    # Define colours
    red = [100, 0, 0]
    white = [100, 100, 100]
    blue = [0, 0, 100]

    # TODO remove this as this has become irrelevant
    # yellow = [100, 100, 0]
    # black = [0, 0, 0]
    
    """This is a flag of the Czech Republic, which will be displayed by the computer when everything is running correctly.
    In order to communicate that the program isn't stalling, the picture will fade using the sin function."""
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
    
    # TODO remove this as this has become irrelevant
    # """This is an image of an angry emoji, which will be displayed when the accelerometr detects acceleration above vib_treshold.
    # In the project proposal we said that we would display a text message, however we have found that program execution stalls while
    # displaying text, which interrupts our measurments."""
    # angry = [
    #     yellow, yellow, yellow, yellow, yellow, yellow, yellow, yellow,
    #     yellow, yellow, black,  yellow, yellow, black,  yellow, yellow,
    #     yellow, yellow, yellow, yellow, yellow, yellow, yellow, yellow,
    #     yellow, yellow, yellow, yellow, yellow, yellow, yellow, yellow,
    #     yellow, yellow, yellow, black,  black,  yellow, yellow, yellow,
    #     yellow, yellow, black,  yellow, yellow, black,  yellow, yellow,
    #     yellow, black,  yellow, yellow, yellow, yellow, black,  yellow,
    #     yellow, yellow, yellow, yellow, yellow, yellow, yellow, yellow
    # ]
    

    start_time = datetime.now()
    now_time = start_time
    # Time of previous measurement
    prev_m = now_time
    # Time of previous display update
    prev_d = now_time
    # The time at which we've started playing the message or None if no message is playing
    m_start = None

    # The program will run for 178 minutes
    # The loop does things in this order:
    #   - First, we check whether to display a vibration warning.
    #   - Then we check whether the display should be updated. There are two display modes.
    #       - If a message is currently playing, it checks what letter to display and displays it.
    #         We do this in such a convoluted way instead of using the `show_message` function on the sensehat,
    #         because this functions stalls execution and so we can't take measurments while displaying text
    #         if we use this function.
    #       - If no message is currently playing, we fade the flag image to communicate that the program hasn't crashed.
    #   - Lastly, we check whether we should take a measurment, and if the time is right, we do just that.
    while (now_time < start_time + timedelta(minutes=178)):
        try:
            # Update the current time
            now_time = datetime.now()
            
            # Compute the acceleration. If the measured acceleration is larger than vib_treshold, we display a warning message.
            accelerometer = sh.get_accelerometer_raw()
            accel = sqrt(accelerometer["x"]**2 + accelerometer["y"]**2 + accelerometer["z"]**2)
            if accel > vib_treshold:
                m_start = now_time
                logger.warning("Detected acceleration above treshold.")

            # This condition checks whether it's time to update the display.
            if delta_t(prev_d, now_time) > (1 / d_freq):
                prev_d = now_time
                # No point in checking the delta time if we aren't even playing a message
                if m_start is not None:
                    message_t = delta_t(now_time, m_start)
                    # Check if we've overshot already
                    if message_t >= m_duration:
                        # Stop playing the message. The display will be updated to display the image.
                        m_start = None
                    else:
                        # Compute what letter we should be displaying
                        idx = int(message_t / m_duration * len(vib_message))
                        letter = vib_message[idx]
                        sh.show_letter(letter, text_colour = m_colour)

                # Display the 'all ok' image
                if m_start is None:
                    image = apply_fade(flag, now_time, time_k, color_l_bound)
                    sh.set_pixels(image)
            
            # This condition checks whether it's time to take a measurment.
            if delta_t(prev_m, now_time) > (1 / m_freq):
                prev_m = now_time
                # Here we collect sensor data. It seems that the non raw variants of the sensor
                # functions all return orientation of the computer, so we use the raw variants
                magnetometer = sh.get_compass_raw()
                accelerometer = sh.get_accelerometer_raw()
                gyroscope = sh.get_gyroscope()

                # Get latitude and longitude just in case we need it
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

        except Exception as e:
            logger.error('{}: {})'.format(e.__class__.__name__, e))

    # Hopefully we haven't crashed :D
    sh.clear()
    logger.info("I haven't crashed!")

if __name__ == "__main__":
    main()
