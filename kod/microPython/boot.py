import machine
import os

import myPrint
from myPrint import DEBUG_LEVELS, dprint

# Nastavení úrovně výpisu pro ladění. Možnosti:
# NONE - žádné výpisy,
# ERROR - pouze chyby,
# WARNING - varování,
# INFO - informační výpisy,
# DEBUG - základní ladicí výpisy,
# DEBUG2 - podrobné ladicí výpisy,
# ALL - všechny výpisy.
myPrint.debug_level = myPrint.DEBUG_LEVELS["DEBUG"]

# Výpis základních informací o spuštění
dprint("Booting ESP32 ...")  # Informace o spuštění ESP32
dprint(f"Filesystem obsahuje: {os.listdir()}")  # Výpis souborů v souborovém systému
myPrint.print_visible_levels()  # Výpis dostupných úrovní výpisu

from time import sleep

# Výpis, že main.py bude spuštěn za 5 sekund, uživatel může stisknout CTRL+C pro zrušení
dprint("Starting main.py in 5 s (press CTRL+C to cancel)")
sleep(5)

# Výpis, že main.py byl úspěšně spuštěn
dprint("main.py started ...")

# Import hlavního skriptu (main.py)
import main
