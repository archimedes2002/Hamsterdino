from machine import Pin, Timer, SPI
import time
import _thread
import os
import sdcard
from myPrint import dprint
import wifi
import socket
from _thread import allocate_lock
import uos

# --- Fronta a zámek ---
log_queue = []
log_lock = allocate_lock()

# --- SD karta ---
spi = SPI(2, baudrate=400_000, polarity=0, phase=0, sck=Pin(18), mosi=Pin(23), miso=Pin(19))
cs = Pin(5, Pin.OUT)
sd = sdcard.SDCard(spi, cs)
vfs = os.VfsFat(sd)
os.mount(vfs, "/sd")

# Test zápisu na SD kartu
def SDtest(cislo=1):
    try:
        with open("/sd/test.txt", "w") as f:
            f.write("Test SD zapisu\n")
        print(f"Test zapisu cislo:[{cislo}] OK")
    except Exception as e:
        print(f"[ERROR] SD test cislo:[{cislo}] selhal: {e}")

# --- Nastaveni ---
PULSE_PIN = 2
LED_PIN = 15
PULSES_PER_REV = 1
DEBOUNCE_TIME_US = 10_000
MAX_ROTATION_PERIOD_US = 2_000_000
WHEEL_RADIUS_MM = 57
pi = 3.141592653589793
wheel_circumference_m = 2 * pi * (WHEEL_RADIUS_MM / 1000)

led = Pin(LED_PIN, Pin.OUT)
pulse_pin = Pin(PULSE_PIN, Pin.IN, Pin.PULL_UP)

dprint("Zacina mereni pulzu")

last_pulse_time = 0
rotations_count = 0
time_deltas = []
last_log_time = time.time()

# --- IRQ handler ---
def edge_handler(pin):
    global last_pulse_time, time_deltas, rotations_count
    now = time.ticks_us()
    if pin.value() == 0:
        if last_pulse_time != 0:
            delta = time.ticks_diff(now, last_pulse_time)
            if delta > DEBOUNCE_TIME_US:
                last_pulse_time = now
                led.value(1)
                if delta < MAX_ROTATION_PERIOD_US:
                    rotations_count += 1
                    time_deltas.append(delta)
        else:
            last_pulse_time = now
            led.value(1)
    else:
        led.value(0)

# --- Timer callback ---
def calc_avg_rpm(timer):
    global time_deltas, rotations_count, last_log_time

    if time_deltas:
        avg_delta_us = sum(time_deltas) / len(time_deltas)
        avg_delta_s = avg_delta_us / 1_000_000
        rps = 1.0 / (avg_delta_s * PULSES_PER_REV)
        rpm = rps * 60
        distance_m = (rotations_count / PULSES_PER_REV) * wheel_circumference_m
        t = time.localtime()
        timestamp = "{:04d}-{:02d}-{:02d} {:02d}:{:02d}:{:02d}".format(*t[:6])

        dprint(f"[{timestamp}] RPM: {rpm:.2f}, vzdalenost: {distance_m:.2f} m")

        now = time.time()
        if now - last_log_time >= 10:
            log_lock.acquire()
            log_queue.append((timestamp, rpm))
            log_lock.release()
            last_log_time = now
    else:
        dprint("Zadne pulzy - RPM: 0")

    time_deltas = []
    rotations_count = 0

# --- Web server ---
def start_webserver():
    time.sleep(1)

    def read_log():
        try:
            if "log.txt" in os.listdir("/sd"):
                with open("/sd/log.txt") as f:
                    return f.read()
        except Exception as e:
            dprint(f"[ERROR] Chyba pri cteni log.txt: {e}", level="ERROR")
        return ""

    def html_page():
        return """\
<html>
<head><script src="https://cdn.jsdelivr.net/npm/chart.js"></script></head>
<body>
<h2>RPM log</h2>
<canvas id="chart" width="400" height="200"></canvas>
<script>
fetch('/data').then(r => r.text()).then(text => {
  const lines = text.trim().split('\\n');
  const labels = [], values = [];
  for (let line of lines) {
    const parts = line.split(',');
    if (parts.length == 2) {
      labels.push(parts[0]);
      values.push(parseFloat(parts[1]));
    }
  }
  new Chart(document.getElementById('chart'), {
    type: 'line',
    data: {
      labels: labels,
      datasets: [{
        label: 'RPM',
        data: values,
        borderColor: 'blue',
        fill: false
      }]
    }
  });
});
</script>
</body>
</html>"""

    def safe_send_lines(client, text, content_type="text/html"):
        try:
            client.send("HTTP/1.0 200 OK\r\nContent-Type: {}\r\n\r\n".format(content_type))
            for line in text.split('\n'):
                client.send(line + '\n')
                time.sleep_ms(5)
        except Exception as e:
            dprint(f"[ERROR] Chyba pri odesilani odpovedi: {e}", level="ERROR")

    try:
        addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]
        s = socket.socket()
        s.bind(addr)
        s.listen(1)
        print("Web server bezi na http://ESP_IPadress:80")

        while True:
            try:
                cl, addr = s.accept()
                print(f"Client connected from {addr}")
                request = cl.recv(1024).decode()

                if "GET /data" in request:
                    safe_send_lines(cl, read_log(), content_type="text/plain")
                else:
                    safe_send_lines(cl, html_page(), content_type="text/html")
                cl.close()
            except Exception as e:
                dprint(f"[ERROR] Chyba webserveru: {e}", level="ERROR")

    except Exception as e:
        dprint(f"[ERROR] Nepodarilo se spustit webserver: {e}", level="ERROR")

# --- Funkce pro zápis do logu ---
def safe_write_to_sd():
    log_lock.acquire()  # Zamek pro zápis
    try:
        if log_queue:
            with open("/sd/log.txt", "a") as f:
                while log_queue:
                    t, r = log_queue.pop(0)
                    f.write("{},{}\n".format(t, r))
            print("Zapsano na SD kartu.")
    except Exception as e:
        dprint(f"Chyba pri zapisu na SD: {e}", level="ERROR")
    finally:
        log_lock.release()  # Odemknuti zámku pro další přístup

# --- Spusteni ---
_thread.start_new_thread(start_webserver, ())
pulse_pin.irq(trigger=Pin.IRQ_RISING | Pin.IRQ_FALLING, handler=edge_handler)
timer = Timer(0)
timer.init(period=10_000, mode=Timer.PERIODIC, callback=calc_avg_rpm)

# --- Hlavní smyčka ---
while True:
    time.sleep(1)
    safe_write_to_sd()  # Zapisujeme do SD karty bez souběžného přístupu
    uos.sync()  # Zajistíme, že data jsou uložena na SD kartu
