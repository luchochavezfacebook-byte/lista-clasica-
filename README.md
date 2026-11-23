# Lista Clásica — TV FULL PRO (V63)

## Ampliación gratuita similar a PlayTV — 23/11/2026 (última actualización)

**Lista Clásica: 346 señales HLS únicas**. Tras depurar a 340, incorporamos **7 señales de acceso público** comprobadas dos veces con FFmpeg: Telemundo Puerto Rico, ViX Deportes 24/7 (Zona TUDN), Fubo Sports Network, Telemundo Noticias Ahora, Telemundo Acción, GLORY Kickboxing y Telemundo Deportes Ahora (con un respaldo igualmente probado). Quitamos de la lista **TyC Sports FAST**, que no entregó imagen en dos pruebas; TyC Sports 24 permanece activo.

No se copió ningún enlace de `cabj91/tvplay/la14hd.m3u` porque sus 108 enlaces tenían tokens caducados. No se agregaron fuentes de canales deportivos premium sin autorización. Informe y pruebas: [PlayTV / FAST noviembre 2026](docs/playtv_free_20261123.md). Las nuevas fuentes se detallan en `fuentes_fast_playtv_20261123.json`, pueden tener geobloqueo en Argentina y están sujetas a los derechos de cada emisora.

## Depuración de señales sin video — 23/11/2026 (última actualización)

**Lista Clásica publicada: 340 fuentes HLS únicas** (frente a 370 antes de la depuración). Se eliminaron de los catálogos activos **31 entradas, correspondientes a 30 URLs únicas**: el canal TV Universidad aparecía duplicado con dos IDs. Se conservaron los registros antiguos, con sus URLs y motivos, en [diagnosticos/bajas_20261123.json](diagnosticos/bajas_20261123.json), para permitir recuperarlos si vuelven a transmitir.

Se cambiaron **3 señales fallidas por fuentes diferentes probadas con video real**: Salsa Gorda Television, 4FUN TV Polonia PL y TV Perú. Los enlaces antiguos de esas tres señales se archivaron en [diagnosticos/reemplazos_20261123.json](diagnosticos/reemplazos_20261123.json), pero ya no están en el M3U. La URL original de Canal 4 Jujuy se conserva porque **sí reprodujo video en ambas pruebas FFmpeg**, aunque los chequeos de manifest muchas veces fallen por una variante HLS. También se conservaron seis señales Dance TV Estonia y una variante funcional de Canal Sur Andalucía. No se eliminaron las fuentes que aprobaron la prueba de reproducción.

