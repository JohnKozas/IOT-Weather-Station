from __future__ import print_function
import sys
import os
import time
import datetime
import BlynkLib
import smbus
import psycopg2
from DFRobot_BME280 import *

sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

# Replace these values with your actual Blynk Auth Token and database credentials
BLYNK_AUTH = ''

# Database parameters to connect, the host ip must be the local ip of the
# pc that runs the docker container with postgres database
db_params = {
    'host': "192.168.x.x",
    'database': "postgres",
    'user': "postgres",
    'password': "1234"
}

sensor = DFRobot_BME280_I2C(i2c_addr=0x77, bus=1)
bus = smbus.SMBus(1)  # Rev 2 Pi uses 1

blynk = BlynkLib.Blynk(BLYNK_AUTH)

# Constants for sensor configurations
DEVICE = 0x23
ONE_TIME_HIGH_RES_MODE_1 = 0x20

# Global variable to store the value from V4
v4_value = 0

def setup():
    while not sensor.begin():
        print('Please check that the device is properly connected')
        time.sleep(3)
    print("Sensor initialized successfully!!!")

    sensor.set_config_filter(BME280_IIR_FILTER_SETTINGS[0])
    sensor.set_config_T_standby(BME280_CONFIG_STANDBY_TIME_125)
    sensor.set_ctrl_meas_sampling_temp(BME280_TEMP_OSR_SETTINGS[3])
    sensor.set_ctrl_meas_sampling_press(BME280_PRESS_OSR_SETTINGS[3])
    sensor.set_ctrl_sampling_humi(BME280_HUMI_OSR_SETTINGS[3])
    sensor.set_ctrl_meas_mode(NORMAL_MODE)

    time.sleep(2)  # Wait for configuration to complete

def convert_to_number(data):
    result = (data[1] + (256 * data[0])) / 1.2
    return result

def read_light(addr=DEVICE):
    data = bus.read_i2c_block_data(addr, ONE_TIME_HIGH_RES_MODE_1)
    return convert_to_number(data)

def loop():
    if sensor.get_data_ready_status:
        temperature = round(sensor.get_temperature, 1)
        pressure = round(sensor.get_pressure, 1)
        humidity = round(sensor.get_humidity, 1)
        light_level = read_light()

        # Blynk communication
        blynk.run()
        blynk.virtual_write(0, temperature)
        blynk.virtual_write(1, humidity)
        blynk.virtual_write(2, pressure)
        blynk.virtual_write(3, light_level)

        # PostgreSQL database communication
        conn = psycopg2.connect(**db_params)
        cursor = conn.cursor()
        cursor.execute("UPDATE weatherproject SET temperature = %s, humidity = %s, pressure = %s, light = %s WHERE id = 1", (temperature, humidity, pressure, light_level))
        conn.commit()

        # Display information
        print("Light Level: {:.2f} lx".format(light_level))
        print('{}C {}Pa {}%'.format(temperature, pressure, humidity))
        time.sleep(60)

if __name__ == "__main__":
    setup()
    while True:
        loop()
