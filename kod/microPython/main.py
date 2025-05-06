from machine import Pin, Timer
import time
from myPrint import dprint

# --- Nastaveni ---
PULSE_PIN = 2
LED_PIN = 19
PULSES_PER_REV = 1
DEBOUNCE_TIME_US = 10_000  # debounce 10 ms v mikrosekundach
MAX_ROTATION_PERIOD_US = 2_000_000 # [us] max. doba, kterou muze trvat jedna otocka (pak se bere, že kolečko stojí)
WHEEL_RADIUS_MM = 57 #milimeters
pi = 3.1415926535897932384626433832795 # just pi constant
wheel_circumference_m = 2*pi*(WHEEL_RADIUS_MM/1000)

# --- Inicializace ---
led = Pin(LED_PIN, Pin.OUT)
pulse_pin = Pin(PULSE_PIN, Pin.IN, Pin.PULL_UP)

#TODO: Komunikace s externim zalohovanym RTC modulem
#TODO: Pripojeni ctecky SD karty

# --- wifi (synchronizace času s NTP serverem)---
import wifi
dprint("Zacina mereni pulzu")

# --- Promenne ---
last_pulse_time = 0
#last_valid_pulse_time = 0
rotations_count = 0
time_deltas = []

# --- IRQ handler ---
def edge_handler(pin):
    global last_pulse_time, last_valid_pulse_time, time_deltas, rotations_count
    now = time.ticks_us()

    if pin.value() == 0:  # Sestupna hrana
        if last_pulse_time != 0: #problém?
            delta = time.ticks_diff(now, last_pulse_time)
            #debounce_delta = time.ticks_diff(now, last_pulse_time)
            if delta > DEBOUNCE_TIME_US:
                last_pulse_time = now
                led.value(1)
                dprint(f"Pulz: dt = {delta} us, debounce_dt = {delta} us", level="DEBUG2")
                if delta < MAX_ROTATION_PERIOD_US:
                    dprint("^ valid pulse ^", level="DEBUG2")
                    rotations_count += 1
                    time_deltas.append(delta)
                    #last_valid_pulse_time = now  # pro vypocet casu mezi nabeznymy hranami
        else:
            dprint("Prvni pulz...", level="DEBUG2")
            led.value(1)
            #last_valid_pulse_time = now  # pro vypocet casu mezi nabeznymy hranami
            last_pulse_time = now
    else:
        led.value(0)
    #last_pulse_time = now  # po ukocnceni pulzu se uloci cas jeho skonceni

# --- Timer pro vypocet prumerneho RPM ---
def calc_avg_rpm(timer):
    global time_deltas, rotations_count

    if time_deltas:
        avg_delta_us = sum(time_deltas) / len(time_deltas)
        avg_delta_s = avg_delta_us / 1_000_000

        # Průměrné RPS a RPM
        rps = 1.0 / (avg_delta_s * PULSES_PER_REV)
        rpm = rps * 60

        # Převod všech delta časů na RPS
        rps_list = [1.0 / (d / 1_000_000 * PULSES_PER_REV) for d in time_deltas]
        distance_m = (rotations_count / PULSES_PER_REV) * wheel_circumference_m # distance per this minute
        min_rps = min(rps_list)
        max_rps = max(rps_list)

        # Výpis
        t = time.localtime() # Casova znacka ve formatu YYYY-MM-DD hh:mm:ss
        timestamp = "{:04d}-{:02d}-{:02d} {:02d}:{:02d}:{:02d}".format(t[0], t[1], t[2], t[3], t[4], t[5])
        delta_list_str = ', '.join(str(d) for d in time_deltas)
        dprint(f"[{timestamp}]", level="INFO")
        dprint(f"dt[us]: [{delta_list_str}]", level="DEBUG2")
        dprint(f"Celych otacek: {len(time_deltas)}", level="INFO")
        dprint(f"min RPS: {min_rps:.2f}, max RPS: {max_rps:.2f}", level="INFO")
        dprint(f"Prumerne dt: {avg_delta_us:.0f} us", level="DEBUG2")
        dprint(f"Prumerne: RPS: {rps:.2f}, RPM: {rpm:.2f}", level="INFO")
        dprint(f"Vzdalenost: {distance_m:.2f} m", level="INFO")
    else:
        dprint("Zadne pulzy - RPM: 0", level="DEBUG")

    time_deltas = []
    rotations_count = 0


# --- IRQ nastaveni ---
pulse_pin.irq(trigger=Pin.IRQ_RISING | Pin.IRQ_FALLING, handler=edge_handler)

# --- Timer ---
timer = Timer(0)
timer.init(period=10_000, mode=Timer.PERIODIC, callback=calc_avg_rpm)

# --- Hlavni smycka ---
while True:
    time.sleep(10)
