import RPi.GPIO as GPIO
import time
import csv
from prefect import flow, get_run_logger
from datetime import datetime
from prefect.task_runners import SequentialTaskRunner

# read with GPIO.input(channel)
# write with GPIO.output(channel, state)

### Watering Schedule ###
### 11:45PM - 12:15AM
### 2:45AM - 3:15AM
### 5:45AM - 6:15AM
### 8:45AM - 9:15AM
### 11:45AM - 12:15PM
### 2:45PM - 3:15 PM
### 5:45PM - 6:15PM
### 8:45PM - 9:15PM
    

WATER_PUMP = 16
LIGHTS = 18
DATA_PATH = '/home/admin/grow-happy/data.csv'


@task
def get_current_state(reason):
    """
    In this function I want to READ all sensors and return their values as a dict
    [datetime, state_water, state_lights, water_conductivity, humidity, temperature, reason]
    """
    datetime = datetime.now()
    state_water = GPIO.input(16)
    state_lights = GPIO.input(18)
    current_ec = Null
    current_humidity = Null
    current_temperature = Null
    reason = reason

    return [datetime, state_water, state_lights, current_ec, current_humidity, current_temperature]


@task
def write_data(data):
    with open(DATA_PATH, 'a') as fd:
        writer = csv.writer(fd)
        writer.wrierow(data)


@flow(task_runner=SequentialTaskRunner)
def log_flow():
    """
    This flow is meant to capture the state of all sensors present and record them
    """
    temp = get_current_state("logging")
    write_data(temp)

 
@flow(task_runner=SequentialTaskRunner)
def water_flow(action):
    """
    This is the main flow that controls the watering of the plants. 
    We want to water for half an hour, every 3 hours.
    """
    logger = get_run_logger()

    # 1(HIGH) is off, 0(LOW) is on
    if action = 'on':
        logger.info("Water is off...Let's get it flowing")
        try:
            GPIO.output(16, GPIO.LOW)
            temp = get_current_state("Turned water on")
            write_data(temp)
    elif action = 'off':
        logger.info("Water is flowing...Turing off")
        try:
            GPIO.output(16, GPIO.HIGH)
            temp = get_current_state("Turned water off")
            write_data(temp)
    else:
        logger.warning(f"UNEXPECTED VALUE ON PIN 16 - {action}")


@flow(task_runner=SequentialTaskRunner)
def main_flow():
    param = Parameter("run-type", default='log')

    if param == 'log':
        log_flow()
    elif param == 'flow-off':
        water_flow('off')
    elif param == 'flow-on':
        water_flow('on')
    

if __name__ == "__main__":
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(16, GPIO.OUT)
    GPIO.setup(18, GPIO.OUT)

    main_flow()

    water_flow(GPIO.input(16))
