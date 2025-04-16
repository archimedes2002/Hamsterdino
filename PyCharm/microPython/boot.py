# This file is executed on every boot (including wake-boot from deepsleep)
#import esp
#esp.osdebug(None)
#import webrepl
#webrepl.start()
#import ledka_blik
from time import sleep
sleep(5)
print("Starting RPMsenzor.py ...")
import RPMsenzor