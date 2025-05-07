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

UPLOAD_PERIOD = 10_000 # [ms]
ADD_HOURS = 2 # GMT+ADD_HOURS

def SDtest(cislo=1):
    """
    Testuje zápis na SD kartu.

    Parametry:
    cislo (int): Číslo testu pro označení výpisu.

    Vytvoří soubor "test.txt" na SD kartě a zapíše testovací zprávu.
    V případě úspěchu vypíše zprávu o úspěchu, v případě chyby vypíše chybu.
    """
    try:
        with open("/sd/test.txt", "w") as f:
            f.write("Test SD zapisu\n")
        print(f"Test zapisu cislo:[{cislo}] OK")
    except Exception as e:
        print(f"[ERROR] SD test cislo:[{cislo}] selhal: {e}")


# --- Nastaveni ---
PULSE_PIN = 2  # Pin pro snímání pulsů
LED_PIN = 15  # Pin pro LED
PULSES_PER_REV = 1  # Počet pulsů na jednu otáčku
DEBOUNCE_TIME_US = 10_000  # Debounce čas v mikrosekundách
MAX_ROTATION_PERIOD_US = 2_000_000  # Maximální perioda rotace v mikrosekundách (pak se bere, že kolečko stojí)
WHEEL_RADIUS_MM = 57  # Poloměr kola v milimetrech
pi = 3.141592653589793  # Hodnota pí
wheel_circumference_m = 2 * pi * (WHEEL_RADIUS_MM / 1000)  # Obvod kola v metrech

led = Pin(LED_PIN, Pin.OUT)  # Inicializace LED
pulse_pin = Pin(PULSE_PIN, Pin.IN, Pin.PULL_UP)  # Inicializace pinu pro puls

dprint("Zacina mereni pulzu")

last_pulse_time = 0
rotations_count = 0
time_deltas = []
last_log_time = time.time()


def edge_handler(pin):
    """
    IRQ handler pro změnu stavu pinu při záznamu pulzu.

    Parametry:
    pin (Pin): Pin, který detekuje změnu stavu.

    Funkce zaznamenává dobu mezi pulzy, počítá otáčky a aktualizuje časové rozdíly mezi pulzy.
    Aktivuje LED při detekci pulzu a zajišťuje, že mezi pulzy neprobíhá žádné zpoždění (debounce).
    """
    global last_pulse_time, time_deltas, rotations_count
    now = time.ticks_us()
    if pin.value() == 0: # Sestupna hrana
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


def calc_avg_rpm(timer):
    """
    Timer pro výpočet průměrných otáček za minutu (RPM) a vzdálenost.

    Parametry:
    timer (Timer): Timer, který spustil tuto funkci.

    Funkce vypočítá průměrné otáčky za minutu na základě zaznamenaných časových rozdílů mezi pulzy.
    Výstupní hodnoty jsou zapsány do logu na SD kartu a vypsány do konzole.
    """
    global time_deltas, rotations_count, last_log_time

    if time_deltas: #pokud byl detekovan pohyb
        avg_delta_us = sum(time_deltas) / len(time_deltas)
        avg_delta_s = avg_delta_us / 1_000_000
        rps = 1.0 / (avg_delta_s * PULSES_PER_REV)
        rpm = rps * 60
        distance_m = (rotations_count / PULSES_PER_REV) * wheel_circumference_m
        t = time.localtime()
        rps_list = [1.0 / (d / 1_000_000 * PULSES_PER_REV) for d in time_deltas]
        min_rps = min(rps_list)
        max_rps = max(rps_list)

        # Vypočteme nové hodiny
        new_hour = (t[3] + ADD_HOURS) % 24
        # Počet dní, které se přidají na základě přetékajících hodin
        days_to_add = (t[3] + ADD_HOURS) // 24
        # Aktualizujeme den podle přidaných dní
        new_day = t[2] + days_to_add
        # Oprava přechodů přes dny, měsíce, roky
        if new_day > 31:  # Ověříme maximální počet dní v měsíci
            if t[1] == 1 or t[1] == 3 or t[1] == 5 or t[1] == 7 or t[1] == 8 or t[1] == 10 or t[1] == 12:
                if new_day > 31:
                    new_day -= 31
                    new_month = t[1] + 1
                    if new_month > 12:  # Pokud přeskočíme na nový rok
                        new_month = 1
                        new_year = t[0] + 1
                    else:
                        new_year = t[0]
            else:
                # Pro ostatní měsíce zohledníme 30 dní a únor (28 nebo 29)
                if t[1] == 2:
                    if new_day > 29:
                        new_day -= 29
                        new_month = 3
                    else:
                        new_month = t[1]
                        new_year = t[0]
                else:
                    # Změna měsíce pro měsíce s 30 dny
                    if new_day > 30:
                        new_day -= 30
                        new_month = t[1] + 1
                        if new_month > 12:
                            new_month = 1
                            new_year = t[0] + 1
                        else:
                            new_year = t[0]
        else:
            new_year = t[0]
            new_month = t[1]

        # Sestavení nového timestampu
        timestamp = "{:04d}-{:02d}-{:02d}T{:02d}:{:02d}:{:02d}".format(new_year, new_month, new_day, new_hour, t[4], t[5])
        dprint(f"[{timestamp}] RPM: {rps:.2f},RPMmax: {max_rps:.2f}, RPMmin: {min_rps:.2f}, vzdalenost: {distance_m:.2f} m")

        now = time.time()
        dprint(f"dif: [{now - last_log_time}] >=? 10",  level="DEBUG")
        if now - last_log_time >= 10:
            log_lock.acquire()
            log_queue.append((timestamp, rps, min_rps, max_rps, distance_m))
            log_lock.release()
            last_log_time = now
    else:
        dprint("Zadne pulzy - RPM: 0")

    time_deltas = []
    rotations_count = 0


