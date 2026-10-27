#!/usr/bin/env python3
"""Lista complementaria para aplicaciones que admitan YouTube, NO HLS directo."""
import json
from pathlib import Path
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parents[1]


def generar(datos):
    lines = [
        '#EXTM3U',
        '#PLAYLIST:Lista Clasica - YouTube Live (reproductor compatible)',
        '# AVISO: enlaces /live de YouTube, NO son m3u8 ni compatibles con todos los IPTV',
        '',
    ]
    for c in datos['canales']:
        u = c['url_permanente']
        p = urlsplit(u)
        if p.scheme != 'https' or p.hostname not in ('www.youtube.com', 'youtube.com') or not p.path.endswith('/live'):
            raise ValueError('URL permanente invalida: ' + c['nombre'])
        for field in ('nombre', 'categoria', 'tvg_id'):
            if any(x in c[field] for x in '\r\n"'):
                raise ValueError('Campo invalido')
        lines.extend([
            f'#EXTINF:-1 tvg-id="{c["tvg_id"]}" group-title="{c["categoria"]}",{c["nombre"]}',
            u, ''
        ])
    return '\n'.join(lines).rstrip() + '\n'


if __name__ == '__main__':
    d = json.loads((ROOT / 'youtube_en_vivo.json').read_text(encoding='utf-8'))
    (ROOT / 'lista_clasica_youtube.m3u').write_text(generar(d), encoding='utf-8')
    print('Lista YouTube generada:', len(d['canales']), 'referencias')
