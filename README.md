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
- `scripts/verificar_canales.py`: prueba manifiestos HLS (sin comprobar continuidad real).
- `.github/workflows/validar-listas.yml`: valida que archivos y listas sean coherentes.

```bash
python3 scripts/validar_repositorio.py
python3 scripts/generar_lista.py
python3 scripts/generar_lista_youtube.py
python3 scripts/verificar_canales.py
```

## Lista HLS conectada a TV FULL PRO V62

La app lee **`lista_clasica.m3u`**, no `lista_clasica_youtube.m3u`. Se mantienen los 9 HLS anteriores y se añadieron **A24 (América 24)** y **Canal E / Perfil TV** como **candidatos de prueba** (11 entradas HLS en total). Las dos nuevas fuentes están publicadas como URLs HLS sin firmas ni sesiones privadas. A24 declara un `User-Agent` para TV FULL PRO V62 mediante `#EXTVLCOPT:http-user-agent`, que su parser admite.

**La presencia de un canal en el M3U no garantiza reproducción.** Se encontraron referencias a esas URLs en catálogos públicos de IPTV, pero no se confirmó HTTP 200, decodificación o continuidad en un TV Box real. Si fallan, no añadir más enlaces dudosos ni sustituir una fuente conocida por otra sin verificar.

Los canales **C5N, Crónica, LN+, Telefe Noticias, Infobae y Telenueve** siguen solo en la lista complementaria de YouTube, porque el reproductor HLS de V62 no resuelve enlaces `/@canal/live`. No publicar los `manifest.googlevideo.com` firmados y caducables como si fueran URL permanentes. Para ofrecer esos canales dentro de la APK hace falta soporte específico de YouTube o encontrar HLS directo legalmente accesible y probado.

En V62, seleccionar Lista Clásica y ejecutar **Actualizar listas** debe solicitar el M3U RAW; verificar en la TV que se reciben 11 canales y que A24/Canal E reproducen antes de anunciarlos como operativos.

## Streaming argentino conocido — LUZU, OLGA y otros

Agregados a **`lista_clasica_youtube.m3u`**: **LUZU TV**, **OLGA**, **BLENDER**, **GELATINA**, **Vorterix**, **Bondi Live**, **Futurock FM**, **AZZ Streaming**, **Neura Media** y **Carajo Stream**. La categoría M3U es `Streaming Argentina`.

Son rutas permanentes hacia el canal de YouTube (`/@canal/live`), no manifiestos HLS. Algunas señales emiten solo en horarios de programación y la disponibilidad puede cambiar. No se encontraron ni verificaron URLs HLS permanentes para esos diez medios. No almacenar `manifest.googlevideo.com` firmado ni copiar sesiones de navegador como enlaces públicos.

**IMPORTANTE — TV FULL PRO V62:** la APK está conectada exclusivamente a `lista_clasica.m3u` (11 HLS) y **no mostrará estas 10 incorporaciones al apretar Actualizar listas**. Para agregarlas en una nueva versión sin enlaces rotos se requiere integrar un reproductor oficial de YouTube o lanzar la aplicación de YouTube del TV Box. La lista principal HLS y el Proveedor 2 permanecen sin cambios.

## Noticias argentinas más conocidas (YouTube)

La lista complementaria incluye TN, A24, C5N, Canal 26, Crónica TV, LN+, Telefe Noticias, Argentina/12, Infobae en Vivo y Telenueve, además de otras referencias. Los nuevos enlaces usan rutas `/@canal/live` que no contienen firmas temporales.

**No implica emisión las 24 horas:** Infobae en Vivo y Telenueve tienen programación en franjas horarias. La pestaña `/live` puede no ofrecer directo cuando no están transmitiendo. Todas estas URLs necesitan un cliente de YouTube compatible; **TV FULL PRO V62 no reproduce estos enlaces directamente con Media3**.

## Telefe Noticias: referencia persistente y actualizaciones

La referencia estable de **Telefe Noticias — 24 h** es `https://www.youtube.com/@telefenoticias/live` (video observado: `XhAYcYpPzTc`). Está incluida **solo** en `lista_clasica_youtube.m3u`, no en `lista_clasica.m3u`, porque la aplicación TV FULL PRO V62 espera HLS directo y **no interpreta una URL `youtube.com/@.../live` como video**.

Si el directo cambia de identificador, la ruta `/@telefenoticias/live` es una referencia al canal; el reproductor oficial de YouTube resuelve la emisión vigente al abrirla. Si el canal deja de emitir o restringe incorporaciones, no se puede garantizar reproducción. La URL de la transmisión en sí no es un M3U8 y no debe enviarse directamente a Media3/ExoPlayer como HLS.

Para reproducirla desde TV FULL PRO se necesita una función específica: **abrir el directo con el reproductor oficial de YouTube o utilizar el IFrame Player autorizado**, sin alterar las fuentes HLS existentes. Este soporte **no está disponible en la V62**. No usar GitHub Actions para reemplazar HLS firmados por sesiones obtenidas en la IP de un runner: los tokens son de corta vida y pueden estar vinculados a la IP o sesión.

Los enlaces `manifest.googlevideo.com` de YouTube con `expire`, `sig` o dirección IP son **temporales** y no se publican. Algunas fuentes, particularmente Telefe, han respondido HTTP 403 desde ciertas redes. Una entrada en la lista no certifica que el video funcione o que esté autorizada su redistribución.

El repositorio **no se integra con tvplayer ni usa Xtream Codes, Proveedor 2, ClearKey o DRM**. No incluye credenciales ni retransmite contenido.
