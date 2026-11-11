#!/usr/bin/env python3
"""Validación offline; no comprueba reproducción ni descarga video."""
import json
import re
from pathlib import Path
from urllib.parse import urlsplit, parse_qsl

ROOT = Path(__file__).resolve().parents[1]


def main():
    hls = json.loads((ROOT / 'fuentes.json').read_text(encoding='utf-8'))['canales']
    mundo = json.loads((ROOT / 'fuentes_mundotv.json').read_text(encoding='utf-8'))['canales']
    popular = json.loads((ROOT / 'fuentes_populares_2026.json').read_text(encoding='utf-8'))['canales']
    all_hls = hls + mundo + popular
    youtube = json.loads((ROOT / 'youtube_en_vivo.json').read_text(encoding='utf-8'))['canales']
    assert hls and mundo and popular and youtube, 'Catálogos vacíos'
    assert len({c['tvg_id'] for c in all_hls}) == len(all_hls), 'IDs HLS duplicados'
    assert len({c['tvg_id'] for c in youtube}) == len(youtube), 'Canales YouTube duplicados'

    for channel in all_hls:
        assert channel.get('pais') and channel.get('categoria') == channel['pais'] + ' TV', 'País/categoría inválido: ' + channel['nombre']
        url = channel['url'].strip()
        parts = urlsplit(url)
        assert parts.scheme == 'https' and parts.hostname, 'URL inválida: ' + channel['nombre']
        assert parts.path.lower().endswith('.m3u8'), 'Señal no HLS: ' + channel['nombre']
        assert parts.hostname != 'manifest.googlevideo.com', 'Manifiesto temporal'
        assert not parts.username and not parts.password, 'Credenciales en URL'
        params = {name.lower() for name, _ in parse_qsl(parts.query, keep_blank_values=True)}
        assert not params.intersection({'access_token', 'token', 'sig', 'signature', 'expire', 'sid', 'uid'}), 'Parámetros temporales'
        assert not re.search(r'[\r\n]', url), 'Salto de línea en URL'
        for field in ('user_agent', 'referrer'):
            val = channel.get(field, '')
            assert isinstance(val, str) and len(val) <= 240 and not re.search(r'[\r\n]', val), 'Encabezado inválido'
        backups = channel.get('backups', [])
        assert isinstance(backups, list) and len(backups) <= 2, 'Demasiados respaldos'
        for backup in backups:
            assert isinstance(backup, dict), 'Respaldo no válido'
            backup_url = backup.get('url', '')
            parts = urlsplit(backup_url)
            assert parts.scheme == 'https' and parts.hostname, 'Respaldo URL no HTTPS'
            assert parts.path.lower().endswith('.m3u8') and parts.hostname != 'manifest.googlevideo.com', 'Respaldo no HLS o firmado'
            backup_params = {name.lower() for name, _ in parse_qsl(parts.query, keep_blank_values=True)}
            assert not backup_params.intersection({'access_token', 'token', 'sig', 'signature', 'expire', 'sid', 'uid'}), 'Respaldo con token'
            assert not re.search(r'[\r\n]', backup_url), 'Salto de línea en respaldo'
            headers = backup.get('headers', {})
            assert isinstance(headers, dict), 'Encabezados de respaldo inválidos'
            assert all(isinstance(k, str) and isinstance(v, str)
                       and not re.search(r'[\r\n]', k + v)
                       and k.lower() not in ('cookie', 'authorization')
                       for k, v in headers.items()), 'Credencial o encabezado inválido'

    for channel in youtube:
        url = channel['url_permanente'].strip()
        parts = urlsplit(url)
        assert parts.scheme == 'https' and parts.hostname in {'youtube.com', 'www.youtube.com'}
        es_video = channel.get('tipo') == 'youtube_video'
        if es_video:
            vid = channel.get('video_id') or channel.get('video_id_pendiente', '')
            assert re.fullmatch(r'[A-Za-z0-9_-]{11}', vid), 'video_id inválido: ' + channel['nombre']
            assert url == f'https://www.youtube.com/watch?v={vid}', 'URL de video incoherente: ' + channel['nombre']
        else:
            assert parts.path.endswith('/live') and not parts.query, 'Enlace YouTube no permanente'
        assert 'manifest.googlevideo.com' not in json.dumps(channel)
        # Lista Clásica YT: el channel_id es opcional (pendiente) pero, si está, debe ser válido.
        cid = channel.get('channel_id', '')
        assert cid == '' or re.fullmatch(r'UC[A-Za-z0-9_-]{22}', cid), 'channel_id inválido: ' + channel['nombre']
        assert channel.get('horario', 'programado') in {'24h', 'programado'}, 'Horario inválido: ' + channel['nombre']
    youtube_listos = [c for c in youtube if c.get('channel_id') or c.get('video_id')]
    ids_canal = [c['channel_id'] for c in youtube_listos if c.get('channel_id')]
    assert len(set(ids_canal)) == len(ids_canal), 'channel_id repetido'
    assert all(c.get('logo') for c in youtube_listos), 'Canal YouTube publicado sin logo'
    categorias = __import__('collections').Counter(c['categoria'] for c in youtube_listos)
    assert all(n >= 2 for n in categorias.values()), f'Categoría YouTube con un solo canal: {categorias}'

    for filename in ('lista_clasica.m3u', 'lista_clasica_youtube.m3u'):
        content = (ROOT / filename).read_text(encoding='utf-8')
        assert content.startswith('#EXTM3U\n'), 'Encabezado M3U inválido'
        assert 'manifest.googlevideo.com' not in content
        assert 'access_token=' not in content and 'expire/' not in content
        expected = len({c['url'] for c in all_hls}) if filename == 'lista_clasica.m3u' else len(youtube_listos)
        assert content.count('#EXTINF:') == expected, 'Cantidad incorrecta de canales'
        if filename == 'lista_clasica.m3u':
            assert 'group-title="Argentina TV"' in content
            assert 'group-title="Argentina YT"' not in content, 'Fuentes YouTube dentro del reproductor HLS'
            assert 'youtube.com/' not in content and 'youtu.be/' not in content, 'Enlace YouTube no reproducible en V62'
            assert 'Mundo TV /' not in content
            urls_m3u = {line.strip() for line in content.splitlines() if line.startswith('https://')}
            assert urls_m3u == {c['url'] for c in all_hls}, 'Falta o sobra una URL HLS'
            seen_urls = set()
            logo_expected = 0
            for c in all_hls:
                if c['url'] in seen_urls:
                    continue
                seen_urls.add(c['url'])
                logo_expected += bool(c.get('logo'))
            assert content.count('tvg-logo="') == logo_expected, 'Se perdieron logos HLS'
        else:
            assert all((f"https://www.youtube.com/channel/{c['channel_id']}/live" if c.get('channel_id')
                        else f"https://www.youtube.com/watch?v={c['video_id']}") in content
                       for c in youtube_listos), 'Lista YouTube incompleta'
            assert content.count('tvfull-player="youtube"') == len(youtube_listos), 'Falta marca de reproductor YouTube'
            assert '.m3u8' not in content, 'La Lista Clásica YT no debe contener HLS'

    print(f'OK: {len(hls)} HLS originales + {len(mundo)} Mundo TV + {len(popular)} populares 2026; {len({c["url"] for c in all_hls})} URL HLS únicas, {len(youtube_listos)} YouTube publicadas ({len(youtube) - len(youtube_listos)} pendientes).')
    print('Advertencia: pruebas estructurales, no certificación de disponibilidad.')


if __name__ == '__main__':
    main()
