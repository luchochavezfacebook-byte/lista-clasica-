#!/usr/bin/env python3
"""Auditar SOLO las 863 URLs manualmente agregadas a lista_clasica.m3u.
No afirma disponibilidad en Argentina: runners de GitHub fuera del país.
Conservar solo video decodificado dos veces; archivar resultados sin exponer tokens.
"""
import concurrent.futures
import datetime
import hashlib
import json
import os
import re
import subprocess
import time
from pathlib import Path
from urllib.parse import urlsplit

ROOT=Path(__file__).resolve().parents[1]
BASE_COMMIT="bb80b9248a48ff09d3463a7437e775d3f42be9a2"
INCOMING_COMMIT="7f53dcb745db"
FFMPEG=os.environ.get("FFMPEG_BINARY","ffmpeg")

def read_git(ref):
    return subprocess.check_output(["git","show",f"{ref}:lista_clasica.m3u"],text=True)
def entries(text):
    result=[]
    meta=None
    headers={}
    for raw in text.splitlines():
        line=raw.strip()
        if line.startswith("#EXTINF:"):
            grp=re.search(r'group-title="([^"]*)"',line)
            logo=re.search(r'tvg-logo="([^"]*)"',line)
            meta={"name":line.split(",",1)[-1].strip(),
                  "group":grp.group(1) if grp else "",
                  "logo":logo.group(1) if logo else ""}
            headers={}
        elif line.startswith("#EXTVLCOPT:http-user-agent="):
            headers["ua"]=line.split("=",1)[1]
        elif line.startswith("#EXTVLCOPT:http-referrer="):
            headers["referer"]=line.split("=",1)[1]
        elif line.startswith(("http://","https://")):
            if meta:
                result.append({**meta,"url":line,**headers})
            meta=None
            headers={}
    return result

def safe(url):
    p=urlsplit(url)
    if p.scheme not in ("http","https") or not p.hostname or p.username or p.password:
        return False,"url_no_admitida"
    if not p.path.lower().endswith(".m3u8"):return False,"no_hls"
    # Evitar publicar credenciales / URL de sesiones privadas o firmadas.
    if p.query or re.search(r"/(?:live|stream)/[^/]+/[^/]+/[^/]+\.m3u8",p.path,re.I):
        return False,"credenciales_o_firma_potencial"
    if p.hostname in {"localhost","127.0.0.1","0.0.0.0"}:
        return False,"host_local"
    return True,"apta_para_prueba"

def ff(item,run):
    url=item["url"]
    command=[FFMPEG,"-hide_banner","-nostdin","-loglevel","error","-rw_timeout","6500000",
      "-user_agent",item.get("ua") or "Mozilla/5.0"]
    if item.get("referer"):command+=["-referer",item["referer"]]
    command+=["-i",url,"-map","0:v:0","-an","-frames:v","18","-progress","pipe:1","-f","null","-"]
    try:
        done=subprocess.run(command,text=True,capture_output=True,timeout=13)
        frames=max([int(x) for x in re.findall(r"^frame=(\d+)$",done.stdout,re.M)] or [0])
        ok=done.returncode==0 and frames>=12
        err=(done.stderr[-300:] if not ok else "")
        err=re.sub(r"https?://[^\s']+","[URL_OCULTA]",err)
        kind=("video_ok" if ok else "sin_video")
        if "403" in err:kind="http_403"
        elif "404" in err:kind="http_404"
        elif "timed out" in err.lower():kind="timeout"
        elif "Invalid data" in err:kind="video_invalido"
        return {"ok":ok,"frames":frames,"estado":kind,"attempt":run}
    except subprocess.TimeoutExpired:return {"ok":False,"frames":0,"estado":"timeout","attempt":run}
    except Exception as e:return {"ok":False,"frames":0,"estado":"error_"+type(e).__name__,"attempt":run}
