#!/usr/bin/env python3
"""Comprobación técnica en runner remoto de fuentes públicas HLS candidatas.
No modifica catálogos, no intenta acceso a DRM, credenciales o tokens."""
import concurrent.futures, datetime, json, re, subprocess, urllib.request, urllib.parse
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
UA="Mozilla/5.0 (Linux; Android 13; Pixel 7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36"
channels=json.loads((ROOT/"diagnosticos/candidatos_nuevos_20261121.json").read_text(encoding="utf-8"))["canales"]
def test(c):
    result={"nombre":c["nombre"],"tvg_id":c["tvg_id"],"url":c["url"],"origen":c["origen"],"estado":"error"}
    headers={"User-Agent":c.get("user_agent") or UA,"Accept":"application/vnd.apple.mpegurl,application/x-mpegURL,*/*"}
    if c.get("referrer"): headers["Referer"]=c["referrer"]
    try:
        request=urllib.request.Request(c["url"],headers=headers)
        with urllib.request.urlopen(request,timeout=12) as f:
            content=f.read(180000).decode("utf-8-sig","replace"); target=f.url
        if not content.lstrip().startswith("#EXTM3U"):raise ValueError("Sin manifiesto HLS")
        if "#EXT-X-KEY" in content:raise ValueError("Manifiesto cifrado: no probar")
        if "#EXT-X-STREAM-INF" in content:
            ls=[line.strip() for line in content.splitlines() if line.strip()]
            variants=[ls[i+1] for i,line in enumerate(ls[:-1]) if line.startswith("#EXT-X-STREAM-INF") and not ls[i+1].startswith("#")]
            if not variants:raise ValueError("Sin variante")
            u=urllib.parse.urljoin(target,variants[-1])
            with urllib.request.urlopen(urllib.request.Request(u,headers=headers),timeout=12) as f:
                content=f.read(180000).decode("utf-8-sig","replace");target=f.url
            if not content.lstrip().startswith("#EXTM3U"):raise ValueError("Variante no HLS")
        segments=[line.strip() for line in content.splitlines() if line.strip() and not line.startswith("#")]
        if not segments:raise ValueError("Sin segmentos")
        seg=urllib.parse.urljoin(target,segments[0])
        with urllib.request.urlopen(urllib.request.Request(seg,headers={**headers,"Range":"bytes=0-4095"}),timeout=12) as f:
            data=f.read(4096);status=f.status
        if not data or status not in (200,206):raise ValueError("Segmento vacío")
        result["segmento"]="accesible"
        cmd=["ffmpeg","-nostdin","-hide_banner","-loglevel","error","-stats_period","1","-user_agent",headers["User-Agent"]]
        if "Referer" in headers:cmd.extend(["-headers","Referer: "+headers["Referer"]+"\\r\\n"])
        cmd.extend(["-rw_timeout","12000000","-i",c["url"],"-t","2","-map","0:v:0","-an","-f","null","-","-progress","pipe:1"])
        p=subprocess.run(cmd,stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True,timeout=32)
        frames=[int(x) for x in re.findall(r"(?m)^frame=(\\d+)$",p.stdout)]
        frames=max(frames) if frames else 0
        result["frames"]=frames
        result["estado"]="video_ok" if p.returncode==0 and frames>0 else "sin_video_decodificado"
        result["detalle"]=(p.stderr or "")[-250:]
    except Exception as e:
        result["detalle"]=(type(e).__name__+": "+str(e))[:250]
    print(result["estado"].ljust(24), result["nombre"], result.get("frames",0), result.get("detalle","")[:80],flush=True)
    return result
with concurrent.futures.ThreadPoolExecutor(max_workers=8) as pool:results=list(pool.map(test,channels))
data={"fecha_utc":datetime.datetime.now(datetime.timezone.utc).isoformat(),"advertencia":"Resultado de runner, no garantiza geolocalización Argentina ni identidad editorial de canal", "resultados":results}
(ROOT/"diagnosticos/reporte_nuevos_20261121.json").write_text(json.dumps(data,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
print("RESUMEN",json.dumps({"total":len(results),"video_ok":sum(x["estado"]=="video_ok" for x in results)}),flush=True)
