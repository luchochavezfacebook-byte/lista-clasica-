# Lista Clásica — TV FULL PRO

La lista principal está organizada **por país de la señal**, con Argentina primero y los enlaces de YouTube separados en **Argentina YT**. Es un catálogo independiente del código de TV FULL PRO, no una promesa de funcionamiento de todos los reproductores.

## Listas

- [**Lista principal**](lista_clasica.m3u): **251 fuentes HLS únicas**, más **una referencia oficial de YouTube para Canal 10 Tucumán**; 252 entradas en total. Las 251 HLS conservan sus URLs, cabeceras, logos y respaldos anteriores.
- [**YouTube en vivo**](lista_clasica_youtube.m3u): 27 referencias a transmisiones públicas que requieren un cliente compatible con YouTube.

URL RAW principal para TV FULL PRO:

https://raw.githubusercontent.com/luchochavezfacebook-byte/lista-clasica-/main/lista_clasica.m3u

## Categorías por países — revisión 2026-11-10

Las fuentes HLS se agrupan como `group-title="<País> TV"`. Las referencias YouTube dentro de la lista principal van a una categoría **separada**, `Argentina YT`. Hay **38 grupos** en total, incluyendo **Internacional TV** para señales multinacionales o de procedencia incierta. No quedan categorías ambiguas como `Mundo TV / GENERAL`, `INT. ASIA` o `Noticias Argentina`.

**Argentina TV** aparece primero, con **59 señales HLS**. A continuación aparece **Argentina YT**, con **Canal 10 Tucumán**, que requiere un reproductor compatible con YouTube. El resto de países aparece ordenado alfabéticamente, y las emisoras se ordenan por nombre dentro de cada país.

La atribución de país se guarda en los campos `pais` y `categoria` de `fuentes.json` y `fuentes_mundotv.json`. El campo `categoria_original` conserva la clasificación histórica importada. Algunas señales multinacionales se marcan `Internacional TV` para no asignarles un país sin respaldo.

## Canal 10 Tucumán

Se agregó **Canal 10 Tucumán (YouTube - requiere app externa)** también a `lista_clasica.m3u`, dentro de **Argentina YT**, usando su referencia estable:

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
