# -*- coding: utf-8 -*-
"""
AlphaBonos · Servidor Local de Renta Fija & Macro Argentina
Corre en http://localhost:8060 (en paralelo a AlphaQuant en el puerto 8050).
Sirve la terminal analítica y mantiene actualizadas las bases en data/*.json.
"""

import gzip
import http.server
import json
import os
import socketserver
import threading
import time
import urllib.request
from datetime import datetime
from pathlib import Path

PORT = int(os.environ.get("PORT", 8060))
BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
DATA_DIR.mkdir(parents=True, exist_ok=True)

REMOTE_DATA_BASE = "https://boneriolocal.com.ar/"


def _fetch_url(url: str, timeout: int = 15) -> bytes:
    req = urllib.request.Request(
        url,
        headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AlphaBonos/1.0",
            "Accept-Encoding": "gzip, deflate",
        },
    )
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        raw = resp.read()
        if resp.headers.get("Content-Encoding") == "gzip":
            raw = gzip.decompress(raw)
        return raw


def sync_file_if_stale(rel_path: str, max_age_sec: int = 3600 * 4) -> bool:
    """Intenta refrescar un archivo de data/ si tiene más de max_age_sec segundos."""
    target = BASE_DIR / rel_path.lstrip("/")
    if target.exists() and target.stat().st_size > 0:
        age = time.time() - target.stat().st_mtime
        if age < max_age_sec:
            return False
    try:
        raw = _fetch_url(REMOTE_DATA_BASE + rel_path.lstrip("/"), timeout=12)
        if raw and len(raw) > 10:
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(raw)
            return True
    except Exception:
        pass
    return False


def update_autonomous_feeds():
    """
    Actualizador autónomo de respaldo desde APIs públicas (data912 y ArgentinaDatos):
    Actualiza riesgo_pais.json y cierres del día en caso de que el origen estático no esté disponible.
    """
    try:
        raw_rp = _fetch_url("https://api.argentinadatos.com/v1/finanzas/indices/riesgo-pais", timeout=10)
        rp_list = json.loads(raw_rp.decode("utf-8"))
        if isinstance(rp_list, list) and len(rp_list) > 100:
            formatted = [[item["fecha"], item["valor"]] for item in rp_list if "fecha" in item and "valor" in item]
            rp_file = DATA_DIR / "riesgo_pais.json"
            if formatted:
                rp_file.write_text(json.dumps(formatted, ensure_ascii=False), encoding="utf-8")
    except Exception:
        pass


class AlphaBonosHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(BASE_DIR), **kwargs)

    def log_message(self, format, *args):
        # Log limpio y silencioso para recursos estáticos frecuentes
        pass

    def end_headers(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Cache-Control", "no-cache")
        super().end_headers()

    def do_GET(self):
        clean_path = self.path.split("?")[0]

        if clean_path == "/api/status":
            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.end_headers()
            files = list(DATA_DIR.glob("*.json"))
            payload = {
                "status": "ok",
                "app": "AlphaBonos",
                "port": PORT,
                "datasets": len(files),
                "timestamp": datetime.now().isoformat(),
            }
            self.wfile.write(json.dumps(payload).encode("utf-8"))
            return

        # Si pide un archivo en /data/*.json y no existe o está vencido, lo sincroniza en background
        if clean_path.startswith("/data/") and clean_path.endswith(".json"):
            local_file = BASE_DIR / clean_path.lstrip("/")
            if not local_file.exists():
                sync_file_if_stale(clean_path, max_age_sec=0)
            else:
                age = time.time() - local_file.stat().st_mtime
                if age > 3600 * 4:
                    threading.Thread(target=sync_file_if_stale, args=(clean_path,), daemon=True).start()

        return super().do_GET()


class ThreadedHTTPServer(socketserver.ThreadingMixIn, http.server.HTTPServer):
    daemon_threads = True
    allow_reuse_address = True


def background_sync_loop():
    """Hilo de sincronización periódica para mantener curvas y series al día."""
    core_files = [
        "data/closes.json",
        "data/closes_ars.json",
        "data/dolar.json",
        "data/tasas.json",
        "data/riesgo_pais.json",
        "data/riesgo_vivo.json",
        "data/indices.json",
        "data/intra.json",
        "data/intra_bonos.json",
        "data/ons.json",
        "data/ons_cierre.json",
        "data/pvs.json",
        "data/pvs_cierre.json",
        "data/relativos.json",
        "data/volumen_lite.json",
        "data/alertas_vivo.json",
    ]
    while True:
        try:
            for f in core_files:
                sync_file_if_stale(f, max_age_sec=3600 * 2)
            update_autonomous_feeds()
        except Exception:
            pass
        time.sleep(1800)


if __name__ == "__main__":
    threading.Thread(target=background_sync_loop, daemon=True).start()
    print("=" * 62)
    print(f"  ALPHABONOS · TERMINAL DE RENTA FIJA & MACRO LOCAL")
    print(f"  URL Local : http://localhost:{PORT}")
    print(f"  Directorio: {BASE_DIR}")
    print("=" * 62)
    with ThreadedHTTPServer(("0.0.0.0", PORT), AlphaBonosHandler) as httpd:
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nCerrando servidor AlphaBonos...")
