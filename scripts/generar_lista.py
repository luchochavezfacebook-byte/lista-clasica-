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
        lines.append(f'#EXTINF:-1 tvg-id="{tvg_id}" tvg-name="{name}" group-title="{category}",{name}')
        # V62 acepta EXTVLCOPT para las fuentes con encabezado HTTP declarado.
        # No incluir cookies, autorización, firmas ni tokens en listas públicas.
        user_agent = channel.get('user_agent', '').strip()
        if user_agent:
            if len(user_agent) > 240 or any(ord(char) < 32 for char in user_agent):
                raise ValueError('User-Agent inválido: ' + name)
            lines.append('#EXTVLCOPT:http-user-agent=' + user_agent)
        referrer = channel.get('referrer', '').strip()
        if referrer:
            if not referrer.startswith('https://') or len(referrer) > 240 or any(ord(c) < 32 for c in referrer):
                raise ValueError('Referer inválido: ' + name)
            lines.append('#EXTVLCOPT:http-referrer=' + referrer)
        # Los respaldos locales se activan solo ante error en el reproductor V62.
        # Sin firmas, cookies ni credenciales privadas en el repositorio público.
        for backup in channel.get('backups', []):
            backup_url = backup['url'].strip()
            p = urlsplit(backup_url)
            if p.scheme != 'https' or not p.hostname or not p.path.lower().endswith('.m3u8'):
                raise ValueError('Respaldo HLS inválido: ' + name)
            if p.hostname == 'manifest.googlevideo.com':
                raise ValueError('Respaldo de sesión YouTube temporal')
            headers = backup.get('headers', {})
            lines.append('#EXT-X-TVFULL-BACKUP:' + json.dumps(
                {'url': backup_url, 'headers': headers},
                ensure_ascii=False, separators=(',', ':')))
        lines.extend([url, ''])
    return '\n'.join(lines).rstrip() + '\n'


if __name__ == '__main__':
    data = json.loads((ROOT / 'fuentes.json').read_text(encoding='utf-8'))
    path = ROOT / 'lista_clasica.m3u'
    path.write_text(build(data), encoding='utf-8')
    print(f"Creada: {path} ({len(data['canales'])} canales)")
