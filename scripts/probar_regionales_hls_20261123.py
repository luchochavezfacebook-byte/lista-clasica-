#!/usr/bin/env python3
"""Prueba de HLS de canales regionales gratuitos publicados en iptv-org.
No prueba fuentes de pago, contraseñas ni requiere tokens.
No altera catálogos ni importa resultados: la salida es evidencia de QA.
"""
from concurrent.futures import ThreadPoolExecutor, as_completed
import hashlib, json, re, subprocess, time, urllib.parse

# Fuentes publicadas en iptv-org, identificadas por código de país y tvg-id.
# Los enlaces se cotejaron con los catálogos de noviembre de 2026.
CANDIDATES=[
 ["Canal 10 Córdoba","Argentina","https://stream.arcast.net:4443/canal10/ngrp:canal10_all/playlist.m3u8","nuevo"],
 ["Canal 13 Jujuy TV","Argentina","https://genexservicios.com:19360/canal13jujuy/canal13jujuy.m3u8","nuevo"],
 ["Canal 79 Mar del Plata","Argentina","https://streamconex.com:19360/mardelplata/mardelplata.m3u8","nuevo"],
 ["Canal 8 San Juan","Argentina","https://live20.bozztv.com/akamaissh101/ssh101/canal8sanjuan/playlist.m3u8","nuevo"],
 ["Canal 10 Chiapas","México","https://5ca9af4645e15.streamlock.net/chiapas/videochiapas/playlist.m3u8","nuevo"],
 ["Canal 10 Durango","México","https://5e50264bd6766.streamlock.net/canal10durango/videocanal10durango/playlist.m3u8","nuevo"],
 ["Canal 8 La Paz","México","https://s5.mexside.net:1936/xhbzc81/xhbzc81/playlist.m3u8","nuevo"],
 ["Onda Cádiz 24h","España","https://ondacadiztv.es:30443/octv/24h/playlist.m3u8","nuevo"],
 ["Canal 8 Visión TV","Paraguay","https://tigocloudgen.desdeparaguay.net/satelitaltv/satelitaltv/playlist.m3u8","nuevo"],
 ["Radio Turrialba TV Sports","Costa Rica","https://sc1.escuela4.com/live/d7316d659b5a77fb8719d49330315886807b02b0.m3u8","nuevo"],
 ["TV Perú","Perú","https://cdnhd3.iblups.net/hls/2ee85c7a0aff45d4b0f05552d81cadb07.m3u8","respaldo"],
 ["Canal 24 Horas RTVE","España","https://n-5-2.eu.cdn-redge.media/livehls/oeu/mt/live/24h/live.livx/playlist.m3u8","respaldo"]
]
def probe(x,pass_id):
 name,country,url,kind=x
 try:
  p=urllib.parse.urlsplit(url)
  if p.scheme!="https" or not p.hostname or p.username or p.password or p.query or not p.path.lower().endswith(".m3u8"):
   return {"name":name,"phase":pass_id,"ok":False,"error":"No HLS HTTPS estable"}
  cp=subprocess.run(["ffmpeg","-hide_banner","-nostdin","-loglevel","error","-rw_timeout","10000000",
     "-user_agent","Mozilla/5.0","-i",url,"-map","0:v:0","-an","-frames:v","30",
     "-progress","pipe:1","-f","null","-"],capture_output=True,text=True,timeout=32)
  frames=max([int(n) for n in re.findall(r"^frame=(\d+)$",cp.stdout,re.M)] or [0])
  return {"name":name,"phase":pass_id,"ok":cp.returncode==0 and frames>=20,"frames":frames,
     "error":cp.stderr[-120:].replace(url,"[STREAM]") if cp.returncode else ""}
 except subprocess.TimeoutExpired:return {"name":name,"phase":pass_id,"ok":False,"error":"timeout"}
 except Exception as e:return {"name":name,"phase":pass_id,"ok":False,"error":str(e)[:100]}
def main():
 results=[]
 for pass_id in [1,2]:
  with ThreadPoolExecutor(max_workers=5) as pool:
   ff={pool.submit(probe,c,pass_id):c[0] for c in CANDIDATES}
   for f in as_completed(ff):
    row=f.result()
    print("PRUEBA",json.dumps(row,ensure_ascii=False),flush=True)
    results.append(row)
  if pass_id==1:time.sleep(4)
 good=[]
 for ch in CANDIDATES:
  n=ch[0];z=[r for r in results if r["name"]==n]
  if len(z)==2 and all(x["ok"] for x in z):good.append(ch)
 for n,p,u,typ in good:
  print("APROBADO",json.dumps({"nombre":n,"pais":p,"url":u,"tipo":typ},ensure_ascii=False),flush=True)
 print("RESUMEN",json.dumps({"probados":len(CANDIDATES),"aprobados":len(good),
  "pendientes":[n for n,p,u,k in CANDIDATES if n not in [x[0] for x in good]]},ensure_ascii=False),flush=True)
if __name__=="__main__":main()
