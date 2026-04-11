---
name: Downhole Test
description: Ensayo sísmico invasivo con fuente en superficie y receptores en un pozo — mide VS y VP directamente a cada profundidad; referencia complementaria al MASW
type: reference
---

# Downhole Test (DHT) — Ensayo Sísmico en Pozo (Sísmica de Pozo Abajo)

> [!CONCEPT] Definición
> El **Downhole Test (DHT)** es un ensayo sísmico invasivo que mide la **velocidad de onda de corte** $V_S$ y de compresión $V_P$ a diferentes profundidades usando una **fuente en superficie** y **receptores en un único pozo**. La fuente (martillo lateral para ondas SH, o pistón para ondas P) genera ondas que viajan verticalmente hacia abajo hasta los receptores (geófonos triaxiales) en el pozo. El tiempo de llegada directo a cada profundidad $z$ da la velocidad de intervalo: $V_S(z_i, z_{i+1}) = (z_{i+1} - z_i)/(t(z_{i+1}) - t(z_i))$. A diferencia del [[Cross-Hole Test]] (dos pozos), el DHT requiere solo **un pozo** — menor costo — pero la trayectoria de la onda no es horizontal sino inclinada (ángulo = $\arctan(x/z)$ donde $x$ es el offset fuente-pozo), lo que requiere una corrección geométrica. Es la referencia de campo estándar para calibrar perfiles $V_S(z)$ de [[MASW Method|MASW]] en estudios de respuesta sísmica de sitio. **Variante**: el **Seismic Cone Penetration Test (SCPTU)** combina el Downhole Test con el ensayo de penetración estática (CPT) en suelos blandos.
>
> — Foti et al. (2018), §1.1; ASTM D7400; Robertson & Cabal (2015).

## Principio de funcionamiento

### Geometría del ensayo

```
Fuente (superficie)
    |  \  offset x
    |   \
    |    \  ángulo θ = arctan(x/z)
    z     \
    |      ●  receptor (profundidad z)
```

El camino de la onda tiene longitud $r = \sqrt{x^2 + z^2}$. El tiempo de llegada directo:

$$t(z) = \frac{r}{V_S} = \frac{\sqrt{x^2 + z^2}}{V_S}$$

### Análisis de tiempos de intervalo

La velocidad de intervalo entre profundidades $z_1$ y $z_2$:

$$V_S^{intervalo}(z_1, z_2) = \frac{r(z_2) - r(z_1)}{t(z_2) - t(z_1)}$$

donde $r(z_i) = \sqrt{x^2 + z_i^2}$ (corrección de la geometría inclinada).

## Comparación con métodos de ondas superficiales

| Aspecto | Downhole Test | [[Cross-Hole Test]] | [[MASW Method\|MASW]] |
|---------|--------------|-------------------|------|
| Pozos requeridos | 1 | ≥2 | 0 |
| Trayectoria onda | Inclinada (fuente-pozo) | Horizontal | Superficial |
| Profundidad máxima | Depth del pozo | Depth del pozo | ~30–50 m (activo) |
| Resolución vertical | ~0.5–1 m | ~0.5–1 m | λ/3–λ/2 |
| Costo | Medio | Alto | Bajo |
| Invasividad | Alta (1 pozo) | Muy alta (≥2 pozos) | Ninguna |

## Rol en la validación de MASW

El DHT es la referencia de campo más usada para validar perfiles $V_S(z)$ de MASW en proyectos de ingeniería geotécnica, porque:
1. Requiere solo un pozo (costo manejable en proyectos reales)
2. Produce $V_S(z)$ directo sin necesidad de inversión
3. El pozo puede ser compartido con otros ensayos geotécnicos (SPT, muestreo)

El acuerdo entre MASW y DHT suele ser dentro de ±15% en profundidades inferiores a 30 m (Foti et al. 2018, §7.4).

> [!EXAMPLE] Evidencia empírica: Xia et al. (2002) — DHT como validación de MASW con modos superiores
> **Paper 009 (Xia, Miller, Park & Tian 2002)** utiliza el Downhole Test como referencia para validar el perfil $V_S(z)$ obtenido por MASW incluyendo modos superiores de ondas de Rayleigh. En el sitio de Kansas (perfil de 20 m de profundidad), el DHT muestra un perfil $V_S$ con variación 150–400 m/s en capas de ~2–3 m de espesor. La inversión MASW con modo fundamental reproduce el perfil DHT con error < 15% excepto en las capas intermedias donde el picking del modo superior mejora el acuerdo al ~8%. El paper establece que el costo del MASW (adquisición + procesamiento + inversión) es inferior a 1/10 del costo del DHT en el mismo sitio, con error comparable — justificando el MASW como alternativa no-invasiva de alta calidad.
>
> — Research Database, entrada 009 (core); Xia, Miller, Park & Tian (2002), *Geophysics* 67(5):1274–1282.

## Referencias

| Fuente | Sección / Página |
|--------|-----------------|
| Foti et al. (2018), *Surface Wave Methods* | §1.1; §7.4 — validación MASW vs ensayos invasivos |
| Xia et al. (2002), *Geophysics* 67(5) | Paper 009 — DHT como referencia para MASW con modos superiores |
| ASTM D7400 | Norma estándar para Downhole Seismic Testing |
| Robertson & Cabal (2015), *CPT Guide* | SCPTU — variante de DHT con ensayo de penetración |
