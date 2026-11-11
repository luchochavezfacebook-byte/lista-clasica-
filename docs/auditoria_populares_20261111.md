# Auditoría de canales populares HLS — 11 de noviembre de 2026

## Resumen

- Rama de trabajo: `fix/hls-populares-nov2026`; cambios a Lista Clásica, **no a la APK**.
- Inicio: **267** HLS; final: **281** HLS únicos.
- **3 canales retirados**, **17 incorporados**, **TN corregido con cabeceras**.
- Análisis remoto con manifiesto `#EXTM3U` y **2 segundos de video decodificado con FFmpeg** desde GitHub Actions.
- Evidencia: [auditoría de 38 enlaces](https://github.com/luchochavezfacebook-byte/lista-clasica-/actions/runs/42985426481). **19 de 38 pasaron**, pero Real Madrid TV ya formaba parte del catálogo y se evitó duplicarlo.
- Las listas fuente `iptv-org/iptv` de Argentina, España, Brasil y EE. UU. tenían cambios registrados **11/11/2026 UTC**. Algunas rutas contrastadas de `reynaldo1311/listas` provienen de una versión de **14/02/2026**, pero las inclusiones de esa fuente se probaron **11/11/2026**.
- La fecha de última modificación de una lista **no demuestra cuándo se originó cada URL**; 2 s de decodificación no garantiza reproducción continua desde Argentina.

## Canales corregidos/eliminados

| Canal | Resultado técnico | Acción |
|---|---|---|
| DeporTV | Fuente habitual y dos alternativas devolvieron certificado HTTPS no válido para el dominio `streamlock.net` | Retirar temporalmente hasta encontrar HTTPS válido y video reproducible |
| Canal Nets | HTTP 404 | Retirar |
| Canal 9 Litoral | HTTP 404; otros repositorios citaban la misma URL antigua | Retirar |
| TN — Todo Noticias | `TN24` y variante 1080 respondieron 404; la URL existente `TN_DAI_Beta` **sí decodifica** al aportar `User-Agent` y `Referer` del sitio oficial de TN | Mantener URL y agregar cabeceras, pendiente prueba TV física |

## 17 nuevas señales con video

- Argentina: **TyC Sports 24, TyC Sports FAST**.
- Deportes internacionales: **beIN SPORTS XTRA, CBS Sports Golazo, NBC Sports NOW, FTF Sports**.
- Películas: **FilmRise Classic TV, Hallmark Movies & More, CinePride, Whiplash Cinema, Magnificent Movies Network, MyTime Movies**.
- Series: **TV Series Clásicas Brasil**.
- Noticias: **NBC News NOW, SBT News, Record News, Newsmax Spanish**.

**Real Madrid TV** superó el test del 11/11 y ya está presente en la lista anterior, por lo que se conserva sin duplicar.

## Criterios

- No se incluyeron enlaces que respondieran 404/500/503, con certificados inválidos, DNS fallido o sin decodificación.
- No se incorporaron enlaces con usuarios/contraseñas, tokens privados o que requieran elusión de DRM.
- El hecho de que aparezca una señal de pago en un repositorio público **no establece que esté autorizada su redistribución**.
- HLS de canales FAST puede variar su contenido y no garantiza partidos de fútbol premium.
- Los canales agregados no tienen logos nuevos verificados; el sistema puede usar sus índices de logos o mostrarlos sin imagen.
- No se modificaron Proveedor 2, YouTube ni el sistema OTA de V63.

## Reversión

Revertir el commit que actualiza `fuentes.json`, `fuentes_mundotv.json`, `fuentes_noviembre_2026.json`, `scripts/generar_lista.py`, `scripts/validar_repositorio.py` y `lista_clasica.m3u`, regenerar las listas y revalidar.
