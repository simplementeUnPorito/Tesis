---
name: Lamé Constants
description: Parámetros elásticos de un medio isótropo (λ, μ) — μ es el módulo de corte (directamente relacionado con VS); λ controla la compresibilidad y junto con μ determina VP
type: reference
---

# Constantes de Lamé (Lamé Constants)

> [!CONCEPT] Definición
> Las **constantes de Lamé** $(\lambda, \mu)$ son los dos parámetros que caracterizan completamente un medio elástico isótropo lineal. En la ley de Hooke generalizada: $\sigma_{ij} = \lambda \varepsilon_{kk} \delta_{ij} + 2\mu \varepsilon_{ij}$. El módulo de corte $\mu = \rho V_S^2$ es el parámetro geotécnico primario — relacionado directamente con la velocidad de corte $V_S$. El primer parámetro de Lamé $\lambda = \rho(V_P^2 - 2V_S^2)$ controla la compresibilidad volumétrica. Las velocidades de propagación de ondas elásticas se expresan directamente en función de $(\lambda, \mu)$: $V_P = \sqrt{(\lambda+2\mu)/\rho}$, $V_S = \sqrt{\mu/\rho}$. En [[Viscoelastic Media|medios viscoelásticos]], $\lambda$ y $\mu$ se reemplazan por módulos complejos dependientes de la frecuencia $\tilde{\lambda}(\omega)$, $\tilde{\mu}(\omega)$ — principio de correspondencia. El [[Poisson Ratio|coeficiente de Poisson]] $\nu = \lambda/(2(\lambda+\mu))$ es un parámetro derivado que describe la relación entre deformación lateral y axial.
>
> — Foti et al. (2018), Cap. 2, §2.1; Aki & Richards (2002), *Quantitative Seismology*.

## Definición matemática

Para un medio elástico isótropo lineal, la ley de Hooke generalizada es:

$$\sigma_{ij} = \lambda\, \varepsilon_{kk}\, \delta_{ij} + 2\mu\, \varepsilon_{ij}$$

donde $\varepsilon_{kk} = \varepsilon_{11} + \varepsilon_{22} + \varepsilon_{33}$ es la dilatación volumétrica.

Las velocidades de propagación de ondas elásticas son:

$$V_P = \sqrt{\frac{\lambda + 2\mu}{\rho}}, \qquad V_S = \sqrt{\frac{\mu}{\rho}}$$

## Interpretación física

| Constante | Símbolo | Significado físico | Relación geotécnica |
|---|---|---|---|
| Módulo de corte | $\mu$ | Rigidez al corte — resistencia a deformación de corte | $\mu = \rho V_S^2$; parámetro primario de [[MASW Method|MASW]] |
| Primer parámetro de Lamé | $\lambda$ | Contribución de la dilatación a los esfuerzos normales | $\lambda = \rho(V_P^2 - 2V_S^2)$; controla compresibilidad |
| [[Poisson Ratio|Coeficiente de Poisson]] | $\nu = \lambda/[2(\lambda+\mu)]$ | Relación deformación lateral/axial | $\nu \to 0.5$ en suelos saturados ($\lambda \to \infty$) |

## Relación con parámetros sísmicos

En suelos no saturados ($V_P \approx 300$–$1500$ m/s):
- $\nu \approx 0.2$–$0.4$ → $\lambda \approx 0.7\mu$–$5\mu$

En suelos saturados ($V_P \approx 1500$ m/s):
- $\nu \to 0.5$ → $\lambda \gg \mu$ → $V_P^2 \approx \lambda/\rho$

La insensibilidad de la [[Dispersion Curve|curva de dispersión]] de Rayleigh a $V_P$ ([[Sensitivity Kernel]]) se explica porque $\mu$ (no $\lambda$) domina la rigidez al corte que controla $c_R$ — $\lambda$ solo entra en la condición de incompresibilidad y su efecto es de segundo orden.

## En medios viscoelásticos

Por el **principio de correspondencia** ([[Viscoelastic Media]]):

$$\tilde{\mu}(\omega) = \mu(1 + 2iD_s), \qquad \tilde{\lambda}(\omega) = \lambda(1 + 2iD_p)$$

donde $D_s$ es el [[Shear Damping Ratio|amortiguamiento al corte]] y $D_p$ el amortiguamiento compresional (generalmente $D_p \approx D_s/2$ en geomateriales).

> [!EXAMPLE] Evidencia empírica: Xia et al. (1999) — μ como parámetro primario en inversión [[MASW Method|MASW]]
> **Paper 002 (Xia et al. 1999)** demuestra mediante kernels de sensibilidad que la [[Phase Velocity|velocidad de fase]] de Rayleigh $c_R(f)$ depende principalmente del módulo de corte $\mu = \rho V_S^2$ (sensibilidad 80–95%) y muy poco de $\lambda$ (a través de $V_P$, <10%) y $\rho$ (<2%). Esto justifica que la inversión [[MASW Method|MASW]] tenga como objetivo único $V_S(z)$ — equivalente a invertir $\mu(z)/\rho(z)$ — mientras $\lambda$ (equivalente a fijar $V_P$ o el [[Poisson Ratio|coeficiente de Poisson]]) se asume conocido a priori desde datos de refracción sísmica o tablas de litología. El resultado confirma que las constantes de Lamé tienen roles muy distintos en la propagación de [[Surface Waves|ondas superficiales]]: $\mu$ controla la respuesta cinemática (velocidad de Rayleigh), mientras $\lambda$ tiene efecto secundario.
>
> — Research Database, entrada 002 (core); Xia et al. (1999), *Geophysics* 64(3).

## Referencias

| Fuente | Sección / Página |
|--------|-----------------|
| Foti et al. (2018), *Surface Wave Methods* | Cap. 2, §2.1, pp. 38–50 — constantes elásticas |
| Aki & Richards (2002), *Quantitative Seismology*, 2nd ed. | Cap. 2 — parámetros elásticos |
| Xia et al. (1999), *Geophysics* 64(3) | Paper 002 — sensibilidad de VS vs VP vs ρ |
