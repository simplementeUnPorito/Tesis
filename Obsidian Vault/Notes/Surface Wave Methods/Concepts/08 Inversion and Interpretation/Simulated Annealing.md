---
name: Simulated Annealing
description: Algoritmo de búsqueda global inspirado en el enfriamiento del metal — acepta soluciones peores con probabilidad decreciente (temperatura), evitando mínimos locales en inversión VS(z)
type: reference
---

# Simulated Annealing — Recocido Simulado (SA)

> [!CONCEPT] Definición
> El **Simulated Annealing (SA)** o *Recocido Simulado* es un algoritmo de optimización global metaheurístico inspirado en el proceso de enfriamiento lento de un metal fundido: a alta temperatura, los átomos tienen alta energía y pueden escapar de configuraciones subóptimas; al bajar la temperatura gradualmente, el sistema converge al estado de mínima energía (mínimo global). En [[Inversión|inversión]] geofísica, el SA explora el espacio de modelos $V_S(z)$ aceptando perturbaciones del modelo con probabilidad:
> $$P(\Delta\phi) = \exp\left(-\frac{\Delta\phi}{T_k}\right) \quad \text{si } \Delta\phi > 0$$
> donde $\Delta\phi = \phi(\mathbf{m}_{nuevo}) - \phi(\mathbf{m}_{actual}) > 0$ es el incremento de misfit y $T_k$ es la **temperatura** en la iteración $k$. Si $\Delta\phi < 0$ (el nuevo modelo es mejor), se acepta siempre. Al inicio ($T_k$ alta), se aceptan muchas soluciones peores — permitiendo escapar de mínimos locales; al final ($T_k$ baja), el algoritmo es casi un gradiente descendente — convergiendo al mínimo encontrado. La **ley de enfriamiento** (schedule) determina cómo $T_k$ decrece con las iteraciones: exponencial ($T_k = T_0 \cdot \alpha^k$, $\alpha$ = 0.95–0.99) o logarítmica ($T_k = T_0/\ln(1+k)$). En [[MASW Method|MASW]], el SA es una alternativa al [[Genetic Algorithm|Algoritmo Genético]] para búsqueda global en inversión de [[Dispersion Curve|curvas de dispersión]].
>
> — Kirkpatrick, Gelatt & Vecchi (1983), *Science*; Foti et al. (2018), §6.4.3; Sen & Stoffa (2013).

## Algoritmo básico

```
T_k = T_0  (temperatura inicial alta)
m = m_inicial  (modelo inicial aleatorio)
Para k = 1, ..., N_iteraciones:
    m_propuesto = perturbar(m)
    Δφ = φ(m_propuesto) - φ(m)
    Si Δφ < 0: m = m_propuesto  (aceptar siempre)
    Si Δφ ≥ 0: m = m_propuesto con P = exp(-Δφ/T_k)
    T_{k+1} = α · T_k  (enfriar)
```

## Comparación con otros métodos de búsqueda global

| Método | Escape de mínimos locales | Parámetros de control | Eficiencia |
|--------|--------------------------|----------------------|------------|
| [[Genetic Algorithm|GA]] | Alto (selección + mutación) | Muchos ($p_m$, $p_c$, población) | Media |
| SA | Alto (temperatura) | Pocos ($T_0$, $\alpha$, schedule) | Media |
| [[Neighbourhood Algorithm|NA]] | Alto (Voronoi adaptativo) | Muy pocos ($n_s$, $n_r$) | Alta |
| [[Monte Carlo Methods|Monte Carlo]] | Bajo (aleatorio ciego) | Ninguno | Baja |

## Aplicación a inversión de [[MASW Method|MASW]]

Para inversión de [[Dispersion Curve|curvas de dispersión]], el SA típicamente:
- **Parámetros por modelo**: $V_{S,1}, \ldots, V_{S,M}, h_1, \ldots, h_{M-1}$ (M capas)
- **Perturbación**: cambio aleatorio de un parámetro en cada paso (±10–30% del valor actual)
- **Misfit**: diferencia entre $c_R^{obs}(f_i)$ y $c_R^{calc}(\mathbf{m}, f_i)$
- **Temperatura inicial** $T_0$: calibrada para aceptar ~80% de soluciones peores al inicio
- **Criterio de convergencia**: temperatura final $T_f$ cuando la tasa de aceptación < 1%

> [!EXAMPLE] Evidencia empírica: Sen & Stoffa (2013) — SA en inversión de [[Surface Waves|ondas superficiales]]
> Sen & Stoffa (2013) comparan el SA con el [[Monte Carlo Methods|Monte Carlo]] y el SA "muy rápido" (Very Fast Simulated Annealing, VFSA) para la inversión de [[Dispersion Curve|curvas de dispersión]] de ondas de Rayleigh. El VFSA, con ley de enfriamiento más agresiva ($T_k = T_0 \cdot e^{-k^{1/N_p}}$), converge ~100× más rápido que el SA estándar sin perder capacidad de encontrar el mínimo global. En un ejemplo sintético de perfil con inversión de velocidad (capa blanda a 8–12 m), el VFSA encuentra el modelo correcto en 85% de los casos con 10,000 evaluaciones del modelo directo — comparable al [[Genetic Algorithm|GA]] (87%) pero con menor costo computacional (sin operaciones de cruce/selección). Los autores concluyen que para problemas de dimensionalidad media ($N_p$ < 30), el VFSA es competitivo con el GA en robustez y eficiencia.
>
> — Sen & Stoffa (2013), *Global Optimization Methods in Geophysical Inversion*, Cambridge UP.

## Referencias

| Fuente | Sección / Página |
|--------|-----------------|
| Foti et al. (2018), *Surface Wave Methods* | §6.4.3 — comparación métodos de búsqueda global |
| Kirkpatrick, Gelatt & Vecchi (1983), *Science* | Formulación original del Simulated Annealing |
| Sen & Stoffa (2013), *Cambridge UP* | SA y VFSA para inversión geofísica |
