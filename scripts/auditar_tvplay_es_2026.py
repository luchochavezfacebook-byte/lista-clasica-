#!/usr/bin/env python3
"""Prueba de señales hispanohablantes públicas en TVPlay.
No integra canales premium/PPV ni URL de procedencia dudosa.
Requiere FFmpeg; imprime resultados separados por canal (sin persistir streams).
"""
from concurrent.futures import ThreadPoolExecutor, as_completed
from urllib.request import urlopen,Request
from urllib.parse import urlsplit,parse_qsl
from collections import Counter
import hashlib, json, os, re, subprocess, time

SOURCE="https://raw.githubusercontent.com/Appdeveloper365/TvPlay/main/TVPlay.m3u"
SOURCE_BLOB="a588a1b3cc4ce151db1db1b1b9605d8d2385099a"
# Identificadores de emisoras anunciadas por los proveedores o distribuidores FAST.
# No incluye relés de suscripción, IPTV de IPs no acreditadas ni fuentes DRM.
CANDIDATES={
  "beIN SPORTS XTRA en Español":"Internacional",
  "FIFA+ (Español)":"Internacional",
  "Fox Deportes (720p)":"Estados Unidos",
  "AS3 Sport TV (1080p)":"Venezuela",
  "Awapa Sports TV (1080p)":"El Salvador",
  "Azteca Deportes Network (720p)":"México",
  "ITV Deportes (720p)":"México",
  "CDN Deportes (720p)":"República Dominicana",
  "Colimdo TV (720p)":"República Dominicana",
  "Tour Spot TV (1280p)":"República Dominicana",
  "CRTV (720p)":"Chile",
  "Teletrak TV (720p)":"Chile",
  "FTV (720p)":"Bolivia",
  "Radio Turrialba TV Sports (720p)":"Costa Rica",
  "Monterrico TV":"Perú",
  "Multivision Sports (720p)":"Guatemala"
}
EXCLUDE={"FTF Sports (720p)", "TyC Sports (1080p)", "Real Madrid TV (720p)"}
def parse_m3u(s):
 items=[];previous=None
 for line in s.splitlines():
  line=line.strip()
  if line.startswith("#EXTINF"):
   previous={"nombre":line.split(",",1)[1].strip(),
    "group":(re.search('group-title="([^"]*)"',line) or [None,""])[1],
    "logo":(re.search('tvg-logo="([^"]*)"',line) or [None,""])[1]}
  elif line.startswith(("http://","https://")) and previous:
   items.append(dict(previous,url=line));previous=None
 return items
def safely_public_url(url):
 p=urlsplit(url)
 if p.scheme!="https" or not p.hostname or not p.path.lower().endswith(".m3u8") or p.username or p.password: return False
 if set(k.lower() for k,_ in parse_qsl(p.query)) & {"token","sig","signature","expire","expires","access_token","key","uid"}:return False
 return True
def probe(x,run):
 name=x["nombre"]; url=x["url"]
 try:
  # 20 fotogramas requieren dos segundos a 10 fps; el video debe decodificarse realmente.
  args=["ffmpeg","-hide_banner","-nostdin","-loglevel","error","-rw_timeout","12000000",
        "-user_agent","Mozilla/5.0 (TVFullPro QA)","-i",url,
        "-map","0:v:0","-an","-frames:v","30","-progress","pipe:1","-f","null","-"]
  cp=subprocess.run(args,capture_output=True,text=True,timeout=32)
  matches=re.findall(r"^frame=(\d+)$",cp.stdout,re.M)
  count=max(map(int,matches),default=0)
  ok=cp.returncode==0 and count>=20
  error=(cp.stderr or "")[-180:].replace(url,"[stream]")
  return {"n":name,"pass":run,"ok":ok,"frames":count,"status":cp.returncode,"error":error if not ok else ""}
 except subprocess.TimeoutExpired:return {"n":name,"pass":run,"ok":False,"frames":0,"error":"timeout"}
 except Exception as e:return {"n":name,"pass":run,"ok":False,"frames":0,"error":str(e)[:120]}
def main():
 response=urlopen(Request(SOURCE,headers={"User-Agent":"TVFULLPRO/QA"}),timeout=20)
 raw=response.read(180000)
 sha=hashlib.sha1(b"blob "+str(len(raw)).encode()+b"\0"+raw).hexdigest()
 if sha!=SOURCE_BLOB:raise SystemExit("Origen modificado desde inspección, abortar para evitar cambios inesperados")
 source=parse_m3u(raw.decode("utf-8","replace"));lookup={x["nombre"]:x for x in source}
 print("CATALOG",json.dumps({"total":len(source),"candidates":len(CANDIDATES),"blob_sha":sha}),flush=True)
 candidates=[]
 for n,country in CANDIDATES.items():
  x=lookup.get(n)
  if x is None: print("SKIP",n,"no está en origen",flush=True);continue
  if not safely_public_url(x["url"]): print("SKIP",n,"URL no HLS HTTPS permanente",flush=True);continue
  candidates.append(x)
 results=[]
 for pass_id in [1,2]:
  with ThreadPoolExecutor(max_workers=6) as ex:
   future={ex.submit(probe,x,pass_id):x["nombre"] for x in candidates}
   for f in as_completed(future):
    out=f.result();results.append(out)
    print("TEST",json.dumps(out,ensure_ascii=False),flush=True)
  if pass_id==1:time.sleep(5)
 pass_by_name={n:[x for x in results if x["n"]==n] for n in CANDIDATES}
 good=[lookup[n] for n in CANDIDATES if n in lookup and len(pass_by_name[n])==2 and all(p["ok"] for p in pass_by_name[n])]
 for item in good:
  assert safely_public_url(item["url"])
  # Only tested streams, no access headers, and no tokenized stream links.
  print("APROBADO",json.dumps({"nombre":item["nombre"],"url":item["url"],"logo":item["logo"],"pais":CANDIDATES[item["nombre"]]},ensure_ascii=False),flush=True)
 print("RESUMEN",json.dumps({"candidatos":len(candidates),"aprobados":len(good),
   "fallidos":[n for n in CANDIDATES if n not in [x["nombre"] for x in good]]},ensure_ascii=False),flush=True)
if __name__=="__main__":main()
