import base64
import re
from urllib.parse import unquote
import hashlib
import argparse
import json

def ghici_strat(s):
    if "%" in s:
        return "url"
    if re.fullmatch(r'[0-9a-fA-F]+', s) and len(s) % 2 == 0:
        return "hex"
    if re.fullmatch(r'[A-Za-z0-9+/]+={0,2}', s):
        return "base64"
    return "necunoscut"

def desfa(s):
    strat = ghici_strat(s)
    if strat == "base64":
        return strat, base64.b64decode(s)
    elif strat == "hex":
        return strat, bytes.fromhex(s)
    elif strat == "url":
        return strat, unquote(s).encode()
    return strat, s.encode()

def citibil(b):
    return all(32 <= c < 127 for c in b)

def main():
    p = argparse.ArgumentParser()
    p.add_argument("intrare")
    p.add_argument("--fisier", action="store_true")
    a = p.parse_args()

    # A7. Citire de la argumente
    if a.fisier:
        val = open(a.intrare, "r").read().strip()
    else:
        val = a.intrare

    # A4. Straturi multiple, într-o buclă
    rezultat_bytes = b""
    strat_final = ""
    for _ in range(8):
        strat, b = desfa(val)
        if citibil(b):
            rezultat_bytes = b
            strat_final = strat
            print(f"Mesaj decodat cu succes: {b.decode()}")
            break
        else:
            try:
                val = b.decode()
            except UnicodeDecodeError:
                break
                
    # A7. Salvare fișa JSON
    with open("arsenal/forensics/fisa.json", "w") as f:
        json.dump({"strat": strat_final, "rezultat": rezultat_bytes.decode(errors="ignore")}, f)

    # A5. Spargi un XOR cu cheie de un octet
    try:
        date_xor = open("probe/xor.bin", "rb").read()
        for k in range(256):
            clar = bytes(b ^ k for b in date_xor)
            if citibil(clar):
                print(f"Cheie XOR gasita: {k} -> Text: {clar.decode()}")
    except FileNotFoundError:
        pass

    # A6. Spargi un hash prin dicționar
    try:
        tinta = open("probe/hashuri.txt").readline().strip()
        print(f"Lungime hash: {len(tinta)}")
        for cuv in open("probe/wordlist.txt", encoding="latin1"):
            cuv = cuv.strip()
            ghici = hashlib.md5(cuv.encode()).hexdigest()
            if ghici == tinta:
                print(f"Parola gasita in dictionar: {cuv}")
                break
    except FileNotFoundError:
        pass

if __name__ == "__main__":
    main()
