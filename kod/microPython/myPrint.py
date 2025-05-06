# my own print function

DEBUG_LEVELS = {
    "NONE": 0,
    "ERROR": 1,
    "WARNING": 2,
    "INFO": 3,
    "DEBUG": 4,
    "DEBUG2": 5,
}
# Speciální alias pro "ALL", který představuje nejvyšší úroveň
DEBUG_LEVELS["ALL"] = max(DEBUG_LEVELS.values()) + 1

debug_level = DEBUG_LEVELS["ERROR"]

# ANSI barvy podle úrovně
LEVEL_COLORS = {
    "DEBUG": "\033[97m",    # Jasně bílá
    "DEBUG2": "\033[90m",   # Šedá
    "INFO": "\033[92m",     # Zelená
    "WARNING": "\033[93m",  # Žlutá
    "ERROR": "\033[91m",    # Červená
}

RESET_COLOR = "\033[0m"

def dprint(*args, level="INFO", **kwargs):
    """
    Vytiskne zprávu na obrazovku, pokud je úroveň debugování rovna nebo vyšší než nastavená úroveň.

    Parametry:
        *args: Argumenty, které budou vytištěny. Obvykle se používá pro textovou zprávu.
        level (str): Úroveň debugování, která určuje, jaký typ zprávy bude vytištěn.
                    Možné hodnoty jsou "ERROR", "WARNING", "INFO", "DEBUG", "DEBUG2".
        **kwargs: Další argumenty pro funkci print (např. `end`, `sep`).

    Příklad použití:
        dprint("This is an info message", level="INFO")
    """
    if DEBUG_LEVELS.get(level, 0) <= debug_level:
        color = LEVEL_COLORS.get(level, "")
        print(f"{color}[{level}]", *args, RESET_COLOR, **kwargs)

from myPrint import DEBUG_LEVELS, debug_level

def print_visible_levels():
    """
    Vytiskne seznam všech úrovní debugování, které jsou aktivní na základě aktuální nastavené úrovně `debug_level`.

    Tato funkce zobrazuje všechny úrovně, které jsou menší nebo rovné aktuální nastavené úrovni `debug_level`.
    Aktivní úrovně jsou zobrazeny zeleně, neaktivní úrovně červeně.

    Příklad použití:
        print_visible_levels()
    """
    GREEN = "\033[92m"
    RED = "\033[91m"
    RESET = "\033[0m"
    # Seřadíme úrovně podle jejich hodnoty
    sorted_levels = sorted(DEBUG_LEVELS.items(), key=lambda item: item[1])
    result = []
    for level, val in sorted_levels:
        if val <= debug_level:
            result.append(f"{GREEN}{level}{RESET}")
        else:
            result.append(f"{RED}{level}{RESET}")
    print("Aktivni vypis:", " | ".join(result))
