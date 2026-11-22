#!/usr/bin/env python3
"""Comprobación puntual de variantes y fragmentos HLS declarados públicamente.
No usa credenciales ni descarga video completo."""
import concurrent.futures,json,urllib.request,urllib.parse
base="http://200.80.230.125:5056/"
def get(url,range_header=False):
 headers={"User-Agent":"Mozilla/5.0","Accept":"application/vnd.apple.mpegurl,application/x-mpegURL,*/*"}
 if range_header:headers["Range"]="bytes=0-2047"
 with urllib.request.urlopen(urllib.request.Request(url,headers=headers),timeout=10) as r:
  return r.read(2048 if range_header else 90000),r.status,r.url,r.headers.get("Content-Type","")
page=get(base+"?tvwatch")[0].decode("utf-8","replace")
marker="var Streams = "
pos=page.find(marker)
end=page.find("];",pos)
items=json.loads(page[pos+len(marker):end+1])
wanted={"telefe","tn","c5n","CronicaTv","canal7salta","canal7jujuy"}
def check(c):
 res={"canal":c.get("name"),"id":c.get("m3u8")}
 try:
  data,status,url,ctype=get(c["url"])
  txt=data.decode("utf-8","replace")
  if not txt.lstrip().startswith("#EXTM3U"):raise ValueError("No HLS")
  res["master_status"]=status
  lines=[x.strip() for x in txt.splitlines() if x.strip()]
  variant=None
  for i,line in enumerate(lines[:-1]):
   if line.startswith("#EXT-X-STREAM-INF") and not lines[i+1].startswith("#"):variant=urllib.parse.urljoin(url,lines[i+1]);break
  if variant:
   data,status,url,ctype=get(variant)
   txt=data.decode("utf-8","replace")
   if not txt.lstrip().startswith("#EXTM3U"):raise ValueError("Variante no HLS")
   res["variant_status"]=status
  if "#EXT-X-KEY" in txt:raise ValueError("Manifiesto cifrado; no se inspeccionan fragmentos")
  lines=[x.strip() for x in txt.splitlines() if x.strip()]
  segments=[x for x in lines if not x.startswith("#")]
  res["segment_entries"]=len(segments)
  if not segments:raise ValueError("Sin fragmentos")
  seg=urllib.parse.urljoin(url,segments[0])
  sample,ss,surl,ct=get(seg,True)
  res.update(segment_status=ss,segment_bytes=len(sample),segment_content_type=ct,segment_host=urllib.parse.urlsplit(surl).hostname)
 except Exception as e:res["error"]=type(e).__name__+": "+str(e)[:135]
 print("RESULT",json.dumps(res,ensure_ascii=False),flush=True)
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
 list(pool.map(check,[x for x in items if x.get("m3u8") in wanted]))
