---
name: Wave
description: Perturbación que se propaga a través de un medio transportando energía sin transporte neto de materia; clasificadas por polarización (P, S, superficiales) y dispersividad
type: reference
---

# Onda (Wave)

> [!CONCEPT] Definición
> Una **onda** es cualquier perturbación reconocible que se transfiere a través de un medio con una velocidad de propagación identificable, transportando energía sin transporte neto de materia. En geofísica near-surface, las ondas elásticas — clasificadas como [[Body Waves]] ([[P-waves]], [[S-Waves]]) y [[Surface Waves]] ([[Rayleigh Waves]], [[Love Waves]]) — son el fundamento de todos los métodos de caracterización del subsuelo con geófonos.
>
> — Foti et al. (2018), §2.1.1, pp. 38–41.

## Intuición física

Cuando se perturba un punto de un medio elástico, la energía se transmite a los vecinos por las fuerzas de elasticidad (proporcionales a la deformación relativa). Estos vecinos, a su vez, perturban a los suyos, y así la perturbación se propaga. Lo que viaja no es materia sino el **patrón de perturbación**: cada partícula del medio oscila alrededor de su posición de reposo mientras la perturbación avanza.

Esta es la distinción fundamental entre onda y flujo de fluido: en una onda, el movimiento neto de material es cero (o despreciable); solo hay transporte de energía.

## Representación matemática de una onda armónica

La solución elemental de la ecuación de onda es la onda plana armónica:

$$\phi(x, t) = A\, e^{i(kx - \omega t)}$$

donde:
- $A$ — amplitud compleja (incluye fase inicial).
- $k = 2\pi/\lambda$ — [[Wavenumber|número de onda]] (rad/m): controla la variación espacial.
- $\omega = 2\pi f$ — [[Angular Frequency|frecuencia angular]] (rad/s): controla la variación temporal.

La función de onda real se toma como la parte real: $\phi = \text{Re}[A\,e^{i(kx-\omega t)}] = |A|\cos(kx - \omega t + \varphi_0)$.

Una señal arbitraria puede representarse como superposición de ondas armónicas mediante la [[Fourier Integral|integral de Fourier]].

## Clasificación de ondas elásticas

### Por tipo de deformación

| Tipo | Deformación | Polarización | Velocidad |
|---|---|---|---|
| [[P-waves\|Onda P]] | Compresional (volumétrica) | Longitudinal (∥ propagación) | $V_P = \sqrt{(\lambda+2\mu)/\rho}$ |
| [[S-Waves\|Onda S]] | Corte (deviatórica) | Transversal (⊥ propagación) | $V_S = \sqrt{\mu/\rho}$ |
| [[Rayleigh Waves\|Onda Rayleigh]] | P + SV acopladas | Elipse retrógrada vertical | $c_R \approx 0.92\,V_S$ |
| [[Love Waves\|Onda Love]] | SH guiada | Horizontal transversal | $V_{S1} < c_L < V_{S2}$ |

### Por confinamiento espacial

- **[[Body Waves|Ondas de cuerpo]]**: se propagan por el interior del medio; decaen como $1/r$ en amplitud.
- **[[Surface Waves|Ondas superficiales]]**: confinadas cerca de una interfaz; decaen exponencialmente en profundidad y como $1/\sqrt{r}$ en la superficie.

### Por dispersividad

- **No dispersivas**: velocidad de fase constante ($\omega = ck$); el paquete de ondas no se deforma. Ejemplo: ondas en semiespacio homogéneo.
- **Dispersivas**: velocidad de fase dependiente de la frecuencia ($c_p = \omega/k$ variable); el paquete se deforma. Ejemplo: ondas de Rayleigh en suelo estratificado. Ver [[Wave Dispersion]].

## Por qué las ondas superficiales dominan los registros sísmicos

Para una fuente puntual en la superficie (ver [[Lamb's Problem]]):
- Las ondas de cuerpo decaen como $1/r$ (frente esférico: energía ∝ $r^2$).
- Las ondas superficiales decaen como $1/\sqrt{r}$ (frente cilíndrico: energía ∝ $r$).

A distancias mayores que unas pocas longitudes de onda, las ondas superficiales dominan el registro. Esta propiedad es la que hace práctico el método MASW: el ground-roll de ondas Rayleigh es la señal predominante en los sismogramas superficiales.

## Instrumentación: qué miden los geófonos

Los geófonos estándar (verticales) miden la **velocidad de partícula** del suelo en la dirección vertical, $\dot{u}_z(x, t)$. Son sensibles a:
- Ondas de Rayleigh (componente vertical de la elipse).
- Ondas P (componente vertical al llegar en incidencia oblicua).
- Ruido sísmico ambiental de origen diverso.

Los geófonos horizontales son necesarios para registrar ondas Love (movimiento transversal horizontal) y la componente horizontal de Rayleigh.

> [!EXAMPLE] Evidencia empírica: Park et al. (1999) — dominancia de Rayleigh en registros MASW
> **Paper 001 (Park, Miller & Xia 1999)** documenta que en registros sísmicos superficiales con fuente activa (martillo), el **ground-roll** de [[Rayleigh Waves]] domina el sismograma a distancias > 5–10 m de la fuente, concentrando > 67% de la energía sísmica total. Esta propiedad — consecuencia directa del decaimiento diferencial $r^{-0.5}$ vs $r^{-2}$ — es la que hace práctico el [[MASW Method]]: la señal útil (Rayleigh) domina sobre el ruido (body waves) sin necesidad de filtrado agresivo.
>
> — Research Database, entrada 001 (core).

## Referencias

| Fuente | Sección / Página |
|--------|-----------------|
| Foti et al. (2018), *Surface Wave Methods* | §2.1.1, pp. 38–41 |
| Foti et al. (2018), *Surface Wave Methods* | §2.1.3, pp. 43–50 |
| Park, Miller & Xia (1999), *Geophysics* 64(3) | Paper 001 |
