#!/usr/bin/env python3
"""Check 2026 HLS candidates by fetching manifests and FFmpeg video decoding.
This tests remote runner capability, not all geographies nor redistribution rights.
"""
import concurrent.futures
import json
import subprocess
import time
import urllib.request
from pathlib import Path
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parents[1]
P = ROOT / "diagnosticos/auditoria_populares_20261111.json"
OUT = ROOT / "diagnosticos/resultado_populares_20261111.json"
UA = "Mozilla/5.0 (Linux; Android 12; Android TV) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36"


def check(c):
    start = time.monotonic()
    obj = {k: c[k] for k in ("nombre", "tvg_id", "url", "tipo", "origen")}
    obj.update(manifest=False, video=False, ok=False)
    try:
        url = c["url"]
        parts = urlsplit(url)
        if parts.scheme != "https" or not parts.hostname or not parts.path.lower().endswith(".m3u8"):
            raise ValueError("Not direct HTTPS HLS")
        req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "*/*"})
        with urllib.request.urlopen(req, timeout=14) as res:
            body = res.read(150000).decode("utf-8-sig", errors="replace")
            obj["status_code"] = res.status
            obj["redirect_host"] = urlsplit(res.url).hostname
        if not body.lstrip().startswith("#EXTM3U") or not any(x in body for x in ("#EXT-X-STREAM-INF", "#EXTINF:", "#EXT-X-TARGETDURATION")):
            raise ValueError("HTTP reachable but not HLS master/media playlist")
        obj["manifest"] = True
        # ffprobe validation of stream index first; ffmpeg must decode actual frames.
        cmd = ["ffmpeg", "-hide_banner", "-nostdin", "-v", "error", "-rw_timeout", "12000000", "-user_agent", UA,
               "-i", url, "-map", "0:v:0", "-t", "2", "-f", "null", "-"]
        p = subprocess.run(cmd, capture_output=True, text=True, timeout=48)
        if p.returncode != 0:
            raise ValueError("FFmpeg decode failed: " + p.stderr.strip()[-210:])
        obj["video"] = True
        obj["ok"] = True
        obj["status"] = "HLS and real video decoded from runner"
    except subprocess.TimeoutExpired:
        obj["status"] = "FFmpeg timeout"
    except Exception as err:
        obj["status"] = str(err)[:260]
    obj["seconds"] = round(time.monotonic() - start, 1)
    return obj


def main():
    channels = json.loads(P.read_text(encoding="utf-8"))["canales"]
    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as pool:
        rows = list(pool.map(check, channels))
    for row in rows:
        print("RESULT | " + ("PASS" if row["ok"] else "FAIL") + " | " + row["nombre"] + " | " + row["status"] + " | " + str(row["seconds"]) + "s", flush=True)
    OUT.write_text(json.dumps({
        "date": "2026-11-11", "method": "HTTP #EXTM3U + FFmpeg 2sec decoded video on GitHub Actions",
        "passing": sum(row["ok"] for row in rows), "total": len(rows), "rows": rows
    }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("TOTAL: " + str(sum(row["ok"] for row in rows)) + "/" + str(len(rows)))


if __name__ == "__main__":
    main()
