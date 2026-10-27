#!/usr/bin/env python3
"""Verifica solamente manifiestos HLS, no confirma audio/video continuo."""
import json
import ssl
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TIMEOUT = 7
MAX_MANIFEST = 256 * 1024


def check(name, url):
    req = urllib.request.Request(url, headers={
        'User-Agent': 'Canales-Free-Playlist-Check/1.0',
        'Accept': 'application/vnd.apple.mpegurl,application/x-mpegURL,*/*',
    })
    try:
        with urllib.request.urlopen(req, timeout=TIMEOUT, context=ssl.create_default_context()) as response:
            data = response.read(MAX_MANIFEST + 1)
            if len(data) > MAX_MANIFEST:
                return {'canal': name, 'estado': 'invalido', 'detalle': 'Manifiesto demasiado grande'}
            if not data.lstrip(b'\xef\xbb\xbf\r\n \t').startswith(b'#EXTM3U'):
                return {'canal': name, 'estado': 'invalido', 'detalle': 'Respuesta no es HLS'}
            return {'canal': name, 'estado': 'manifiesto', 'detalle': 'M3U8 respondió; verificar segmentos y video'}
    except urllib.error.HTTPError as e:
        return {'canal': name, 'estado': 'error', 'detalle': f'HTTP {e.code}'}
    except (urllib.error.URLError, TimeoutError, OSError) as e:
        return {'canal': name, 'estado': 'error', 'detalle': type(e).__name__}


if __name__ == '__main__':
    sources = json.loads((ROOT / 'fuentes.json').read_text(encoding='utf-8'))
    results = [check(c['nombre'], c['url']) for c in sources['canales']]
    (ROOT / 'reporte_verificacion.json').write_text(
        json.dumps({'nombre': sources['nombre'], 'resultados': results}, ensure_ascii=False, indent=2) + '\n',
        encoding='utf-8')
    for r in results:
        print(f"{r['canal']}: {r['estado']} - {r['detalle']}")
    print('Nota: no demuestra reproducción fluida ni disponibilidad regional.')
