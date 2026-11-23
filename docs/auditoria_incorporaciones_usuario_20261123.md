# Auditoría de canales incorporados el 23 de noviembre de 2026

## Alcance

- Se comparó la lista de **1.216** canales del commit manual `7f53dcb745db` contra la base conocida de **353** del commit `bb80b9248a48`.
- Se identificaron **863 direcciones HLS nuevas**, alojadas en **seis servidores distintos**.
- Se excluyó **1** URL potencialmente sensible/no apta; **862** se sometieron a prueba con FFmpeg.
- En la primera pasada **594** decodificaron al menos 12 fotogramas. Se repitieron las 594 y **todas aprobaron la segunda pasada**.
- **269** nuevas entradas no se publican; no se asegura que estén definitivamente caídas en todas las redes.
- Se conserva el inventario de las 863, con estado y dos muestras, en `diagnosticos/qa_usuario_20261123.json` (sin repetir enlaces privados).
- **947 canales finales** = 353 anteriores + 594 nuevos aprobados. Todos los nuevos se incorporan a `Argentina TV`, independientemente del país de origen de la emisora.

## Evidencia y reproducción

[GitHub Actions — auditoría FFmpeg completa](https://github.com/luchochavezfacebook-byte/lista-clasica-/actions/runs/45240741627)

Validación del generador y control de 947 direcciones únicas incluida en el mismo trabajo.

**Limitación geográfica crucial:** estas pruebas **NO se hicieron desde una IP argentina**. Confirman accesibilidad y video desde los runners de GitHub, pero no garantizan que cada canal pueda verse desde Argentina o en la TV Box. Al configurar `Argentina TV` se define únicamente la **categoría visual de la app**. No debe interpretarse como origen nacional, licencia de emisión ni garantía de disponibilidad territorial.

No se modificaron las 353 URL principales previas, las URL de respaldos de esas fuentes, Lista Clásica YouTube, otras listas, la APK o los proveedores de TV FULL PRO.

## Mantenimiento

La fuente agregada se gestiona en `fuentes_usuario_argentina_20261123.json`, no con pegados manuales en `lista_clasica.m3u`. El generador la agrega automáticamente y la auditoría general también puede comprobar sus URLs. Las fuentes nuevas se diferencian por IDs `Usuario20261123.XXXX` para poder darlas de baja posteriormente sin tocar las fuentes históricas.

La versión anterior de 1.216 entradas se puede recuperar desde [commit de incorporación](https://github.com/luchochavezfacebook-byte/lista-clasica-/commit/7f53dcb745db).

