#!/usr/bin/python

import random
import math
import time

counter = 1
with open('data1.csv', 'w') as file1, open('data2.csv', 'w') as file2, open('data3.csv', 'w') as file3:
    file1.write("time,altitude\n")
    file2.write("time,pressure\n")
    file3.write("time,temperature\n")

    # Update pressure calculation using the given formula
    R = 8.314  # Gas constant in J/(mol*K)
    g = 9.81  # Acceleration due to gravity in m/s^2
    M = 0.02897  # Molar mass of air in kg/mol
    h0 = 0  # Reference altitude in meters

    altitude = 1000
    speed = 10
    pressure_sea = 1013.25
    temperature = 10.134  # Initial temperature in Celsius

    while True:
        prev_alt = altitude
        altitude -= speed  # Linearly decreasing altitude
        if altitude <= 0:
            speed = 0
            altitude = 0
            break
        if altitude <= 800:
            speed = 3

        altitude_error = random.randint(-5, 5)  # Gaussian error for altitude (-5 to 5)
        altitude += altitude_error  # Add error to altitude
        distance_dropped = prev_alt - altitude

        temperature += 0.012166 * distance_dropped  # Linearly increase temperature by 0.033 degrees Celsius per unit decrease in altitude

        temperature_kelvin = temperature + 273.15  # Convert temperature to Kelvin

        pressure = pressure_sea * math.exp(-g * M * (altitude - h0) / (R * temperature_kelvin))

        pressure_error = random.randint(-5, 5)/3  # Gaussian error for pressure (-5 to 5)
        pressure += pressure_error  # Add error to pressure

        file1.write(f"{counter}, {altitude}\n")  # Append counter and altitude to data1.csv
        file2.write(f"{counter}, {pressure}\n")  # Append counter and pressure to data2.csv
        file3.write(f"{counter}, {temperature}\n")  # Append counter and temperature to data3.csv

        file1.flush()  # Flush the buffer to write data immediately
        file2.flush()
        file3.flush()

        counter += 1  # Increment counter by 1 for each iteration

        # Wait for 1 second before the next iteration
        time.sleep(1)
