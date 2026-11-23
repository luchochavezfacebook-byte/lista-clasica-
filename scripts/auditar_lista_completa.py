#!/usr/bin/env python3
"""Auditoría de todas las fuentes HLS publicadas.
Solo diagnóstico, no altera URLs ni elimina canales al fallar.
Registra dos muestras para fallos, más cualquier backup configurado.
No comprueba derechos de difusión ni decodificación de video.
"""
import concurrent.futures
import collections
import datetime as dt
import json
import time
from pathlib import Path
from verificar_canales import check

ROOT=Path(__file__).resolve().parents[1]
CATALOGS=[
    'fuentes.json',
    'fuentes_mundotv.json',
    'fuentes_populares_2026.json',
    'fuentes_noviembre_2026.json',
    'fuentes_netvideo_2026.json',
    'fuentes_tvplay_es_2026.json',
    'fuentes_regionales_20261123.json',
    'fuentes_fast_playtv_20261123.json',
]
GOOD={'segmento_accesible'}
def tag(src, kind='principal'):
    return {'canal':src['nombre'],'id':src.get('tvg_id',''),
            'pais':src.get('pais',''),'fuente':kind}
def key(src):
    return src.get('tvg_id') or src['url']
def safe_check(src):
    try: return check(src)
    except Exception as exc: return {'canal':src['nombre'],'fuente':src.get('tipo','principal'),
       'estado':'error_interno','detalle':type(exc).__name__}
def batch(source_list, phase, workers=18):
    if not source_list:return {}
    results={}
    with concurrent.futures.ThreadPoolExecutor(max_workers=workers) as pool:
        futures={pool.submit(safe_check,dict(src,tipo=phase)):src for src in source_list}
        for f in concurrent.futures.as_completed(futures):
            src=futures[f];r=f.result()
            results[key(src)]={**tag(src,phase),'estado':r['estado'],'detalle':r.get('detalle','')}
    return results
def main():
    all_channels=[]
    for filename in CATALOGS:
        p=ROOT / filename
        if not p.exists(): continue
        rows=json.loads(p.read_text(encoding='utf-8'))['canales']
        for ch in rows:
            ch=dict(ch,archivo=filename)
            all_channels.append(ch)
        print('CATALOGO',filename,len(rows),flush=True)
    seen=set()
    channels=[]
    for src in all_channels:
        if src['url'] not in seen:
            seen.add(src['url']);channels.append(src)
    print('TOTAL',len(channels),'fuentes únicas. Inicio de primera pasada...',flush=True)
    first=batch(channels,'principal')
    failed=[ch for ch in channels if first[key(ch)]['estado'] not in GOOD]
    print('PRIMERA_PASADA',json.dumps({'ok':len(channels)-len(failed),'pendientes':len(failed)},ensure_ascii=False),flush=True)
    time.sleep(5)
    second=batch(failed,'reintento')
    backups=[]
    for ch in failed:
        for i,b in enumerate(ch.get('backups',[])[:2]):
            if not isinstance(b,dict) or not b.get('url'): continue
            alias=dict(ch,nombre=ch['nombre']+' [respaldo '+str(i+1)+']',url=b['url'],
                user_agent=b.get('headers',{}).get('User-Agent',ch.get('user_agent','')),
                referrer=b.get('headers',{}).get('Referer',ch.get('referrer','')),
                tvg_id=key(ch)+':backup:'+str(i+1))
            backups.append(alias)
    backup_results=batch(backups,'respaldo')
    enriched=[]
    for ch in channels:
        id=key(ch)
        one=first[id]
        two=second.get(id)
        backupchecks=[v for k,v in backup_results.items() if k.startswith(id+':backup:')]
        healthy=one['estado'] in GOOD or bool(two and two['estado'] in GOOD)
        backuphealthy=any(x['estado'] in GOOD for x in backupchecks)
        result={
            **tag(ch),'catalogo':ch['archivo'],'primera':one,
            'segunda':two,'respaldos':backupchecks,
            'clasificacion':('accesible' if healthy else ('respaldo_accesible' if backuphealthy else 'requiere_revision'))
        }
        enriched.append(result)
    counter=collections.Counter(x['clasificacion'] for x in enriched)
    by_country=collections.defaultdict(lambda:collections.Counter())
    for e in enriched: by_country[e['pais']][e['clasificacion']]+=1
    payload={'fecha_utc':dt.datetime.now(dt.timezone.utc).isoformat(),
             'total':len(enriched),'conteo':dict(counter),
             'por_pais':{p:dict(v) for p,v in sorted(by_country.items())},
             'limitaciones':'Prueba desde servidor GitHub; no mide reproduccion continua ni certifica imagen/audio. 403/404/timeouts pueden ser transitorios o regionales. No dar de baja automaticamente.',
             'resultados':enriched}
    (ROOT/'reporte_verificacion.json').write_text(json.dumps(payload,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
    print('RESUMEN',json.dumps({'total':len(enriched),**counter},ensure_ascii=False),flush=True)
    print('POR_PAIS',json.dumps(payload['por_pais'],ensure_ascii=False),flush=True)
    for x in enriched:
        if x['clasificacion']=='accesible':continue
        one=x['primera'];two=x.get('segunda') or {}
        detail=one['detalle']+' | '+two.get('detalle','')
        print('PENDIENTE',json.dumps({'canal':x['canal'],'pais':x['pais'],
               'catalogo':x['catalogo'],'estado':x['clasificacion'],'detalle':detail[:180],
               'respaldos':[(b['estado'],b['detalle']) for b in x['respaldos']]},ensure_ascii=False),flush=True)
    print('No se borró ni reemplazó ningún canal.',flush=True)
if __name__=='__main__':main()
