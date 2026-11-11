#!/usr/bin/env python3
"""Lista Clásica YT: canales de YouTube en vivo para el reproductor embebido
(WebView + IFrame API) de TV FULL PRO V63 o superior.

NO son HLS: nunca se cargan en Media3 ni en lista_clasica.m3u.
Se publican los canales con `channel_id` verificado (el reproductor abre el
directo actual con youtube.com/embed/live_stream?channel=UC…) y, cuando no hay
ID de canal, los que tienen `video_id` de un directo 24 h. El resto queda en
youtube_en_vivo.json como pendiente.
"""
import json
import re
from pathlib import Path
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parents[1]
CHANNEL_ID = re.compile(r'UC[A-Za-z0-9_-]{22}')
VIDEO_ID = re.compile(r'[A-Za-z0-9_-]{11}')
HORARIOS = {'24h', 'programado'}
ORDEN_CATEGORIAS = [
    'Noticias Argentina',
    'TV Regional Argentina',
    'Deportes',
    'Streaming, radio y música',
    'Internacionales',
]


def texto_seguro(valor, campo, nombre):
    valor = str(valor or '')
    if any(x in valor for x in '\r\n"') or len(valor) > 240:
        raise ValueError(f'Campo {campo} inválido: {nombre}')
    return valor


def listos(datos):
    """Canales publicables: con channel_id o, si no hay, video_id válido."""
    return [c for c in datos['canales']
            if CHANNEL_ID.fullmatch(c.get('channel_id', '')) or VIDEO_ID.fullmatch(c.get('video_id', ''))]


def orden(c):
    cat = c['categoria']
    pos = ORDEN_CATEGORIAS.index(cat) if cat in ORDEN_CATEGORIAS else len(ORDEN_CATEGORIAS)
    return (pos, c['nombre'].casefold())


def url_canal(channel_id):
    return f'https://www.youtube.com/channel/{channel_id}/live'


def url_publicada(c):
    if CHANNEL_ID.fullmatch(c.get('channel_id', '')):
        return url_canal(c['channel_id'])
    return f"https://www.youtube.com/watch?v={c['video_id']}"


def generar(datos):
    canales = sorted(listos(datos), key=orden)
    lines = [
        '#EXTM3U',
        '#PLAYLIST:Lista Clásica YT - YouTube en vivo',
        '# Solo para el reproductor YouTube embebido (WebView) de TV FULL PRO V63 o superior.',
        '# NO son HLS: no cargar en Media3 ni mezclar con lista_clasica.m3u.',
        '# Cada URL abre el directo actual del canal; fuera de horario el reproductor muestra "sin transmisión".',
        '',
    ]
    for c in canales:
        nombre = texto_seguro(c['nombre'], 'nombre', c['nombre'])
        categoria = texto_seguro(c['categoria'], 'categoria', nombre)
        tvg_id = texto_seguro(c['tvg_id'], 'tvg_id', nombre)
        logo = texto_seguro(c.get('logo', ''), 'logo', nombre)
        horario = c.get('horario', 'programado')
        if horario not in HORARIOS:
            raise ValueError('Horario inválido: ' + nombre)
        if c.get('categoria') not in ORDEN_CATEGORIAS:
            raise ValueError('Categoría no permitida: ' + nombre)
        url = url_publicada(c)
        if c['url_permanente'] != url:
            raise ValueError('url_permanente no coincide con channel_id/video_id: ' + nombre)
        attrs = [f'tvg-id="{tvg_id}"', f'tvg-name="{nombre}"']
        if logo:
            attrs.append(f'tvg-logo="{logo}"')
        attrs += [
            f'group-title="{categoria}"',
            'tvfull-player="youtube"',
        ]
        if c.get('channel_id'):
            attrs.append(f'tvfull-youtube-channel="{c["channel_id"]}"')
        else:
            attrs.append(f'tvfull-youtube-video="{c["video_id"]}"')
        alt = c.get('video_alternativo', '')
        if alt:
            if not VIDEO_ID.fullmatch(alt):
                raise ValueError('video_alternativo inválido: ' + nombre)
            # Respaldo para futuras versiones si el directo del canal falla.
            attrs.append(f'tvfull-youtube-video-alt="{alt}"')
        attrs.append(f'tvfull-horario="{horario}"')
        lines.extend([f'#EXTINF:-1 {" ".join(attrs)},{nombre}', url, ''])
    return '\n'.join(lines).rstrip() + '\n'


if __name__ == '__main__':
    d = json.loads((ROOT / 'youtube_en_vivo.json').read_text(encoding='utf-8'))
    (ROOT / 'lista_clasica_youtube.m3u').write_text(generar(d), encoding='utf-8')
    total, publicados = len(d['canales']), len(listos(d))
    print(f'Lista Clásica YT generada: {publicados} canales publicados, {total - publicados} pendientes')
