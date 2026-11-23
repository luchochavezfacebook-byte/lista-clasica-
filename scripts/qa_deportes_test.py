#!/usr/bin/env python3
"""QA de señales deportivas en acceso abierto: dos intentos de decodificación.
No distribuye streams de suscripción ni publica listas sin prueba de video.
No añade estas señales a Lista Clásica de producción.
"""
import concurrent.futures
import json
import re
import subprocess
import time

# Fuentes en listas públicas de iptv-org; preferentemente CDNs oficiales/FAST.
# Evitar servidores de reemisión premium, credenciales y firmas temporales.
STREAMS=[
 ("TVS Sports","Estados Unidos","https://rpn.bozztv.com/gusa/gusa-tvssports/index.m3u8"),
 ("TVS Classic Sports","Estados Unidos","https://rpn.bozztv.com/gusa/gusa-tvs/index.m3u8"),
 ("TVS Sports Bureau","Estados Unidos","https://rpn.bozztv.com/gusa/gusa-tvssportsbureau/index.m3u8"),
 ("TVS Women Sports","Estados Unidos","https://rpn.bozztv.com/gusa/gusa-tvswsn/index.m3u8"),
 ("Fight Network","Canadá","https://d12a2vxqkkh1bo.cloudfront.net/hls/main.m3u8"),
 ("Willow Sports FAST","Estados Unidos","https://amg01269-amg01269c1-sportstribal-emea-5204.playouts.now.amagi.tv/ts-eu-w1-n2/playlist/amg01269-willowtvfast-willowplus-sportstribalemea/playlist.m3u8"),
 ("Esport3","España","https://directes-tv-int.3catdirectes.cat/live-content/esport3-hls/master.m3u8"),
 ("Esport3 (alternativa oficial)","España","https://directes-tv-int.3catdirectes.cat/live-origin/esport3-hls/master.m3u8"),
 ("Teledeporte RTVE","España","https://rtvelivestream.rtve.es/rtvesec/tdp/tdp_main.m3u8"),
 ("N Sports","Brasil","https://ogc-nsprt-tcl-roku-syndication.otteravision.com/ogc/nsprt/nsprt.m3u8"),
 ("África 24 Sport","Francia","https://africa24.vedge.infomaniak.com/livecast/ik:africa24sport/manifest.m3u8"),
 ("DD Sports HD","India","https://cdn.pishow.tv/ott/live/1161/master.m3u8"),
 ("DD Sports","India","https://mumbai-edge.smartplaytv.in/DDSportsHD/index.m3u8"),
 ("Trace Sport Stars","Francia","https://channels.trace.plus/Traceprod/TRACE_SPORT_STARS_sd/index.m3u8"),
 ("Sport1 Alemania","Alemania","https://r.eu.cdn-redge.media/livehls/oeu/mt/live/sport1/live.livx/playlist.m3u8"),
 ("FTF Sports (respaldo)","Estados Unidos","https://1657061170.rsc.cdn77.org/HLS/FTF-LINEAR.m3u8")
]
def test(item,phase):
 name,country,url=item
 try:
  cp=subprocess.run(["ffmpeg","-hide_banner","-nostdin","-loglevel","error",
   "-rw_timeout","10000000","-user_agent","Mozilla/5.0",
   "-i",url,"-map","0:v:0","-an","-frames:v","25",
   "-progress","pipe:1","-f","null","-"],
   capture_output=True,text=True,timeout=30)
  frames=max([int(x) for x in re.findall(r"^frame=(\d+)$",cp.stdout,re.M)] or [0])
  return {"name":name,"pass":phase,"ok":cp.returncode==0 and frames>=20,"frames":frames,
    "error":re.sub(r"https?://\S+","[URL]",cp.stderr[-170:]) if cp.returncode else ""}
 except subprocess.TimeoutExpired:
  return {"name":name,"pass":phase,"ok":False,"frames":0,"error":"timeout"}
 except Exception as e:
  return {"name":name,"pass":phase,"ok":False,"frames":0,"error":type(e).__name__}
def main():
 results={}
 for phase in (1,2):
  with concurrent.futures.ThreadPoolExecutor(max_workers=7) as pool:
   jobs=[pool.submit(test,x,phase) for x in STREAMS]
   for future in concurrent.futures.as_completed(jobs):
    row=future.result()
    results.setdefault(row["name"],[]).append(row)
    print("QA",json.dumps(row,ensure_ascii=False),flush=True)
  if phase==1:time.sleep(5)
 good=[]
 for name,country,url in STREAMS:
  checks=results.get(name,[])
  if len(checks)==2 and all(x["ok"] for x in checks):
   good.append({"nombre":name,"pais":country,"url":url})
   print("APROBADO",json.dumps(good[-1],ensure_ascii=False),flush=True)
 print("RESUMEN",json.dumps({"candidatos":len(STREAMS),"aprobados":len(good),
  "pendientes":[name for name,country,url in STREAMS if name not in {c["nombre"] for c in good}]},ensure_ascii=False),flush=True)
if __name__=="__main__":main()
