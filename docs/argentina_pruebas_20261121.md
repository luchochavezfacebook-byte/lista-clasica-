# Incorporación de señales argentinas para prueba — 21/11/2026

19 canales agregados en Argentina TV. Total: 300 URL HLS principales únicas. Se mantienen los 281 enlaces principales anteriores. Se añade también un respaldo HTTPS oficial de El Ocho, sin crear otra entrada duplicada.

Prueba local realizada el 21/11/2026: manifiesto, variante HLS, dos segmentos recientes, FFprobe y dos segundos de video decodificado con FFmpeg; capturas revisadas. No certifica continuidad ni disponibilidad desde Argentina. La tabla muestra la variante probada, no la resolución máxima.

| Canal | ID | URL |
|---|---|---|
| ABTV Bariloche | ABTVBariloche.ar | https://videostream.shockmedia.com.ar/hls/abtvbariloche/abtvbariloche.m3u8 |
| Canal 2 Misiones / Telefe | Canal2Misiones.ar | https://nd106.republicaservers.com:4433/hls/canal2misioness/index.m3u8 |
| Canal Universidad Mar del Plata | CanalUniversidad.ar | https://videostream.shockmedia.com.ar/hls/canaluniversidadmdp/canaluniversidadmdp.m3u8 |
| Catamarca TV | CatamarcaTV.ar | https://stream.arcast.com.ar/canal7catamarca/ngrp:canal7catamarca_all/playlist.m3u8?DVR= |
| Litus TV | LitusTV.ar | https://edge.enhdtv.com/litustv/index.m3u8 |
| NG Federal | NGFederal.ar | https://617c5175c970b.streamlock.net:4444/tvlink/live/playlist.m3u8 |
| TV Publica Fueguina | TVPublicaFueguina.ar | https://nd106.republicaservers.com/hls/c8094/index.m3u8 |
| TV Publica Marcos Paz | TVPublicaMarcosPaz.ar | https://ca.centaurychile.com:2443/hls/mediospublicos.m3u8 |
| Canal 2 Gualeguay | Canal2Gualeguay.ar | https://stream.arcast.net:4443/gualeguay/gualeguay/playlist.m3u8 |
| Canal 2 NexTV Rafaela | Canal2NexTVRafaela.ar | https://edge.enhdtv.com/nexthd/index.m3u8 |
| Canal 3 Arroyito | Canal3Arroyito.ar | https://envivo.cespalarroyito.coop/live/Canal3Arroyito.m3u8 |
| Canal 9 Link Resistencia | Canal9Link.ar | https://617c5175c970b.streamlock.net:4444/9linklivert/smil:9linkmultibr.smil/playlist.m3u8 |
| Canal 10 Goya | Canal10Goya.ar | https://tv.streamcasthd.com:3637/live/canal10goyalive.m3u8 |
| Canal 12 Venado Tuerto | Canal12VenadoTuerto.ar | https://nd106.republicaservers.com:4433/hls/diegologonitv/index.m3u8 |
| Ciudad TV Resistencia | CiudadTVResistencia.ar | https://617c5175c970b.streamlock.net:4444/chacodxdtv/livenew/playlist.m3u8 |
| Correa Radiovision | CorreaRadiovision.ar | https://stream.arcast.net:4443/correadigital/canal12/playlist.m3u8 |
| Corrientes TV | CorrientesTV.ar | https://617c5175c970b.streamlock.net:4444/13max2/live13maxtv2026/playlist.m3u8 |
| Itel TV Canal 2 | ItelTVCanal2.ar | https://proxystream.iteltv.com.ar/output/iteltv/playlist.m3u8 |
| Metropolitana TV - Canal 12 Tucumán | MetroTV.ar | https://streamtv12.ddns.net:5443/LiveApp/streams/193945633734205616732920.m3u8 |

## El Ocho / Telefe Tucumán

Principal preservada: `https://g2.mc-hor.transport.edge-access.net/a05/ngrp:elochotv-100168_all/Playlist.m3u8?sense=true`.

Respaldo probado: `https://g3.proy-slo.transport.edge-access.net/a05/ngrp:elochotv-100168_all/Playlist.m3u8?sense=true`. Cabeceras: `User-Agent: Mozilla/5.0`, `Referer: https://vmf.edge-apps.net/`. Fuente: https://www.elocho.tv/el-ocho-en-vivo.html y su reproductor público en vmf.edge-apps.net.

## Alcance

Solo señales argentinas HLS HTTPS verificadas. Norte TV/Canal 7 usa DASH y queda fuera del catálogo HLS actual. Canal 13 La Rioja solo se verificó por HTTP y queda pendiente. La Voz de Tucumán, Panc TV, Canal 5 Interior y El Palomar no pasaron las pruebas.

Origen: https://github.com/iptv-org/iptv/blob/master/streams/ar.m3u ; https://github.com/IamJony/IPTVListaLibre/blob/main/generated/ar_canales.m3u ; Metropolitana TV confirmada en https://cadenametro.com.ar/ .

No requiere cambios de APK. Para probar: Lista Clásica → Recargar lista → Argentina TV.
