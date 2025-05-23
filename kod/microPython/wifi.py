import network
import ntptime
import time
import sys
from myPrint import dprint

# --- Funkce pro nacitani SSID a PASSWORD z externího souboru ---
def load_wifi_credentials(file_path):
    """
    Načte SSID a heslo Wi-Fi z externího souboru.

    Funkce otevře soubor na zadané cestě, prohledá jej a vyhledá řádky obsahující
    'SSID=' a 'PASSWORD='. Tyto hodnoty následně vrátí jako řetězce.

    :param file_path: Cesta k souboru, který obsahuje přihlašovací údaje k Wi-Fi.
    :return: Nalezené SSID a heslo (jako řetězce).
    """
    ssid = ''
    password = ''
    try:
        with open(file_path, 'r') as file:
            lines = file.readlines()
            for line in lines:
                # vymazání všech bílých znaků (mezery, tabulatory, nové řádky)
                line = line.strip()
                line = line.replace("\t", "").replace("\n", "").replace(" ", "")
                if 'SSID=' in line:
                    ssid = line.split('=')[1]
                elif 'PASSWORD=' in line:
                    password = line.split('=')[1]
    except Exception as e:
        dprint(f"Chyba pri nacitani souboru s prihlasovacimi udaji: {e}", level="ERROR")
    return ssid, password

# --- Funkce pro synchronizaci casu pres NTP ---
def sync_time_with_ntp(retries=5, delay=2):
    """
    Pokusí se synchronizovat čas s NTP serverem.

    Funkce se pokusí několikrát synchronizovat čas pomocí NTP serveru. Pokud se
    synchronizace nezdaří, pokusí se znovu po určitém zpoždění. Pokud zařízení
    není připojeno k Wi-Fi, pokusí se o připojení.

    :param retries: Počet pokusů o synchronizaci.
    :param delay: Zpoždění mezi pokusy v sekundách.
    :return: True, pokud byla synchronizace úspěšná, jinak False.
    """
    global sta_if
    for attempt in range(retries):
        try:
            ntptime.settime()
            dprint("Synchronizace casu byla uspesna", level="INFO")
            return True
        except Exception as e:
            dprint(f"Pokus {attempt+1}/{retries} – Chyba pri synchronizaci casu: {e}", level="WARNING")
            if not sta_if.active():  # pokud by nebyl připojen k síti
                connect_to_wifi(SSID, PASSWORD)
            time.sleep(delay)
    dprint(f"Synchronizace casu selhala po {retries} pokusech", level="ERROR")
    return False

# --- Funkce pro restart Wi-Fi ---
def reset_wifi():
    """
    Restartuje Wi-Fi rozhraní.

    Tato funkce deaktivuje a následně znovu aktivuje Wi-Fi rozhraní.
    """
    global sta_if
    dprint("Restartuji Wi-Fi rozhrani", level="WARNING")
    sta_if.active(False)
    time.sleep(1)
    sta_if.active(True)
    time.sleep(1)

# --- Funkce pro pripojeni k Wi-Fi ---
def connect_to_wifi(ssid, password, timeout=30):
    """
    Připojí zařízení k Wi-Fi síti.

    Funkce se pokusí připojit zařízení k Wi-Fi síti s uvedeným SSID a heslem.
    Pokud se připojení nezdaří během stanoveného časového limitu, Wi-Fi bude restartováno.

    :param ssid: SSID Wi-Fi sítě.
    :param password: Heslo pro připojení k Wi-Fi síti.
    :param timeout: Maximální doba čekání na připojení (v sekundách).
    :return: True, pokud bylo zařízení připojeno k síti, jinak False.
    """
    global sta_if
    dprint(f"Wi-Fi active status: {sta_if.active()}", level="DEBUG")
    reset_wifi()
    sta_if.connect(ssid, password)

    # čekání na připojení
    dot_count = 0
    start_time = time.time()
    while not sta_if.isconnected():
        dots = "." * dot_count
        sys.stdout.write(f"\rCekam na pripojeni k Wi-Fi{dots}   ")
        time.sleep(0.5)
        dot_count = (dot_count + 1) % 4
        if time.time() - start_time > timeout:  # timeout
            print("\n")
            reset_wifi()
            dprint("Nezdarilo se pripojit k Wi-Fi behem stanoveneho casu", level="ERROR")
            return False
    print("\n")
    dprint("Pripojeno k Wi-Fi siti")
    dprint("IP adresa:", sta_if.ifconfig()[0])
    return True

# --- Funkce pro ziskani IP adresy ---
def get_ip():
    """
    Získá aktuální IP adresu připojeného zařízení.

    :return: IP adresa zařízení jako řetězec.
    """
    wlan = network.WLAN(network.STA_IF)
    return wlan.ifconfig()[0]
#-----------------------------------------------------------------------------------------------

dprint("Zahajuji pripojovani k wifi")
sta_if = network.WLAN(network.STA_IF)

# --- Nacteni SSID a PASSWORD z externího souboru ---
SSID, PASSWORD = load_wifi_credentials('wifi_credentials.txt')
dprint("Network credinteals:", level="DEBUG")
dprint(f"SSID: {SSID}, PASSWORD: {PASSWORD}")

if not SSID or not PASSWORD:
    dprint("Chyba: Nejsou k dispozici prihlasovaci udaje k siti!", level="ERROR")
    raise SystemExit

# --- Připojení k Wi-Fi --- a --- Synchronizace casu pres NTP --- (pokud se připojil k síti)
if connect_to_wifi(SSID, PASSWORD) and sync_time_with_ntp():
    pass  # Všechno proběhlo v pořádku, nic netřeba vypisovat
else:
    dprint("Pouzivam cas z RTC. Pokracuji bez casove synchronizace...", level="WARNING")

t = time.localtime()
dprint(f"Aktualni cas: {t[0]:04d}-{t[1]:02d}-{t[2]:02d} {t[3]:02d}:{t[4]:02d}:{t[5]:02d}")
