# -*- coding: utf-8 -*-
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

BASE_URL = "https://boneriolocal.com.ar/"
DEST_DIR = Path(r"C:\Users\crist\.gemini\antigravity\scratch\alphabonos")
DATA_DIR = DEST_DIR / "data"
DATA_DIR.mkdir(parents=True, exist_ok=True)

FILES_TO_FETCH = [
    "data/alertas_vivo.json",
    "data/bandas.json",
    "data/calendario.json",
    "data/calificaciones.json",
    "data/closes.json",
    "data/closes_ars.json",
    "data/dolar.json",
    "data/flujos.xlsx",
    "data/fred_spreads.json",
    "data/indices.json",
    "data/intra.json",
    "data/intra_bonos.json",
    "data/intra_hist.json",
    "data/logos.json",
    "data/ons.json",
    "data/ons_cierre.json",
    "data/ons_emisores.json",
    "data/ons_vn.json",
    "data/outstanding.json",
    "data/pvs.json",
    "data/pvs_cierre.json",
    "data/pvs_emisores.json",
    "data/relativos.json",
    "data/riesgo_pais.json",
    "data/riesgo_vivo.json",
    "data/tasas.json",
    "data/ust.json",
    "data/volumen.json",
    "data/volumen_lite.json",
    "data/licitaciones.json",
    "licitaciones.html",
]

def fetch_one(rel):
    target = DEST_DIR / rel
    if target.exists() and target.stat().st_size > 0:
        return f"[SKIP] {rel} ({target.stat().st_size:,} bytes)"
    target.parent.mkdir(parents=True, exist_ok=True)
    url = BASE_URL + rel
    try:
        req = urllib.request.Request(
            url,
            headers={
                "User-Agent": "Mozilla/5.0",
                "Accept-Encoding": "gzip, deflate",
            },
        )
        with urllib.request.urlopen(req, timeout=25) as resp:
            raw = resp.read()
            if resp.headers.get("Content-Encoding") == "gzip":
                import gzip
                raw = gzip.decompress(raw)
        target.write_bytes(raw)
        return f"[OK] {rel} ({len(raw):,} bytes)"
    except Exception as e:
        return f"[WARN] {rel}: {e}"

if __name__ == "__main__":
    with ThreadPoolExecutor(max_workers=10) as ex:
        futs = [ex.submit(fetch_one, r) for r in FILES_TO_FETCH]
        for f in as_completed(futs):
            print(f.result(), flush=True)
