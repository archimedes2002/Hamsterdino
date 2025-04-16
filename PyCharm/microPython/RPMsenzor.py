from machine import Pin, Timer
import time

# --- Nastavení ---
PULSE_PIN = 2              # GPIO pin, který podporuje IRQ
PULSES_PER_REV = 1         # Počet pulzů na jednu otáčku
DEBOUNCE_TIME_MS = 50      # Doba blokace (debounce) v milisekundách

# --- Proměnné ---
pulse_count = 0
rpm = 0
last_pulse_time = 0        # Pro debounce

# --- Přerušení při náběžné hraně ---
def pulse_handler(pin):
    global pulse_count, last_pulse_time
    # Porovnání času od posledního pulzu (debounce)
    now = time.ticks_ms()
    if time.ticks_diff(now, last_pulse_time) > DEBOUNCE_TIME_MS:
        pulse_count += 1
        last_pulse_time = now
        #print("pulz detekovan!")

# --- Timer pro výpočet RPM ---
def calc_rpm(timer):
    global pulse_count, rpm
    rps = pulse_count / PULSES_PER_REV
    rpm = rps * 60
    print("RPS: {:.2f}  RPM: {:.2f}".format(rps, rpm))
    pulse_count = 0

# --- Inicializace pinu a přerušení ---
pulse_pin = Pin(PULSE_PIN, Pin.IN, Pin.PULL_UP)
pulse_pin.irq(trigger=Pin.IRQ_RISING, handler=pulse_handler)

# --- Timer každou sekundu vypočítá RPM ---
timer = Timer(0)
timer.init(period=1000, mode=Timer.PERIODIC, callback=calc_rpm)

# --- Hlavní smyčka ---
while True:
    time.sleep(1)
