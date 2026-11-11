# Auditoría HLS de canales populares — 11/11/2026

## Procedencia y actualidad

- Repositorio fuente: [iptv-org/iptv](https://github.com/iptv-org/iptv), archivos `streams/ar.m3u`, `streams/cl.m3u` y `streams/py.m3u`.
- Último cambio observado en los archivos de Argentina y Chile: **2026-11-11 UTC**; Paraguay: **2026-11-07 UTC**. Estas fechas son de los archivos M3U, **no** de creación de cada enlace.
- Validación realizada desde GitHub Actions el **2026-11-11**, con URLs HTTPS, respuesta HTTP 200, manifiesto `#EXTM3U` y un segundo de video decodificado con FFmpeg.
- Ejecución: https://github.com/luchochavezfacebook-byte/lista-clasica-/actions/runs/42982858033
- La prueba de runner **no garantiza** acceso regional, continuidad 24/7, logo ni reproducción desde todas las TV Box. La fuente puede cambiar en el futuro.

## Resultado

- **29** candidatos evaluados.
- **17** pasaron manifiesto y decodificación.
- **1** ya existía con la misma URL (Xtrema Acción).
- **16** canales nuevos incorporados; **251** enlaces existentes preservados; **267** totales.

| País | Incorporaciones |
| --- | --- |
| Argentina (10) | Canal 3 Formosa, Chamamé TV, Folcloreando TV, Cumbia Mix, La 100, Xtrema Cine Clásico, Xtrema Terror, Xtrema Cartoons, Caras TV, Multivisión Federal |
| Chile (5) | 13 Kids, 13 Humor, 13 Festival, 13 Teleseries, Bio Bío TV |
| Paraguay (1) | Paraguay TV |

Se excluyeron por fallo de comprobación Cine.AR, Pakapaka, Encuentro, Tec TV, Aunar, La Voz de Tucumán, Canal 10 Córdoba, MusicTop, Chacra TV, 13 Prime, C9N Paraguay y Farra Play. Para algunas fuentes el servidor respondió 200, pero no fue posible decodificar video.

## Observaciones técnicas

- Algunos canales de Chile tardaron más de diez segundos en iniciar decodificación desde el runner, especialmente 13 Kids y 13 Festival. En TV Box pueden iniciar más lentamente.
- La lista principal contiene solo HLS; no incluye enlaces de YouTube, parámetros típicos de sesión ni claves DRM.
- `fuentes_populares_2026.json` es la fuente regenerable de las 16 incorporaciones. No editar únicamente `lista_clasica.m3u`: ejecutar `python3 scripts/generar_lista.py`.
- El cambio **no modifica** la APK, la lista de YouTube, ni Proveedor 2.
