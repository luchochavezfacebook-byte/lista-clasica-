#!/usr/bin/env python3
"""Diagnóstico de lectura de HTTP público. Sin autenticación ni enumeración."""
import http.client, json, re, socket, ssl, time, urllib.request, urllib.error
from urllib.parse import urlsplit
url="http://200.80.230.125:5056/"
results=[]
for scheme in ("http","https"):
    address=scheme+"://200.80.230.125:5056/"
    record={"url":address}
    try:
        req=urllib.request.Request(address,headers={"User-Agent":"Mozilla/5.0 (compatible; SiteConnectivityCheck/1.0)","Accept":"text/html,application/json,text/plain,*/*"})
        with urllib.request.urlopen(req,timeout=12) as r:
            body=r.read(100000)
            content_type=r.headers.get("Content-Type","")
            snippet=body.decode("utf-8","replace")
            title_match=re.search(r"<title[^>]*>(.*?)</title>",snippet,re.I|re.S)
            record.update(status=r.status,redirected_to=r.url,content_type=content_type,server=r.headers.get("Server",""),content_bytes_sampled=len(body),title=(re.sub(r"\\s+"," ",title_match.group(1))[:200] if title_match else None))
            record["page_shape"]={
                "html":bool(re.search(r"<html|<!doctype",snippet,re.I)),
                "m3u":snippet.strip().startswith("#EXTM3U"),
                "json":snippet.lstrip().startswith(("{","[")),
                "hls_links":list(dict.fromkeys(re.findall(r"https?://[^'\\\"\\s<>]+?\\.m3u8(?:\\?[^'\\\"\\s<>]*)?",snippet,re.I)))[:30],
                "path_refs":list(dict.fromkeys(re.findall(r"(?:src|href)=['\\\"]([^'\\\"]+)['\\\"]",snippet,re.I)))[:25],
                "visible_text_excerpt":re.sub(r"\\s+"," ",re.sub(r"<[^>]+>"," ",snippet))[:400]
            }
    except Exception as e:record.update(error=type(e).__name__+": "+str(e)[:250])
    results.append(record)
    print("RESULT",json.dumps(record,ensure_ascii=False),flush=True)
try:
    with socket.create_connection(("200.80.230.125",5056),timeout=12) as s: 
        print("TCP_CONNECTION","connected",flush=True)
except Exception as e:
    print("TCP_CONNECTION",type(e).__name__,str(e)[:180],flush=True)
