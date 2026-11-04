"""Visual QA: log in as the service test account and screenshot site pages (agent reads the PNGs).

Usage:
  BASE_URL=https://<test-stand> TEST_EMAIL=... TEST_PASSWORD=... python screenshot.py [outdir] [path ...]
  default path: /

BASE_URL is required (no default). Credentials come from the environment (see project.md)
and are never printed. LOGIN_PATH overrides the login page (default /login), WIDTH the viewport width (default 1440).
Requires: pip install playwright && python -m playwright install chromium
"""
import os
import sys
from pathlib import Path
from playwright.sync_api import sync_playwright

BASE = os.environ.get("BASE_URL")
assert BASE, "BASE_URL is required (test stand address, see project.md)"
LOGIN_PATH = os.environ.get("LOGIN_PATH", "/login")
OUT = Path(sys.argv[1]) if len(sys.argv) > 1 else Path.cwd()
PAGES = sys.argv[2:] or ["/"]

email, password = os.environ.get("TEST_EMAIL"), os.environ.get("TEST_PASSWORD")
assert email and password, "no TEST_EMAIL/TEST_PASSWORD in environment"

OUT.mkdir(parents=True, exist_ok=True)
with sync_playwright() as p:
    b = p.chromium.launch()
    page = b.new_page(viewport={"width": int(os.environ.get("WIDTH", "1440")), "height": 900})
    page.goto(f"{BASE}{LOGIN_PATH}", wait_until="networkidle", timeout=60000)
    page.fill('input[type="email"]', email)
    page.fill('input[type="password"]', password)
    page.click('button[type="submit"]')
    page.wait_for_url(lambda u: LOGIN_PATH not in u, timeout=30000)
    for path in PAGES:
        page.goto(f"{BASE}{path}", wait_until="networkidle", timeout=60000)
        name = path.strip("/").replace("/", "_") or "home"
        page.screenshot(path=str(OUT / f"shot_{name}.png"))
        print(f"{path} -> {page.url} -> shot_{name}.png")
    b.close()
