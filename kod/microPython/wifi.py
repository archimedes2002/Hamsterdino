import network
import time


def connect_wifi(ssid, password):
    sta_if = network.WLAN(network.STA_IF)

    if not sta_if.active():  # Aktivujte pouze pokud není aktivní
        sta_if.active(True)
    sta_if.connect(ssid, password)

    # Čekání na připojení
    start_time = time.time()
    while not sta_if.isconnected():
        if time.time() - start_time > 10:  # Čeká max. 10 sekund
            raise OSError("Nezdařilo se připojit k Wi-Fi")
        time.sleep(1)
    print("Připojeno k Wi-Fi")
    print("IP adresa:", sta_if.ifconfig()[0])

# Příklad použití
connect_wifi('', '')
