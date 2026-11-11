#!/usr/bin/env python3
"""Genera Lista Clásica por país sin perder fuentes ni respaldos."""
import json
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
        if parsed.scheme != 'https' or not parsed.netloc or not parsed.path.lower().endswith('.m3u8'):
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
            if p.scheme != 'https' or not p.hostname or not p.path.lower().endswith('.m3u8'):
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
    data['canales'].extend(mundo['canales'])
    data['canales'].extend(popular['canales'])
    path = ROOT / 'lista_clasica.m3u'
    path.write_text(build(data), encoding='utf-8')
    print(f"Creada: {path} ({len({c['url'] for c in data['canales']})} fuentes HLS únicas, YouTube separado)")
