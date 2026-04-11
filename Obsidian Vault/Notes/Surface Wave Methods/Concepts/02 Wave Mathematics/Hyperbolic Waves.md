---
name: Hyperbolic Waves
description: Ondas no dispersivas descritas por EDPs hiperbólicas; todas las frecuencias viajan a la misma velocidad; contraste con ondas dispersivas en medios estratificados
type: reference
---

# Ondas Hiperbólicas (Hyperbolic Waves)

> [!CONCEPT] Definición
> Las **ondas hiperbólicas** son ondas no dispersivas descritas por ecuaciones diferenciales parciales de tipo hiperbólico. En ellas, **todas las frecuencias se propagan a la misma velocidad** $c_0$ y la forma del paquete no cambia durante la propagación ($c_p = c_g = c_0$ = constante). Las [[P-waves|ondas P]] y [[S-Waves|ondas S]] en medios homogéneos son hiperbólicas. El contraste con las ondas dispersivas en [[Layered Media|medios estratificados]] — donde $c_p(\omega) \neq c_0$ — es el fundamento de por qué la [[Dispersion Relation|relación de dispersión]] de Rayleigh aporta información sobre la estructura del subsuelo.
>
> — Foti et al. (2018), §2.1.1, pp. 38–39.

## Formulación matemática

El ejemplo canónico es la ecuación de onda 1D (ver [[1D Wave Equation]]):

$$\frac{\partial^2 \phi}{\partial x^2} = \frac{1}{c_0^2}\frac{\partial^2 \phi}{\partial t^2}$$

La solución general es la [[d'Alembert Solution|solución de d'Alembert]]:

$$\phi(x,t) = f(x - c_0 t) + g(x + c_0 t)$$

donde $f$ y $g$ son funciones arbitrarias que representan ondas viajando en sentidos opuestos a velocidad constante $c_0$, sin deformación.

La relación de dispersión es lineal: $\omega = c_0 k$ — lo que implica $c_p = c_g = c_0$. Esta es la caracterización matemática de la no-dispersividad.

## Contexto en geofísica

Las [[P-waves]] y [[S-Waves]] en medios elásticos homogéneos son aproximadamente hiperbólicas: viajan a velocidades constantes $V_P$ y $V_S$ independientemente de la frecuencia. En contraste, las [[Rayleigh Waves]] en [[Layered Media|medios estratificados]] son dispersivas: la relación $\omega(k)$ es no lineal (ver [[Wave Dispersion]] y [[Geometric Dispersion]]).

> [!EXAMPLE] Evidencia empírica: separación en tiempo entre ondas de cuerpo y ground-roll en sismogramas MASW
> **Paper 001 (Park, Miller & Xia 1999)** muestra sismogramas de Kansas donde las primeras llegadas P (ondas hiperbólicas, llegan primero) están claramente separadas del ground-roll de Rayleigh (onda dispersiva, llega después). Esta separación temporal valida que las ondas P se comportan como hiperbólicas (velocidad constante $V_P$), mientras que el ground-roll exhibe la dispersión característica de medios estratificados. La diferencia de comportamiento entre ondas hiperbólicas (no dispersivas) y ondas de Rayleigh (dispersivas) es el fundamento conceptual del análisis f-k que extrae la curva de dispersión del ground-roll.
>
> — Research Database, entrada 001 (core).

## Relaciones con otros conceptos

- [[1D Wave Equation]] — la EDP hiperbólica canónica
- [[d'Alembert Solution]] — solución general de la EDP hiperbólica 1D
- [[Wave Dispersion]] — contraste: ondas dispersivas vs. no dispersivas
- [[Hyperbolic Partial Differential Equations]] — clasificación matemática de EDPs
- [[P-waves]], [[S-Waves]] — ondas hiperbólicas en medios homogéneos
- [[Rayleigh Waves]] — ondas no hiperbólicas (dispersivas) en medios estratificados

## Fuentes

| Fuente | Sección / Página |
|--------|-----------------|
| Foti et al. (2018), *Surface Wave Methods* | §2.1.1, pp. 38–39 — categorías de propagación ondulatoria |
| Park, Miller & Xia (1999), *Geophysics* 64(3) | Paper 001 — contraste hiperbólico vs dispersivo en sismogramas |
