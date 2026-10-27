# Canales — Lista Clásica

Repositorio **independiente de TV FULL PRO** con una lista de señales gratuitas argentinas y una lista complementaria de transmisiones en YouTube.

## Listas

- [Lista Clásica HLS](lista_clasica.m3u): 11 fuentes HLS candidatas. **No todas están verificadas ni garantizadas**.
- [YouTube LIVE](lista_clasica_youtube.m3u): 26 referencias a canales oficiales de YouTube. **No son enlaces HLS** y requieren reproductor compatible con YouTube.

Usá la dirección RAW para cargar la lista HLS en un reproductor compatible:

https://raw.githubusercontent.com/luchochavezfacebook-byte/lista-clasica-/main/lista_clasica.m3u

Para YouTube LIVE (solo en reproductores compatibles):

https://raw.githubusercontent.com/luchochavezfacebook-byte/lista-clasica-/main/lista_clasica_youtube.m3u

## Archivos y mantenimiento

- `fuentes.json`: fuentes HLS y estado de verificación.
- `youtube_en_vivo.json`: canales YouTube con direcciones `/live` persistentes.
- `scripts/generar_lista.py` y `scripts/generar_lista_youtube.py`: regeneran las listas.
- `scripts/validar_repositorio.py`: rechaza manifiestos firmados, tokens y duplicados.
- `scripts/verificar_canales.py`: prueba manifiestos HLS y acceso a un segmento, sin confirmar decodificación.
- `diagnosticos/candidatos.json`: alternativas pendientes de prueba, no incluidas automáticamente en la M3U.
- `.github/workflows/auditar-hls.yml`: auditoría informativa cada 6 horas; guarda reporte de los canales y alternativas durante 7 días.
- `.github/workflows/validar-listas.yml`: valida que archivos y listas sean coherentes.

```bash
python3 scripts/validar_repositorio.py
python3 scripts/generar_lista.py
python3 scripts/generar_lista_youtube.py
python3 scripts/verificar_canales.py
```

## Lista HLS conectada a TV FULL PRO V62 — revisión 2026-10-27

La APK V62 lee `lista_clasica.m3u` directamente. **11 entradas HLS**, actualizadas tras una auditoría ejecutada en GitHub Actions:

- **América TV:** fuente DAI anterior devolvía HTTP 410. Sustituida por HLS directo catalogado en iptv-org con `User-Agent` declarado; el manifiesto y un segmento respondieron desde GitHub.
- **El Trece:** fuente anterior devolvía una variante que no era HLS en el runner. Sustituida por la alternativa que requiere `Referer: https://vodgc.net`; manifiesto y un segmento respondieron.
- **Telemax:** fuente anterior no respondió; sustituida por `stream-gtlc.telecentro.net.ar/hls/telemaxhls/main.m3u8`, que pasó el mismo chequeo.
- **Telefe:** la fuente nacional anterior `mdstrm.com` devolvía HTTP 403 y el usuario confirmó que no reproduce. Se quitó de la M3U activa y se incorporó **Telefe Tucumán (regional)** en una categoría propia. La señal regional **NO es la misma emisión que Telefe Buenos Aires/nacional**.
- **Net TV:** conserva su fuente principal y suma un respaldo de `unlimited6-cl.dps.live`, compatible con el fallback de V62 mediante `#EXT-X-TVFULL-BACKUP`.
- **TN, Canal 26, A24 y Canal E:** manifestos y primer segmento accesibles desde el runner; no se modificaron.
- **DeporTV y TV Universidad:** error de red desde el runner; se conservan sin declararlos caídos en Argentina.

**ATENCIÓN:** el estado `segmento_accesible` significa que se pudo descargar el manifiesto y una muestra del primer fragmento, **no que haya imagen, sonido ni estabilidad continua en los TV Box argentinos**. Los 403 externos tampoco son prueba de caída global debido a restricciones geográficas.

Se ejecuta una auditoría automática cada seis horas, con resultados en la sección Actions del repositorio. **No cambia los enlaces automáticamente** para evitar publicar fuentes incorrectas, fuera de región o temporales.

