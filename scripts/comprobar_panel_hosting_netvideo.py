#!/usr/bin/env python3
"""Auditoría pasiva: comprobar SI el HTML/JS públicos mencionan un panel
de hosting. No adivina rutas, no prueba contraseñas, no escanea puertos."""
import html
import json
import re
import socket
import urllib.parse
import urllib.request
from html.parser import HTMLParser

BASE="http://200.80.230.125:5056/"
PAGES=["","?movies","?tvplay","?help","?login","?downapp","?item=1368337&movie","?watch=1368337&movie"]
HOST = "200.80.230.125"
TERMS=["cpanel","whm","plesk","directadmin","cloudpanel","hestia","cyberpanel",
       "webmin","virtualmin","hosting","vps","datacenter","admin","administrator",
       "backoffice","dashboard","webhost","hostinger","hostgator","serverondemand"]
class Parser(HTMLParser):
 def __init__(self):
  super().__init__();self.src=[];self.links=[]
 def handle_starttag(self,t,attrs):
  d=dict(attrs)
  if t=="script" and d.get("src"):self.src.append(d["src"])
  if t=="a" and d.get("href"):self.links.append(d["href"])
def get(url):
 req=urllib.request.Request(url,headers={"User-Agent":"Mozilla/5.0 (compatible; PassiveSourceAudit/1.0)"})
 with urllib.request.urlopen(req,timeout=14) as response:
  return response.read(100000), response.headers, response.url

assets=set(); observed_urls=set()
for route in PAGES:
 try:
  data,h,url=get(urllib.parse.urljoin(BASE,route))
  page=data.decode("utf-8","replace")
  p=Parser();p.feed(page)
  for value in p.src:
   ref=urllib.parse.urljoin(url,value)
   if urllib.parse.urlsplit(ref).hostname==HOST: assets.add(ref)
  for value in p.links:
   if not value.startswith(("#","javascript:")):
    observed_urls.add(urllib.parse.urljoin(url,value))
  m=re.search("admin",page,re.I)
  if m:
   excerpt=re.sub(r"\\s+"," ",page[max(0,m.start()-130):m.end()+150])
   excerpt=re.sub(r"https?://[^\\s\'\\\"<>]+","[URL]",excerpt)
   print("ADMIN_CONTEXT",json.dumps({"route":route or "/","context":excerpt[:300]},ensure_ascii=False),flush=True)
  print("PAGE",json.dumps({"route":route or "/","status":200,
    "server":h.get("Server"),"powered_by":h.get("X-Powered-By"),
    "script_count":len(p.src),"html_term_count":{t:len(re.findall(re.escape(t),page,re.I)) for t in TERMS if re.search(re.escape(t),page,re.I)},
    "public_script_paths":[urllib.parse.urlsplit(urllib.parse.urljoin(url,x)).path for x in p.src],
   },ensure_ascii=False),flush=True)
 except Exception as e:print("PAGE_ERROR",route,type(e).__name__,flush=True)

# Solo archivos JS explícitamente enlazados; nada de exploración de rutas.
for asset in sorted(assets)[:15]:
 try:
  data,h,u=get(asset);page=data.decode("utf-8","replace")
  hits=[]
  for term in TERMS:
   for match in list(re.finditer(re.escape(term),page,re.I))[:4]:
    raw=page[max(0,match.start()-100):min(len(page),match.end()+140)]
    raw=re.sub(r"https?://[^\s'\"<>]+","[URL_REDACTED]",raw)
    raw=re.sub(r"(?i)(?:token|password|secret|api_key|authorization)\s*[:=]\s*[^\s,;]+","[SENSITIVE_REDACTED]",raw)
    hits.append({"term":term,"excerpt":re.sub(r"\s+"," ",raw)[:210]})
  print("ASSET",json.dumps({"path":urllib.parse.urlsplit(u).path,"size":len(data),
    "matches":hits[:20]},ensure_ascii=False),flush=True)
 except Exception as e:print("ASSET_ERROR",urllib.parse.urlsplit(asset).path,type(e).__name__,flush=True)

print("LINKS_RELATED",json.dumps(sorted([
  {"host":urllib.parse.urlsplit(u).hostname,"path":urllib.parse.urlsplit(u).path}
  for u in observed_urls
  if any(t in u.lower() for t in TERMS)
]),ensure_ascii=False),flush=True)
try:
 print("PTR_RECORD",json.dumps({"hostname":socket.gethostbyaddr(HOST)[0]}),flush=True)
except Exception as e:
 print("PTR_ERROR",type(e).__name__,flush=True)
