#!/usr/bin/env python3
"""Audita candidatos HLS en runner GitHub, sin modificar la playlist de producción."""
import concurrent.futures
import json
import subprocess
import time
import urllib.error
import urllib.request
from pathlib import Path
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "diagnosticos/populares_candidatos_20261111.json"
RESULT = ROOT / "diagnosticos/resultado_populares_20261111.json"
UA = "Mozilla/5.0 (Linux; Android 12; Android TV) AppleWebKit/537.36 Chrome/120.0 Safari/537.36"


def probe(ch):
    started = time.monotonic()
    out = {key: ch[key] for key in ("nombre", "tvg_id", "pais", "url")}
    out["ok"] = False
    try:
        parsed = urlsplit(ch["url"])
        if parsed.scheme != "https" or not parsed.path.lower().endswith(".m3u8") or parsed.username:
            raise ValueError("No es HTTPS HLS directo")
        headers = {"User-Agent": UA, "Accept": "*/*"}
        if ch.get("referrer"):
            headers["Referer"] = ch["referrer"]
        request = urllib.request.Request(ch["url"], headers=headers)
        with urllib.request.urlopen(request, timeout=12) as resp:
            data = resp.read(262144)
            out["http"] = resp.status
            out["final_host"] = urlsplit(resp.url).hostname
        text = data.decode("utf-8-sig", errors="replace")
        if not text.lstrip().startswith("#EXTM3U") or (
            "#EXT-X-STREAM-INF" not in text and "#EXTINF:" not in text
        ):
            raise ValueError("HTTP OK pero no devuelve un manifiesto HLS")
        out["manifest"] = True
        cmd = [
            "ffmpeg", "-hide_banner", "-nostdin", "-v", "error",
            "-rw_timeout", "10000000", "-user_agent", UA,
        ]
        if ch.get("referrer"):
            cmd += ["-headers", "Referer: " + ch["referrer"] + "\r\n"]
        cmd += [
            "-i", ch["url"], "-t", "1", "-map", "0:v:0",
            "-an", "-f", "null", "-",
        ]
        p = subprocess.run(cmd, capture_output=True, text=True, timeout=36)
        out["decode"] = p.returncode == 0
        if p.returncode != 0:
            raise ValueError("FFmpeg no decodificó video: " + p.stderr.strip()[-200:])
        out["ok"] = True
        out["diagnostico"] = "Manifiesto accesible y FFmpeg decodificó video"
    except subprocess.TimeoutExpired:
        out["diagnostico"] = "Tiempo agotado durante decodificación"
    except Exception as err:
        out["diagnostico"] = str(err)[:350]
    out["elapsed_s"] = round(time.monotonic() - started, 2)
    return out


def main():
    channels = json.loads(SOURCE.read_text(encoding="utf-8"))["canales"]
    with concurrent.futures.ThreadPoolExecutor(max_workers=7) as pool:
        results = list(pool.map(probe, channels))
    for x in results:
        print(f"{'OK  ' if x['ok'] else 'FAIL'} {x['nombre']}: {x['diagnostico']} ({x['elapsed_s']}s)", flush=True)
    RESULT.parent.mkdir(parents=True, exist_ok=True)
    RESULT.write_text(json.dumps({
        "fecha": "2026-11-11",
        "criterio": "HTTP HLS más 1 segundo de decodificación con FFmpeg en Ubuntu; no certifica reproducción regional en TV",
        "total": len(results),
        "aprobados": sum(x["ok"] for x in results),
        "resultados": results,
    }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"RESULTADO: {sum(x['ok'] for x in results)}/{len(results)} probados OK.")


if __name__ == "__main__":
    main()
