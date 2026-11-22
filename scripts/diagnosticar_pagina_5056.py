#!/usr/bin/env python3
"""Inventario de TVPlay público comparado con Lista Clásica.
No descarga medios ni publica las rutas de acceso o identificadores opacos."""
import json,re,urllib.request,collections,unicodedata,difflib
from pathlib import Path
from urllib.parse import urlsplit
ROOT=Path(__file__).resolve().parents[1]
def norm(value):
 s=''.join(x for x in unicodedata.normalize("NFKD",str(value).casefold()) if not unicodedata.combining(x))
 s=re.sub(r"\\([^)]*\\)"," ",s)
 return re.sub(r"[^a-z0-9]+","",s).replace("television","tv")
catalog=[]
for p in ["fuentes.json","fuentes_mundotv.json","fuentes_populares_2026.json","fuentes_noviembre_2026.json"]:
 catalog.extend(json.loads((ROOT/p).read_text(encoding="utf-8"))["canales"])
names={norm(x["nombre"]):x["nombre"] for x in catalog}
ids={norm(x["tvg_id"].replace(".ar","")):x["nombre"] for x in catalog}
URL="http://200.80.230.125:5056/?tvwatch"
req=urllib.request.Request(URL,headers={"User-Agent":"Mozilla/5.0","Accept":"text/html"})
with urllib.request.urlopen(req,timeout=15) as r: page=r.read(150000).decode("utf-8","replace")
marker="var Streams = "
a=page.find(marker)
b=page.find("];",a)
if a<0 or b<0:raise RuntimeError("Streams no disponible")
streams=json.loads(page[a+len(marker):b+1])
aliases={
"tvpublica":"tv publica","canalnet":"net tv","c26":"canal 26","lntv":"la nacion",
"canal7jujuy":"canal 7 jujuy","canal7salta":"canal 7 salta","c7nq":"canal 7 neuquen",
"rtnneuquen":"rtn","canal9televida":"canal 9 televida",
"cronicatv":"cronica tv","tn":"tn","a24":"a24","c5n":"c5n",
"americatv":"america tv","eltrece":"el trece","telemax":"telemax",
"5tv":"5tv","cn247":"24/7 canal de noticias","10mardelplata":"canal 10 mar del plata",
"redbull":"red bull tv","argentinisima":"argentinisima satelital",
"garage":"garage tv","multivision":"multivision federal",
"ciudadchaco":"ciudad tv resistencia","canalorbe21":"canal orbe 21",
"ewtn":"ewtn","t5satelital":"t5 satelital","canalluz":"canal luz","musictop":"music top",
"portalfoxmix":"portal foxmix","oneworldradio":"one world radio"}
def match(c):
 key=norm(c["name"]); id=norm(c["m3u8"]); candidates=[key,id]
 if id in aliases:candidates.append(norm(aliases[id]))
 if key in aliases:candidates.append(norm(aliases[key]))
 hit=next((names[v] for v in candidates if v in names),None)
 if not hit: hit=next((ids[v] for v in candidates if v in ids),None)
 close=difflib.get_close_matches(key,names.keys(),n=2,cutoff=.79)
 return hit,[names[v] for v in close]
def src_type(c):
 u=urlsplit(c["url"])
 return {"type":"hls" if u.path.lower().endswith(".m3u8") else "other","scheme":u.scheme,"host":u.hostname,"opaque_32hex_path":bool(re.search(r"/[a-f0-9]{32}/",u.path,re.I))}
print("COUNT",len(streams),"HLS",sum(src_type(c)["type"]=="hls" for c in streams),flush=True)
for c in streams:
 h,similar=match(c);src=src_type(c)
 print("ENTRY",json.dumps({"id":c.get("m3u8"),"name":c["name"],"source_type":src["type"],"host":src["host"],"opaque_path":src["opaque_32hex_path"],"matched":h,"similar":similar[:2]},ensure_ascii=False),flush=True)
