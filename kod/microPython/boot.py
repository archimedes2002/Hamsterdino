import machine
import os

import myPrint
from myPrint import DEBUG_LEVELS, dprint
myPrint.debug_level = myPrint.DEBUG_LEVELS["DEBUG"] # nastavení úrovně výpisu:
# NONE, ERROR, WARNING, INFO, DEBUG, DEBUG2, ALL

# výpis základních informací
dprint("Booting ESP32 ...")
dprint(f"Filesystem obsahuje: {os.listdir()}")
myPrint.print_visible_levels()

from time import sleep
dprint("Starting main.py in 5 s (press CTRL+C to cancel)")
sleep(5)
dprint("main.py started ...")
import main
