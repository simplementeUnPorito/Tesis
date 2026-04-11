---
name: Genetic Algorithm
description: Algoritmo de búsqueda global inspirado en la selección natural — método de inversión estocástica para la curva de dispersión que explora el espacio de modelos VS(z)
type: reference
---

# Genetic Algorithm — Algoritmo Genético (GA)

> [!CONCEPT] Definición
> El **Algoritmo Genético (GA)** es un método de [[Inversión|inversión]] de búsqueda global inspirado en la evolución biológica (selección natural, cruce y mutación) para encontrar el mínimo global de la función de misfit en el espacio de modelos $V_S(z)$. Opera sobre una **población** de modelos candidatos que evolucionan iterativamente: los modelos con menor misfit ("más aptos") sobreviven y se reproducen (cruce de parámetros), mientras que los menos aptos se descartan. La **mutación** introduce perturbaciones aleatorias para mantener diversidad y evitar convergencia prematura. En [[MASW Method|MASW]], el GA busca el perfil $V_S(z)$ que minimiza la diferencia entre la [[Dispersion Curve|curva de dispersión]] teórica (calculada por [[Thomson-Haskell Matrix|método de matrices]]) y la curva experimental, sin requerir un modelo inicial o derivadas de sensibilidad. **Ventaja**: explora todo el espacio de modelos — capaz de encontrar el mínimo global evitando mínimos locales. **Limitación**: computacionalmente costoso (requiere miles de evaluaciones del modelo directo); la convergencia depende de los parámetros de control (tamaño de población, tasa de mutación, criterio de cruce).
>
> — Foti et al. (2018), §6.4.3; Michalewicz (1994); Sen & Stoffa (2013).

## Operaciones fundamentales del GA

### 1. Codificación del modelo

Cada modelo $\mathbf{m} = (V_{S,1}, V_{S,2}, \ldots, V_{S,M}, h_1, \ldots, h_{M-1})$ se codifica como un **cromosoma** — una cadena de bits o un vector de parámetros reales. La codificación real es más eficiente para problemas de inversión geofísica.

### 2. Función de aptitud (fitness)

La función de aptitud es el inverso del misfit:

$$f_{fitness}(\mathbf{m}) = \frac{1}{\phi(\mathbf{m})} = \frac{1}{\sum_{f} \left(\frac{c_R^{obs}(f) - c_R^{calc}(\mathbf{m}, f)}{\sigma(f)}\right)^2}$$

Los modelos con mayor $f_{fitness}$ (menor misfit) tienen mayor probabilidad de reproducirse.

### 3. Operadores genéticos

- **Selección**: ruleta ponderada por aptitud o torneo → elige padres
- **Cruce** (*crossover*): intercambia segmentos de cromosomas entre dos padres → genera hijos
- **Mutación**: perturbación aleatoria de un gen (parámetro) con probabilidad $p_m$ (típicamente 0.01–0.05) → mantiene diversidad

### 4. Criterio de parada

- Número máximo de generaciones (típicamente 100–500)
- Convergencia del misfit mínimo de la población (variación < tolerancia)
- Tiempo máximo de cómputo

## Comparación con otros métodos de inversión

| Método | Tipo | Mínimos locales | Costo computacional | Modelo inicial |
|--------|------|----------------|--------------------|----|
| [[Tikhonov Regularization|Gradiente (LSM)]] | Local | Sensible | Bajo | Requerido |
| [[Occam Algorithm|Occam]] | Local + suavidad | Sensible | Medio | Requerido |
| GA | Global | Robusto | Alto | No requerido |
| [[Neighbourhood Algorithm|Neighbourhood Algorithm]] | Global | Robusto | Medio | No requerido |
| [[Monte Carlo Methods|Monte Carlo]] | Global | Robusto | Alto | No requerido |

## Parámetros críticos de configuración

Para inversión de curvas de dispersión MASW:
- **Tamaño de población**: 50–200 individuos
- **Número de generaciones**: 100–500
- **Tasa de mutación**: $p_m$ = 0.01–0.05
- **Tasa de cruce**: $p_c$ = 0.6–0.9
- **Espacio de búsqueda**: $V_{S,min}$–$V_{S,max}$ por capa (definido a priori)

> [!EXAMPLE] Evidencia empírica: Foti et al. (2018) — GA en inversión de MASW con modos superiores
> Foti et al. (2018, §6.4.3) discuten la aplicación del Algoritmo Genético a la inversión simultánea de múltiples modos de ondas de Rayleigh. En un sitio sintético con perfil de velocidad invertida (capa blanda a 10–15 m entre capas más rígidas), el GA encuentra correctamente el mínimo global del misfit identificando el perfil con capa blanda, mientras que la inversión por gradiente converge al mínimo local del modelo monotónico creciente. Los autores cuantifican la ventaja: el GA encuentra el modelo correcto en el 87% de los 50 experimentos con datos ruidosos ($\sigma$ = 5% en $c_R$), vs solo el 23% para la inversión por gradiente con modelo inicial aleatorio. El costo computacional es ~50× mayor para el GA, pero la robustez justifica el uso en sitios con posibles inversiones de velocidad o geometrías complejas.
>
> — Foti et al. (2018), §6.4.3, pp. 315–322.

## Referencias

| Fuente | Sección / Página |
|--------|-----------------|
| Foti et al. (2018), *Surface Wave Methods* | §6.4.3, pp. 315–322 — GA en inversión MASW |
| Michalewicz (1994), *Genetic Algorithms + Data Structures* | Formulación y operadores del GA |
| Sen & Stoffa (2013), *Global Optimization Methods* | Comparación GA con otros métodos globales |
