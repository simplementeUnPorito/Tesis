---
name: Inversión
description: Proceso de identificación de parámetros del subsuelo (perfil VS) a partir de la [[Dispersion Curve|curva de dispersión]] experimental — problema inverso ill-posed con múltiples estrategias de [[Regularization|regularización]] y búsqueda
type: reference
---

# Inversión de la Curva de Dispersión

> [!CONCEPT] Definición
> La **inversión** es el paso final del flujo de trabajo de ondas superficiales: determina el perfil de velocidad de corte $V_S(z)$ que mejor explica la **[[Dispersion Curve|curva de dispersión]] experimental** $c_R(f)$ medida en campo. Se formula como un problema de identificación de parámetros: dado el modelo $\mathbf{m} = \{V_{S,i}, V_{P,i}, \rho_i, h_i\}$ de capas planas, minimizar el desajuste $E(\mathbf{m}) = \|c_R^{\text{obs}}(f) - c_R^{\text{teórica}}(\mathbf{m}, f)\|$. El problema es **ill-posed** (Hadamard 1923): viola unicidad y estabilidad → requiere [[Non-uniqueness|información a priori]] y [[Tikhonov Regularization|regularización]]. Los enfoques van de métodos locales (gradiente, mínimos cuadrados) a globales ([[Monte Carlo Methods|Monte Carlo]], algoritmos genéticos). El producto es el perfil $V_S(z)$ para calcular $[[Vs30|Vs,30]]$ y la clasificación sísmica del sitio.
>
> — Foti et al. (2018), Cap. 6, pp. 277–340; Xia et al. (1999), Paper 002.

## [[Forward Problem|problema directo]] e inverso

- **[[Forward Problem|problema directo]]**: dado un perfil del subsuelo $\mathbf{m}$, calcular la [[Dispersion Curve|curva de dispersión]] teórica $c_R(f, \mathbf{m})$. Se resuelve con el método de la [[Rayleigh Eigenproblem|matriz de transferencia de Thomson-Haskell]]: propaga condiciones de frontera a través de capas planas horizontales. Determinístico y eficiente.

- **Problema inverso**: dado $c_R^{\text{obs}}(f)$, encontrar $\mathbf{m}$ tal que $c_R(f, \mathbf{m}) \approx c_R^{\text{obs}}(f)$. No tiene solución analítica cerrada — se resuelve iterativamente.

## El proceso matemático

La inversión minimiza la función de desajuste:

$$E(\mathbf{m}) = \sum_{i} \left[\frac{c_R^{\text{obs}}(f_i) - c_R^{\text{teórica}}(\mathbf{m}, f_i)}{\sigma_i}\right]^2$$

donde $\sigma_i$ es la incertidumbre experimental en la frecuencia $f_i$.

**Modelo inicial**: se parte de un perfil $\mathbf{m}_0$ basado en conocimiento geológico, datos de borehole o una estimación simple (e.g., [[Phase Velocity|velocidad de fase]] a cada frecuencia ÷ 1.1 como estimación de $V_S$ a profundidad $\lambda/3$).

## Estrategias de búsqueda

### Métodos locales (Local Search Methods, LSM)

Parten de un modelo inicial y buscan el mínimo en su vecindad mediante el gradiente de la función de desajuste.

- **Mínimos cuadrados linealizados** (e.g., SVD): linealiza $c_R(\mathbf{m})$ alrededor de $\mathbf{m}_0$ y resuelve el sistema linearizado.
- **Levenberg-Marquardt**: combina descenso de gradiente y método de Gauss-Newton; robusto cerca del mínimo.
- **Ventaja**: convergencia rápida si el modelo inicial es bueno.
- **Limitación**: puede quedar atrapado en mínimos locales.

### Métodos globales (Global Search Methods, GSM)

Exploran el espacio completo de parámetros sin depender del modelo inicial.

- **[[Monte Carlo Methods|Monte Carlo]]**: genera aleatoriamente modelos en el espacio de parámetros y evalúa $E(\mathbf{m})$ para cada uno. Permite mapear el conjunto completo de soluciones equivalentes.
- **Algoritmos genéticos**: evolución iterativa de una población de modelos; operadores de cruce y mutación.
- **Simulated annealing**: acepta soluciones peores con probabilidad decreciente — escapa de mínimos locales.
- **Ventaja**: robusto ante [[Non-uniqueness|no-unicidad]]; caracteriza el ensemble de soluciones.
- **Limitación**: costo computacional alto (10³–10⁶ evaluaciones del [[Forward Problem|problema directo]]).

## Ill-posedness y [[Regularization|regularización]]

El problema inverso viola las condiciones de Hadamard en unicidad y estabilidad. Las estrategias de mitigación son:

1. **Información a priori**: datos de borehole, SPT/CPT, posición del nivel freático → restringe el espacio de modelos admisibles.
2. **[[Tikhonov Regularization|Regularización de Tikhonov]]**: añade término de penalización $\lambda \|\mathbf{L}\mathbf{m}\|^2$ a la función de error, donde $\mathbf{L}$ controla la suavidad del perfil (orden 0: amplitud, orden 1: gradiente, orden 2: curvatura). El **algoritmo de Occam** busca el modelo más suave compatible con los datos.
3. **Parámetros fijos**: $V_P$ y $\rho$ suelen fijarse desde refracción sísmica o tablas de litología — reducen el espacio de parámetros libres.

## Sensibilidad diferencial

La [[Dispersion Curve|curva de dispersión]] de Rayleigh es:
- **Muy sensible a $V_S$**: cambios de 10% en $V_S$ producen cambios de 5–8% en $c_R$ → inversión confiable de $V_S$.
- **Poco sensible a $V_P$**: cambios de 50% en $V_P$ producen cambios <2% en $c_R$ → $V_P$ debe fijarse a priori.
- **Muy poco sensible a $\rho$**: generalmente se toma de tablas → no se invierte.

> [!EXAMPLE] Evidencia empírica: Xia et al. (1999) — sensibilidad de la [[Dispersion Curve|curva de dispersión]] y algoritmo de inversión
> **Paper 002 (Xia et al. 1999)** realiza el análisis de sensibilidad completo de la [[Dispersion Curve|curva de dispersión]] de Rayleigh respecto a $V_S$, $V_P$ y $\rho$ para perfiles de suelo típicos. Los kernels de sensibilidad muestran que $V_S$ domina la respuesta en todo el rango de frecuencias (sensibilidad relativa 80–95%), mientras $V_P$ contribuye menos del 10% y $\rho$ es despreciable. El paper propone un algoritmo de inversión por mínimos cuadrados con estabilización SVD que converge en <10 iteraciones desde modelos iniciales razonables. Aplicado a datos de campo en Kansas, el perfil $V_S(z)$ resultante concuerda con datos de borehole con error RMS < 15% — estableciendo el benchmark de precisión del [[MASW Method|MASW]].
>
> — Research Database, entrada 002 (core); Xia et al. (1999), *Geophysics* 64(3), pp. 691–700.

## Referencias

| Fuente | Sección / Página |
|--------|-----------------|
| Foti et al. (2018), *Surface Wave Methods* | Cap. 6, pp. 277–340 — inversión completa |
| Xia et al. (1999), *Geophysics* 64(3) | Paper 002 — sensibilidad + algoritmo LSM |
| Hadamard, J. (1923), *Lectures on Cauchy's Problem* | Criterios de bien-posedness |
