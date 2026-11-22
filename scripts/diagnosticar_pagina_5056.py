#!/usr/bin/env python3
"""Pruebas técnicas de señales TvPlay públicas autorizadas para inventario.
No escribe ni muestra URLs o rutas opacas en registros. No requiere autenticación."""
import concurrent.futures,datetime,json,re,subprocess,urllib.request,urllib.error,urllib.parse
from pathlib import Path
from urllib.parse import urlsplit
ROOT=Path(__file__).resolve().parents[1]
PAGE="http://200.80.230.125:5056/?tvwatch"
headers={"User-Agent":"Mozilla/5.0","Accept":"application/vnd.apple.mpegurl,application/x-mpegURL,*/*"}
with urllib.request.urlopen(urllib.request.Request(PAGE,headers=headers),timeout=15) as r:
 page=r.read(160000).decode("utf-8","replace")
mark="var Streams = ";a=page.find(mark);b=page.find("];",a)
if a<0 or b<0:raise RuntimeError("Streams no encontrado")
streams=json.loads(page[a+len(mark):b+1])
already={"eltrece","americatv","argentinisima","a24","c26","Multivision","telemax","CanalNet","t5satelital","c5sf","10MardelPlata","canal7jujuy","canal7salta","c7nq","cn247","ciudadchaco","5tv","canalorbe21","EWTN","canalluz","tn","4sanjuan","RedBull","Airang","garage","portalfoxmix"}
# Sin duplicados: canal ya presente, sin importar la dirección usada por proveedor.
selection=[c for c in streams if c.get("m3u8") not in already and urlsplit(c.get("url","")).path.lower().endswith(".m3u8")]
print("OVERVIEW",json.dumps({"stream_total":len(streams),"hls_total":sum(urlsplit(c.get("url","")).path.lower().endswith(".m3u8") for c in streams),"excluded_duplicate_ids":len(already),"candidates":len(selection)}),flush=True)
def get(url, peek=False):
 req=urllib.request.Request(url,headers={**headers,**({"Range":"bytes=0-2047"} if peek else {})})
 with urllib.request.urlopen(req,timeout=11) as r:
  return r.read(2048 if peek else 160000),r.status,r.url
def test(c):
 name=c["name"];result={"id":c["m3u8"],"name":name,"stage":"start","frames":0}
 try:
  uri=c["url"]
  payload,st,real=get(uri);txt=payload.decode("utf-8-sig","replace")
  if not txt.lstrip().startswith("#EXTM3U"):raise ValueError("invalid_manifest")
  result["master_status"]=st;result["stage"]="master"
  lines=[line.strip() for line in txt.splitlines() if line.strip()]
  variants=[urllib.parse.urljoin(real,lines[i+1]) for i,ln in enumerate(lines[:-1]) if ln.startswith("#EXT-X-STREAM-INF") and not lines[i+1].startswith("#")]
  if variants:
   payload,st,real=get(variants[-1]);txt=payload.decode("utf-8-sig","replace")
   if not txt.lstrip().startswith("#EXTM3U"):raise ValueError("invalid_variant")
   result["variant_status"]=st
  result["stage"]="variant"
  if "#EXT-X-KEY" in txt:raise ValueError("encrypted_hls")
  segs=[ln.strip() for ln in txt.splitlines() if ln.strip() and not ln.startswith("#")]
  if not segs:raise ValueError("missing_segments")
  sample,ss,su=get(urllib.parse.urljoin(real,segs[0]),True)
  if not sample or ss not in (200,206):raise ValueError("segment_unavailable")
  result["segment_status"]=ss;result["stage"]="segment"
  cmd=["ffmpeg","-nostdin","-hide_banner","-loglevel","error","-rw_timeout","12000000","-user_agent",headers["User-Agent"],"-i",uri,"-t","2","-map","0:v:0","-an","-f","null","-","-progress","pipe:1"]
  proc=subprocess.run(cmd,stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True,timeout=35)
  frames=[int(v) for v in re.findall(r"(?m)^frame=([0-9]+)$",proc.stdout)]
  result["frames"]=max(frames) if frames else 0
  result["status"]="video_ok" if proc.returncode==0 and result["frames"]>=20 else "no_video"
  result["stage"]="decoded" if result["status"]=="video_ok" else "decode_error"
  result["audio_hint"]=bool(re.search(r"Audio:",proc.stderr))
 except urllib.error.HTTPError as e:
  result["status"]="http_error";result["code"]=e.code
 except Exception as e:
  result["status"]="error";result["error_type"]=type(e).__name__;result["stage_reason"]=(str(e) if isinstance(e,ValueError) else "")[:80]
 print("RESULT",json.dumps(result,ensure_ascii=False),flush=True)
 return result
with concurrent.futures.ThreadPoolExecutor(max_workers=7) as pool:
 results=list(pool.map(test,selection))
summary={"candidates":len(results),"video_ok":sum(x.get("status")=="video_ok" for x in results),"manifest_ok":sum(x.get("master_status")==200 for x in results),"segment_ok":sum(x.get("segment_status") in (200,206) for x in results)}
print("SUMMARY",json.dumps(summary),flush=True)
