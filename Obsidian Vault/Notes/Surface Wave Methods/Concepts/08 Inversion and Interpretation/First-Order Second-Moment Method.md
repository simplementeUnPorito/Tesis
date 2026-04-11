---
name: First-Order Second-Moment Method
description: Método de propagación de incertidumbre basado en linealización de primer orden — cuantifica la varianza de VS(z) debido a errores en la [[Dispersion Curve|curva de dispersión]] experimental
type: reference
---

# First-Order Second-Moment Method (FOSM) — Método de Primer Orden Segundo Momento

> [!CONCEPT] Definición
> El **First-Order Second-Moment Method (FOSM)** es una técnica de propagación de incertidumbre que linealiza la función no-lineal de interés alrededor del punto estimado para propagar la **varianza** de los datos hacia la varianza del modelo. En la [[Inversión|inversión]] de [[Dispersion Curve|curvas de dispersión]] de [[MASW Method|MASW]], la función de interés es $\mathbf{m} = F^{-1}(\mathbf{d})$ (modelo VS a partir de los datos de dispersión). El FOSM aproxima la covarianza del modelo como:
> $$\mathbf{C}_m \approx (\mathbf{J}^T \mathbf{C}_d^{-1} \mathbf{J} + \lambda \mathbf{R}^T\mathbf{R})^{-1} \mathbf{J}^T \mathbf{C}_d^{-1} \mathbf{J} \cdot (\mathbf{J}^T \mathbf{C}_d^{-1} \mathbf{J} + \lambda \mathbf{R}^T\mathbf{R})^{-T}$$
> donde $\mathbf{J}$ es el Jacobiano (matriz de [[Sensitivity Kernel|sensibilidad]]), $\mathbf{C}_d$ es la covarianza de los datos de dispersión, y $\lambda \mathbf{R}^T\mathbf{R}$ es la [[Regularization|regularización]]. El FOSM permite **cuantificar la incertidumbre del perfil $V_S(z)$** — la banda de ±1σ alrededor del perfil invertido — directamente a partir de la incertidumbre de picking de la [[Dispersion Curve|curva de dispersión]] y la [[Sensitivity Kernel|resolución del kernel]]. Es el método analítico de propagación de incertidumbre más eficiente (no requiere múltiples inversiones), pero asume linealidad local: si el problema es altamente no-lineal o si la incertidumbre de los datos es grande, el FOSM puede subestimar la incertidumbre real del modelo.
>
> — Foti et al. (2018), §6.5; Tarantola (2005), §3.4; Xia et al. (2000).

## Formulación en inversión de dispersión

### Propagación de covarianza

Si los datos de dispersión tienen covarianza $\mathbf{C}_d$ (diagonal si los errores son independientes, con $\sigma_{c_R}(f_i)$ en la diagonal), la covarianza del modelo invertido es:

$$\mathbf{C}_m = (\mathbf{J}^T \mathbf{C}_d^{-1} \mathbf{J} + \lambda \mathbf{R}^T\mathbf{R})^{-1}$$

La **desviación estándar del perfil** a la profundidad $z_j$:

$$\sigma_{V_S}(z_j) = \sqrt{[\mathbf{C}_m]_{jj}}$$

### Incertidumbre de la [[Dispersion Curve|curva de dispersión]]

La covarianza $\mathbf{C}_d$ se estima a partir de:
1. **Picking múltiple**: varianza del picking de $c_R(f)$ entre múltiples disparos o posiciones
2. **Ancho espectral**: ancho del pico en el espectrograma f-k a cada frecuencia
3. **Error estándar de la media**: si se promedian $N_{shots}$ disparos, $\sigma_{c_R}(f)/\sqrt{N_{shots}}$

## Ventajas y limitaciones

| Aspecto | FOSM | [[Monte Carlo Methods|Monte Carlo]] |
|---------|------|------|
| Costo computacional | Bajo (una inversión) | Alto (miles de inversiones) |
| Asume linealidad | Sí | No |
| Intervalo de confianza | Gaussiano (aproximado) | Exacto (distribución empírica) |
| Captura [[Non-uniqueness|no-unicidad]] | No | Sí |
| Validez | Cerca del mínimo, errores pequeños | Siempre |

> [!EXAMPLE] Evidencia empírica: Foti et al. (2018) — FOSM para bandas de incertidumbre del perfil VS
> Foti et al. (2018, §6.5) aplican el FOSM a la inversión de la [[Dispersion Curve|curva de dispersión]] del sitio La Salle para estimar las bandas de incertidumbre del perfil $V_S(z)$. La covarianza de los datos $\mathbf{C}_d$ se estima del picking de múltiples disparos (variabilidad de ±5–10 m/s en $c_R$ en el rango 10–50 Hz). El resultado del FOSM produce bandas ±1σ de $\sigma_{V_S}$ = 10–30 m/s en los primeros 15 m y $\sigma_{V_S}$ = 20–60 m/s a mayor profundidad. Estas bandas son consistentes con las obtenidas por [[Monte Carlo Methods|inversión de Monte Carlo]] en el mismo sitio (50,000 modelos aceptables), aunque el FOSM subestima la incertidumbre en la zona de mayor no-linealidad (5–10 m) por ~20%. Los autores recomiendan el FOSM como estimación rápida de primer orden y el [[Monte Carlo Methods|Monte Carlo]] para la cuantificación rigurosa de incertidumbre.
>
> — Foti et al. (2018), §6.5, pp. 330–338.

## Referencias

| Fuente | Sección / Página |
|--------|-----------------|
| Foti et al. (2018), *Surface Wave Methods* | §6.5, pp. 330–338 — FOSM en incertidumbre [[MASW Method|MASW]] |
| Tarantola (2005), *Inverse Problem Theory* | §3.4 — formulación general del FOSM |
| Xia et al. (2000), *Pure Appl. Geophys.* | Aplicación de FOSM a inversión de ondas superficiales |
