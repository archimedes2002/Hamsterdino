# This file is executed on every boot (including wake-boot from deepsleep)
#import esp
#esp.osdebug(None)
#import webrepl
#webrepl.start()
#import ledka_blik

import machine
import os

# výpis základních informací
print("Booting ESP32...")
print("Filesystem obsahuje:", os.listdir())

# (Volitelně) můžeš sem dát inicializaci sériového spojení nebo jiných periferií, ale není nutné

from time import sleep
print("Starting RPMsenzor.py in 5 s (press CTRL+C to cancel)")
sleep(5)
print("Starting RPMsenzor.py ...")
import RPMsenzor