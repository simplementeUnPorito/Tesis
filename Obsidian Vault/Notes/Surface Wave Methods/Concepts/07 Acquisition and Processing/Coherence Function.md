---
name: Coherence Function
description: Función de coherencia γ²(f) entre dos señales sísmicas — indicador de SNR del espectro cruzado; criterio de calidad en [[SASW Method|SASW]] para seleccionar puntos confiables de la [[Dispersion Curve|curva de dispersión]]
type: reference
---

# Coherence Function — Función de Coherencia

> [!CONCEPT] Definición
> La **función de coherencia** $\gamma^2(f)$ cuantifica la correlación lineal entre dos señales sísmicas $u_1(t)$ y $u_2(t)$ en cada frecuencia $f$: $\gamma^2(f) = |G_{12}(f)|^2 / (G_{11}(f) \cdot G_{22}(f))$, donde $G_{12}$ es el [[Cross-Power Spectrum|espectro cruzado]] y $G_{11}$, $G_{22}$ son los espectros de potencia individuales. Toma valores entre 0 y 1: $\gamma^2 \approx 1$ indica alta SNR (la señal es completamente determinista entre los dos receptores); $\gamma^2 < 0.7$–$0.9$ indica baja SNR (ruido incoherente o contaminación por otros tipos de ondas). En el [[SASW Method|método SASW]], la coherencia es el **criterio de calidad** que determina qué frecuencias de la [[Dispersion Curve|curva de dispersión]] son confiables: solo se retienen los puntos $(f_i, c_R(f_i))$ donde $\gamma^2(f_i) > \gamma^2_{thr}$ (tipicamente $\gamma^2_{thr} = 0.9$). Los datos con baja coherencia se descartan antes de la [[Inversión|inversión]].
>
> — Nazarian & Stokoe (1984), Paper 003; Foti et al. (2018), Cap. 4, §4.2.

## Definición matemática

$$\gamma^2(f) = \frac{|G_{12}(f)|^2}{G_{11}(f) \cdot G_{22}(f)}, \qquad 0 \leq \gamma^2 \leq 1$$

Se estima promediando sobre múltiples realizaciones (disparos):

$$\hat{\gamma}^2(f) = \frac{|\hat{G}_{12}(f)|^2}{\hat{G}_{11}(f) \cdot \hat{G}_{22}(f)}$$

**Nota**: con una sola realización (un disparo), $\hat{\gamma}^2 = 1$ siempre — no tiene poder discriminante. Se necesitan múltiples disparos ($N \geq 5$–10) para que la coherencia sea estadísticamente significativa.

## Interpretación física

| Valor de $\gamma^2$ | Interpretación | Acción |
|---|---|---|
| $\gamma^2 \approx 1$ | Alta SNR, señal determinista | Retener punto de la [[Dispersion Curve|curva de dispersión]] |
| $0.7 \leq \gamma^2 < 0.9$ | SNR moderada, posible ruido | Usar con cautela; marcar incertidumbre mayor |
| $\gamma^2 < 0.7$ | Baja SNR | Descartar punto |
| $\gamma^2 \approx 0$ | Sin correlación entre receptores | Completamente dominado por ruido |

## Causas de baja coherencia

- **Ruido incoherente**: vibraciones aleatorias no relacionadas con la fuente (tráfico, viento)
- **Contaminación por múltiples modos**: si dos modos de Rayleigh con velocidades distintas contribuyen con energía comparable, la señal no es determinista entre receptores
- **Efectos de campo cercano**: en los receptores más cercanos a la fuente, la curvatura del frente de onda viola la hipótesis de onda plana
- **Fuente inestable**: variaciones de la respuesta de la fuente entre disparos

## Relación con la incertidumbre de la [[Dispersion Curve|curva de dispersión]]

La coherencia está inversamente relacionada con la incertidumbre de la [[Phase Velocity|velocidad de fase]] estimada mediante el espectro cruzado (método [[SASW Method|SASW]]/[[MOPA]]). Cuanto menor la coherencia, mayor la dispersión estadística de la fase entre disparos y mayor la incertidumbre $\sigma_{c_R}(f)$.

> [!EXAMPLE] Evidencia empírica: Nazarian & Stokoe (1984) — coherencia como criterio de calidad en [[SASW Method|SASW]]
> **Paper 003 (Nazarian & Stokoe 1984)** establece el uso de la función de coherencia como criterio estándar para seleccionar las frecuencias confiables de la [[Dispersion Curve|curva de dispersión]] [[SASW Method|SASW]]. Los autores muestran que en el rango de frecuencias donde $\gamma^2 > 0.9$, la fase del [[Cross-Power Spectrum|espectro cruzado]] es estable entre disparos repetidos y produce velocidades de fase reproducibles. En contraste, en las frecuencias fuera de ese rango (típicamente las bajas frecuencias con bajo SNR para el sledgehammer usado, y las altas frecuencias con aliasing), la coherencia cae y la fase es inestable — esas frecuencias se excluyen. El procedimiento de filtrado por coherencia se convirtió en el estándar de facto para el control de calidad de datos [[SASW Method|SASW]] y se extendió posteriormente al [[MASW Method|MASW]] (donde la coherencia se estima entre pares de receptores del arreglo multicanal).
>
> — Research Database, entrada 003 (core); Nazarian & Stokoe (1984), *8th World Conf. on Earthquake Engineering*.

## Referencias

| Fuente | Sección / Página |
|--------|-----------------|
| Foti et al. (2018), *Surface Wave Methods* | Cap. 4, §4.2 — coherencia en [[SASW Method|SASW]]/[[MASW Method|MASW]] |
| Nazarian & Stokoe (1984), *8th WCEE* | Paper 003 — coherencia como criterio de calidad |
