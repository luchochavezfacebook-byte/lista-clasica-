#!/usr/bin/env python3
"""Revisar más señales FAST públicas en 2026; no usar DRM ni tokens.
Incluye alternativas por canal, con resultados diferenciados.
"""
from concurrent.futures import ThreadPoolExecutor,as_completed
import re,json,subprocess,time
CANDIDATES=[
 ["Zona TUDN (FAST)","Estados Unidos","https://linear-357.frequency.stream/mt/vizio/357/hls/master/playlist.m3u8","nuevo"],
 ["Fubo Sports Network (Vizio)","Estados Unidos","https://wurlfubo.global.transmit.live/hls/67eb094ee3ed1615e41629ae/v1/fubotv_fubo_sports_network_1/vizio_us/latest/main/hls/playlist.m3u8","nuevo"],
 ["Fubo Sports Network (Tubi)","Estados Unidos","https://apollo.production-public.tubi.io/live/ac-fubo.m3u8","alternativa"],
 ["Telemundo Al Día (Samsung)","Estados Unidos","https://d1kq7q3vteqjb.cloudfront.net/master.m3u8","nuevo"],
 ["Telemundo Noticias Ahora","Estados Unidos","https://xumo-xumoent-ch827-uj0ch.fast.nbcuni.com/live/master.m3u8","nuevo"],
 ["Telemundo Acción","Estados Unidos","https://xumo-drct-ch835-ekq0p.fast.nbcuni.com/live/master.m3u8","nuevo"],
 ["GLORY Kickboxing","Internacional","https://6f972d29.wurl.com/master/f36d25e7e52f1ba8d7e56eb859c636563214f541/UmFrdXRlblRWLWV1X0dsb3J5S2lja2JveGluZ19ITFM/playlist.m3u8","nuevo"]
]
def run(c,passno):
 name,p,url,typ=c
 try:
  cmd=["ffmpeg","-hide_banner","-nostdin","-loglevel","error","-rw_timeout","9000000",
       "-user_agent","Mozilla/5.0","-i",url,"-map","0:v:0","-an","-frames:v","25",
       "-progress","pipe:1","-f","null","-"]
  cp=subprocess.run(cmd,stdout=subprocess.PIPE,stderr=subprocess.PIPE,universal_newlines=True,timeout=29)
  frames=max([int(x) for x in re.findall(r"^frame=(\d+)$",cp.stdout,re.M)] or [0])
  return {"nombre":name,"pasada":passno,"ok":cp.returncode==0 and frames>=20,"frames":frames,
          "error":re.sub(r"https?://\S+","[URL]",cp.stderr[-150:]) if cp.returncode else ""}
 except subprocess.TimeoutExpired:return {"nombre":name,"pasada":passno,"ok":False,"error":"timeout"}
 except Exception as e:return {"nombre":name,"pasada":passno,"ok":False,"error":type(e).__name__}
def main():
 tests=[]
 for n in [1,2]:
  with ThreadPoolExecutor(max_workers=7) as ex:
   for f in as_completed([ex.submit(run,c,n) for c in CANDIDATES]):
    x=f.result();tests.append(x)
    print("PRUEBA",json.dumps(x,ensure_ascii=False),flush=True)
  if n==1:time.sleep(5)
 good=[c for c in CANDIDATES if len([x for x in tests if x["nombre"]==c[0]])==2 and all(x["ok"] for x in tests if x["nombre"]==c[0])]
 for n,p,u,t in good:print("APROBADO",json.dumps({"nombre":n,"pais":p,"url":u,"tipo":t},ensure_ascii=False),flush=True)
 print("RESUMEN",json.dumps({"total":len(CANDIDATES),"ok":len(good),"aprobados":[c[0] for c in good],
  "pendientes":[c[0] for c in CANDIDATES if c not in good]},ensure_ascii=False),flush=True)
if __name__=="__main__":main()
