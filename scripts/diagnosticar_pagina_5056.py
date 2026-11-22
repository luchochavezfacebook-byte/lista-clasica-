#!/usr/bin/env python3
"""Analiza solo páginas públicas enlazadas desde la portada del servidor consultado.
No elude autenticación, no enumera URLs ocultas y no descarga video."""
import html, json, re, urllib.request, urllib.error, urllib.parse
from html.parser import HTMLParser

BASE="http://200.80.230.125:5056/"
PATHS=["","?index","?movies","?series","?kids","?tvplay","?search","?help","?login","?downapp"]
class Document(HTMLParser):
 def __init__(self):
  super().__init__(); self.text=[];self.links=[];self.scripts=[];self.forms=[];self.media=[];self.stored=[];self.drop=0;self.heading=False;self.title=False;self.titletext=[];self.headings=[]
 def handle_starttag(self,tag,attrs):
  d=dict(attrs)
  if tag in ("style","script"):self.drop+=1
  if tag=="title":self.title=True
  if tag in ("h1","h2","h3","h4"):self.heading=tag
  if tag=="a":self.links.append({"href":d.get("href",""),"title":d.get("title",""),"aria":d.get("aria-label","")})
  if tag=="script" and d.get("src"):self.scripts.append(d["src"])
  if tag=="form":self.forms.append({"method":d.get("method","GET"),"action":d.get("action","")})
  if tag in ("video","audio","source","iframe"):self.media.append({"tag":tag,"src":d.get("src",""),"type":d.get("type","")})
 def handle_endtag(self,tag):
  if tag in ("style","script"):self.drop=max(0,self.drop-1)
  if tag=="title":self.title=False
  if tag in ("h1","h2","h3","h4"):self.heading=False
 def handle_data(self,data):
  if self.title:self.titletext.append(data)
  if self.heading:self.headings.append(data.strip())
  if not self.drop and data.strip():self.text.append(data.strip())
for path in PATHS:
 url=BASE+path; result={"route":path or "/"}
 try:
  req=urllib.request.Request(url,headers={"User-Agent":"Mozilla/5.0","Accept":"text/html,application/json,*/*"})
  with urllib.request.urlopen(req,timeout=15) as resp:
   raw=resp.read(180000);page=raw.decode("utf-8","replace");target=resp.url
   result.update(status=resp.status,final=target,server=resp.headers.get("Server"),content_type=resp.headers.get("Content-Type"),bytes=len(raw))
  doc=Document();doc.feed(page)
  result.update(title=" ".join(doc.titletext).strip()[:120],headings=[x for x in doc.headings if x][:15],text=" ".join(doc.text)[:850],forms=doc.forms[:10],media=doc.media[:15],scripts=doc.scripts[:20],links=doc.links[:24])
  result["m3u8_count"]=len(re.findall(r"\\.m3u8",page,re.I))
  result["external_links"]=[x for x in re.findall(r"https?://[^'\\\"\\s<>]+",page) if "200.80.230.125" not in x][:10]
  result["javascript_keywords"]={k:len(re.findall(k,page,re.I)) for k in ("m3u8","mpegurl","hls","playlist","videojs","jwplayer","xtream","live","stream","fetch\\(","ajax","player")}
 except Exception as e:result["error"]=type(e).__name__+": "+str(e)[:180]
 print("PAGE",json.dumps(result,ensure_ascii=False),flush=True)
