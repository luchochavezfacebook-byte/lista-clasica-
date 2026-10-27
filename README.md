# Canales — Lista Clásica

Repositorio **independiente de TV FULL PRO** con una lista de señales gratuitas argentinas y una lista complementaria de transmisiones en YouTube.

## Listas

- [Lista Clásica HLS](lista_clasica.m3u): 9 fuentes HLS candidatas. **No todas están verificadas ni garantizadas**.
- [YouTube LIVE](lista_clasica_youtube.m3u): 11 referencias a canales oficiales de YouTube. **No son enlaces HLS** y requieren reproductor compatible con YouTube.

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

## Telefe Noticias: referencia persistente y actualizaciones

La referencia estable de **Telefe Noticias — 24 h** es `https://www.youtube.com/@telefenoticias/live` (video observado: `XhAYcYpPzTc`). Está incluida **solo** en `lista_clasica_youtube.m3u`, no en `lista_clasica.m3u`, porque la aplicación TV FULL PRO V62 espera HLS directo y **no interpreta una URL `youtube.com/@.../live` como video**.

Si el directo cambia de identificador, la ruta `/@telefenoticias/live` es una referencia al canal; el reproductor oficial de YouTube resuelve la emisión vigente al abrirla. Si el canal deja de emitir o restringe incorporaciones, no se puede garantizar reproducción. La URL de la transmisión en sí no es un M3U8 y no debe enviarse directamente a Media3/ExoPlayer como HLS.

Para reproducirla desde TV FULL PRO se necesita una función específica: **abrir el directo con el reproductor oficial de YouTube o utilizar el IFrame Player autorizado**, sin alterar las fuentes HLS existentes. Este soporte **no está disponible en la V62**. No usar GitHub Actions para reemplazar HLS firmados por sesiones obtenidas en la IP de un runner: los tokens son de corta vida y pueden estar vinculados a la IP o sesión.

Los enlaces `manifest.googlevideo.com` de YouTube con `expire`, `sig` o dirección IP son **temporales** y no se publican. Algunas fuentes, particularmente Telefe, han respondido HTTP 403 desde ciertas redes. Una entrada en la lista no certifica que el video funcione o que esté autorizada su redistribución.

El repositorio **no se integra con tvplayer ni usa Xtream Codes, Proveedor 2, ClearKey o DRM**. No incluye credenciales ni retransmite contenido.
