from PIL import Image

def ascunde():
    img = Image.open("probe/foto.jpg").convert("RGB")
    px = list(img.getdata())
    mesaj = b"FLAG{ascuns_in_pixeli}\x00" 
    biti = "".join(f"{x:08b}" for x in mesaj)
    
    px_nou = []
    bit_idx = 0
    for r, g, b in px:
        if bit_idx < len(biti):
            r = (r & ~1) | int(biti[bit_idx])
            bit_idx += 1
        if bit_idx < len(biti):
            g = (g & ~1) | int(biti[bit_idx])
            bit_idx += 1
        if bit_idx < len(biti):
            b = (b & ~1) | int(biti[bit_idx])
            bit_idx += 1
        px_nou.append((r, g, b))
        
    img.putdata(px_nou)
    img.save("stego.png")
    print("Mesajul a fost ascuns in stego.png")

def dezvaluie():
    px = list(Image.open("stego.png").convert("RGB").getdata())
    biti = "".join(str(c & 1) for px_rgb in px for c in px_rgb)
        
    octeti = [biti[i:i+8] for i in range(0, len(biti), 8)]
    mesaj = bytearray()
    for octet in octeti:
        if len(octet) == 8:
            val = int(octet, 2)
            if val == 0:
                break
            mesaj.append(val)
    print("Mesaj dezvaluit:", mesaj.decode(errors="ignore"))

print("\n=== B5 & B6. Steganografie (LSB) ===")
ascunde()
dezvaluie()
