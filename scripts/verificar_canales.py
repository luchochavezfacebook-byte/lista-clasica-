#!/usr/bin/env python3
"""Comprueba HLS desde GitHub Actions; no prueba reproducción ni modifica listas."""
import concurrent.futures
import datetime as dt
import json
import ssl
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TIMEOUT = 8
MAX_MANIFEST = 128 * 1024
UA = ('Mozilla/5.0 (Linux; Android 13; Pixel 7) AppleWebKit/537.36 '
      '(KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36')


def get(url, headers, *, peek=False):
    if not url.startswith(('https://', 'http://')):
        raise ValueError('Protocolo no permitido')
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req, timeout=TIMEOUT, context=ssl.create_default_context()) as response:
        data = response.read(2048 if peek else MAX_MANIFEST + 1)
        if not peek and len(data) > MAX_MANIFEST:
            raise ValueError('Manifiesto mayor a 128 KiB')
        return data, response.status, response.url


def check(source):
    name = source['nombre']
    headers = {
        'User-Agent': source.get('user_agent') or UA,
        'Accept': 'application/vnd.apple.mpegurl,application/x-mpegURL,*/*'
    }
    if source.get('referrer'):
        headers['Referer'] = source['referrer']
    result = {'canal': name, 'fuente': source.get('tipo', 'principal'),
              'estado': 'error', 'detalle': 'Sin respuesta'}
    try:
        data, status, url = get(source['url'], headers)
        text = data.decode('utf-8-sig', errors='replace')
        if not text.lstrip().startswith('#EXTM3U'):
            result.update(estado='invalido', detalle='HTTP %s sin manifiesto HLS' % status)
            return result
        lines = [line.strip() for line in text.splitlines() if line.strip()]
        if any(line.startswith('#EXT-X-STREAM-INF') for line in lines):
            next_url = next(
                (lines[i + 1] for i, line in enumerate(lines[:-1])
                 if line.startswith('#EXT-X-STREAM-INF') and not lines[i + 1].startswith('#')), None)
            if not next_url:
                result.update(estado='invalido', detalle='Master sin variantes')
                return result
            data, _, url = get(urllib.parse.urljoin(url, next_url), headers)
            text = data.decode('utf-8-sig', errors='replace')
            if not text.lstrip().startswith('#EXTM3U'):
                result.update(estado='invalido', detalle='Variante no HLS')
                return result
            lines = [line.strip() for line in text.splitlines() if line.strip()]
        segment = next((line for line in lines if not line.startswith('#')), None)
        if not segment:
            result.update(estado='sin_segmentos', detalle='M3U8 sin segmentos listados')
            return result
        sample_headers = dict(headers, Range='bytes=0-2047')
        sample, seg_status, _ = get(urllib.parse.urljoin(url, segment), sample_headers, peek=True)
        if sample and seg_status in (200, 206):
            result.update(estado='segmento_accesible', detalle='M3U8 y primer segmento responden; no se certifica video')
        else:
            result.update(estado='sin_segmentos', detalle='Segmento vacío o HTTP %s' % seg_status)
    except urllib.error.HTTPError as e:
        result.update(estado='http_error', detalle='HTTP %s' % e.code)
    except (urllib.error.URLError, TimeoutError, OSError) as e:
        result.update(estado='red_error', detalle=type(e).__name__)
    except (ValueError, UnicodeError, IndexError) as e:
        result.update(estado='invalido', detalle=str(e)[:100])
    return result


if __name__ == '__main__':
    catalog = json.loads((ROOT / 'fuentes.json').read_text(encoding='utf-8'))
    main_sources = [dict(c, tipo='principal') for c in catalog['canales']]
    candidates_path = ROOT / 'diagnosticos' / 'candidatos.json'
    alternate = json.loads(candidates_path.read_text(encoding='utf-8'))['canales'] if candidates_path.exists() else []
    sources = main_sources + [dict(c, tipo='alternativa') for c in alternate]
    with concurrent.futures.ThreadPoolExecutor(max_workers=6) as pool:
        results = list(pool.map(check, sources))
    payload = {
        'fecha_utc': dt.datetime.now(dt.timezone.utc).isoformat(),
        'advertencia': 'Pruebas desde runner remoto; fallos no implican caída en Argentina. Segmento accesible no garantiza imagen/sonido.',
        'resultados': results,
    }
    (ROOT / 'reporte_verificacion.json').write_text(
        json.dumps(payload, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')
    for r in results:
        print('%-11s | %-35s | %-19s | %s' %
              (r['fuente'], r['canal'][:35], r['estado'], r['detalle']), flush=True)
    print('No se modificó ningún canal. Reporte diagnóstico solamente.')
