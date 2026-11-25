#!/usr/bin/env python3
"""Genera Lista Clásica por temática sin perder fuentes ni respaldos."""
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


# Clasificación temática; el país original sigue en el inventario.
CATEGORIES = ["Televisión Nacional","Deportes","Deportes Internacionales","Películas y Series","Noticias","Noticias Internacionales","Infantiles","Documentales y Cultura","Entretenimiento","Música y Radio","Estilo de Vida","Religión","Televisión Internacional","Adultos"]
RULES = [["Adultos","^(playboy|sextreme|venus)$"],["Deportes","^(deportv|dsports( 2)?|espn( [2-7]| premium)?|fox sports( 2)?|tnt sports( premium)?|tyc( sports 24)?|eventos)$"],["Deportes Internacionales","sport|deportes|fifa\\+|kickboxing|teletrak|monterrico|^ecdf$|^win$|^itv deportes$|real madrid|via x esports|portal foxmix"],["Noticias","^(a24.*|c5n|canal 26|canal e / perfil tv.*|cronica tv|la nacion\\+.*|tn( - todo noticias)?|aire de santa fe|merc urio noticias|ng federal|medios provincia|24/7 canal de noticias)$"],["Noticias Internacionales","noticias|news|24 horas|^\\+24$|^24h( |$)|3cat info|cnn|^dw( |$)|france 24|al jazeera|al arabiya|tagesschau|bloomberg|^adn40|^npy$|^ntn24$|^rpp$|^exitosa tv$|^rt en espanol$|^telesur|globovision|trt world|nhk world|india today|new delhi tv|channel newsasia|medi1|bio bio|^red\\+$|current time|america.s voice|el toro tv|negocios tv|weathernation|^c9n$|^qu iero tv"],["Infantiles","baby|cartoon|kids|disney|nick(?! music)|plim plim|tooncast|teen nick|13 kids"],["Películas y Series","cine|movie|teleseries|novela|^a&e$|^amc( |$)|^atres series$|^axn$|^dhe$|^fx$|^golden( |$)|^hbo( |$)|^europa europa$|^kanal d drama$|^lifetime$|^pasiones$|^sony$|^space$|^star channel$|^tcm$|^tnt( series)?$|^universal( |$)|^usa$|^warner tv$|^telemundo accion$|^xtrema terror$|^tv series clasicas|filmrise|^ent channel$"],["Documentales y Cultura","^animal planet$|^discovery(?! h&h| kids| turbo)|^history|^nat geo$|^film&arts$|^tv cultura|^classic arts|^canal universidad|^litus tv$|^uniteve$|^canal institucional$|parlamento|congreso|^akc tv|^rural$"],["Música y Radio","musica|music|radio|^htv$|^hei$|^mtv$|^la 100$|^chamame|^cumbia|^folclore|^parranda|^salsa gorda|^kpop|^urban mix|^dance tv|^ocko|^cmc |^vm latino|^sky folk|^m2o|^rtl 102|^4fun|^number1|^venus media|^m olahits|^molahits|^spektra|^cadena103|^frecuencia f|^correa radiovision"],["Estilo de Vida","gourmet|tastemade|^hgtv$|^hola tv$|^discovery h&h$|^discovery turbo$|^garage tv|^tlc$|^sun channel$|^maeschic$|^mæs chic$|^mæschic$|turismo|travel|tour spot|^plus tv life$|^miami tv gold$"],["Religión","^bethel|^daystar|^enlace$|^esne$|^ewtn|^canal luz$|^canal orbe 21$|^canal santa maria$|^unife|^3abn|^spirit tv|^novo tempo|^redevida|^nuevo tiempo|^aliento vision|^comunion tv|^maria vision|^ecclesia|diocesana|^rtv vida|^red avenir$"],["Entretenimiento","^adult swim$|^ciudad magazine$|^caras tv$|^comedy central$|^distrito comedia$|^e! entertainment$|^ent family$|^13 humor$|^13 festival$|^buzzr|^court tv|^courttv|^retro tv$|^zona latina$|^via x$|^zoom$|^clover$|^silver channel$|^extrema tv$|^xtrema cartoons$"],["Televisión Nacional","^(5tv|abtv bariloche|america tv|argentin isima satelital|argentinisima satelital|cable imagen armstrong|canal (10 goya|11 de la costa|12 misiones|2 gualeguay|2 mar del plata|2 misiones.*|2 nextv rafaela|20 villa maria|22|3 arroyito|3 formosa|3 la pampa|3 las heras|4 esquel|4 jujuy|4 posadas|5 del pueblo|5 santa fe|5 tv chepes|50 morteros|6 posadas|7 neuquen|7 salta|7 santiago del estero|79 .*|8 tv\\+|9 link resistencia|9 televida|99 miramar|de la ciudad|provincial|pulpo tv)|catamarca tv|chaco tv|ciudad tv resistencia|corrientes tv|el nueve|el trece|freyre tv|itel tv canal 2|mas norte tv|metropolitana tv.*|misiones cuatro|multivision federal|net tv|rtn neuquen|senillosa tv|sicardi tv|t5 satelital|telefe.*|telemax|telesol san juan|tierra mia tv|tv publica.*|villa mantero tv|vertv|vive tv|sin limites|popu tv|sur tv)$"]]

def thematic_category(c):
    name = norm(c['nombre']).strip()
    country_group = c['categoria']
    for category, pattern in RULES:
        if category == 'Televisión Nacional' and country_group != 'Argentina TV':
            continue
        if re.search(pattern, name):
            if category == 'Deportes' and country_group not in ('Argentina TV', 'Internacional TV'):
                return 'Deportes Internacionales'
            return category
    return 'Televisión Internacional'


def sort_key(c):
    return (CATEGORIES.index(thematic_category(c)), norm(c['nombre']), norm(c['tvg_id']))


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
        '#PLAYLIST:Lista Clásica - Canales por temática',
        '# Solo fuentes HLS directas compatibles con Media3; sin URLs YouTube.',
        '# Categorías temáticas; país conservado únicamente en el inventario de fuentes.',
        '# Fuentes YouTube separadas: lista_clasica_youtube.m3u (no compatible directamente con V62).',
        '# Sin tokens, firmas temporales ni claves; disponibilidad HLS no certificada en TV Box.',
        ''
    ]
    for channel in sorted(channels, key=sort_key):
        name = escape_attr(channel['nombre'])
        category = escape_attr(thematic_category(channel))
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
