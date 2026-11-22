#!/usr/bin/env python3
"""Inspección de rutas públicas vinculadas a TvPlay; sin autenticación."""
import collections,json,re,urllib.request
base="http://200.80.230.125:5056/"
for route in ("?tvplay","?tvwatch"):
 req=urllib.request.Request(base+route,headers={"User-Agent":"Mozilla/5.0"})
 try:
  with urllib.request.urlopen(req,timeout=15) as f:
   page=f.read(150000).decode("utf-8","replace")
   status=f.status
 except Exception as e:
  print("ERROR",route,type(e).__name__,str(e)[:130],flush=True);continue
 title=re.search(r"<title[^>]*>(.*?)</title>",page,re.I|re.S)
 print("PAGE",route,"STATUS",status,"TITLE",title.group(1).strip() if title else "-","SIZE",len(page),flush=True)
 if route=="?tvplay":
  items=re.findall(r"onclick=[\"']appClick\\([\"']([^\"']+)",page,re.I)
  logos=re.findall(r"<a[^>]*onclick=[\"']appClick\\([\"']([^\"']+)[\"']\\);[^>]*>\\s*<div>\\s*<img[^>]+src=[\"']([^\"']+)",page,re.I|re.S)
  print("CHANNELS_COUNT",len(items),"IDS",json.dumps(items,ensure_ascii=False),flush=True)
  print("LOGOS",json.dumps(logos[:70],ensure_ascii=False),flush=True)
 else:
  print("M3U8_COUNT",len(re.findall(r"\\.m3u8",page,re.I)),"IFRAME_COUNT",len(re.findall(r"<iframe",page,re.I)),flush=True)
  for pattern in ("tvwatch","video","login","session","player","m3u8","jwplayer","mpegurl","stream","script","fetch","ajax"):
   matches=list(re.finditer(pattern,page,re.I))
   snippets=[re.sub(r"\\s+"," ",page[max(0,m.start()-130):min(len(page),m.end()+400)])[:520] for m in matches[:3]]
   print("FIND",pattern,len(matches),json.dumps(snippets,ensure_ascii=False),flush=True)
