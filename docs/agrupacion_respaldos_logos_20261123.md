# Consolidación de canales del usuario — 23 de noviembre de 2026

## Resultado

Los **594 enlaces nuevos** que pasaron la auditoría previa se consolidaron en **196 canales visibles**, cada uno con el conjunto completo de **398 direcciones alternativas** asociadas como respaldos.

**No se modificó ninguna de las 353 entradas originales** de Lista Clásica, ni sus logos, URLs, categorías, User-Agent o respaldos. El archivo resultante tiene **549 canales visibles HLS** (353 originales + 196 nuevos). La Lista Clásica YouTube y la APK tampoco fueron modificadas.

## Logos en cada nuevo canal

- **123** con imagen provista por `ByRafaelSystem/futboltotal-links` en su directorio público [logos](https://github.com/ByRafaelSystem/futboltotal-links/tree/main/logos).
- **46** con imagen correspondiente identificada en el catálogo público `iptv-org/database` (`data/channels.csv` y `data/logos.csv`), sin incluir SVG.
- **27** con PNG local personalizado con el **nombre de la señal**, generado en [logos/usuario_20261123](../logos/usuario_20261123) al no encontrarse un logo de marca fiable. No se presenta como logo oficial.

El catálogo [fuentes_usuario_argentina_20261123.json](../fuentes_usuario_argentina_20261123.json) registra el origen de cada logo. Un URL de logo externo puede dejar de funcionar: no se afirma disponibilidad permanente.

## Respaldos: cómo se guardan

La playlist muestra un único canal por nombre; las alternativas restantes están en el atributo `backups` del JSON de origen y en las líneas `#EXT-X-TVFULL-BACKUP:` del M3U generado, sin crear entradas visibles adicionales. Los 398 enlaces quedaron conservados, incluso los HTTP que ya habían superado la auditoría de video desde GitHub, con restricciones para no aceptar servidores locales o credenciales.

**Importante:** el formato `#EXT-X-TVFULL-BACKUP:` es una extensión propia, no parte obligatoria del estándar M3U. **No se verificó en esta tarea que la APK de TV FULL PRO realice el cambio automático de respaldo**; para eso hay que comprobar la compatibilidad de su importador. La conservación de respaldos en el archivo es verificable, pero no implica uso automático.

## Verificación

La integración [de GitHub Actions](https://github.com/luchochavezfacebook-byte/lista-clasica-/actions/workflows/consolidar-usuario-20261123.yml) comprobó:

1. Las 594 URLs nuevas originales están todas presentes una vez, ya sea como fuente principal o como respaldo.
2. Los 353 bloques M3U anteriores coinciden **byte por byte a nivel de bloque** con los de la versión anterior, incluida su metadata, headers y backups.
3. La lista nueva tiene 549 canales visibles únicos y las 196 incorporaciones poseen logo.
4. Se generaron 27 PNG locales para los que no tenían imagen de marca.

El diagnóstico detallado y el respaldo de las 594 entradas sin agrupar están en `diagnosticos/agrupaciones_logos_usuario_20261123.json` y `diagnosticos/fuentes_usuario_antes_agrupacion_20261123.json`.

**Disponibilidad desde Argentina:** la auditoría previa demostró decodificación de video de las 594 URLs desde GitHub Actions, pero no se confirmó geolocalización desde una IP argentina, continuidad prolongada ni permisos para retransmisión.

**TV FULL PRO:** Lista Clásica → Recargar lista → Argentina TV.
