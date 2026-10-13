from checker import build_url, is_https, show_response, check_site, scan_sites, check_headers, retry_check

print("Partea 1: build_url si is_https")
print("build_url fara slash:", build_url("example.com", "login"))
print("build_url cu slash:", build_url("example.com", "/login"))
print("is_https valid:", is_https("https://example.com"))
print("is_https invalid:", is_https("http://example.com"))

print("\n Partea 2: show_response ")
show_response("https://example.com")
show_response("http://this-site-does-not-exist.invalid")

print("\nPartea 3: check_site")
print("Valid:", check_site("https://example.com"))
print("Invalid:", check_site("http://this-site-does-not-exist.invalid"))

print("\nPartea 4: scan_sites")
scan_sites()

print("\nPartea 5: check_headers")
print("Valid:", check_headers("https://httpbin.org/response-headers?X-Frame-Options=DENY"))
print("Invalid:", check_headers("http://this-site-does-not-exist.invalid"))

print("\nPartea 6: retry_check")
print("Status 200 (se opreste):", retry_check("https://httpbin.org/status/200"))
print("Status 404 (se opreste):", retry_check("https://httpbin.org/status/404"))
print("Status 500 (3 incercari):", retry_check("https://httpbin.org/status/500"))
print("Invalid (eroare conexiune):", retry_check("http://this-site-does-not-exist.invalid"))