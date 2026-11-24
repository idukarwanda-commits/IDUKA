from pathlib import Path
from urllib.request import urlopen
import hashlib

URL = "https://archive.ics.uci.edu/static/public/352/online+retail.zip"
OUT_DIR = Path(__file__).resolve().parents[1] / "data" / "raw"
ZIP_PATH = OUT_DIR / "uci_online_retail_original.zip"

OUT_DIR.mkdir(parents=True, exist_ok=True)
print("Downloading the UCI Online Retail source archive...")
with urlopen(URL, timeout=120) as response:
    payload = response.read()

ZIP_PATH.write_bytes(payload)
sha256 = hashlib.sha256(payload).hexdigest()
print(f"Saved original archive: {ZIP_PATH}")
print(f"Bytes: {len(payload):,}")
print(f"SHA-256: {sha256}")
print("Do not edit or overwrite this source archive.")
print("Extract a working copy of Online Retail.xlsx for analysis; keep the archive unchanged.")
