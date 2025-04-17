from machine import Pin, Timer
import time

# --- Nastaveni ---
PULSE_PIN = 2
LED_PIN = 19
PULSES_PER_REV = 1
DEBOUNCE_TIME_MS = 10

# --- Inicializace ---
led = Pin(LED_PIN, Pin.OUT)
pulse_pin = Pin(PULSE_PIN, Pin.IN, Pin.PULL_UP)

# --- Promenne ---
pulse_count = 0
rpm = 0
last_pulse_time = 0
last_state = 1  # predchozi stav pinu (1 == HIGH)

# --- Spolecny IRQ handler ---
def edge_handler(pin):
    global pulse_count, rpm, last_pulse_time, last_state
    now = time.ticks_ms()
    state = pin.value()

    # Debounce
    if time.ticks_diff(now, last_pulse_time) > DEBOUNCE_TIME_MS:
        if state == 1 and last_state == 0:
            # Nabezna hrana (inverzní logika)
            led.value(0)
            print("UVOLNENI")
        elif state == 0 and last_state == 1:
            # Sestupna hrana (inverzní logika)
            pulse_count += 1
            led.value(1)
            print("PULZ DETEKOVAN")
        last_pulse_time = now
        last_state = state

# --- Timer pro vypocet RPM ---
def calc_rpm(timer):
    global pulse_count, rpm
    rps = pulse_count / PULSES_PER_REV
    rpm = rps * 60
    print("RPS: {:.2f}  RPM: {:.2f}".format(rps, rpm))
    pulse_count = 0

# --- Nastaveni IRQ pro obe hrany ---
pulse_pin.irq(trigger=Pin.IRQ_RISING | Pin.IRQ_FALLING, handler=edge_handler)

# --- Timer ---
timer = Timer(0)
timer.init(period=1000, mode=Timer.PERIODIC, callback=calc_rpm)
# --- Hlavni smycka ---
while True:
    time.sleep(10)
