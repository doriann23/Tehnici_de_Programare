# -*- coding: utf-8 -*-
"""Laboratorul 8 - partea A. Scoate si numara esecurile din auth.log.
Generat din programul de laborator, cu codul scris de student."""
import re
from collections import Counter

TIPAR = re.compile(r"Failed password for (?:invalid user )?(\S+) from (\S+) port")


def esec(linie):
    """Sarcina 1. Scoate (user, ip) dintr-un rand de esec."""
    m = TIPAR.search(linie)
    if m is None:
        return None
    return (m.group(1), m.group(2))

def citeste_esecuri(cale):
    """Sarcina 2. Lista de esecuri din fisier, robusta la randuri stricate."""
    rezultat = []
    try:
        with open(cale, "r", encoding="utf-8") as f:
            for rand in f:
                r = esec(rand)
                if r is not None:
                    rezultat.append({"user": r[0], "ip": r[1]})
    except FileNotFoundError:
        print("Fisierul nu a fost gasit:", cale)
        return []
    return rezultat

def pe_ip(esecuri):
    """Sarcina 3. Numara esecurile pe fiecare adresa IP."""
    return Counter(e["ip"] for e in esecuri)

def rezumat(cale):
    """Sarcina 4. Leaga totul: citeste, numara, intoarce rezumatul."""
    esecuri = citeste_esecuri(cale)
    return {
        "esecuri": len(esecuri),
        "pe_ip": pe_ip(esecuri)
    }


# ---------------------------------------------------------------------------
#  PARTEA B - detectorul de brute force
# ---------------------------------------------------------------------------

def main():
    import sys
    cale = sys.argv[1] if len(sys.argv) > 1 else 'start/auth.log'
    esecuri = citeste_esecuri(cale)
    counts = pe_ip(esecuri)
    print('Esecuri de autentificare:', len(esecuri))
    for ip, n in counts.most_common():
        print('  %s: %d' % (ip, n))


if __name__ == '__main__':
    main()
