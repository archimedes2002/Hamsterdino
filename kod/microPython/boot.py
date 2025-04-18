import machine
import os

import myPrint
from myPrint import DEBUG_LEVELS, dprint, debug_level
debug_level = DEBUG_LEVELS["WARNING"]  # Změňte na INFO, abyste viděli všechny zprávy

# výpis základních informací
dprint("Booting ESP32 ...")
dprint("Filesystem obsahuje:", os.listdir())
myPrint.print_visible_levels()

from time import sleep
dprint("Starting RPMsenzor.py in 5 s (press CTRL+C to cancel)")
sleep(5)
dprint("RPMsenzor.py started ...")
import RPMsenzor
