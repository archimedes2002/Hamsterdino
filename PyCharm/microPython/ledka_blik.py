import machine
from time import sleep

led = machine.Pin(19, machine.Pin.OUT)

while True:
    led.value(1)
    sleep(3)
    led.value(0)
    sleep(3)