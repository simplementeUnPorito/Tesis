---
name: Refraction Seismics
description: Véase Seismic Refraction — método sísmico de primeras llegadas de ondas P para obtener VP(z) y detectar la tabla de agua
type: reference
---

# Refraction Seismics — Sísmica de Refracción

> [!CONCEPT] Definición
> La **sísmica de refracción** (también llamada *refraction seismics* o *seismic refraction*) es un método sísmico no invasivo que mide los **tiempos de llegada de primeras llegadas** (*first arrivals*) de ondas P refractadas críticamente en interfaces de velocidad creciente con la profundidad. Ver la nota completa en [[Seismic Refraction]].
>
> La refracción sísmica complementa al [[MASW Method|MASW]] en el flujo de trabajo estándar:
> - Proporciona el perfil $V_P(z)$ necesario para calcular el [[Poisson Ratio|coeficiente de Poisson]] que se fija en la [[Inversión|inversión]] de la [[Dispersion Curve|curva de dispersión]] de Rayleigh
> - Detecta la profundidad de la **tabla de agua** (salto de $V_P$ de ~300–600 m/s a ~1500 m/s)
> - Usa el mismo equipamiento que el [[MASW Method|MASW]] activo ([[Geophone|geófono]], sismógrafo, sledgehammer) y se adquiere simultáneamente
>
> **Limitación crítica**: falla ante **inversiones de velocidad** (capa blanda bajo capa dura) — situación donde el [[MASW Method|MASW]] tiene ventaja.

## Principio físico

La refracción crítica ocurre en interfaces donde $V_2 > V_1$. El tiempo de viaje de la onda refractada es:

$$t(x) = \frac{x}{V_2} + \frac{2H\cos\theta_c}{V_1}, \quad \theta_c = \arcsin\left(\frac{V_1}{V_2}\right)$$

donde $H$ es la profundidad de la interfaz. En la gráfica $t(x)$ vs $x$, la pendiente da $1/V_2$ y la intercepción da $H$.

> [!EXAMPLE] Evidencia empírica: Foti et al. (2018) — refracción como complemento de [[MASW Method|MASW]] en La Salle
> Foti et al. (2018, §6.3) usan la sísmica de refracción en el sitio La Salle para obtener el perfil $V_P(z)$, identificando el salto a $V_P \approx 1500$ m/s a ~4 m de profundidad como la posición de la tabla de agua. Este valor se fija en las capas saturadas durante la inversión de la [[Dispersion Curve|curva de dispersión]] de Rayleigh, reduciendo la [[Non-uniqueness|no-unicidad]]. Ver detalles en [[Seismic Refraction]].
>
> — Foti et al. (2018), §6.3, pp. 293–298.

## Referencias

Ver [[Seismic Refraction]] para la nota completa.

| Fuente | Sección / Página |
|--------|-----------------|
| Foti et al. (2018), *Surface Wave Methods* | §1.1; §6.3 — refracción en flujo [[MASW Method|MASW]] |
| Sheriff & Geldart (1995), *Exploration Seismology* | Cap. 4 — teoría de refracción sísmica |
