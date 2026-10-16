import os, base64, urllib.parse, hashlib, zipfile
from PIL import Image

def main():
    os.makedirs("probe", exist_ok=True)
    
    # 1. mesaj.txt
    flag = b"FLAG{straturi_rezolvate}"
    with open("probe/mesaj.txt", "wb") as f:
        f.write(urllib.parse.quote(base64.b64encode(flag.hex().encode()).decode()).encode())

    # 2. xor.bin
    with open("probe/xor.bin", "wb") as f:
        f.write(bytes(b ^ 42 for b in b"Acesta este textul descifrat din xor.bin! Felicitari!"))

    # 3. hashuri.txt & wordlist.txt
    with open("probe/hashuri.txt", "w") as f:
        f.write(hashlib.md5(b"student").hexdigest() + "\n")
    with open("probe/wordlist.txt", "w", encoding="latin1") as f:
        f.write("admin\npassword\n123456\nstudent\nqwerty\n")

    # 4. foto.jpg cu EXIF (Corectat pentru Pillow 12+)
    img = Image.new('RGB', (100, 100), color='red')
    exif = img.getexif()
    gps_ifd = exif.get_ifd(34853)
    gps_ifd[1] = 'N'
    gps_ifd[2] = (47.0, 1.0, 0.0)
    gps_ifd[3] = 'E'
    gps_ifd[4] = (28.0, 50.0, 0.0)
    img.save("probe/foto.jpg", exif=exif)

    # 5. ascuns.png
    img_png = Image.new('RGB', (50, 50), color='blue')
    img_png.save("probe/ascuns.png")
    with zipfile.ZipFile("probe/temp.zip", "w") as zf:
        zf.writestr("secret.txt", "Bravo! Ai extras arhiva ascunsa.")
    with open("probe/ascuns.png", "ab") as f_img, open("probe/temp.zip", "rb") as f_zip:
        f_img.write(f_zip.read())
    os.remove("probe/temp.zip")
    
    print("Fisierele de proba au fost generate cu succes!")

if __name__ == "__main__":
    main()
