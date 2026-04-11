---
name: Geometric Spreading
description: Decaimiento de amplitud de ondas sísmicas con la distancia por expansión geométrica del frente de onda — distinto de la atenuación material; crítico para estimar el coeficiente de amortiguamiento DS en [[MASW Method|MASW]]
type: reference
---

# Geometric Spreading — Extensión Geométrica

> [!CONCEPT] Definición
> La **extensión geométrica** (o *geometric spreading*) es el decaimiento de amplitud de una onda sísmica con la distancia a la fuente causado por la **expansión del frente de onda** en el espacio, sin disipación de energía. Para ondas de superficie en 2D (propagación a lo largo de una línea de geófonos), la amplitud decae como $A(r) \propto 1/\sqrt{r}$ (cilíndrico 2D). Para ondas de cuerpo en 3D, decae como $A(r) \propto 1/r$ (esférico). En el análisis de amplitudes para estimar el [[Shear Damping Ratio|coeficiente de amortiguamiento]] $D_s$ desde la [[Dispersion Curve|curva de atenuación]] $\alpha_R(f)$, es **imprescindible separar** la extensión geométrica de la **atenuación material** $e^{-\alpha_R r}$: $A(r, f) \propto \frac{1}{\sqrt{r}} \cdot e^{-\alpha_R(f) r}$. Un error en la corrección de extensión geométrica produce un sesgo sistemático en la estimación de $D_s$.
>
> — Foti et al. (2018), Cap. 5, §5.2, pp. 234–245; Cap. 2, §2.3.

## Tipos de extensión geométrica

### 2D: ondas de superficie (Rayleigh, Love)

Para una fuente puntual en superficie y receptor a distancia $r$ en la dirección de propagación, la energía se distribuye a lo largo de un frente de onda cilíndrico de circunferencia $2\pi r$. La amplitud decae como:

$$A(r) \propto \frac{1}{\sqrt{r}}$$

Este es el comportamiento de **ondas de superficie en campo lejano** ([[Rayleigh Waves]], [[Love Waves]]) — la base de la corrección en [[MASW Method|MASW]] para estimar $D_s$.

### 3D: ondas de cuerpo (P y S)

Para ondas de cuerpo que se propagan esféricamente:

$$A(r) \propto \frac{1}{r}$$

El decaimiento más rápido con la distancia hace que las ondas de cuerpo (P, S) sean relativamente menos importantes en registros de campo lejano — confirmando que el [[Ground Roll|ground-roll]] (ondas de Rayleigh) domina a grandes offsets.

## Implicación para la estimación de DS

En un sismograma [[MASW Method|MASW]], la amplitud observada en el receptor $j$ a distancia $r_j$ de la fuente combina:

$$A(r_j, f) = \frac{S(f)}{\sqrt{r_j}} \cdot e^{-\alpha_R(f) r_j} \cdot G(r_j, f)$$

donde:
- $S(f)$ = espectro de la fuente
- $1/\sqrt{r_j}$ = extensión geométrica (ondas de superficie 2D)
- $e^{-\alpha_R r_j}$ = atenuación material (a extraer)
- $G(r_j, f)$ = factor de acoplamiento geófono-suelo (idealmente = 1)

La regresión de amplitud versus distancia — tras corregir la extensión geométrica y normalizar por el espectro de fuente — da directamente $\alpha_R(f)$ y, por tanto, $D_s \approx \alpha_R V_R / (2\pi f)$.

## Relevancia para el diseño experimental

- Los geófonos lejanos (grandes $r_j$) tienen señal débil por extensión geométrica — necesitan mayor SNR o mayor número de apilados.
- La corrección $\sqrt{r_j}$ debe aplicarse **antes** de cualquier análisis de amplitudes.
- El campo cercano ([[Near-field Effect]]) viola la ley $1/\sqrt{r}$ — la corrección solo es válida para $r \geq$ offset mínimo.
- Fuentes asintótricas (e.g., vibroseis en configuración no-point) pueden tener factor de spreading diferente de $1/\sqrt{r}$.

> [!EXAMPLE] Evidencia empírica: Foti et al. (2018) — corrección de spreading en estimación de DS en Pisa
> Foti et al. (2018, §5.2) demuestran que en el sitio de la Torre de Pisa (arcilla suave), el decaimiento de amplitud de las ondas de Rayleigh sigue la ley $1/\sqrt{r}$ en el rango de offsets 5–40 m, con desviaciones < 5% del modelo teórico. Esto confirma que la extensión geométrica 2D es el componente dominante del decaimiento de amplitud a largo offset, y que la atenuación material $e^{-\alpha_R r}$ con $\alpha_R \sim 0.05$–$0.15$ m$^{-1}$ es un efecto de segundo orden visible solo después de corregir $1/\sqrt{r}$. La corrección precisa de geometric spreading es la condición necesaria para estimar $D_s$ con incertidumbre < 1% (absoluto) desde la curva de atenuación.
>
> — Foti et al. (2018), §5.2, pp. 234–245; §7.3.

## Referencias

| Fuente | Sección / Página |
|--------|-----------------|
| Foti et al. (2018), *Surface Wave Methods* | Cap. 5, §5.2, pp. 234–245 — corrección de spreading |
| Foti et al. (2018), *Surface Wave Methods* | Cap. 2, §2.3 — fundamentos de propagación energética |