def start_webserver():
    """
    Spustí webový server na ESP32 pro zobrazení logu RPM a grafu.

    Tento server přijímá HTTP požadavky a zobrazuje HTML stránku s grafem otáček.
    Data jsou načítána ze souboru log.txt na SD kartě a zobrazována v grafu pomocí knihovny Chart.js.
    """
    time.sleep(1)

    def read_log():
        """
        Načte obsah logu z SD karty.

        Vrací obsah souboru "log.txt" na SD kartě jako text.

        Vrací:
        str: Obsah log souboru.
        """
        try:
            if "log.txt" in os.listdir("/sd"):
                with open("/sd/log.txt") as f:
                    return f.read()
        except Exception as e:
            dprint(f"[ERROR] Chyba pri cteni log.txt: {e}", level="ERROR")
        return ""

    def html_page():
        """
        Načte HTML stránku ze souboru na SD kartě.

        Vrací:
        str: HTML kód stránky, nebo prázdný řetězec při chybě.
        """
        try:
            with open("index.html") as f:
                return f.read()
        except Exception as e:
            dprint(f"[ERROR] Nelze načíst index.html: {e}", level="ERROR")
            return "<html><body><h1>Chyba: Nelze načíst stránku</h1></body></html>"

    def safe_send_lines(client, text, content_type="text/html"):
        """
        Bezpečně pošle HTTP odpověď klientovi.

        Parametry:
        client (socket): Socket připojeného klienta.
        text (str): Textová odpověď, která bude odeslána.
        content_type (str): Typ obsahu (např. "text/html").
        """
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


def safe_write_to_sd():
    """
    Bezpečně zapisuje log do SD karty.

    Funkce zajišťuje, že při zápisu na SD kartu nebude docházet k souběžnému přístupu,
    a zajišťuje, že zápis bude proveden atomicky.
    """
    log_lock.acquire()  # Zamek pro zápis
    try:
        if log_queue:
            with open("/sd/log.txt", "a") as f:
                while log_queue:
                    t, avs, mins, maxs, d = log_queue.pop(0)
                    f.write("{},{},{},{},{}\n".format(t, avs, mins, maxs, d))
            print("Zapsano na SD kartu.")
    except Exception as e:
        dprint(f"Chyba pri zapisu na SD: {e}", level="ERROR")
    finally:
        log_lock.release()  # Odemknuti zámku pro další přístup


# --- Spusteni ---
_thread.start_new_thread(start_webserver, ())
pulse_pin.irq(trigger=Pin.IRQ_RISING | Pin.IRQ_FALLING, handler=edge_handler)
timer = Timer(0)
timer.init(period=UPLOAD_PERIOD, mode=Timer.PERIODIC, callback=calc_avg_rpm)

# --- Hlavní smyčka ---
while True:
    time.sleep(1)
    safe_write_to_sd()  # Zapisujeme do SD karty bez souběžného přístupu
    uos.sync()  # Zajistíme, že data jsou uložena na SD kartu
