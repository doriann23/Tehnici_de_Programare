# Raport Laborator 5 - Forensics și Steganografie

## Lucrarea A: Decodorul Universal
* **Mesajul decodat din straturi:** `464c41477b73747261747572695f72657a6f6c766174657d`
* **Cheia XOR și textul:** Cheia găsită a fost `42`, iar textul descifrat este "Acesta este textul descifrat din xor.bin! Felicitari!"
* **Parola spartă:** Hash-ul MD5 a corespuns parolei `student`.

## Lucrarea B: Forensics și Steganografie
* **Tipul real al fișierului foto.jpg:** `jpeg`
* **Metadate GPS găsite:** Latitudine (47.0, 1.0, 0.0) N, Longitudine (28.0, 50.0, 0.0) E
* **Arhiva ascunsă:** În binarul `ascuns.png` a fost găsită o arhivă ZIP conținând textul "Bravo! Ai extras arhiva ascunsa."
* **Mesajul steganografic (LSB) dezvăluit:** `FLAG{ascuns_in_pixeli}`
