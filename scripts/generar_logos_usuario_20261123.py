#!/usr/bin/env python3
"""Generar identificadores PNG para canales nuevos que no tienen logo verificable.

No cambia ningún logo de los 353 canales antiguos. Para los nuevos usa:
- logos externos exactos de ByRafaelSystem/futboltotal-links;
- logos de iptv-org/database;
- PNG local con nombre del canal SOLO donde no se encontró marca.
"""
from pathlib import Path
from urllib.parse import urlsplit
import json
import re
from PIL import Image, ImageDraw, ImageFont

ROOT=Path(__file__).resolve().parents[1]
FILE=ROOT/"fuentes_usuario_argentina_20261123.json"
OUT=ROOT/"logos/usuario_20261123"
URL_BASE="https://raw.githubusercontent.com/luchochavezfacebook-byte/lista-clasica-/main/logos/usuario_20261123/"

def font(size):
    for p in [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
        "/usr/share/fonts/truetype/liberation2/LiberationSans-Bold.ttf",
    ]:
        try: return ImageFont.truetype(p,size)
        except OSError: pass
    return ImageFont.load_default()

def wrap_words(text,max_width,draw,f):
    lines=[]
    current=""
    for word in text.split():
        maybe=(current+" "+word).strip()
        box=draw.textbbox((0,0),maybe,font=f)
        if current and box[2]-box[0]>max_width:
            lines.append(current)
            current=word
        else:current=maybe
    if current:lines.append(current)
    return lines

def render(name,path):
    canvas=Image.new("RGBA",(512,288),(7,11,20,255))
    pen=ImageDraw.Draw(canvas)
    pen.rounded_rectangle((15,15,497,273),radius=26,outline=(46,155,255,255),width=5)
    pen.rounded_rectangle((208,28,304,87),radius=13,outline=(46,155,255,255),width=6)
    pen.line((242,94,270,94),fill=(46,155,255,255),width=5)
    pen.text((256,121),"CANAL",font=font(22),fill=(148,171,201,255),anchor="mm")
    f=font(36)
    lines=wrap_words(name,422,pen,f)
    if len(lines)>3:
        f=font(29)
        lines=wrap_words(name,438,pen,f)
    lines=lines[:3]
    spacing=40 if len(lines)<3 else 33
    top=190-(len(lines)-1)*spacing/2
    for i,line in enumerate(lines):
        if len(line)>29: line=line[:27]+"…"
        pen.text((256,int(top+i*spacing)),line,font=f,fill=(245,248,253,255),anchor="mm")
    pen.text((256,258),"TV FULL PRO",font=font(13),fill=(148,171,201,255),anchor="mm")
    canvas.save(path,format="PNG",optimize=True)

def main():
    data=json.loads(FILE.read_text(encoding="utf-8"))
    channels=data["canales"]
    assert channels and len(channels)<300
    OUT.mkdir(parents=True,exist_ok=True)
    count=0
    pathset=set()
    for c in channels:
        assert c["logo"].startswith("https://"),"No logo: "+c["nombre"]
        if c.get("logo_origen")!="identificador_generado":
            continue
        link=c["logo"]
        assert link.startswith(URL_BASE),"Logo de respaldo fuera de ruta"
        name=urlsplit(link).path.rsplit("/",1)[-1]
        assert re.fullmatch(r"[a-z0-9-]+\.png",name)
        assert name not in pathset,"Colisión de nombre"
        pathset.add(name)
        render(c["nombre"],OUT/name)
        count+=1
    print("Logos PNG con nombre generados:",count)
    print("Logos externos elegidos:",len(channels)-count)
    assert all((OUT/x).stat().st_size>900 for x in pathset)
if __name__=="__main__":
    main()
