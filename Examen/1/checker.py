import requests

SITES = [
    # Pagini obișnuite (Părțile 2, 3 și 4)
    "https://example.com",
    "https://httpbin.org/html",
    "https://httpbin.org/json",
    "https://httpbin.org/status/200",
    "https://httpbin.org/redirect/1",
    "https://httpbin.org/delay/2",
    # Pagini care eșuează
    "https://httpbin.org/status/404",
    "https://httpbin.org/status/500",
    "https://httpbin.org/delay/10",
    "http://this-site-does-not-exist.invalid",
    # Anteturi de securitate (Partea 5)
    "https://httpbin.org/response-headers?X-Frame-Options=DENY&X-Content-Type-Options=nosniff",
    "https://httpbin.org/response-headers?x-frame-options=DENY",
    # Răspunde aleatoriu cu 200 sau 500 (Partea 6)
    "https://httpbin.org/status/200,500",
]

SECURITY_HEADERS = [
    "Strict-Transport-Security",
    "Content-Security-Policy",
    "X-Frame-Options",
    "X-Content-Type-Options",
]

def build_url(host, path):
    """Returnează o adresă completă, de exemplu https://example.com/login."""
    if path.startswith("/"):
        return f"https://{host}{path}"
    return f"https://{host}/{path}"

def is_https(url):
    """Returnează True dacă adresa începe cu https://, altfel False."""
    return url.startswith("https://")

def show_response(url):
    """Trimite un GET la url și afișează statusul și Content-Type."""
    try:
        response = requests.get(url, timeout=5)
        print(f"Status: {response.status_code}")
        print(f"Content-Type: {response.headers.get('Content-Type', 'unknown')}")
    except requests.RequestException:
        print("Eroare la conectarea la site.")


def check_site(url):
    """Returnează un dicționar cu: status, content_type, length, server."""
    try:
        response = requests.get(url, timeout=5)
        return {
            "status": response.status_code,
            "content_type": response.headers.get("Content-Type", "unknown"),
            "length": len(response.content),
            "server": response.headers.get("Server", "unknown")
        }
    except requests.RequestException:
        return {"status": None, "error": "Timeout sau eroare retea"}


def scan_sites():
    """Verifică toate site-urile din SITES, afișează-le pe cele care merg și un rezumat."""
    rezultate_bune = []
    reusite = 0
    esuate = 0

    for url in SITES:
        rez = check_site(url)
        if rez["status"] == 200:
            rezultate_bune.append((url, rez["status"], rez["length"]))
            reusite += 1
        else:
            esuate += 1

    rezultate_bune.sort(key=lambda x: x[2], reverse=True)
    for url, status, length in rezultate_bune:
        print(f"{url} -> {status}, {length} octeți")
    print(f"Reuşite: {reusite} Eşuate: {esuate}")


def check_headers(url):
    """Returnează un dicționar cu: present, missing, score."""
    try:
        response = requests.get(url, timeout=5)
        h_primite = {k.lower(): v for k, v in response.headers.items()}

        present = []
        missing = []
        for h in SECURITY_HEADERS:
            if h.lower() in h_primite:
                present.append(h)
            else:
                missing.append(h)

        return {
            "present": present,
            "missing": missing,
            "score": int((len(present) / len(SECURITY_HEADERS)) * 100)
        }
    except requests.RequestException:
        return {"status": None, "error": "Site inaccesibil"}


def retry_check(url, attempts=3):
    """Încearcă de cel mult `attempts` ori; returnează un dicționar cu: status, attempts."""
    incercari = 0
    u_status = None
    u_err = None

    while incercari < attempts:
        incercari += 1
        try:
            r = requests.get(url, timeout=5)
            u_status = r.status_code
            if u_status < 500:
                break
        except requests.RequestException:
            u_status = None
            u_err = "Eroare conexiune"

    rez = {"status": u_status, "attempts": incercari}
    if u_status is None and u_err:
        rez["error"] = u_err
    return rez
