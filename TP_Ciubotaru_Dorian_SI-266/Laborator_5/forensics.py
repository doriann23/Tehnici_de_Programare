import re
from PIL import Image

# B1. Magic bytes
def tip_real(cale):
    cap = open(cale, "rb").read(8)
    if cap.startswith(b"%PDF"): return "pdf"
    if cap.startswith(b"\x89PNG"): return "png"
    if cap.startswith(b"\xff\xd8"): return "jpeg"
    if cap.startswith(b"PK\x03\x04"): return "zip/docx"
    return cap.hex()

print("=== B1. Tip real ===")
print("foto.jpg este de fapt:", tip_real("probe/foto.jpg"))

# B2. Strings in binar
print("\n=== B2. Strings in ascuns.png ===")
date = open("probe/ascuns.png", "rb").read()
for m in re.findall(rb"[ -~]{4,}", date):
    text = m.decode(errors="ignore")
    if "Bravo" in text:
        print("Indiciu gasit ascuns in binar:", text)

# B3. Metadate GPS
print("\n=== B3. EXIF si GPS ===")
exif = Image.open("probe/foto.jpg").getexif()
gps_info = exif.get_ifd(34853)
if gps_info:
    print(f"Latitudine: {gps_info.get(2)} {gps_info.get(1)}")
    print(f"Longitudine: {gps_info.get(4)} {gps_info.get(3)}")

# B4. File carving
print("\n=== B4. File carving ===")
i = date.find(b"PK\x03\x04")
if i != -1:
    open("gasit.zip", "wb").write(date[i:])
    print("Arhiva ZIP a fost extrasa cu succes si salvata ca 'gasit.zip'!")