Para probar: entrar a Lista Clásica en V62, elegir **Actualizar listas** y verificar el nuevo canal **Telefe Tucumán (regional)**, América TV, El Trece, Telemax y el respaldo de Net TV. Los cambios no requieren actualizar la APK ni afectan Proveedor 2.

La lista complementaria de YouTube contiene **C5N, Crónica, LN+, Telefe Noticias, LUZU, OLGA** y otras referencias que V62 todavía no reproduce directamente; no mezclarlas como HLS.

## Streaming argentino conocido — LUZU, OLGA y otros

Agregados a **`lista_clasica_youtube.m3u`**: **LUZU TV**, **OLGA**, **BLENDER**, **GELATINA**, **Vorterix**, **Bondi Live**, **Futurock FM**, **AZZ Streaming**, **Neura Media** y **Carajo Stream**. La categoría M3U es `Streaming Argentina`.

Son rutas permanentes hacia el canal de YouTube (`/@canal/live`), no manifiestos HLS. Algunas señales emiten solo en horarios de programación y la disponibilidad puede cambiar. No se encontraron ni verificaron URLs HLS permanentes para esos diez medios. No almacenar `manifest.googlevideo.com` firmado ni copiar sesiones de navegador como enlaces públicos.

**IMPORTANTE — TV FULL PRO V62:** la APK está conectada exclusivamente a `lista_clasica.m3u` (11 HLS) y **no mostrará estas 10 incorporaciones al apretar Actualizar listas**. Para agregarlas en una nueva versión sin enlaces rotos se requiere integrar un reproductor oficial de YouTube o lanzar la aplicación de YouTube del TV Box. La Lista Clásica HLS fue revisada en 2026-10-27. La APK y el Proveedor 2 permanecen sin cambios.

## Noticias argentinas más conocidas (YouTube)

La lista complementaria incluye TN, A24, C5N, Canal 26, Crónica TV, LN+, Telefe Noticias, Argentina/12, Infobae en Vivo y Telenueve, además de otras referencias. Los nuevos enlaces usan rutas `/@canal/live` que no contienen firmas temporales.

**No implica emisión las 24 horas:** Infobae en Vivo y Telenueve tienen programación en franjas horarias. La pestaña `/live` puede no ofrecer directo cuando no están transmitiendo. Todas estas URLs necesitan un cliente de YouTube compatible; **TV FULL PRO V62 no reproduce estos enlaces directamente con Media3**.

## Telefe Noticias: referencia persistente y actualizaciones

La referencia estable de **Telefe Noticias — 24 h** es `https://www.youtube.com/@telefenoticias/live` (video observado: `XhAYcYpPzTc`). Está incluida **solo** en `lista_clasica_youtube.m3u`, no en `lista_clasica.m3u`, porque la aplicación TV FULL PRO V62 espera HLS directo y **no interpreta una URL `youtube.com/@.../live` como video**.

Si el directo cambia de identificador, la ruta `/@telefenoticias/live` es una referencia al canal; el reproductor oficial de YouTube resuelve la emisión vigente al abrirla. Si el canal deja de emitir o restringe incorporaciones, no se puede garantizar reproducción. La URL de la transmisión en sí no es un M3U8 y no debe enviarse directamente a Media3/ExoPlayer como HLS.

Para reproducirla desde TV FULL PRO se necesita una función específica: **abrir el directo con el reproductor oficial de YouTube o utilizar el IFrame Player autorizado**, sin alterar las fuentes HLS existentes. Este soporte **no está disponible en la V62**. No usar GitHub Actions para reemplazar HLS firmados por sesiones obtenidas en la IP de un runner: los tokens son de corta vida y pueden estar vinculados a la IP o sesión.

Los enlaces `manifest.googlevideo.com` de YouTube con `expire`, `sig` o dirección IP son **temporales** y no se publican. Algunas fuentes, particularmente Telefe, han respondido HTTP 403 desde ciertas redes. Una entrada en la lista no certifica que el video funcione o que esté autorizada su redistribución.

El repositorio es **independiente del código de tvplayer**, pero V62 consume su archivo RAW `lista_clasica.m3u`. No usa Xtream Codes, Proveedor 2, ClearKey ni DRM. No incluye credenciales ni retransmite contenido.
