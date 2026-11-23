# Señales similares a la14hd.m3u sin tokens temporales — 23/11/2026

Fuente de comparación: [cabj91/tvplay/la14hd.m3u](https://github.com/cabj91/tvplay/blob/main/la14hd.m3u) — 108 entradas, todas con `token` y marcas de tiempo de octubre de 2026. No se utiliza ninguna URL de aquel archivo ni sus tokens. Los paquetes premium de ESPN, DSports, TNT Sports, Sky, Fox Premium y DAZN exigen fuentes de distribución autorizadas.

## Selección de siete emisiones abiertas / FAST y una baja

Se localizaron emisiones de anunciantes y distribuidores gratuitos y se probaron **dos veces** con FFmpeg y al menos **25 fotogramas**. La reproducción de pruebas se realizó en GitHub Actions, no en TV Box.

| Nueva señal (nombre real) | País | Origen público | Prueba |
| --- | --- | --- | --- |
| Telemundo Puerto Rico (WKAQ) | Puerto Rico | NBCUniversal / iptv-org | 2 × 25 fotogramas |
| ViX Deportes 24/7 (Zona TUDN) | Estados Unidos | Vizio FAST / iptv-org | 2 × 25 |
| Fubo Sports Network | Estados Unidos | Vizio FAST / iptv-org | 2 × 25 |
| Telemundo Noticias Ahora | Estados Unidos | NBCUniversal FAST | 2 × 25 |
| Telemundo Acción | Estados Unidos | NBCUniversal FAST | 2 × 25 |
| GLORY Kickboxing | Internacional | Rakuten FAST / Wurl | 2 × 25 |
| Telemundo Deportes Ahora | Estados Unidos | NBCUniversal FAST | 2 × 25, además **respaldo** comprobado (2 × 25) |

Se **retira TyC Sports FAST** de los catálogos publicados: dos pruebas FFmpeg sin flujo de video, sin un respaldo de la misma emisión que funcione. **TyC Sports 24 sí permanece** y pasó las dos pruebas. Se conserva el registro en `diagnosticos/bajas_playtv_20261123.json`.

Se comprobaron también siete señales preexistentes que siguen entregando video: beIN-SPORTS, beIN SPORTS XTRA, Fox Deportes, TyC Sports 24, CBS Sports Golazo, FIFA+ (Español) y Azteca Deportes Network. No se duplicaron.

## Pruebas y decisiones

- [Primera ronda: 15 candidatos, 8 aprobados, una señal nueva](https://github.com/luchochavezfacebook-byte/lista-clasica-/actions/runs/45222247935).
- [Segunda ronda: 7 fuentes adicionales, 5 aprobadas](https://github.com/luchochavezfacebook-byte/lista-clasica-/actions/runs/45222921973).
- [Tercera ronda: Telemundo Deportes Ahora principal y respaldo probados](https://github.com/luchochavezfacebook-byte/lista-clasica-/actions/runs/45223271790).

No se agregaron fuentes fallidas: La 1 RTVE (timeout/geolocalización posible), Telemundo Al Día (400/5xx/manifest inválido), Fubo Tubi (404 y errores), ni beIN SPORTS XTRA *en Español* de Tubi (404). La fuente española existente beIN-SPORTS desde Amagi sí pasó video y se conserva.

Las emisiones FAST suelen tener **restricciones geográficas** y reglas de uso/redistribución por proveedor. Que un enlace público reproduzca desde GitHub no demuestra su disponibilidad desde Argentina ni da permiso para redistribuirlo comercialmente. Las señales deben mantener su nombre verdadero; no sustituir canales premium por señales de programación distinta.

## Recuento

- Antes: **340** HLS únicos después de la depuración [PR #11](https://github.com/luchochavezfacebook-byte/lista-clasica-/pull/11).
- +7 emisiones públicas nuevas de video comprobado.
- −1 TyC Sports FAST sin imagen.
- Después: **346** HLS únicos en `lista_clasica.m3u`.
- Se conserva `lista_clasica_youtube.m3u`, sin cambios en APK, LIVE ni Provider 2.

La auditoría automatizada cada seis horas incluirá `fuentes_fast_playtv_20261123.json`.
