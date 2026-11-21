# Revisión de seis señales reportadas — 21/11/2026

Se mantienen todos los canales y todas las fuentes anteriores. Tres canales reciben una fuente principal actualizada, con la anterior guardada como respaldo. La lista continúa con 300 entradas HLS únicas. No se modificó la APK ni la lista YT.

Un error aislado, un 403/404, un timeout, una carta de prueba o un período sin transmisión no confirma que un canal o una fuente hayan dejado de funcionar de forma permanente. No se eliminó ninguno. El script de auditoría del repositorio genera diagnósticos y no elimina canales.

## Resultados

| Canal | Evidencia | Acción |
|---|---|---|
| Aire de Santa Fe | La fuente DPS anterior devolvió 404 en varias consultas. La web oficial usa Mediastream con ID 6931a0eb06778645348008e0. Su HLS produjo video 360p y audio en dos muestras separadas. | Actualizar principal; conservar anterior como respaldo. |
| Canal 22 | La fuente anterior dio timeout/503 desde el entorno de revisión. canal22web.com publica play.cdnvid.com/canal-22; el resolvedor público devuelve dos HLS. Ambos reprodujeron video 1080p; principal repetido y audio confirmado. | Principal y alternativa actuales; conservar también la fuente anterior como segundo respaldo. |
| VerTV | La fuente anterior dio timeout/503. quierovertv.com, el canal regional de Venado Tuerto, publica play.cdnvid.com/aloa. El resolvedor del reproductor publica dos HLS con video 1080p y audio; principal repetido. | Principal y alternativa actuales; conservar anterior como segundo respaldo. |
| Canal 4 Jujuy | Master HTTP 200. Variantes 480p y 720p: 404. Variante 1080p: programación con logo Canal 4, video y audio decodificados. La web responde status disabled, pero el HLS HD sí entregó programación: ese estado no demuestra un cese total. | Conservar el master original. El fallo parcial de calidades puede explicar el error del reproductor; no se publica una URL de sesión temporal. |
| TV Maná Argentina | La web oficial publica la misma fuente. Master HTTP 200, pero sus tres variantes dieron 404. También se probó con Referer/Origin oficiales y nueva solicitud. | Conservar sin dar de baja: transmisión no confirmada durante esta revisión. |
| TV Universidad UNLP | tv.unlp.edu.ar publica la misma URL stratus.stream.cespi.unlp.edu.ar. Responde 403 tanto sin cabeceras como con Referer/Origin oficiales. | Conservar: acceso denegado desde este entorno, no cese confirmado. |

## Principales actualizadas

- Aire: https://mdstrm.com/live-stream-playlist/6931a0eb06778645348008e0.m3u8
- Canal 22: https://media.cdnvid.com/public/7c3g8h159tip.m3u8
- VerTV: https://media.cdnvid.com/public/uovlwqzikeyf.m3u8

Las rutas secundarias de Canal 22 y VerTV pertenecen al mismo proveedor; no garantizan independencia de infraestructura. Las fuentes anteriores se conservan para permitir su recuperación si vuelven a estar disponibles.

## Verificación

Se descargaron manifiestos y segmentos HLS y se decodificaron muestras. Además del código de salida de FFmpeg, se contaron fotogramas de video y audio mediante framemd5 y se revisaron capturas con los logotipos. En Canal 4 Jujuy, FFprobe inicialmente informó dimensiones 0×0; una prueba ampliada confirmó 49 fotogramas de video y 87 de audio, y se obtuvo captura de imagen. No se debe decidir una baja por el primer error ni por datos incompletos del sondeo.

Las pruebas se realizaron el 21/11/2026. Son muestras breves desde un entorno remoto; queda por comprobar reproducción continua en la TV Box del usuario.

Fuentes oficiales contrastadas:

- https://www.airedesantafe.com.ar/aire-de-santa-fe-en-vivo
- https://canal22web.com/ y https://play.cdnvid.com/canal-22
- https://www.quierovertv.com/ y https://play.cdnvid.com/aloa
- https://canal4jujuy.elcuatro.com/ y su reproductor público /player/index?autoplay=true
- https://tvmana-argentina.ar/
- https://tv.unlp.edu.ar/

Para probar las correcciones: Lista Clásica → Recargar lista → Argentina TV.
