#!/usr/bin/env python3
"""QA de fuentes libres/oficiales comparables a canales de la14hd.m3u.
Nunca utiliza sus tokens ni intenta acceder a servicios pagos.
Dos tandas de decodificación FFmpeg 25 fotogramas.
"""
from concurrent.futures import ThreadPoolExecutor,as_completed
import json,re,subprocess,time,urllib.parse
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
CANDIDATES=[
 ("La 1 RTVE","España","https://ztnr.rtve.es/ztnr/1688877.m3u8","nuevo"),
 ("La 1 RTVE (alternativa regional)","España","https://rtvelivestream.rtve.es/rtvesec/la1/la1_main.m3u8","alternativa"),
 ("Telemundo Puerto Rico WKAQ","Puerto Rico","https://nbculocallive.akamaized.net/hls/live/2037499/puertorico/stream1/master.m3u8","nuevo"),
 ("Telemundo Al Día","Estados Unidos","https://d1rqgw5gocwo9i.cloudfront.net/manifest/3fec3e5cac39a52b2132f9c66c83dae043dc17d4/prod_default_xumo-nbcu-stitched/10a44c37-f976-4d2b-ab23-8637a7a094ca/3.m3u8","nuevo"),
 ("Telemundo Al Día (alternativa)","Estados Unidos","https://d3f4oii5n0oeqi.cloudfront.net/11701/88814573/hls/master.m3u8?ads.xumo_channelId=88814573","alternativa"),
 ("Fubo Sports Network","Estados Unidos","https://aegis-cloudfront-1.tubi.video/c2ac89da-5c69-439e-b85d-d87de0548b54/5.m3u8","nuevo"),
 ("beIN SPORTS XTRA en Español","Estados Unidos","https://aegis-cloudfront-1.tubi.video/01f6c149-449b-4248-8bda-2278799205ec/playlist.m3u8","nuevo"),
]
EXISTING=[
 "beIN-SPORTS","beIN SPORTS XTRA","Fox Deportes","TyC Sports FAST",
 "TyC Sports 24","CBS Sports Golazo","FIFA+ (Español)","Azteca Deportes Network"
]
def parse(s):
 out={}; name=None
 for ln in s.splitlines():
  ln=ln.strip()
  if ln.startswith("#EXTINF:"):name=ln.rsplit(",",1)[-1]
  elif ln.startswith(("https://","http://")) and name:
   out[name]=ln;name=None
 return out
def run(job,pass_id):
 name,pais,url,kind=job
 try:
  u=urllib.parse.urlsplit(url)
  if u.scheme!="https" or not u.hostname or u.username or u.password or not u.path.endswith(".m3u8"):
   return {"name":name,"phase":pass_id,"ok":False,"error":"invalid public HLS URL"}
  cmd=["ffmpeg","-hide_banner","-nostdin","-loglevel","error","-rw_timeout","9000000",
       "-user_agent","Mozilla/5.0 (TVFULLPRO Public Feed QA)","-i",url,"-map","0:v:0","-an",
       "-frames:v","25","-progress","pipe:1","-f","null","-"]
  cp=subprocess.run(cmd,capture_output=True,text=True,timeout=29)
  frames=max([int(x) for x in re.findall(r"^frame=(\d+)$",cp.stdout,re.M)] or [0])
  return {"name":name,"phase":pass_id,"ok":cp.returncode==0 and frames>=20,
   "frames":frames,"error":re.sub(r"https?://\S+","[STREAM]",cp.stderr[-180:]) if cp.returncode else ""}
 except subprocess.TimeoutExpired:return {"name":name,"phase":pass_id,"ok":False,"frames":0,"error":"timeout"}
 except Exception as e:return {"name":name,"phase":pass_id,"ok":False,"frames":0,"error":type(e).__name__}
def main():
 now=parse((ROOT/"lista_clasica.m3u").read_text())
 items=CANDIDATES+[ (name,"lista existente",now[name],"ya_existente") for name in EXISTING if name in now]
 rows=[]
 for phase in [1,2]:
  with ThreadPoolExecutor(max_workers=9) as pool:
   for f in as_completed([pool.submit(run,c,phase) for c in items]):
    row=f.result();rows.append(row)
    print("TEST",json.dumps(row,ensure_ascii=False),flush=True)
  if phase==1:time.sleep(5)
 grouped={x[0]:[y for y in rows if y["name"]==x[0]] for x in items}
 ok=[x for x in items if len(grouped[x[0]])==2 and all(y["ok"] for y in grouped[x[0]])]
 for n,p,u,k in ok:
  print("APROBADO",json.dumps({"nombre":n,"pais":p,"url":u,"tipo":k},ensure_ascii=False),flush=True)
 print("RESUMEN",json.dumps({"total":len(items),"aprobados":len(ok),
  "nuevos":[x[0] for x in ok if x[3]!="ya_existente"],
  "ya_existentes":[x[0] for x in ok if x[3]=="ya_existente"],
  "fallidos":[x[0] for x in items if x not in ok]},ensure_ascii=False),flush=True)
if __name__=="__main__":main()
