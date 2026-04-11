---
name: Quality Factor
description: Factor adimensional Q que mide el amortiguamiento de un oscilador o medio — inverso del doble del coeficiente de amortiguamiento DS; Q = 1/(2DS)
type: reference
---

# Quality Factor — Factor de Calidad Q

> [!CONCEPT] Definición
> El **Factor de Calidad Q** es una medida adimensional del amortiguamiento de un sistema oscilatorio o de un medio de propagación de ondas, definido como la razón entre la energía almacenada y la energía disipada por ciclo:
> $$Q = 2\pi \frac{E_{almacenada}}{E_{disipada/ciclo}} = \frac{1}{2D_s}$$
> donde $D_s$ es el [[Shear Damping Ratio|coeficiente de amortiguamiento]] del suelo. Para suelos, $Q_S$ = 5–200 ($D_s$ = 0.25–10%); para rocas, $Q_S$ = 50–1000 ($D_s$ = 0.05–1%). El factor Q aparece en la expresión del [[Attenuation Coefficient|coeficiente de atenuación]]:
> $$\alpha = \frac{\omega}{2Q c} = \frac{\pi f}{Qc} \quad [\text{Np/m}]$$
> y en el **modelo de Q constante** (*constant-Q model*), ampliamente usado en sismología aplicada: el coeficiente de amortiguamiento es independiente de la frecuencia ($Q$ = constante, $D_s$ = constante), lo que implica atenuación proporcional a la frecuencia $\alpha \propto f$. En métodos de ondas superficiales, $Q_R$ es el factor de calidad de la onda de Rayleigh, relacionado con $Q_S$ (dominante) y $Q_P$ (secundario) por los [[Sensitivity Kernel|kernels de sensibilidad]]:
> $$\frac{1}{Q_R(\omega)} \approx \frac{1}{Q_S} \cdot w_S(\omega) + \frac{1}{Q_P} \cdot w_P(\omega), \quad w_S \approx 0.8{-}0.95$$
>
> — Foti et al. (2018), §2.2; Aki & Richards (2002), §5.5; Knopoff (1964).

## Relaciones entre Q, DS y atenuación

| Cantidad | Símbolo | Relación | Rango típico suelos |
|---------|---------|---------|---------------------|
| Factor de calidad | $Q_S$ | $Q_S = 1/(2D_s)$ | 5–200 |
| Coeficiente amortiguamiento | $D_s$ | $D_s = 1/(2Q_S)$ | 0.25–10% |
| Coeficiente de atenuación | $\alpha$ | $\alpha = \pi f/(Q_S V_S)$ | 0.001–0.1 Np/m |
| Longitud de atenuación | $1/\alpha$ | $1/\alpha = Q_S V_S/(\pi f)$ | 10–1000 m |

## Modelos de Q en sismología

1. **Q constante** (*constant-Q*): $Q$ independiente de $f$ → $\alpha \propto f$ → dispersión de material logarítmica → satisface las [[Kramers-Kronig Relations|Relaciones de Kramers-Kronig]]
2. **Q proporcional a $f$** (*linear-Q*): $Q \propto f$ → $\alpha$ constante → no dispersivo
3. **Modelo de Maxwell estándar**: $Q(\omega) = Q_0(\omega\tau)/(1+(\omega\tau)^2)$ → pico de absorción a $\omega_0 = 1/\tau$
4. **Modelo de Kelvin-Voigt**: $Q(\omega) = 1/(\eta\omega/G)$ → $Q$ decreciente con $f$ → no realista a alta $f$

> [!EXAMPLE] Evidencia empírica: Foti et al. (2018) — Q de Rayleigh en inversión DS de MASW
> Foti et al. (2018, §2.2 y §7.3) utilizan el factor de calidad $Q_R$ de la onda de Rayleigh para relacionar el coeficiente de atenuación experimental $\alpha_R^{obs}(f)$ con el perfil de amortiguamiento $D_s(z)$ del suelo. En el sitio de Pisa (arcilla de alta plasticidad), los valores estimados son $Q_R$ = 8–25 en el rango 5–30 Hz (equivalente a $D_s^{eff}$ = 2–6%). La comparación con los ensayos de [[Resonant Column Test|columna resonante]] muestra que $Q_S^{RCT}$ ≈ $Q_R^{MASW}$ dentro de ±15%, confirmando que el factor de calidad de Rayleigh es dominado por $Q_S$ (el factor de calidad de la onda S) — como predice la teoría de sensibilidad ($w_S \approx 0.9$ en el rango de frecuencias estudiado).
>
> — Foti et al. (2018), §2.2, pp. 45–55; §7.3, pp. 375–380.

## Referencias

| Fuente | Sección / Página |
|--------|-----------------|
| Foti et al. (2018), *Surface Wave Methods* | §2.2; §7.3 — Q de Rayleigh y estimación DS |
| Aki & Richards (2002), *Quantitative Seismology* | §5.5 — modelos de Q en sismología |
| Knopoff (1964), *Rev. Geophys.* | Revisión de modelos de Q para materiales geológicos |
