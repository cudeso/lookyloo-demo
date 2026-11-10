#!/usr/bin/env python3
"""Serve the Lookyloo demo sites, choosing each site's document root from the Host header."""
import os
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlsplit

# Deployment settings. Sites answer on <site>.<DEMO_BASE_DOMAIN>, for example market.internetpolice.com.
# Use DEMO_BASE_DOMAIN=localhost for local development (market.localhost resolves to loopback in browsers).
BASE_DOMAIN = os.environ.get("DEMO_BASE_DOMAIN", "internetpolice.com")
BIND = os.environ.get("DEMO_BIND", "127.0.0.1")
PORT = int(os.environ.get("DEMO_PORT", "80"))

SITES_DIR = Path(__file__).resolve().parent / "sites"

# Fixed synthetic cookie per site, set on the homepage. Without a Domain attribute it stays host-only.
HOMEPAGE_COOKIES = {
    "market": "ash_guest=guest-4471",
    "hfh": "hfh_visitor=v-20261020-0815",
    "newscorp": "nld_reader=reader-0042",
}
SITES = (*HOMEPAGE_COOKIES, "tools4leas", "primenews")
HOSTS = {f"{site}.{BASE_DOMAIN}": site for site in SITES}

# Redirect chain for the HFH demo. 302 rather than 301, so a browser does not cache a hop between captures.
REDIRECTS = {
    ("hfh", "/services"): "/external",
    ("hfh", "/external"): "https://www.cudeso.be/",
}

# The browser's time zone never reaches the server, so Market's region-check.js decides and requests this path.
FORBIDDEN = {
    ("market", "/blocked"): "blocked.html",
}


class DemoHandler(SimpleHTTPRequestHandler):
    extensions_map = {
        ".html": "text/html; charset=utf-8",
        ".css": "text/css; charset=utf-8",
        ".js": "text/javascript; charset=utf-8",
        ".json": "application/json",
        ".svg": "image/svg+xml",
        ".ico": "image/x-icon",
        ".png": "image/png",
        ".jpeg": "image/jpeg",
        ".ttf": "font/ttf",
        ".otf": "font/otf",
        ".woff2": "font/woff2",
        ".txt": "text/plain; charset=utf-8",
    }
    site = None

    def do_GET(self):
        if self.select_site() and not self.send_redirect() and not self.send_forbidden():
            super().do_GET()

    def do_HEAD(self):
        if self.select_site() and not self.send_redirect() and not self.send_forbidden():
            super().do_HEAD()

    def select_site(self):
        host = self.headers.get("Host", "").split(":")[0].lower()
        self.site = HOSTS.get(host)
        if self.site is None:
            self.send_error(404, "Unknown demo host")
            return False
        self.directory = str(SITES_DIR / self.site)
        return True

    def send_redirect(self):
        target = REDIRECTS.get((self.site, urlsplit(self.path).path))
        if target is None:
            return False
        self.send_response(302)
        self.send_header("Location", target)
        self.send_header("Content-Length", "0")
        self.end_headers()
        return True

    def send_forbidden(self):
        page = FORBIDDEN.get((self.site, urlsplit(self.path).path))
        if page is None:
            return False
        body = (SITES_DIR / self.site / page).read_bytes()
        self.send_response(403)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        if self.command == "GET":
            self.wfile.write(body)
        return True

    def end_headers(self):
        if self.site:
            self.send_header("X-Demo-Site", self.site)
            if self.site in HOMEPAGE_COOKIES and urlsplit(self.path).path in ("/", "/index.html"):
                self.send_header("Set-Cookie", f"{HOMEPAGE_COOKIES[self.site]}; Path=/; HttpOnly; SameSite=Lax")
        super().end_headers()

    def list_directory(self, path):
        self.send_error(404, "File not found")


if __name__ == "__main__":
    print(f"Serving {', '.join(HOSTS)} on http://{BIND}:{PORT}/")
    ThreadingHTTPServer((BIND, PORT), DemoHandler).serve_forever()
