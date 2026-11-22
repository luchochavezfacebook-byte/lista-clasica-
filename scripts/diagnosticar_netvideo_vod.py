#!/usr/bin/env python3
"""Audita SOLO el catálogo público VOD de Netvideo: metadatos y comportamiento
de páginas visibles, sin descargar medios, descifrar ni iniciar sesión."""
from urllib.request import Request, urlopen
from urllib.parse import urljoin, urlsplit, parse_qs
from html.parser import HTMLParser
from collections import Counter
import re, json

BASE = "http://200.80.230.125:5056/"
HEADERS = {"User-Agent": "Mozilla/5.0 (compatible; PublicCatalogAudit/1.0)"}

class PageParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.anchors = []; self.images = []; self.headings = []; self.forms = []
        self.meta=[]; self.title=""; self._active=None; self._tag=None
    def handle_starttag(self, tag, attrs):
        d=dict(attrs)
        if tag=="a":
            self._active={"href":d.get("href",""),"text":""}
            self.anchors.append(self._active)
        if tag=="img": self.images.append({k:d.get(k) for k in ("src","alt","title","loading") if k in d})
        if tag in ("h1","h2","h3","h4"):
            self._tag=tag; self.headings.append({"tag":tag,"text":""})
        if tag=="form": self.forms.append({"method":d.get("method","GET"),"action":d.get("action","")})
        if tag=="meta" and (d.get("name") or d.get("property")):
            if (d.get("name") or d.get("property")) in ("description","og:description","og:title","og:image"):
                self.meta.append({"tag":d.get("name") or d.get("property"),"value":d.get("content","")[:160]})
    def handle_data(self,data):
        if self._active is not None: self._active["text"]+=data[:100]
        if self._tag is not None and self.headings: self.headings[-1]["text"]+=data[:120]
    def handle_endtag(self,tag):
        if tag=="a": self._active=None
        if tag in ("h1","h2","h3","h4"):self._tag=None

def fetch(route):
    req=Request(urljoin(BASE,route),headers=HEADERS)
    with urlopen(req,timeout=16) as resp:
        raw=resp.read(200000)
        return {"status":resp.status,"content_type":resp.headers.get("Content-Type",""),"url":resp.url,"body":raw.decode("utf-8","replace")}

def detail(route,body):
    parser=PageParser()
    parser.feed(body)
    matches=re.findall(r"(?:\?|\.\./\?)(?:item=)([0-9]+)&(?:movie|serie)",body,re.I)
    variants=re.findall(r"(?:href|onclick|action|src)=(?:['\"])([^'\"]+)",body,re.I)
    title=re.search(r"<title\b[^>]*>(.*?)</title>",body,re.S|re.I)
    # Un poco de marcado circundante permite identificar si hay metadatos estructurados
    markers={}
    for phrase in ("cargar más","Tendencias","Estrenos","Agregados Recientes","temporad","reparto","duración","sinopsis","géneros","trailer","ver ahora","servidor","video","player","nextPage","ajax","fetch(","poster/","tmdb","IMDb","data-id"):
        hits=list(re.finditer(re.escape(phrase),body,re.I))
        markers[phrase]=len(hits)
        if phrase in ("cargar más","nextPage","ajax","fetch(","data-id") and hits:
            m=hits[0]
            excerpt=re.sub(r"\s+"," ",body[max(0,m.start()-100):m.start()+170])
            markers[phrase+"_context"]=excerpt[:270]
    external_links=[u for u in variants if u.startswith(("http://","https://")) and urlsplit(u).hostname!="200.80.230.125"]
    return {
        "http": 200,
        "title":re.sub(r"<[^>]*>","",title.group(1)).strip()[:80] if title else None,
        "size_chars":len(body),
        "unique_movie_or_serie_ids":len(set(matches)),
        "sample_item_ids":list(dict.fromkeys(matches))[:15],
        "anchor_count":len(parser.anchors),
        "image_count":len(parser.images),
        "image_samples":parser.images[:8],
        "heading_samples":parser.headings[:12],
        "link_samples":[a for a in parser.anchors if "item=" in a["href"]][:6],
        "forms":parser.forms[:6],
        "markers":markers,
        "external_hosts":list(dict.fromkeys(urlsplit(u).hostname for u in external_links))[:8],
        "meta":parser.meta[:6],
        "file_extensions":Counter(re.findall(r"\.(m3u8|mp4|mkv|mpd)\b",body,re.I)),
        "has_jsonld":'application/ld+json' in body,
    }

PAGES=["?movies","?series","?kids","?index"]
page_results={}
for route in PAGES:
    try:
        res=fetch(route); data=detail(route,res["body"])
        data["http"]=res["status"];data["content_type"]=res["content_type"]
        page_results[route]=data
        print("PAGE",json.dumps({"route":route,**data},ensure_ascii=False,default=dict),flush=True)
    except Exception as e:
        print("ERROR",json.dumps({"route":route,"error_type":type(e).__name__,"error":str(e)[:120]}),flush=True)