def batch(items,attempt):
    results={}
    with concurrent.futures.ThreadPoolExecutor(max_workers=16) as ex:
        jobs={ex.submit(ff,item,attempt):i for i,item in items}
        for k,fut in enumerate(concurrent.futures.as_completed(jobs),1):
            i=jobs[fut]
            results[i]=fut.result()
            if k % 50==0 or k==len(items):
                successes=sum(x["ok"] for x in results.values())
                print("AVANCE",json.dumps({"pasada":attempt,"completados":k,"total":len(items),"video_ok":successes}),flush=True)
    return results
def main():
    base=entries(read_git(BASE_COMMIT))
    incoming=entries(read_git(INCOMING_COMMIT))
    old_urls={x["url"] for x in base}
    fresh=[x for x in incoming if x["url"] not in old_urls]
    if len(base)!=353 or len(fresh)!=863 or len(incoming)!=1216:
        raise RuntimeError(f"BASE O INGRESOS IMPREVISTOS: {len(base)} / {len(fresh)} / {len(incoming)}")
    excluded={}
    eligible=[]
    for i,item in enumerate(fresh):
        yes,why=safe(item["url"])
        if yes:eligible.append((i,item))
        else:excluded[i]=why
    print("INICIO",json.dumps({"anteriores":len(base),"anadidos":len(fresh),"elegibles":len(eligible),"no_elegibles":len(excluded)}),flush=True)
    first=batch(eligible,1)
    winners=[(i,item) for i,item in eligible if first[i]["ok"]]
    print("PRIMERA",json.dumps({"probados":len(eligible),"video_ok":len(winners)}),flush=True)
    time.sleep(5)
    second=batch(winners,2)
    keep_ids={i for i,item in winners if second[i]["ok"]}
    keep=[]
    details=[]
    for i,item in enumerate(fresh):
        p=first.get(i)
        q=second.get(i)
        reason=excluded.get(i) or ("aprobado" if i in keep_ids else "sin_video_confirmado")
        details.append({"indice":i+1,"nombre":item["name"],"grupo_origen":item["group"],
          "estado":reason,"primera":p,"segunda":q})
        if i in keep_ids:
            keep.append({"nombre":item["name"][:140],
               "tvg_id":f"Usuario20261123.{i+1:04d}",
               "categoria":"Argentina TV","pais":"Argentina","url":item["url"],
               "user_agent":item.get("ua","Mozilla/5.0")[:240],
               "logo":item.get("logo","") if item.get("logo","").startswith("https://") else "",
               "origen":"catalogo_usuario_20261123",
               "verificacion":"2026-11-23: video decodificado en 2 pasadas FFmpeg desde GitHub Actions; disponibilidad y derechos en Argentina NO confirmados"})
    payload={"nombre":"Señales del catálogo agregado manualmente; QA 23/11/2026",
      "advertencia":"Sólo aprobadas desde GitHub Actions fuera de Argentina, no se afirma disponibilidad regional. No publicar credenciales.",
      "canales":keep}
    report={"fecha_utc":datetime.datetime.now(datetime.timezone.utc).isoformat(),
      "base":len(base),"nuevas":len(fresh),"elegibles":len(eligible),"excluidas":len(excluded),
      "primera_video_ok":len(winners),"segunda_video_ok":len(keep),"no_aprobadas":len(fresh)-len(keep),
      "criterio":"Dos pasadas FFmpeg, >=12 fotogramas por pasada. Resultado en servidor externo, no test geográfico desde Argentina.",
      "entradas":details}
    (ROOT/"fuentes_usuario_argentina_20261123.json").write_text(json.dumps(payload,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    dr=ROOT/"diagnosticos"
    dr.mkdir(exist_ok=True)
    (dr/"qa_usuario_20261123.json").write_text(json.dumps(report,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print("RESULTADO",json.dumps({k:report[k] for k in ("base","nuevas","elegibles","excluidas","primera_video_ok","segunda_video_ok","no_aprobadas")}),flush=True)
    print("No se alteraron los canales previos, fuentes del proveedor ni Lista Clásica YT",flush=True)
if __name__=="__main__":main()
