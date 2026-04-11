---
name: Seismic Refraction
description: Método sísmico no invasivo que mide los tiempos de llegada de primeras ondas P refractadas — complementario a MASW para obtener VP y detectar la tabla de agua
type: reference
---

# Seismic Refraction — Sísmica de Refracción

> [!CONCEPT] Definición
> La **sísmica de refracción** es un método sísmico no invasivo que mide los **tiempos de llegada de primeras llegadas** (first arrivals) de ondas P refractadas críticamente en interfaces de velocidad creciente con la profundidad. A diferencia de los [[Métodos Sísmicos No Invasivos|métodos de ondas superficiales]] ([[MASW Method|MASW]], [[SASW Method|SASW]]), la refracción invierte los tiempos de viaje de ondas de cuerpo (no superficiales) y produce el perfil de $V_P(z)$, no de $V_S(z)$. En el contexto del MASW, la refracción cumple un rol complementario: (1) proporciona $V_P(z)$ o el [[Poisson Ratio|coeficiente de Poisson]] que se fija a priori en la [[Inversión|inversión]] de la curva de dispersión de Rayleigh; (2) detecta la profundidad de la tabla de agua (donde $V_P$ salta a ~1500 m/s) como dato geotécnico independiente. **Limitación crítica**: falla en presencia de **inversiones de velocidad** (capa blanda bajo capa dura) porque las ondas no se refractan de vuelta a la superficie — es la situación donde el MASW tiene ventaja.
>
> — Foti et al. (2018), §1.1, pp. 1–10; Sheriff & Geldart (1995), Cap. 4.

## Principio físico

La refracción crítica ocurre en una interfaz donde $V_2 > V_1$ (velocidad aumenta con la profundidad). Un rayo sísmico que incide con el ángulo crítico $\theta_c = \arcsin(V_1/V_2)$ se propaga horizontalmente a lo largo de la interfaz y genera **cabezas de onda** (head waves) que vuelven a la superficie. El tiempo de viaje sigue la ley:

$$t(x) = \frac{x}{V_2} + \frac{2H\cos\theta_c}{V_1}$$

donde $H$ es la profundidad de la interfaz. Graficando $t(x)$ vs $x$, la pendiente da $1/V_2$ y la intercepción temporal da $H$.

## Geometría y equipamiento

La refracción usa el mismo hardware que el MASW activo (geófonos, sismógrafo, sledgehammer) con la misma geometría de arreglo. Las primeras llegadas de ondas P se identifican en el sismograma (arribo más temprano, mayor velocidad que Rayleigh) y se interpolan para obtener la curva de tiempo-distancia $t(x)$.

## Rol en el flujo de trabajo MASW

1. **Simultáneo con MASW**: los datos de refracción y de ondas superficiales se adquieren con el mismo disparo y el mismo arreglo.
2. **Proporciona $V_P(z)$**: la inversión de los tiempos de refracción da el perfil $V_P(z)$ que se usa para calcular el [[Poisson Ratio|coeficiente de Poisson]] $\nu = (V_P^2 - 2V_S^2)/(2(V_P^2 - V_S^2))$.
3. **Detecta tabla de agua**: el salto de $V_P$ de ~300–600 m/s (no saturado) a ~1500 m/s (saturado) indica la profundidad freática — relevante para la corrección de $\nu$ en la inversión de Rayleigh (ver [[Poisson Ratio]]).

## Limitación: inversión de velocidad

Si existe una **capa blanda bajo una capa dura** (inversión de velocidad), las ondas P no se refractan de vuelta a la superficie desde la capa blanda → el método de refracción omite esa capa. El perfil de $V_P$ resultante aparece simplificado, sin la capa blanda. El MASW puede detectar inversiones de velocidad (aunque la inversión se complica), lo que es una ventaja clave sobre la refracción.

> [!EXAMPLE] Evidencia empírica: Foti et al. (2018) — refracción como complemento de MASW para estimar VP a priori
> Foti et al. (2018, §6.3) describen el protocolo estándar para usar datos de refracción sísmica como entrada a la inversión de la curva de dispersión. En el sitio La Salle, el perfil $V_P(z)$ de refracción muestra un salto claro a ~4 m de profundidad (de ~500 m/s a ~1500 m/s) identificado como la posición de la tabla de agua. Este valor de $V_P \approx 1500$ m/s se fija en las capas saturadas durante la inversión de la curva de dispersión de Rayleigh, reduciendo el número de parámetros libres y mejorando el condicionamiento del problema inverso. Sin la información de $V_P$ de refracción, la [[Non-uniqueness|no-unicidad]] de la inversión de Rayleigh sería mayor — el coeficiente de Poisson en la zona saturada sería un parámetro libre que el MASW no puede estimar confiablemente.
>
> — Foti et al. (2018), §6.3, pp. 293–298.

## Referencias

| Fuente | Sección / Página |
|--------|-----------------|
| Foti et al. (2018), *Surface Wave Methods* | §1.1, pp. 1–10; §6.3, pp. 293–298 — refracción como complemento |
| Sheriff & Geldart (1995), *Exploration Seismology* | Cap. 4 — teoría de refracción sísmica |
