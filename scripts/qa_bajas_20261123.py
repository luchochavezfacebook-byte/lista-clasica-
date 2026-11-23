#!/usr/bin/env python3
"""Verificación real de video para fuentes fallidas en tres auditorías.
No guarda segmentos ni toca la lista; salidas aptas para decidir bajas.
"""
import concurrent.futures, json, re, subprocess, time
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
CATALOGS=[
 "fuentes.json","fuentes_mundotv.json",
 "fuentes_populares_2026.json","fuentes_noviembre_2026.json",
 "fuentes_netvideo_2026.json","fuentes_tvplay_es_2026.json",
 "fuentes_regionales_20261123.json"
]
FAILED_NAMES={
 "TV Universidad (UNLP)","Canal 4 Jujuy","Canal 4 San Juan",
 "Canal 7 Jujuy","Canal 21 TV","TeleCinco Trelew","TV Solidaria",
 "Salsa Gorda Television","Cadena Elite España","Verbena TV España",
 "4FUN TV Polonia PL","Dance TV Estonia","Retro Plus TV Chile",
 "Canal Sur Andalucía","7TV Granada","Canal 6 Multimedios Mexico",
 "TV Perú","TV Perú Noticias","Canal IPe Perú","Oromar TV Ecuador",
 "Avivamiento TV","Radio Sublime Gracia TV","TV Maná Argentina",
 "Solidaria TV España","TBN España","CGTN China",
 "Republic World TV India EN","ServusTV WetterPanorama",
 "Ultra Casanare TV","Ondambiental TV",
 "Canal 12 Venado Tuerto","Canal 2 de Ushuaia",
 "Canal 10 Mar del Plata","Neo TV"
}
# Alternativas para las MISMAS señales, de fuentes abiertas con URL HTTPS.
ALTERNATES=[
 {"id":"alt:Salsa Gorda Television","name":"Salsa Gorda Television","url":"https://stmv1.voxtvhd.com.br/salsagorda/salsagorda/playlist.m3u8","pais":"Colombia"},
 {"id":"alt:4FUN TV Polonia PL:sd","name":"4FUN TV Polonia PL","url":"https://stream.4fun.tv:8888/sd/4fun_sd_high.m3u8","pais":"Polonia"},
 {"id":"alt:4FUN TV Polonia PL:hls","name":"4FUN TV Polonia PL","url":"https://stream.4fun.tv:8888/hls/4f.m3u8","pais":"Polonia"},
 {"id":"alt:Canal IPe Perú","name":"Canal IPe Perú","url":"https://bantel-cdn1.iptvperu.tv:1936/btnscrtn/ipe.stream/playlist.m3u8","pais":"Perú"},
 {"id":"alt:Oromar TV Ecuador Plus","name":"Oromar TV+ (distinto canal, no reemplaza)","url":"https://stream.oromar.tv/hls/camriva/index.m3u8","pais":"Ecuador"},
 {"id":"alt:Republic TV India (distinto canal)","name":"Republic TV India (distinto canal, no reemplaza Republic World TV)","url":"https://samsung-republictv.amagi.tv/ts-ap-s1-n1/playlist/samsungin-republictv-samsungindia/playlist.m3u8","pais":"India"}
]
def probe(item,phase):
 p={"id":item["id"],"name":item["nombre"],"phase":phase}
 if not item["url"].startswith("https://"):return dict(p,ok=False,why="no HTTPS")
 try:
  cmd=["ffmpeg","-hide_banner","-nostdin","-loglevel","error",
       "-rw_timeout","10000000","-user_agent",item.get("user_agent") or "Mozilla/5.0"]
  if item.get("referrer"):cmd+=["-referer",item["referrer"]]
  cmd+=["-i",item["url"],"-map","0:v:0","-an","-frames:v","25","-progress","pipe:1","-f","null","-"]
  cp=subprocess.run(cmd,capture_output=True,text=True,timeout=28)
  frames=max([int(x) for x in re.findall(r"^frame=(\d+)$",cp.stdout,re.M)] or [0])
  return dict(p,ok=(cp.returncode==0 and frames>=20),frames=frames,status=cp.returncode,
              error="" if cp.returncode==0 else re.sub(r"https?://\S+","[URL]",cp.stderr[-240:])[:180])
 except subprocess.TimeoutExpired:return dict(p,ok=False,error="timeout")
 except Exception as ex:return dict(p,ok=False,error=type(ex).__name__)
def main():
 data=[]
 for file in CATALOGS:
  p=ROOT/file
  if not p.exists():continue
  data.extend(dict(x,archivo=file,id=x["tvg_id"]) for x in json.loads(p.read_text())["canales"] if x["nombre"] in FAILED_NAMES)
 for a in ALTERNATES:
  data.append({"nombre":a["name"],"id":a["id"],"url":a["url"],"pais":a["pais"],"archivo":"alternativa"})
 print("TOTAL",len(data),"candidatos incluidos repetidos + alternativas",flush=True)
 results=[]
 for phase in (1,2):
  with concurrent.futures.ThreadPoolExecutor(max_workers=8) as executor:
   for res in concurrent.futures.as_completed([executor.submit(probe,x,phase) for x in data]):
    value=res.result()
    results.append(value)
    print("VIDEO",json.dumps(value,ensure_ascii=False),flush=True)
  if phase==1:time.sleep(6)
 by={}
 for x in results:by.setdefault(x["id"],[]).append(x)
 passed=[item["id"] for item in data if len(by.get(item["id"],[]))==2 and all(x["ok"] for x in by[item["id"]])]
 failed=[item["id"] for item in data if item["id"] not in passed]
 print("RESUMEN",json.dumps({"total":len(data),"aprobados":passed,"fallidos":failed},ensure_ascii=False),flush=True)
if __name__=="__main__":main()
