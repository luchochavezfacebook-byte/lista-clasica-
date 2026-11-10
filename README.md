# Lista Clásica — TV FULL PRO V62

## Estado de recuperación — 10/11/2026

Se retiraron **27 enlaces de YouTube** que se habían agregado por error a la lista M3U principal. Se detectó que V62 los entregaba a Media3 como si fueran URLs HLS, lo cual produce **Formato de señal no compatible**. No son HLS y una categoría como «Argentina YT» no puede cambiar su formato.

**Lista principal:** [lista_clasica.m3u](lista_clasica.m3u) — **251 enlaces HLS únicos**, por país, con Argentina primero. Conserva los **251 URL HLS, User-Agent, Referer y respaldos** previos al error. Se añadieron **9 logos** ya presentes en el índice de la APK, con lo que la lista principal ahora declara **247 logos**. No se alteraron URLs, proveedores ni claves.

**Referencias de YouTube:** [lista_clasica_youtube.m3u](lista_clasica_youtube.m3u) — **27 enlaces de canales**, incluidos Canal 10 Tucumán, C5N, LUZU, OLGA y otros. Se conservan para reproductores compatibles con YouTube, pero **no deben cargarse como HLS en TV FULL PRO V62**. No se mezclan en `lista_clasica.m3u`.

### Fuente RAW usada por la APK

https://raw.githubusercontent.com/luchochavezfacebook-byte/lista-clasica-/main/lista_clasica.m3u

## Agrupación

Los HLS están organizados por país mediante `group-title="<País> TV"`: Argentina TV primero; luego países por orden alfabético; Internacional TV para procedencia multinacional o incierta. **No se quitó ningún HLS al recuperar la lista.**

## Logos

La lista original tenía **238 logos** en 251 señales HLS. Se copiaron **9 URL públicas de logos del propio índice de TV FULL PRO** a los canales HLS originales que carecían de `tvg-logo`, alcanzando **247 logos declarados**. Se mantienen **4 canales sin logo explícito** porque no se encontró una correspondencia fiable en ese índice (Canal E, TV Universidad, Canal y Cine Acción). Estos cambios son solo metadatos visuales, no alteran reproducción. La disponibilidad de cada imagen externa no se ha probado en todos los dispositivos.

## Canal 8 y Canal 10 Tucumán

- **Canal 8 / Telefe Tucumán** se conserva como señal HLS, incluida la cabecera de compatibilidad previamente configurada. Su reproducción debe verificarse desde una red argentina; GitHub Actions solo certificó manifiesto y un segmento, no imagen/sonido.
- **Canal 10 Tucumán** solo tiene una referencia estable a YouTube en el catálogo; no se ha identificado un HLS directo estable, público y verificado para la APK. La URL firmada `manifest.googlevideo.com` vence y puede depender de IP/sesión, por eso **no se publica**. Canal 10 permanece en la lista YouTube independiente hasta que se encuentre una fuente HLS legítima o se incorpore un reproductor de YouTube en la APK.

## Mantenimiento

- `fuentes.json`: 11 fuentes HLS originales
- `fuentes_mundotv.json`: 245 fuentes HLS importadas, clasificadas por país
- `youtube_en_vivo.json`: 27 referencias YouTube, separadas del reproductor HLS
- `scripts/generar_lista.py`: genera **solo HLS**
- `scripts/generar_lista_youtube.py`: genera la lista de YouTube por separado
- `scripts/validar_repositorio.py`: comprueba estructura, URLs, logos y ausencia de enlaces YouTube en la lista principal
- `scripts/verificar_canales.py` y `.github/workflows/auditar-hls.yml`: chequean conectividad HLS original; **no garantizan reproducción** en un TV Box

### Comprobación automática

```bash
python3 scripts/validar_repositorio.py
python3 scripts/generar_lista.py
python3 scripts/generar_lista_youtube.py
git diff --exit-code -- lista_clasica.m3u lista_clasica_youtube.m3u
```

**No se modificaron TV FULL PRO V62 ni Proveedor 2.**
