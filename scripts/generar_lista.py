#!/usr/bin/env python3
"""Genera Lista Clásica por país sin perder fuentes ni respaldos."""
import json
import ipaddress
import re
import unicodedata
from pathlib import Path
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parents[1]


def escape_attr(value):
    return str(value or '').replace('"', "'").replace('\n', ' ').replace('\r', ' ')


def norm(value):
    return ''.join(
        c for c in unicodedata.normalize('NFKD', str(value or '')).lower()
        if not unicodedata.combining(c)
    )


def sort_key(c):
    country = c['pais']
    country_rank = '0' if country == 'Argentina' else ('2' if country == 'Internacional' else '1')
    return f"{country_rank}|{norm(country)}|{norm(c['nombre'])}|{norm(c['tvg_id'])}"


def build(data):
    base = data['canales']
    seen = set()
    channels = []
    for channel in base:
        url = channel['url'].strip()
        parsed = urlsplit(url)
        proveedor_http = (parsed.scheme == 'http' and parsed.hostname == '200.80.230.125' and parsed.port == 5056
                          and re.fullmatch(r'/Live/[0-9a-f]{32}/[A-Za-z0-9_-]+\.playlist\.m3u8', parsed.path, re.I))
        proveedor_usuario_http = False
        if parsed.scheme == 'http' and channel.get('origen') == 'catalogo_usuario_20261123' and parsed.hostname and not parsed.query and not parsed.username and not parsed.password:
            try:
                proveedor_usuario_http = ipaddress.ip_address(parsed.hostname).is_global
            except ValueError:
                proveedor_usuario_http = False
        if not (parsed.scheme == 'https' or proveedor_http or proveedor_usuario_http) or not parsed.netloc or not parsed.path.lower().endswith('.m3u8'):
            raise ValueError(f"URL HLS no válida para {channel['nombre']}")
        if channel['categoria'] != channel['pais'] + ' TV':
            raise ValueError('Categoría por país incoherente: ' + channel['nombre'])
        if url in seen:
            continue
        seen.add(url)
        channels.append(channel)
    lines = [
        '#EXTM3U',
        '#PLAYLIST:Lista Clásica - Canales por país',
        '# Solo fuentes HLS directas compatibles con Media3; sin URLs YouTube.',
        '# Categorías por país: Argentina TV, España TV, Colombia TV, etc.',
        '# Fuentes YouTube separadas: lista_clasica_youtube.m3u (no compatible directamente con V62).',
        '# Sin tokens, firmas temporales ni claves; disponibilidad HLS no certificada en TV Box.',
        ''
    ]
    for channel in sorted(channels, key=sort_key):
        name = escape_attr(channel['nombre'])
        category = escape_attr(channel['categoria'])
        tvg_id = escape_attr(channel['tvg_id'])
        logo = escape_attr(channel.get('logo', ''))
        logo_attr = f' tvg-logo="{logo}"' if logo else ''
        lines.append(f'#EXTINF:-1 tvg-id="{tvg_id}" tvg-name="{name}"{logo_attr} group-title="{category}",{name}')
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
        for backup in channel.get('backups', []):
            backup_url = backup['url'].strip()
            p = urlsplit(backup_url)
            respaldo_usuario_http = False
            if channel.get('origen') == 'catalogo_usuario_20261123' and p.scheme == 'http' and p.hostname and not p.query and not p.username and not p.password:
                try:
                    respaldo_usuario_http = ipaddress.ip_address(p.hostname).is_global
                except ValueError:
                    respaldo_usuario_http = False
            if not (p.scheme == 'https' or respaldo_usuario_http) or not p.hostname or p.username or p.password or not p.path.lower().endswith('.m3u8'):
                raise ValueError('Respaldo HLS inválido: ' + name)
            if p.hostname == 'manifest.googlevideo.com':
                raise ValueError('No publicar respaldos de YouTube temporales')
            lines.append('#EXT-X-TVFULL-BACKUP:' + json.dumps({
                'url': backup_url, 'headers': backup.get('headers', {})
            }, ensure_ascii=False, separators=(',', ':')))
        lines.extend([channel['url'], ''])
    return '\n'.join(lines).rstrip() + '\n'


if __name__ == '__main__':
    data = json.loads((ROOT / 'fuentes.json').read_text(encoding='utf-8'))
    mundo = json.loads((ROOT / 'fuentes_mundotv.json').read_text(encoding='utf-8'))
    popular = json.loads((ROOT / 'fuentes_populares_2026.json').read_text(encoding='utf-8'))
    noviembre = json.loads((ROOT / 'fuentes_noviembre_2026.json').read_text(encoding='utf-8'))
    data['canales'].extend(mundo['canales'])
    data['canales'].extend(popular['canales'])
    data['canales'].extend(noviembre['canales'])
    netvideo = ROOT / 'fuentes_netvideo_2026.json'
    if netvideo.exists():
        data['canales'].extend(json.loads(netvideo.read_text(encoding='utf-8'))['canales'])
    tvplay_es = ROOT / 'fuentes_tvplay_es_2026.json'
    if tvplay_es.exists():
        data['canales'].extend(json.loads(tvplay_es.read_text(encoding='utf-8'))['canales'])
    regional = ROOT / 'fuentes_regionales_20261123.json'
    if regional.exists():
        data['canales'].extend(json.loads(regional.read_text(encoding='utf-8'))['canales'])
    fast_playtv = ROOT / 'fuentes_fast_playtv_20261123.json'
    if fast_playtv.exists():
        data['canales'].extend(json.loads(fast_playtv.read_text(encoding='utf-8'))['canales'])
    deportes_test = ROOT / 'fuentes_deportes_prueba_20261123.json'
    if deportes_test.exists():
        data['canales'].extend(json.loads(deportes_test.read_text(encoding='utf-8'))['canales'])
    manual = ROOT / 'fuentes_usuario_argentina_20261123.json'
    if manual.exists():
        data['canales'].extend(json.loads(manual.read_text(encoding='utf-8'))['canales'])
    path = ROOT / 'lista_clasica.m3u'
    path.write_text(build(data), encoding='utf-8')
    print(f"Creada: {path} ({len({c['url'] for c in data['canales']})} fuentes HLS únicas, YouTube separado)")
