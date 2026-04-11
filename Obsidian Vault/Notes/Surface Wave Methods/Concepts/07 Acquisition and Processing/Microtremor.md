---
name: Microtremor
description: Vibración sísmica ambiental de baja amplitud usada como fuente pasiva en [[MASW Method|MASW]], SPAC, ReMi y HVSR — generada por actividad humana, oceánica y atmosférica
type: reference
---

# Microtremor — Ruido Sísmico Ambiental

> [!CONCEPT] Definición
> Los **microtremores** (o *ambient seismic noise*) son las vibraciones sísmicas de baja amplitud ($10^{-9}$–$10^{-6}$ m) presentes continuamente en la corteza terrestre, generadas por fuentes naturales y antropogénicas. Son la fuente de los métodos sísmicos pasivos: [[ReMi Method|ReMi]], [[SPAC Method|SPAC]], [[Seismic Interferometry|interferometría sísmica]] y [[HVSR]]. Están dominados por **ondas superficiales** ([[Rayleigh Waves|Rayleigh]] y [[Love Waves|Love]]) en el rango de frecuencias de ingeniería (0.1–100 Hz). Su principal ventaja como fuente es que aportan energía en **bajas frecuencias** (0.1–5 Hz) que fuentes activas (sledgehammer) no pueden generar — permitiendo investigar profundidades >50 m. Su limitación es que su distribución espacial puede ser anisotrópica, lo que sesga los métodos que asumen isotropía (ReMi, SPAC convencional).
>
> — Foti et al. (2018), Cap. 3, §3.4.3; Cap. 8 — métodos pasivos; Peterson (1993) NLNM/NHNM.

## Origen y características espectrales

Los microtremores tienen tres rangos de origen distintos:

| Rango de período | Nombre | Fuente dominante |
|---|---|---|
| 0.01–0.1 s (10–100 Hz) | Ruido de alta frecuencia | Tráfico, maquinaria, actividad humana |
| 1–10 s | *Período primario oceánico* | Ondas oceánicas directas → energía sísmica |
| 5–20 s | *Período secundario oceánico* | Interacción de ondas oceánicas opuestas |

Para ingeniería geotécnica ([[MASW Method|MASW]] pasivo, VS30), el rango relevante es 1–20 Hz (profundidades 10–100 m), dominado por tráfico y actividad industrial en zonas urbanas.

## Composición del campo de ondas

En el rango de frecuencias de ingeniería (1–100 Hz):
- ~70% de la energía corresponde a [[Rayleigh Waves|ondas de Rayleigh]] (modo fundamental)
- ~20% a [[Love Waves|ondas de Love]] (modo fundamental)
- ~10% a ondas de cuerpo (P, S) directas y refractadas

Esta dominancia de ondas superficiales es lo que hace posible los métodos de ondas superficiales pasivos.

## Hipótesis de campo difuso

La mayoría de los métodos pasivos asumen que el campo de microtremores es **estadísticamente estacionario, ergódico e isotrópico** en el plano horizontal — el *campo difuso*. Bajo esta hipótesis:
- SPAC: la autocorrelación espacial es $J_0(k_0 r)$
- Interferometría: la cross-correlación converge a la función de Green
- ReMi: el mínimo de velocidad en el panel tau-p corresponde a $c_R(f)$

Si el campo de microtremores tiene una dirección preferencial (fuente dominante), estas hipótesis se violan y los resultados pueden ser sesgados.

## Adquisición de microtremores

- **Duración mínima**: 10–30 minutos para $f_0 > 1$ Hz; hasta 1 hora para $f_0 < 1$ Hz (SESAME 2004)
- **Sensores**: sismómetros de banda ancha (0.008–50 Hz) o geófonos de baja frecuencia (4.5 Hz o menos) para capturar el rango de bajas frecuencias
- **Horario**: preferiblemente de noche (menor ruido cultural, campo más isotrópico)
- **Selección de ventanas**: descartar transitorios (pasos de camión, impactos) que violan la estacionariedad

> [!EXAMPLE] Evidencia empírica: Garofalo et al. (2016) — microtremores como fuente pasiva en InterPACIFIC
> **Papers 006+007 (Garofalo et al. 2016a/b)** usan registros de microtremores de 30–60 minutos en los 3 sitios InterPACIFIC para extraer [[Dispersion Curve|curvas de dispersión]] mediante [[SPAC Method|SPAC]], [[ReMi Method|ReMi]] e [[Seismic Interferometry|interferometría]]. Los microtremores en los sitios europeos (Grenoble, Mirandola, Cadarache) tienen características diferentes: en Grenoble (zona montañosa) el campo es fuertemente anisotrópico (fuentes oceánicas y de tráfico en dirección N-S), mientras en Mirandola (llanura Padana) el campo es más isotrópico. Esta diferencia explica el mejor desempeño de los métodos pasivos en Mirandola vs Grenoble. El estudio demuestra que la caracterización del campo de microtremores (mediante beamforming 2D) es un paso previo esencial antes de elegir el método de extracción de la [[Dispersion Curve|curva de dispersión]].
>
> — Research Database, entradas 006, 007 (core); Garofalo et al. (2016a/b).

## Referencias

| Fuente | Sección / Página |
|--------|-----------------|
| Foti et al. (2018), *Surface Wave Methods* | Cap. 3, §3.4.3; Cap. 8 — métodos pasivos |
| Peterson (1993), *USGS OFR 93-322* | Modelos NLNM/NHNM de ruido sísmico de referencia |
| SESAME Project (2004) | Guías de adquisición de microtremores para HVSR |
| Garofalo et al. (2016a/b) | Papers 006, 007 — microtremores en InterPACIFIC |
