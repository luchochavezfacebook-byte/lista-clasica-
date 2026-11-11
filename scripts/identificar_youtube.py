#!/usr/bin/env python3
"""Identifica videos de YouTube pendientes con oEmbed (API pública oficial).

Solo lectura: no modifica la lista. Imprime título y canal de cada video
pendiente o publicado por video_id, y si YouTube permite embeberlo.
"""
import json
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def oembed(video_id):
    url = 'https://www.youtube.com/oembed?format=json&url=' + urllib.parse.quote(
        f'https://www.youtube.com/watch?v={video_id}', safe='')
    try:
        with urllib.request.urlopen(url, timeout=15) as r:
            data = json.load(r)
            return 'ok', data.get('title', ''), data.get('author_name', ''), data.get('author_url', '')
    except urllib.error.HTTPError as e:
        estado = {401: 'no-embebible', 403: 'no-embebible', 404: 'no-existe', 400: 'invalido'}.get(e.code, f'http-{e.code}')
        return estado, '', '', ''
    except (urllib.error.URLError, TimeoutError) as e:
        return 'red', type(e).__name__, '', ''


if __name__ == '__main__':
    canales = json.loads((ROOT / 'youtube_en_vivo.json').read_text(encoding='utf-8'))['canales']
    for c in canales:
        vid = c.get('video_id') or c.get('video_id_pendiente') or c.get('video_alternativo')
        if not vid:
            continue
        estado, titulo, autor, autor_url = oembed(vid)
        linea = f'{c["nombre"]} | {vid} | {estado} | {autor} | {autor_url} | {titulo}'
        print(f'::notice title=youtube-{vid}::{linea}')
