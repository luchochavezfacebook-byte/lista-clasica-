# Importación de Netvideo TvPlay — 22/11/2026

**Origen:** grilla pública de Netvideo facilitada por el proveedor para integrar canales en TV FULL PRO.

**Inventario:** 70 elementos: 62 HLS y 8 radios/flujos no-HLS. Tras cruzar los nombres, se excluyeron 28 señales coincidentes o equivalentes a las ya presentes; se probaron 36 candidatas. De estas, 30 decodificaron video en dos muestras, se eliminaron 2 duplicados adicionales por nombres alternativos (Radio Power Max y LinkTV), y se incorporaron 28.

**Pruebas de video:** GitHub Actions (muestras de al menos 20 fotogramas en 2 segundos, con manifiesto y primer fragmento accesibles). Solo son pruebas desde un servidor externo: no garantizan la identidad exacta del contenido, el audio, la continuidad ni el acceso geográfico.

- [Primera prueba HLS](https://github.com/luchochavezfacebook-byte/lista-clasica-/actions/runs/45016048000/attempts/1)
- [Segunda prueba HLS](https://github.com/luchochavezfacebook-byte/lista-clasica-/actions/runs/45016048000/attempts/2)

## Canales incorporados

| Canal | Grupo | Logo |
|---|---|---|
| Online 24/7 | Internacional TV | Sí |
| C5N | Argentina TV | Sí |
| TV Pública | Argentina TV | Sí |
| Crónica TV | Argentina TV | Sí |
| Rural | Argentina TV | Sí |
| Tierra Mía TV | Argentina TV | Sí |
| Telefe (nacional) | Argentina TV | Sí |
| La Nación+ (LN+) | Argentina TV | Sí |
| Canal 9 Televida | Argentina TV | Sí |
| Ciudad Magazine | Argentina TV | Sí |
| Freyre TV | Argentina TV | Sí |
| Medios Provincia | Argentina TV | Sí |
| IRE | Argentina TV | Sí |
| Telesol San Juan | Argentina TV | Sí |
| RTN Neuquén | Argentina TV | Sí |
| Canal 12 Misiones | Argentina TV | Sí |
| Silver Channel | Internacional TV | Sí |
| Nuevo Tiempo | Internacional TV | Sí |
| RT en Español | Internacional TV | Sí |
| Novo Tempo | Brasil TV | Sí |
| Extrema TV | Internacional TV | Sí |
| Aliento Visión | Internacional TV | Sí |
| Red Avenir | Internacional TV | Sí |
| Comunión TV | Internacional TV | Sí |
| Music Top | Argentina TV | Sí |
| Radio Urbana | Argentina TV | Sí |
| Retro TV | Argentina TV | Sí |
| Enlace | Internacional TV | Sí |

## No incorporados

**Ya existentes:** TN, El Trece, América, A24, Canal 26, Net TV, Telemax, Canal 7 Jujuy, Canal 7 Salta, Canal 10 Mar del Plata, Radio Power Max, LinkTV y otras señales ya catalogadas. No se reemplazaron sus fuentes principales ni sus respaldos.

**Pendientes de recuperación:** CGTN en Español, TECtv, OK FM 95.5, Norte Visión, CTNi, Canal 5. En las auditorías tuvieron timeout, respuesta inesperada o video no decodificado; una falla temporal no implica baja definitiva.

**No HLS:** ocho fuentes externas de radios y audio no se agregaron a la lista de video compatible con Media3.

## Compatibilidad y seguridad

Las 28 URL nuevas proceden de rutas HTTP en `200.80.230.125:5056`, con un componente opaco en la ruta. Se permite esa excepción exacta en las validaciones; los restantes canales conservan la política HTTPS. La publicación de la lista hace visibles estas rutas, por lo que corresponde mantener confirmada la autorización del proveedor para compartirlas. No se cargaron cuentas, contraseñas, cabeceras de autorización ni contenidos protegidos por DRM.

No se modificó `lista_clasica_youtube.m3u` ni la app Android.
