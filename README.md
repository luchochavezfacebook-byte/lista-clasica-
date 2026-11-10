# Lista Clásica — TV FULL PRO

La lista principal está organizada **por país de la señal**, con Argentina primero y los enlaces de YouTube separados en **Argentina YT**. Es un catálogo independiente del código de TV FULL PRO, no una promesa de funcionamiento de todos los reproductores.

## Listas

- [**Lista principal**](lista_clasica.m3u): **251 fuentes HLS únicas**, más **27 referencias de YouTube** en Argentina YT; 278 entradas en total. Las 251 HLS conservan sus URLs, cabeceras, logos y respaldos anteriores.
- [**YouTube en vivo**](lista_clasica_youtube.m3u): 27 referencias a transmisiones públicas que requieren un cliente compatible con YouTube.

URL RAW principal para TV FULL PRO:

https://raw.githubusercontent.com/luchochavezfacebook-byte/lista-clasica-/main/lista_clasica.m3u

## Categorías por país y tipo de fuente — revisión 2026-11-10

La lista principal agrupa los **251 canales HLS** por país, con **59 señales en Argentina TV**, y agrega **todos los 27 enlaces de `youtube_en_vivo.json`** dentro de **Argentina YT**. Esta última es una categoría técnica para distinguir YouTube, no una atribución de nacionalidad: incluye también CNN en Español y DW Español.

**Total: 278 entradas**, agrupadas en **38 categorías**. Las señales HLS mantienen los nombres, logos, respaldos y direcciones anteriores. Los enlaces YT se identifican con el sufijo «YouTube - requiere app externa», porque V62 no los reproduce directamente.

El generador usa los 27 enlaces de `youtube_en_vivo.json` (en lugar de uno solo) para que una regeneración no los quite. Los identificadores YT no se confunden con los HLS.

## Canal 10 Tucumán

Se agregó **Canal 10 Tucumán (YouTube - requiere app externa)** también a `lista_clasica.m3u`, dentro de **Argentina YT** junto con los otros 26 enlaces YouTube, usando su referencia estable:

https://www.youtube.com/channel/UCRlakPhec4-k3vkBeyWBojg/live

**Advertencia técnica importante:** es una URL de YouTube, **no un manifiesto HLS**; **TV FULL PRO V62 no puede reproducirla directamente**. Es visible en el catálogo, pero requeriría que una versión futura de la aplicación invoque YouTube o un reproductor autorizado. No se ha encontrado un HLS permanente oficial de este canal. No se publicó ninguna URL temporal de `manifest.googlevideo.com`: esas URLs caducan y pueden estar vinculadas a la sesión o la IP.

No confundir Canal 10 Tucumán con **Canal 10 Televida (Mendoza)** ni con **Canal 8 / Telefe Tucumán**. Son señales distintas.

## Mantenimiento y validación

- `fuentes.json`: 11 fuentes argentinas principales, con encabezados y respaldos que tenía la lista.
- `fuentes_mundotv.json`: 245 fuentes importadas, clasificadas por país.
- `youtube_en_vivo.json`: referencias permanentes a YouTube.
- `scripts/generar_lista.py`: crea la lista principal con Argentina primero y la referencia Canal 10.
- `scripts/generar_lista_youtube.py`: mantiene la lista complementaria de YouTube.
- `scripts/validar_repositorio.py`: verifica países, URLs, duplicados, firmas temporales y estructura M3U.
- `scripts/verificar_canales.py`: comprueba las 11 fuentes originales y algunos candidatos, **no las 251 señales**.
- `.github/workflows/auditar-hls.yml`: diagnóstico cada 6 horas; no reemplaza automáticamente enlaces.

Para comprobar la coherencia de la lista:

```bash
python3 scripts/validar_repositorio.py
python3 scripts/generar_lista.py
python3 scripts/generar_lista_youtube.py
git diff --exit-code -- lista_clasica.m3u lista_clasica_youtube.m3u
```

La clasificación por país **no certifica la reproducción**. Las fuentes pueden tener restricciones regionales o fallar en dispositivos Android TV; se necesita comprobar imagen/sonido en la APK. No se han añadido credenciales, claves DRM ni enlaces de pago.

## Antecedentes

La lista original contenía 11 canales argentinos y 245 importados (251 URLs HLS únicas después de deduplicar). Se conservan todos los enlaces HLS. Se mantiene el encabezado de compatibilidad de **Canal 8 / Telefe Tucumán**, actualizado anteriormente, pero todavía pendiente de prueba física.

**TV FULL PRO V62 y Proveedor 2 no fueron modificados.**
