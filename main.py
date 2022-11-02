import RPi.GPIO as GPIO
import time
from prefect import flow, get_run_logger
from prefect.task_runners import SequentialTaskRunner

WATER_PUMP = 16
LIGHTS = 18


 
@flow(task_runner=SequentialTaskRunner)
def water_flow():
    logger = get_run_logger()

    
    

    

    # 1 is off, 0 is on
    # read with GPIO.input(channel)
    # write with GPIO.output(channel, state)





    print(f'GPIO.input(16) - {GPIO.input(16)}')
    GPIO.output(16, GPIO.LOW) 
    print(f'GPIO.input(16) - {GPIO.input(16)}')
    time.sleep(1)
    GPIO.output(16, GPIO.HIGH) 

if __name__ == "__main__":
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BOARD)

    GPIO.setup(16, GPIO.OUT)
    GPIO.setup(18, GPIO.OUT)

    water_flow()
