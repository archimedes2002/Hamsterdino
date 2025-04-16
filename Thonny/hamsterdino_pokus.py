from machine import Pin, Timer
import time

# --- Nastavení ---
PULSE_PIN = 35  # GPIO číslo, kde je připojen snímač
PULSES_PER_REV = 1  # Počet pulzů na jednu otáčku

# --- Proměnné ---
pulse_count = 0
rpm = 0

# --- Přerušení při náběžné hraně ---
def pulse_handler(pin):
    global pulse_count
    pulse_count += 1

# --- Timer pro výpočet RPM ---
def calc_rpm(timer):
    global pulse_count, rpm
    # Počet otáček za sekundu
    rps = pulse_count / PULSES_PER_REV
    # Přepočet na otáčky za minutu
    rpm = rps * 60
    print("RPM:", rpm)
    pulse_count = 0  # Vynulovat počítadlo pro další interval

# --- Inicializace pinu a přerušení ---
pulse_pin = Pin(PULSE_PIN, Pin.IN, Pin.PULL_UP)
pulse_pin.irq(trigger=Pin.IRQ_RISING, handler=pulse_handler)

# --- Timer každou sekundu vypočítá RPM ---
timer = Timer(0)
timer.init(period=1000, mode=Timer.PERIODIC, callback=calc_rpm)

# --- Hlavní smyčka ---
while True:
    time.sleep(1)  # Hlavní smyčka může zůstat prázdná
