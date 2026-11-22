#!/usr/bin/env python3
"""Inspección de marcado HTML públicamente accesible del menú TvPlay."""
import collections,html,json,re,urllib.request
from html.parser import HTMLParser
base="http://200.80.230.125:5056/"
class Parser(HTMLParser):
 def __init__(self):
  super().__init__();self.tags=[];self.anchors=[];self.current=None
 def handle_starttag(self,tag,attrs):
  d=dict(attrs)
  if tag in ("a","img","video","source","iframe","button","input"):
   self.tags.append({"tag":tag,"attrs":{k:v[:180] for k,v in d.items() if k in ("href","src","alt","title","id","class","data-id","data-src","onclick","name","type") and isinstance(v,str)}})
  if tag=="a":
   self.current={"href":d.get("href",""),"title":d.get("title",""),"text":""}
   self.anchors.append(self.current)
 def handle_data(self,data):
  if self.current:self.current["text"]+=data.strip()[:100]
 def handle_endtag(self,tag):
  if tag=="a":self.current=None
for route in ("?tvplay","?downapp"):
 req=urllib.request.Request(base+route,headers={"User-Agent":"Mozilla/5.0"})
 with urllib.request.urlopen(req,timeout=15) as f:
  raw=f.read(200000).decode("utf-8","replace")
 p=Parser();p.feed(raw)
 print("ROUTE",route,"LENGTH",len(raw),flush=True)
 print("ANCHORS_TOTAL",len(p.anchors),"COUNTS",json.dumps(collections.Counter(a["href"].split("?")[0] for a in p.anchors).most_common(15)),flush=True)
 print("ANCHORS_NON_MENU",json.dumps([a for a in p.anchors if a["href"] not in ("javascript:void(0)","../?index","../?movies","../?series","../?kids","../?tvplay","../?search","../?help","../?login","../?downapp")][:65],ensure_ascii=False),flush=True)
 print("IMG_ALT_SAMPLES",json.dumps([t for t in p.tags if t["tag"]=="img" and (t["attrs"].get("alt") or t["attrs"].get("title"))][:32],ensure_ascii=False),flush=True)
 print("INPUTS_BUTTONS",json.dumps([t for t in p.tags if t["tag"] in ("input","button")][:35],ensure_ascii=False),flush=True)
 for pattern in ("Grilla","Nacionales","playlist","canal","channel","data-id","data-src","onclick","tvplay","<script"):
  matches=list(re.finditer(re.escape(pattern),raw,re.I))
  samples=[]
  for m in matches[:4]:
   sample=re.sub(r"\\s+"," ",raw[max(0,m.start()-110):min(len(raw),m.end()+260)])
   samples.append(sample[:340])
  print("PATTERN",route,pattern,len(matches),json.dumps(samples,ensure_ascii=False),flush=True)
