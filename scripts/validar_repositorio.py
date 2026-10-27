#!/usr/bin/env python3
"""Validación offline; no comprueba reproducción ni descarga video."""
import json
import re
from pathlib import Path
from urllib.parse import urlsplit, parse_qsl

ROOT = Path(__file__).resolve().parents[1]


def main():
    hls = json.loads((ROOT / 'fuentes.json').read_text(encoding='utf-8'))['canales']
    youtube = json.loads((ROOT / 'youtube_en_vivo.json').read_text(encoding='utf-8'))['canales']
    assert hls and youtube, 'Catálogos vacíos'
    assert len({c['tvg_id'] for c in hls}) == len(hls), 'Canales HLS duplicados'
    assert len({c['tvg_id'] for c in youtube}) == len(youtube), 'Canales YouTube duplicados'

    for channel in hls:
        url = channel['url'].strip()
        parts = urlsplit(url)
        assert parts.scheme == 'https' and parts.hostname, 'URL inválida: ' + channel['nombre']
        assert parts.path.lower().endswith('.m3u8'), 'Señal no HLS: ' + channel['nombre']
        assert parts.hostname != 'manifest.googlevideo.com', 'Manifiesto temporal'
        assert not parts.username and not parts.password, 'Credenciales en URL'
        params = {name.lower() for name, _ in parse_qsl(parts.query, keep_blank_values=True)}
        assert not params.intersection({'access_token', 'token', 'sig', 'signature', 'expire', 'sid', 'uid'}), 'Parámetros temporales'
        assert not re.search(r'[\r\n]', url), 'Salto de línea en URL'

    for channel in youtube:
        url = channel['url_permanente'].strip()
        parts = urlsplit(url)
        assert parts.scheme == 'https' and parts.hostname in {'youtube.com', 'www.youtube.com'}
        assert parts.path.endswith('/live') and not parts.query, 'Enlace YouTube no permanente'
        assert 'manifest.googlevideo.com' not in json.dumps(channel)

    for filename in ('lista_clasica.m3u', 'lista_clasica_youtube.m3u'):
        content = (ROOT / filename).read_text(encoding='utf-8')
        assert content.startswith('#EXTM3U\n'), 'Encabezado M3U inválido'
        assert 'manifest.googlevideo.com' not in content
        assert 'access_token=' not in content and 'expire/' not in content
        assert content.count('#EXTINF:') == len(hls if filename == 'lista_clasica.m3u' else youtube)

    print(f'OK: {len(hls)} HLS y {len(youtube)} YouTube, sin sesiones privadas.')
    print('Advertencia: pruebas estructurales, no certificación de disponibilidad.')


if __name__ == '__main__':
    main()
