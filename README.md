# Lista Clásica — TV FULL PRO (V63)

## Nuevas señales verificadas — 11/11/2026

Se incorporaron **16 señales HLS** tras obtener manifiesto HTTP 200 y decodificar video con FFmpeg en GitHub Actions; **251 fuentes preexistentes preservadas**. El catálogo de origen `iptv-org/iptv` se actualizó el 7 y el 11 de noviembre de 2026. Estos datos acreditan una comprobación reciente, **no la fecha en que se creó cada URL** ni su funcionamiento garantizado desde una TV Box argentina. Informe técnico: [auditoría 2026](docs/auditoria_hls_noviembre_2026.md). Fuentes reproducibles: `fuentes_populares_2026.json`. No se incluyen los candidatos que fallaron.

## Estado de recuperación — 10/11/2026

Se retiraron **27 enlaces de YouTube** que se habían agregado por error a la lista M3U principal. Se detectó que V62 los entregaba a Media3 como si fueran URLs HLS, lo cual produce **Formato de señal no compatible**. No son HLS y una categoría como «Argentina YT» no puede cambiar su formato.

**Lista principal:** [lista_clasica.m3u](lista_clasica.m3u) — **267 enlaces HLS únicos**, por país, con Argentina primero. Conserva los **251 URL HLS originales, User-Agent, Referer y respaldos** previos al error. Se añadieron **9 logos** ya presentes en el índice de la APK, con lo que la lista principal ahora declara **247 logos**. No se alteraron URLs, proveedores ni claves.

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
- `fuentes_populares_2026.json`: 16 señales HLS nuevas verificadas el 11/11/2026; este archivo sí se incluye al regenerar la lista
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
