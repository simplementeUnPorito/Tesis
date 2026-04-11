---
name: Cross-Hole Test
description: Ensayo invasivo entre pozos que mide VS y VP directamente por propagación entre perforaciones — referencia de validación in situ para métodos de ondas superficiales
type: reference
---

# Cross-Hole Test (CHT) — Ensayo Entre Pozos

> [!CONCEPT] Definición
> El **Cross-Hole Test (CHT)** es un ensayo sísmico invasivo que mide la **velocidad de onda de corte** $V_S$ y de onda de compresión $V_P$ directamente entre dos o más perforaciones. Una fuente sísmica en un pozo genera ondas que viajan horizontalmente hasta receptores ubicados a la misma profundidad en un pozo adyacente. Como el camino de propagación es conocido (la distancia entre pozos $d$) y el tiempo de viaje $t$ se registra, la velocidad se calcula directamente: $V_S = d/t$. El CHT mide $V_S$ a cada profundidad de forma directa y no-invasiva en términos de interpretación — no requiere inversión de ningún tipo. Es el estándar de referencia para la validación de los perfiles $V_S(z)$ obtenidos por [[MASW Method|MASW]] y otros métodos de ondas superficiales. **Limitaciones**: requiere perforación de al menos dos pozos (costo elevado, perturbación del terreno), mide solo en la línea entre pozos (representatividad limitada), y las condiciones de acoplamiento fuente-receptor afectan la calidad.
>
> — Foti et al. (2018), §1.1; ASTM D4428; ISO 22476-11.

## Principio de funcionamiento

### Geometría estándar

1. Se perforan dos o más pozos separados una distancia $d$ = 3–6 m (típicamente $d$ = 3 m para el estándar ASTM D4428)
2. La fuente en el pozo S genera ondas impulsivas (martillo automático, explosivo, spark-gap)
3. Los receptores (geófonos tri-axiales) en el pozo R registran la onda directa

### Tipos de onda medidos

| Onda | Fuente | Receptor | Velocidad obtenida |
|------|--------|----------|--------------------|
| Compresión (P) | Pistón axial | Hidrófonos / geófonos axiales | $V_P$ |
| Corte (SH) | Martillo lateral (horizontal) | Geófonos horizontales | $V_S$ (SH) |
| Corte (SV) | Martillo axial | Geófonos verticales | $V_S$ (SV) |

### Corrección de inclinación

En pozos inclinados o desviados, el camino de propagación real difiere de $d$. La ASTM D4428 exige medir la posición exacta de cada pozo con inclinómetro y corregir el tiempo de viaje con la distancia verdadera.

## Perfil VS(z) — medición directa

El CHT produce el perfil $V_S(z)$ con resolución vertical igual al intervalo de muestreo (típicamente 0.5–1 m). No requiere inversión:

$$V_S(z_i) = \frac{d(z_i)}{t_S(z_i) - t_0}$$

donde $t_0$ es el tiempo de disparo y $t_S$ el tiempo de llegada de la onda S a la profundidad $z_i$.

## Comparación con métodos de ondas superficiales

| Aspecto | Cross-Hole Test | [[MASW Method|MASW]] |
|---------|----------------|------|
| Invasividad | Alta (≥2 pozos) | No invasivo |
| Costo | Alto (perforación) | Bajo |
| Interpretación | Directa (sin inversión) | Requiere inversión |
| Resolución vertical | Alta (0.5–1 m) | Moderada (λ/3–λ/2) |
| Profundidad máxima | Depende del pozo | ~30–50 m (activo) |
| Sensibilidad a inversiones de velocidad | Directa | Moderada |
| Representatividad lateral | Puntual | Promedio lateral |

## Rol en la validación de MASW

El CHT es la referencia preferida para calibrar y validar perfiles $V_S(z)$ de MASW porque:
1. No requiere suposiciones de modelo (directamente medido)
2. Tiene resolución vertical superior
3. Mide in situ con el estado de esfuerzos real del suelo

El protocolo estándar de validación: realizar CHT y MASW en el mismo sitio → comparar perfiles $V_S(z)$ → diferencias < 15% se consideran aceptables para MASW (Foti et al. 2018).

> [!EXAMPLE] Evidencia empírica: Garofalo et al. (2016) — CHT como referencia en InterPACIFIC
> **Papers 006+007 (Garofalo et al. 2016a/b)** usan el Cross-Hole Test como una de las referencias de laboratorio e in situ en los tres sitios del estudio InterPACIFIC (Grenoble, Cadarache y Mirandola). En Mirandola (sitio de alta variabilidad estratigráfica), el perfil $V_S(z)$ del CHT muestra variaciones rápidas de velocidad (120 → 400 m/s en los primeros 20 m) que coinciden con los depósitos aluviales post-seísmo del 2012. Las 30 estimaciones de $V_S(z)$ obtenidas por los equipos participantes con MASW y arrays pasivos reproducen la estructura general del CHT dentro de ±15%, aunque las capas de alta variabilidad (3–8 m de profundidad) muestran dispersión de hasta ±25% entre equipos. El $V_{S,30}$ del CHT (198 m/s) es reproducido por MASW dentro de ±10% en la mayoría de los equipos. Los autores concluyen que la variabilidad entre operadores MASW domina sobre el error intrínseco del método — el CHT sirve como anclaje cuantitativo de la verdad de campo.
>
> — Research Database, entradas 006, 007 (core); Garofalo et al. (2016a), *Near Surface Geophysics*; Garofalo et al. (2016b), *Near Surface Geophysics*.

## Referencias

| Fuente | Sección / Página |
|--------|-----------------|
| Foti et al. (2018), *Surface Wave Methods* | §1.1 — métodos de referencia para VS |
| Garofalo et al. (2016a/b) | Papers 006, 007 — CHT como referencia en InterPACIFIC |
| ASTM D4428 | Norma estándar para Cross-Hole Seismic Testing |
| ISO 22476-11 | Estándar internacional para ensayos sísmicos entre pozos |
