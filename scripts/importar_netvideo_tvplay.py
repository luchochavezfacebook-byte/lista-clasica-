#!/usr/bin/env python3
"""Importación controlada de las señales HLS autorizadas de Netvideo TvPlay.

Selecciona únicamente 28 canales ausentes de Lista Clásica, verificados
con manifiesto+fragmento+video en dos ejecuciones independientes
del 22/11/2026. Sin credenciales ni autenticación.
"""
import datetime as dt
import json
import re
import urllib.request
from pathlib import Path
from urllib.parse import urljoin, urlsplit

ROOT = Path(__file__).resolve().parents[1]
BASE = "http://200.80.230.125:5056/"
IDS = [
    "online-24-7", "c5n", "tvpublica", "CronicaTv", "rural", "tierramiatv",
    "telefe", "lntv", "canal9televida", "Ciudadmagazine", "freyre",
    "MediosProvincia", "fmirelive", "telesolsanjuan", "RTNNeuquen",
    "docemisiones", "silverchannel", "nuevotiempo", "rttve",
    "novotempo", "Extrema", "alientovision", "RedAvenir",
    "ComunionTV", "musictop", "RadioUrbana", "retro", "enlace"
]
DISPLAY = {
    "online-24-7": "Online 24/7",
    "c5n": "C5N", "tvpublica": "TV Pública",
    "CronicaTv": "Crónica TV", "rural": "Rural",
    "tierramiatv": "Tierra Mía TV", "telefe": "Telefe (nacional)",
    "lntv": "La Nación+ (LN+)", "canal9televida": "Canal 9 Televida",
    "Ciudadmagazine": "Ciudad Magazine", "freyre": "Freyre TV",
    "MediosProvincia": "Medios Provincia", "fmirelive": "IRE",
    "telesolsanjuan": "Telesol San Juan", "RTNNeuquen": "RTN Neuquén",
    "docemisiones": "Canal 12 Misiones", "silverchannel": "Silver Channel",
    "nuevotiempo": "Nuevo Tiempo", "rttve": "RT en Español",
    "novotempo": "Novo Tempo", "Extrema": "Extrema TV",
    "alientovision": "Aliento Visión", "RedAvenir": "Red Avenir",
    "ComunionTV": "Comunión TV", "musictop": "Music Top",
    "RadioUrbana": "Radio Urbana", "retro": "Retro TV", "enlace": "Enlace"
}
INTERNATIONAL = {
    "online-24-7", "silverchannel", "nuevotiempo", "rttve",
    "Extrema", "alientovision", "RedAvenir", "ComunionTV", "enlace"
}

def fetch(url, limit=180000):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=15) as response:
        return response.read(limit), response.headers.get("Content-Type", "")

page = fetch(BASE + "?tvwatch")[0].decode("utf-8", errors="replace")
marker = "var Streams = "
start = page.find(marker)
end = page.find("];", start)
if start < 0 or end < 0:
    raise RuntimeError("No se encontró la grilla TvPlay")
streams = json.loads(page[start + len(marker):end + 1])
provider = {c["m3u8"]: c for c in streams}
assert len(IDS) == len(set(IDS)), "ID importado duplicado"
assert len(IDS) == 28, "Revisar recuento de canales"
assert all(channel_id in provider for channel_id in IDS), "Faltan canales declarados en el sitio"

existing = []
for filename in ("fuentes.json", "fuentes_mundotv.json", "fuentes_populares_2026.json", "fuentes_noviembre_2026.json"):
    existing.extend(json.loads((ROOT / filename).read_text(encoding="utf-8"))["canales"])
existing_urls = {c["url"] for c in existing}
existing_names = {c["nombre"].casefold() for c in existing}
existing_ids = {c["tvg_id"] for c in existing}
imported = []
for channel_id in IDS:
    original = provider[channel_id]
    url = original.get("url", "")
    parts = urlsplit(url)
    if (parts.scheme != "http" or parts.hostname != "200.80.230.125"
        or parts.port != 5056 or parts.query
        or not re.fullmatch(r"/Live/[0-9a-f]{32}/[A-Za-z0-9_-]+\.playlist\.m3u8", parts.path, re.I)
        or parts.path.rsplit("/", 1)[-1] != channel_id + ".playlist.m3u8"):
        raise ValueError("Fuente externa inesperada para " + channel_id)
    name = DISPLAY[channel_id]
    tvg_id = "NetvideoTVPlay." + channel_id
    if url in existing_urls or name.casefold() in existing_names or tvg_id in existing_ids:
        raise ValueError("Posible canal duplicado: " + name)
    country = "Brasil" if channel_id == "novotempo" else ("Internacional" if channel_id in INTERNATIONAL else "Argentina")
    entry = {
        "nombre": name, "tvg_id": tvg_id, "pais": country,
        "categoria": country + " TV", "url": url,
        "origen": "Netvideo TvPlay, proporcionado por el proveedor",
        "verificacion": "2026-11-22: manifiesto HLS, primer segmento y >=20 fotogramas en dos muestras FFmpeg GitHub Actions. Pendiente continuidad, audio e imagen en TV Box Argentina.",
        "user_agent": "Mozilla/5.0"
    }
    poster = original.get("poster", "")
    if poster and not poster.startswith(("http:", "https:", "//")) and ".." not in poster:
        logo_url = urljoin(BASE, poster.lstrip("/"))
        if urlsplit(logo_url).hostname == "200.80.230.125":
            try:
                blob, kind = fetch(logo_url, 150)
                if blob and kind.lower().startswith("image/"):
                    entry["logo"] = logo_url
            except Exception:
                pass
    imported.append(entry)
    existing_urls.add(url)
    existing_ids.add(tvg_id)
    existing_names.add(name.casefold())
    print("IMPORTADO", name, "(logo)" if "logo" in entry else "(sin logo)", flush=True)

payload = {
    "nombre": "Canales Netvideo TvPlay autorizados, nuevos en Lista Clásica",
    "fecha": "2026-11-22",
    "nota": "Fuentes HTTP del servidor del proveedor, verificadas en dos muestras con GitHub Actions. La disponibilidad puede depender de red o región; no reemplazar canales preexistentes.",
    "canales": imported
}
target = ROOT / "fuentes_netvideo_2026.json"
target.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
print("IMPORT_OK", len(imported), "fuentes nuevas. No se cambiaron fuentes antiguas.", flush=True)
