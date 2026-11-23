# Auditoría integral de Lista Clásica y nuevas señales — 23 de noviembre de 2026

## Diagnóstico de 364 canales antes de la ampliación

La auditoría anterior, programada cada seis horas, solo cubría `fuentes.json` (10 canales base) y `diagnosticos/candidatos.json`. De ese modo ignoraba muchos canales ya presentes en la M3U.

El nuevo `scripts/auditar_lista_completa.py` lee y deduplica todos los catálogos, prueba HLS/segmento con su User-Agent/Referer, repite una vez las fuentes fallidas y comprueba respaldos declarados. No cambia canales automáticamente. El verificador admite hasta 1 MiB de manifiesto y hasta cuatro niveles de masters HLS para reducir falsos positivos.

- Primera inspección con el límite antiguo: **316 accesibles / 48 pendientes** (364 únicas). [Logs](https://github.com/luchochavezfacebook-byte/lista-clasica-/actions/runs/45217431134).
- Segunda inspección tras corregir el límite: **327 accesibles / 37 pendientes**. **11 falsos positivos resueltos.** [Logs y reporte JSON como artefacto](https://github.com/luchochavezfacebook-byte/lista-clasica-/actions/runs/45217837312).
- Argentina: **116 de 129 accesibles**, 13 pendientes; otras geografías: 211 de 235 accesibles, 24 pendientes.

### Trece fuentes argentinas que requieren revisar la señal o ubicación de la prueba

| Canal | Resultado GitHub Actions |
| --- | --- |
| TV Universidad (UNLP) | HTTP 403 |
| Canal 4 Jujuy | HTTP 404 en variante elegida; otra calidad funcionó anteriormente |
| Canal 7 Jujuy | HTTP 404 |
| Canal 7 Neuquén | HTTP 403 |
| Canal 21 TV | HTTP 404 |
| TeleCinco Trelew | HTTP 404 |
| TV Solidaria | Error de red |
| Radio Sublime Gracia TV | Error de red |
| TV Maná Argentina | HTTP 404 en variante seleccionada |
| Canal 12 Venado Tuerto | Sin segmentos accesibles en playlist |
| Canal 2 de Ushuaia | Sin segmentos accesibles en playlist |
| Canal 10 Mar del Plata | HTTP 404 |
| Neo TV | HTTP 404 |

Los 24 pendientes de otros países se encuentran en el reporte JSON del artefacto: RTV ESPAÑA, Salsa Gorda Television, Cadena Elite España, Verbena TV España, 4FUN TV Polonia, Dance TV Estonia (dos fuentes), Retro Plus TV Chile, Canal Sur Andalucía, 7TV Granada, Canal 6 Multimedios México, TV Perú, TV Perú Noticias, Canal IPe Perú, Oromar TV Ecuador, Avivamiento TV, Solidaria TV España, TBN España, CGTN China, Republic World TV India, ServusTV WetterPanorama, 24h España, Ultra Casanare TV, Ondambiental TV Colombia.

**No se debe interpretar ninguna de estas respuestas como fin permanente de emisión**: 403/404 pueden ser causados por CDN, geobloqueo, segmentos o variantes de HLS, y el runner está fuera de Argentina.

## Búsqueda de reemplazos y nuevos canales

Se inspeccionaron canales hispanohablantes gratuitos de `iptv-org/iptv` (`streams/ar.m3u`, `mx.m3u`, `es.m3u`, `py.m3u`, `cr.m3u`, `pe.m3u`). Se probaron 12 candidatos con FFmpeg en dos tandas y 30 fotogramas por canal y tanda. [Auditoría de nuevas señales](https://github.com/luchochavezfacebook-byte/lista-clasica-/actions/runs/45218231882).

**6 nuevas fuentes aceptadas** (no incluidas entre las 364 anteriores):

| País | Nombre | URL de origen |
| --- | --- | --- |
| Argentina | Canal 79 Mar del Plata | `streams/ar.m3u` |
| México | Canal 10 Chiapas | `streams/mx.m3u` |
| México | Canal 10 Durango | `streams/mx.m3u` |
| México | IERTBCS Canal 8 La Paz | `streams/mx.m3u` |
| España | Onda Cádiz 24h | `streams/es.m3u` |
| Paraguay | Canal 8 Visión TV | `streams/py.m3u` |

**2 respaldos aprobados** y añadidos sin cambiar la fuente principal: TV Perú (`https://cdnhd3.iblups.net/hls/2ee85c7a0aff45d4b0f05552d81cadb07.m3u8`) y 24h de España (`https://n-5-2.eu.cdn-redge.media/livehls/oeu/mt/live/24h/live.livx/playlist.m3u8`). Ambos decodificaron 30 fotogramas por tanda. Si la principal funciona desde Argentina, sigue siendo prioritaria; el respaldo queda disponible para recuperación.

**4 candidatos no aprobados:** Canal 10 Córdoba (404), Canal 13 Jujuy TV (403), Canal 8 San Juan (error de E/S), Radio Turrialba TV Sports alternativo (403). No se añadieron.

**Resultado de la ampliación: 370 señales HLS.** Las 364 URL originales y sus respaldos se preservan. No se altera la lista de YouTube, la app Android ni otros proveedores.

### Alcance y límites

Que un manifiesto y fragmento sean accesibles no implica audio, imagen continua, compatibilidad con un TV Box concreto ni disponibilidad regional. Las 6 nuevas tienen **video efectivamente decodificado** en la nube, pero debe probarse su funcionamiento desde Argentina. Se seleccionaron señales abiertas y se excluyeron enlaces con tokens temporales, credenciales, DRM y reemisiones no acreditadas de canales deportivos de pago. La accesibilidad técnica no concede por sí sola derechos de retransmisión.
