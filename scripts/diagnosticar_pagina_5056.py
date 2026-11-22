#!/usr/bin/env python3
"""Lectura de fuentes públicamente declaradas; prueba limitada de manifiestos.
No realiza autenticación ni descarga contenidos audiovisuales completos."""
import concurrent.futures,collections,json,re,urllib.request,urllib.parse,urllib.error
from urllib.parse import urlsplit
base="http://200.80.230.125:5056/"
req=urllib.request.Request(base+"?tvwatch",headers={"User-Agent":"Mozilla/5.0"})
with urllib.request.urlopen(req,timeout=15) as f:page=f.read(200000).decode("utf-8","replace")
marker="var Streams = "
pos=page.find(marker)
if pos < 0:raise RuntimeError("Streams no encontrado")
end=page.find("];",pos)
streams=json.loads(page[pos+len(marker):end+1])
hosts=collections.Counter(urlsplit(c.get("url","")).hostname for c in streams)
m3u=[c for c in streams if ".m3u8" in c.get("url","").lower()]
print("CATALOG",json.dumps({"total":len(streams),"m3u8":len(m3u),"schemes":scheme,"domains":hosts,"non_m3u8":[{"name":c["name"],"scheme":urlsplit(c.get("url","")).scheme,"host":urlsplit(c.get("url","")).hostname} for c in streams if c not in m3u]},ensure_ascii=False),flush=True)
targets={"telefe","eltrece","tvpublica","tn","CronicaTv","c5n","canal7salta","10MardelPlata","telemax","canal7jujuy","5tv"}
selected=[c for c in streams if c.get("m3u8") in targets]
def check(c):
 u=c["url"]; result={"channel":c["name"],"id":c.get("m3u8"),"source_scheme":urlsplit(u).scheme,"source_host":urlsplit(u).hostname}
 try:
  req=urllib.request.Request(u,headers={"User-Agent":"Mozilla/5.0","Accept":"application/vnd.apple.mpegurl,application/x-mpegURL,*/*"})
  with urllib.request.urlopen(req,timeout=10) as r:
   data=r.read(35000).decode("utf-8","replace"); result.update(http_status=r.status,content_type=r.headers.get("Content-Type",""),redirect_host=urlsplit(r.url).hostname)
  result["valid_hls"]=data.lstrip().startswith("#EXTM3U")
  result["media_segments"]=len(re.findall(r"#EXTINF:",data))
  result["variants"]=len(re.findall(r"#EXT-X-STREAM-INF",data))
  result["encrypted"]=("#EXT-X-KEY" in data)
 except Exception as e: result["error"]=type(e).__name__+": "+str(e)[:130]
 print("TEST",json.dumps(result,ensure_ascii=False),flush=True)
with concurrent.futures.ThreadPoolExecutor(max_workers=5) as pool:list(pool.map(check,selected))