# Abrir solo 2 detalles públicos enlazados desde la sección Movies.
listing=fetch("?movies")["body"]
ids=list(dict.fromkeys(re.findall(r"\?item=([0-9]+)&movie",listing,re.I)))
print("MOVIES_LINKED",len(ids),flush=True)
for mid in ids[:2]:
    route=f"?item={mid}&movie"
    try:
        res=fetch(route); d=detail(route,res["body"])
        # Exposición de metadatos o claves de video: solo registrar tipo, NO URLs.
        d["http"]=res["status"]
        d["media_urls_present"] = bool(re.search(r'https?://[^"\s<>]+\.(?:m3u8|mp4|mpd)',res["body"],re.I))
        d["login_text_present"] = bool(re.search(r"iniciar sesi[oó]n|ingresar|registrarse",res["body"],re.I))
        print("DETAIL",json.dumps({"route":route,**d},ensure_ascii=False,default=dict),flush=True)
    except Exception as e: print("DETAIL_ERROR",str(e)[:150],flush=True)


# Revisión del flujo visible en la sección Películas y una ficha de ejemplo.
for route in ("?movies","?item=1368337&movie","?series"):
    try:
        page=fetch(route)["body"]
        print("FLOW_ROUTE",route,flush=True)
        for phrase in ("cargar más","loadmore","loadMore","MoreItems","?movies&","?item=","?watch","?play","?movie","?server","ver película","reproducir","playvideo","movieplay","data-link","location.href","window.location","href=\"javascript:void(0)\"","action=","onclick="):
            hits=list(re.finditer(re.escape(phrase),page,re.I))
            examples=[]
            for m in hits[:2]:
                excerpt=page[max(0,m.start()-220):min(len(page),m.end()+300)]
                excerpt=re.sub(r"\s+"," ",excerpt)
                # El HTML puede incluir recursos privados. No volcar URLs multimedia ni sesiones.
                excerpt=re.sub(r"https?://[^ \t\"'<>\n]+", "[URL]", excerpt)
                examples.append(excerpt[:500])
            print("FLOW",json.dumps({"phrase":phrase,"count":len(hits),"excerpts":examples},ensure_ascii=False),flush=True)
        # Eventos de interfaz con referencias a reproducción / páginas adicionales.
        tags=re.findall(r"<(?:a|button|form)\b[^>]{0,700}>",page,re.I|re.S)
        relevant=[re.sub(r"\s+"," ",tag)[:400] for tag in tags if any(p in tag.lower() for p in ("cargar","ver ahora","reprod","load","pagin","play","watch","movie","item="))]
        print("FLOW_ACTION_TAGS",json.dumps(relevant[:28],ensure_ascii=False),flush=True)
    except Exception as e:print("FLOW_ERROR",route,type(e).__name__,str(e)[:140],flush=True)


# Comprobación controlada de páginas enlazadas y de la ruta del reproductor visible.
for route in ("?movies&page=1","?movies&page=2","?movies&page=3","?watch=1368337&movie","?item=1368337&movie"):
    try:
        res=fetch(route)
        page=res["body"]
        mids=list(dict.fromkeys(re.findall(r"\?item=([0-9]+)&movie",page,re.I)))
        title=re.search(r"<title\b[^>]*>(.*?)</title>",page,re.I|re.S)
        next_pages=re.findall(r'href=["\']([^"\']*\?movies&page=[0-9]+)["\']',page,re.I)
        movie_playback_types={
            "m3u8":len(re.findall(r"\.m3u8\b",page,re.I)),
            "mp4":len(re.findall(r"\.mp4\b",page,re.I)),
            "mpd":len(re.findall(r"\.mpd\b",page,re.I)),
            "iframe":len(re.findall(r"<iframe\b",page,re.I)),
            "video":len(re.findall(r"<video\b",page,re.I)),
            "hls_js":len(re.findall(r"hls\.min|hlsjs|new Hls",page,re.I)),
            "login_required_text":len(re.findall(r"debes iniciar sesi[oó]n|inicia sesi[oó]n para|accede con tu cuenta|usuario y contrase",page,re.I)),
        }
        lines=[]
        for label in ("director","elenco","trailer","subtitulado","latino","duración","genero","género","año","sinopsis","Reproducir Video","disponible"):
            m=re.search(re.escape(label),page,re.I)
            if m:
                excerpt=re.sub(r"\s+"," ",re.sub(r"<[^>]+>"," ",page[max(0,m.start()-160):m.start()+250]))
                lines.append({"label":label,"context":excerpt[:260]})
        print("PAGE_ADV",json.dumps({"route":route,"status":res["status"],"title":re.sub("<[^>]+>","",title.group(1)).strip() if title else "", "unique_movies":len(mids),"id_samples":mids[:8],"next_pages":next_pages[:5],"has_next_button":'cargar más' in page.lower(),"playback_features":movie_playback_types,"text_samples":lines[:8]},ensure_ascii=False),flush=True)
    except Exception as e:
        print("PAGE_ADV_ERROR",route,type(e).__name__,str(e)[:140],flush=True)
