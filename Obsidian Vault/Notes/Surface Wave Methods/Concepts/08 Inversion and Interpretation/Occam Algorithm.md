---
name: Occam Algorithm
description: Algoritmo de inversión que minimiza la complejidad del modelo (máxima suavidad) bajo la restricción de ajustar los datos — versión geofísica del principio de Occam's Razor
type: reference
---

# Occam Algorithm — Algoritmo de Occam (Inversión de Suavidad Máxima)

> [!CONCEPT] Definición
> El **Algoritmo de Occam** (*Occam's Inversion*) es un método de [[Inversión|inversión geofísica]] que busca el **modelo más simple** (más suave) que ajusta los datos observados con un nivel de ajuste predefinido (chi-cuadrado objetivo). Propuesto por Constable, Parker & Constable (1987) para inversión de datos de sondeo electromagnético, se formaliza como la minimización de la rugosidad del modelo sujeta a ajuste de datos:
> $$\min_{\mathbf{m}} \|\mathbf{R}\mathbf{m}\|^2 \quad \text{s.t.} \quad \|\mathbf{W}(\mathbf{d} - F(\mathbf{m}))\|^2 = \chi^2_{objetivo}$$
> donde $\mathbf{R}$ es el operador de rugosidad (primer o segundo orden de diferencias), $\mathbf{W}$ es la matriz de pesos de los datos (inversas de los errores), y $\chi^2_{objetivo} = N_{datos}$ (ajuste estadístico óptimo). En la práctica, esto se implementa como [[Tikhonov Regularization|regularización de Tikhonov]] de primer o segundo orden con búsqueda del parámetro de regularización $\lambda$ que produce $\chi^2 \approx \chi^2_{objetivo}$. Para [[MASW Method|MASW]], el "modelo simple" es un perfil $V_S(z)$ sin cambios bruscos de velocidad — la mínima estructura compatible con la [[Dispersion Curve|curva de dispersión]] observada. **Ventaja**: evita sobreajuste y produce el perfil de mínima información necesaria. **Limitación**: puede suavizar interfaces reales (la capa blanda bajo capa dura puede aparecer diluida en el perfil).
>
> — Constable, Parker & Constable (1987), *Geophysics*; Foti et al. (2018), §6.4.2; Maraschini & Foti (2010).

## Formulación matemática

### Función objetivo de Occam

$$\Phi(\mathbf{m}) = \|\mathbf{W}\mathbf{d} - \mathbf{W}F(\mathbf{m})\|^2 + \lambda \|\mathbf{R}\mathbf{m}\|^2$$

El operador de rugosidad de primer orden para un perfil discreto de $M$ capas:

$$\mathbf{R}_1 = \begin{pmatrix} -1 & 1 & 0 & \cdots \\ 0 & -1 & 1 & \cdots \\ \vdots & & \ddots & \end{pmatrix} \in \mathbb{R}^{(M-1)\times M}$$

### Búsqueda del parámetro $\lambda$

El algoritmo de Occam no fija $\lambda$ a priori sino que lo busca iterativamente:
1. Comenzar con $\lambda$ grande (modelo muy suave)
2. Invertir → obtener $\chi^2(\lambda)$
3. Si $\chi^2 > \chi^2_{obj}$: reducir $\lambda$ (permitir más estructura)
4. Si $\chi^2 < \chi^2_{obj}$: aumentar $\lambda$ (simplificar modelo)
5. Repetir hasta $\chi^2 \approx \chi^2_{obj}$

El proceso converge en ~5–20 iteraciones; cada iteración resuelve un sistema lineal.

## Diferencias con Tikhonov estándar

| Aspecto | [[Tikhonov Regularization|Tikhonov]] clásico | Occam |
|---------|------|-------|
| $\lambda$ | Fijo a priori | Buscado para $\chi^2 = \chi^2_{obj}$ |
| Criterio de parada | Número de iteraciones | $\chi^2$ objetivo |
| Selección de modelo | Única solución | Más simple con $\chi^2$ dado |
| Principio | Regularización | Parsimonia (Occam's Razor) |

## Aplicación en inversión de [[Dispersion Curve|curvas de dispersión]]

En [[MASW Method|MASW]], el Algoritmo de Occam produce el perfil $V_S(z)$ de **mínima variación vertical** que reproduce la [[Dispersion Curve|curva de dispersión]] experimental dentro de la incertidumbre de los datos. El resultado es interpretado como el modelo "más conservador" — sin capas adicionales que no estén justificadas por los datos.

> [!EXAMPLE] Evidencia empírica: Maraschini & Foti (2010) — Occam como benchmark de inversión determinista
> **Paper 034 (Maraschini & Foti 2010)** utiliza la inversión por Occam (regularización de suavidad máxima) como punto de comparación para el método de inversión basado en el determinante del secular equation. En el sitio de prueba de Torino (perfiles $V_S$ de 100–600 m/s en 30 m), el perfil obtenido por Occam reproduce la [[Dispersion Curve|curva de dispersión]] con $\chi^2 \approx N_{datos}$ (ajuste estadístico óptimo) pero produce un perfil significativamente más suave que el perfil de referencia del [[Cross-Hole Test]]. Las diferencias se concentran en las interfaces abruptas (capas de VS alta sobre VS baja): el perfil de Occam las suaviza en zonas de transición de ~3–5 m, mientras que el método determinante las resuelve con mayor precisión. Los autores concluyen que el Occam es un método de referencia robusto para la inversión determinista de [[MASW Method|MASW]], pero que la [[Non-uniqueness|no-unicidad]] residual requiere métodos estocásticos o el enfoque determinante para obtener interfaces definidas.
>
> — Research Database, entrada 034 (core); Maraschini & Foti (2010), *Geophysics* 75(3):B75–B83.

## Referencias

| Fuente | Sección / Página |
|--------|-----------------|
| Foti et al. (2018), *Surface Wave Methods* | §6.4.2 — métodos de inversión determinista |
| Maraschini & Foti (2010), *Geophysics* | Paper 034 — comparación Occam vs determinante |
| Constable, Parker & Constable (1987), *Geophysics* | Formulación original del Algoritmo de Occam |
