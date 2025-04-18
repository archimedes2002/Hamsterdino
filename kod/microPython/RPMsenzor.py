from machine import Pin, Timer
import time

# --- Nastaveni ---
PULSE_PIN = 2
LED_PIN = 19
PULSES_PER_REV = 1
DEBOUNCE_TIME_US = 10_000  # debounce 10 ms v mikrosekundach
MAX_ROTATION_PERIOD_US = 2_000_000 # [us] max. doba, kterou muze trvat jedna otocka (pak se bere, že kolečko stojí)
WHEEL_RADIUS_MM = 57 #milimeters
pi = 3.1415926535897932384626433832795
wheel_circumference_m = 2*pi*(WHEEL_RADIUS_MM/1000)

# --- Inicializace ---
led = Pin(LED_PIN, Pin.OUT)
pulse_pin = Pin(PULSE_PIN, Pin.IN, Pin.PULL_UP)

# --- Promenne ---
last_pulse_time = 0
rotations_count = 0
time_deltas = []

# --- IRQ handler ---
def edge_handler(pin):
    global last_pulse_time, time_deltas, rotations_count
    now = time.ticks_us()

    if pin.value() == 0:  # Sestupna hrana
        if last_pulse_time != 0: #problém?
            delta = time.ticks_diff(now, last_pulse_time)
            if delta > DEBOUNCE_TIME_US:
                led.value(1)
                print("Pulz: dt = {} us".format(delta))
                if delta < MAX_ROTATION_PERIOD_US:
                    rotations_count += 1
                    time_deltas.append(delta)
                    last_pulse_time = now  # pro vypocet casu mezi nabeznymy hranami
        else:
            print("Prvni pulz...")
            led.value(1)
            last_pulse_time = now  # pro vypocet casu mezi nabeznymy hranami
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
        print("[{}]".format(timestamp))
        print("dt[us]: [{}]".format(delta_list_str))
        print("Pulzu: {}, min RPS: {:.2f}, max RPS: {:.2f}".format(len(time_deltas), min_rps, max_rps))
        print("Prumerne dt: {:.0f} us, RPS: {:.2f}, RPM: {:.2f}".format(avg_delta_us, rps, rpm))
        print("Vzdalenost: {:.2f} m".format(distance_m))
    else:
        print("Zadne pulzy - RPM: 0")

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
