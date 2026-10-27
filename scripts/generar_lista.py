#!/usr/bin/env python3
"""Genera Lista Clásica M3U desde fuentes.json; no usa TV FULL PRO."""
import json
from pathlib import Path
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parents[1]


def escape_attr(value):
    return str(value).replace('"', "'").replace('\n', ' ').replace('\r', ' ')


def build(data):
    lines = [
        '#EXTM3U',
        '#PLAYLIST:Lista Clásica - Canales gratuitos',
        '# Proyecto: Canales (independiente de TV FULL PRO)',
        '# Solo HLS directo: sin enlaces watch de YouTube, sin cuentas Xtream ni DRM',
        '# IMPORTANTE: enlaces de prueba, disponibilidad sujeta a verificación',
        '',
    ]
    seen = set()
    for channel in data['canales']:
        url = channel['url'].strip()
        parsed = urlsplit(url)
        if parsed.scheme != 'https' or not parsed.netloc or not parsed.path.lower().endswith('.m3u8'):
            raise ValueError(f"URL HLS no válida para {channel['nombre']}")
        if url in seen:
            continue
        seen.add(url)
        name = escape_attr(channel['nombre'])
        category = escape_attr(channel['categoria'])
        tvg_id = escape_attr(channel['tvg_id'])
        lines += [f'#EXTINF:-1 tvg-id="{tvg_id}" tvg-name="{name}" group-title="{category}",{name}', url, '']
    return '\n'.join(lines).rstrip() + '\n'


if __name__ == '__main__':
    data = json.loads((ROOT / 'fuentes.json').read_text(encoding='utf-8'))
    path = ROOT / 'lista_clasica.m3u'
    path.write_text(build(data), encoding='utf-8')
    print(f"Creada: {path} ({len(data['canales'])} canales)")