**Pruebas:** dos pasadas con FFmpeg, al menos 25 fotogramas por señal: [QA de video y alternativas](https://github.com/luchochavezfacebook-byte/lista-clasica-/actions/runs/45220497264). [Validación estructural y reconstrucción del M3U depurado](https://github.com/luchochavezfacebook-byte/lista-clasica-/actions/runs/45221271216). Ningún cambio en `lista_clasica_youtube.m3u` ni en la APK. El funcionamiento desde Argentina puede diferir del runner; las bajas son técnicas y no afirman que el canal dejara de emitir definitivamente.

## Auditoría completa y nuevas fuentes regionales — 23/11/2026

**Se corrigió un fallo de cobertura del auditor**: la revisión programada cada 6 horas examinaba solo el pequeño archivo `fuentes.json` y no los demás catálogos. El nuevo `scripts/auditar_lista_completa.py` lee todas las fuentes, prueba un segmento HLS, repite los fallos y comprueba respaldos, sin dar de baja ningún canal por un 403, 404, timeout o corte temporal.

**Resultado corregido sobre las 364 fuentes previas:** **327 accesibles y 37 pendientes de revisión** desde GitHub Actions; Argentina **116 accesibles y 13 pendientes**. La primera pasada daba 316/48, pero al admitir manifiestos hasta 1 MiB y masters anidados se recuperaron 11 falsos positivos. Detalle en [auditoría completa y diagnóstico](docs/auditoria_completa_20261123.md).

También se integran **6 señales HLS regionales nuevas** (Canal 79 Mar del Plata, Canal 10 Chiapas, Canal 10 Durango, IERTBCS Canal 8 La Paz, Onda Cádiz 24h y Canal 8 Visión TV Paraguay), tras dos pruebas FFmpeg con 30 fotogramas por pasada. Total actualizado: **370 fuentes HLS**, sin eliminar ni reemplazar las 364 anteriores. TV Perú y `24h` de España suman un **respaldo probado** cada uno, conservando la fuente principal.

**Importante:** estos resultados reflejan pruebas de conexión desde GitHub, no certifican reproducción continua, audio, derechos de retransmisión ni funcionamiento desde Argentina. Los 37 canales problemáticos no se consideran definitivamente caídos y no se eliminan automáticamente. Lista Clásica YT queda intacta.

**TV FULL PRO:** Lista Clásica → Recargar lista, sin recompilar.

## Señales en español de TVPlay — 23/11/2026

Se revisó la lista pública [Appdeveloper365/TvPlay](https://github.com/Appdeveloper365/TvPlay/blob/main/TVPlay.m3u), con **243 entradas de diferentes idiomas**. Se seleccionaron **16 candidatos públicos hispanohablantes**; **12 aprobaron dos pasadas independientes** con FFmpeg (30 fotogramas por pasada). Cuatro fallaron y quedan pendientes: beIN SPORTS XTRA en Español (404), Awapa Sports TV (400), Radio Turrialba TV Sports (error de entrada/salida), Multivision Sports (error 5xx). No se considera que estén permanentemente caídos.

Se integraron **12 nuevas fuentes HLS HTTPS**, sin reemplazar ninguna de las 352 URL anteriores, para un total de **364 señales** en Lista Clásica. Las fuentes nuevas se guardan en `fuentes_tvplay_es_2026.json`, y los resultados de validación están documentados en [auditoría TVPlay ES](docs/tvplay_es_20261123.md). Se conservaron las demás fuentes, respaldos y Lista Clásica YT.

**Limitaciones:** estas pruebas son desde el runner de GitHub y no garantizan audio, continuidad, funcionamiento en Argentina ni disponibilidad en Android TV. La ausencia de protección técnica no equivale a permiso de retransmisión; usar conforme a los derechos de cada canal. En TV FULL PRO: **Lista Clásica → Recargar lista**, sin recompilar.

## Nuevas señales autorizadas de Netvideo — 22/11/2026

Se incorporaron **28 señales HLS nuevas**, con **28 logos** procedentes de la grilla web de Netvideo TvPlay, facilitada por el proveedor para esta integración. Se compararon los **70 elementos** de TvPlay (**62 HLS** y 8 flujos de otro tipo) con Lista Clásica y se descartaron duplicados, incluyendo TN, El Trece, América, Canal 7 Jujuy/Salta, Radio Power Max y LinkTV. Se descartaron también 6 candidatos con pruebas insuficientes, sin declararlos dados de baja.

La lista principal pasa de **324 a 352 señales HLS únicas**. Se conservaron intactas las 324 URL originales, respaldos y Lista Clásica YT. Las 28 señales seleccionadas superaron dos pruebas de fragmentos HLS y decodificación de al menos 20 fotogramas en GitHub Actions. **Su reproducción continua y el audio deben probarse en TV FULL PRO desde Argentina.**

**Nota técnica:** estas señales utilizan HTTP (no HTTPS) en el puerto 5056 de la dirección entregada por el proveedor. El generador solo permite HTTP para ese servidor y para el formato HLS específico de su sitio. Las rutas completas quedan visibles en este repositorio público; confirmar con el proveedor que está autorizada su publicación y distribución. El sitio puede modificar su ruta o controlar acceso por región.

[Detalle técnico y lista de incorporaciones](docs/netvideo_tvplay_20261122.md). En TV FULL PRO: **Lista Clásica → Recargar lista**. No requiere recompilar.

## Ampliación de señales regionales — 21/11/2026 (dos pruebas)

Se incorporaron **24 canales HLS argentinos nuevos**, luego de verificar manifiesto, primer segmento y decodificación de al menos 20 fotogramas durante 2 segundos de video en **dos ejecuciones independientes** de GitHub Actions. La lista pasa de **300 a 324 señales HLS únicas**. Se conservaron todas las 300 fuentes anteriores, con sus cabeceras y respaldos. Canal 4 Villa Dolores y otros candidatos con pruebas insuficientes **no se incorporaron**. Esto no garantiza reproducción desde una TV Box o disponibilidad permanente.

Auditorías: [primera muestra](https://github.com/luchochavezfacebook-byte/lista-clasica-/actions/runs/44911529535/attempts/1) y [segunda muestra](https://github.com/luchochavezfacebook-byte/lista-clasica-/actions/runs/44911529535/attempts/2). [Listado técnico de incorporaciones](docs/altas_hls_20261121.md).

## Revisión de señales reportadas — 21/11/2026

Se actualizaron las fuentes principales de **Aire de Santa Fe, Canal 22 y VerTV**, con video y audio decodificados y una segunda muestra correcta. Las direcciones anteriores permanecen como respaldos. **No se eliminó ningún canal**: Canal 4 Jujuy tiene emisión HD con fallos en otras calidades; TV Maná y TV Universidad quedan pendientes de recuperación/acceso. Un error temporal no implica baja definitiva. La lista conserva **300 entradas HLS**.

Detalle de pruebas y criterios: [revisión de seis señales](docs/revision_senales_20261121.md). En la app: **Lista Clásica → Recargar lista → Argentina TV**. No requiere APK nueva.

## Señales argentinas para prueba — 21/11/2026

Se agregaron **19 canales en Argentina TV**, incluyendo **Metropolitana TV / Canal 12 Tucumán**, y un **respaldo HTTPS de El Ocho / Telefe Tucumán**. La lista tiene **300 enlaces HLS únicos**. Los canales nuevos tienen manifiesto, segmentos y una muestra de 2 segundos de video decodificados; requieren prueba de continuidad en TV Box. El Ocho conserva su fuente principal y añade el respaldo oficial g3 con sus cabeceras.

En la app: abrir **Lista Clásica → Recargar lista → Argentina TV**. No requiere recompilar ni instalar APK. Los cambios están en `fuentes_noviembre_2026.json` y `fuentes.json`; `lista_clasica.m3u` se regenera desde esos catálogos. Detalle de canales y evidencia: [incorporación Argentina 21/11](docs/argentina_pruebas_20261121.md).

## Actualización de salud y canales populares — 11/11/2026

La Lista Clásica ahora tiene **281 enlaces HLS únicos**. Se **eliminaron** DeporTV (HTTPS certificado inválido en tres intentos), Canal Nets (404) y Canal 9 Litoral (404). Las alternativas abiertas localizadas para esos canales fallaron, así que no se sustituyeron por señales incorrectas.

**TN / Todo Noticias** se mantiene con su URL actual `TN_DAI_Beta` y cabeceras `User-Agent` y `Referer` de `https://tn.com.ar/envivo/24hs`. Estas cabeceras consiguieron decodificar video desde GitHub Actions el 11/11. La alternativa `TN24` respondió 404.

Se incorporaron **17 señales nuevas** con manifiesto HLS y dos segundos de video decodificados el 11/11: TyC Sports 24, TyC Sports FAST, beIN SPORTS XTRA, CBS Sports Golazo, NBC Sports NOW, FTF Sports, FilmRise Classic TV, Hallmark Movies & More, CinePride, Whiplash Cinema, Magnificent Movies Network, MyTime Movies, TV Series Clásicas Brasil, NBC News NOW, SBT News, Record News y Newsmax Spanish. Real Madrid TV también pasó la prueba, pero **ya estaba en el catálogo** y se evitó duplicarlo.

Prueba del runner: [GitHub Actions #42985426481](https://github.com/luchochavezfacebook-byte/lista-clasica-/actions/runs/42985426481). Algunas fuentes pueden no estar disponibles desde todas las regiones o dispositivos; la prueba no concede derechos de redistribución.

Fuente adicional: `fuentes_noviembre_2026.json`; se genera junto con los demás catálogos. Informe: [auditoría de señales populares](docs/auditoria_populares_20261111.md).

## Nuevas señales verificadas — 11/11/2026

Se incorporaron **16 señales HLS** tras obtener manifiesto HTTP 200 y decodificar video con FFmpeg en GitHub Actions; **251 fuentes preexistentes preservadas**. El catálogo de origen `iptv-org/iptv` se actualizó el 7 y el 11 de noviembre de 2026. Estos datos acreditan una comprobación reciente, **no la fecha en que se creó cada URL** ni su funcionamiento garantizado desde una TV Box argentina. Informe técnico: [auditoría 2026](docs/auditoria_hls_noviembre_2026.md). Fuentes reproducibles: `fuentes_populares_2026.json`. No se incluyen los candidatos que fallaron.

## Estado de recuperación — 10/11/2026

Se retiraron **27 enlaces de YouTube** que se habían agregado por error a la lista M3U principal. Se detectó que V62 los entregaba a Media3 como si fueran URLs HLS, lo cual produce **Formato de señal no compatible**. No son HLS y una categoría como «Argentina YT» no puede cambiar su formato.

**Lista principal:** [lista_clasica.m3u](lista_clasica.m3u) — **281 enlaces HLS únicos**, por país, con Argentina primero. Conserva los **251 URL HLS originales, User-Agent, Referer y respaldos** previos al error. Se añadieron **9 logos** ya presentes en el índice de la APK, con lo que la lista principal ahora declara **247 logos**. No se alteraron URLs, proveedores ni claves.

**Lista Clásica YT:** [lista_clasica_youtube.m3u](lista_clasica_youtube.m3u) — **25 canales de YouTube en vivo**, todos con logo, en 5 categorías: Noticias Argentina, TV Regional Argentina, Deportes, Streaming, radio y música, e Internacionales. Es una lista **separada**, para el reproductor YouTube embebido (WebView) de **TV FULL PRO V63 o superior**. Se genera desde `youtube_en_vivo.json` con `scripts/generar_lista_youtube.py`: **no editar el .m3u a mano** (el chequeo automático falla). Los canales usan `youtube.com/channel/UC…/live` (directo actual, no vence) o, si no hay ID de canal, el video de un directo 24 h. **No son HLS:** no se cargan en Media3 ni en `lista_clasica.m3u`, y la V62 no la consulta. Los canales sin ID ni video verificado quedan como pendientes en `youtube_en_vivo.json`.

### Fuente RAW usada por la APK

https://raw.githubusercontent.com/luchochavezfacebook-byte/lista-clasica-/main/lista_clasica.m3u

## Agrupación

Los HLS están organizados por país mediante `group-title="<País> TV"`: Argentina TV primero; luego países por orden alfabético; Internacional TV para procedencia multinacional o incierta. **No se quitó ningún HLS al recuperar la lista.**

## Logos

La lista original tenía **238 logos** en 251 señales HLS. Se copiaron **9 URL públicas de logos del propio índice de TV FULL PRO** a los canales HLS originales que carecían de `tvg-logo`, alcanzando **247 logos declarados**. En el conjunto original se mantienen **4 canales sin logo explícito** (Canal E, TV Universidad, Canal y Cine Acción). Las 16 señales agregadas aún no tienen un logo confirmado, para evitar imágenes incorrectas. Estos cambios son solo metadatos visuales, no alteran reproducción. La disponibilidad de cada imagen externa no se ha probado en todos los dispositivos.

## Canal 8 y Canal 10 Tucumán

- **Canal 8 / Telefe Tucumán** se conserva como señal HLS, incluida la cabecera de compatibilidad previamente configurada. Su reproducción debe verificarse desde una red argentina; GitHub Actions solo certificó manifiesto y un segmento, no imagen/sonido.
- **Canal 10 Tucumán** solo tiene una referencia estable a YouTube en el catálogo; no se ha identificado un HLS directo estable, público y verificado para la APK. La URL firmada `manifest.googlevideo.com` vence y puede depender de IP/sesión, por eso **no se publica**. Canal 10 permanece en la lista YouTube independiente hasta que se encuentre una fuente HLS legítima o se incorpore un reproductor de YouTube en la APK.

## Crónica TV — fuente HLS descartada por decodificación fallida (10/11/2026)

Se retiró de la lista principal el HLS comunitario g5 de Crónica TV tras el reporte de falla en TV FULL PRO y el diagnóstico independiente [GitHub Actions #42900191922](https://github.com/luchochavezfacebook-byte/lista-clasica-/actions/runs/42900191922). Aunque el manifiesto y 2048 bytes de un segmento respondían, FFmpeg registró errores de H.264 `decode_slice_header` y no consiguió completar 3 segundos de decodificación en los servidores g5 ni g3 (tiempo de espera). La ruta g1 consultada respondió HTTP 404. Como control, Canal 8 Tucumán decodificó correctamente 3 segundos.

**No atribuir el error solo al reproductor:** el servidor HLS no superó la prueba técnica. Ninguna de esas fuentes se incorpora como HLS válido sin reproducción verificada. La referencia oficial de Crónica en YouTube sigue catalogada por separado en `lista_clasica_youtube.m3u`; TV FULL PRO V62 no reproduce sus enlaces `/live` directamente.

## Mantenimiento

- `fuentes.json`: 11 fuentes HLS originales
- `fuentes_mundotv.json`: 245 fuentes HLS importadas, clasificadas por país
- `fuentes_populares_2026.json`: 16 señales HLS incorporadas el 11/11/2026
- `fuentes_noviembre_2026.json`: 17 señales HLS de deportes, cine, series y noticias comprobadas el 11/11/2026
- `youtube_en_vivo.json`: canales YouTube (25 publicados, el resto pendientes); **fuente única** de la Lista Clásica YT
- `scripts/identificar_youtube.py`: identifica videos con oEmbed de YouTube (solo lectura)
- `scripts/generar_lista.py`: genera **solo HLS**
- `scripts/generar_lista_youtube.py`: genera la Lista Clásica YT, solo con canales que tienen `channel_id` verificado
- `scripts/validar_repositorio.py`: comprueba estructura, URLs, logos y ausencia de enlaces YouTube en la lista principal
- `scripts/verificar_canales.py` y `.github/workflows/auditar-hls.yml`: chequean conectividad HLS original; **no garantizan reproducción** en un TV Box

### Comprobación automática

```bash
python3 scripts/validar_repositorio.py
python3 scripts/generar_lista.py
python3 scripts/generar_lista_youtube.py
git diff --exit-code -- lista_clasica.m3u lista_clasica_youtube.m3u
```

**Esta actualización de Lista Clásica no modifica la APK V63 ni Proveedor 2.**
