---
name: Métodos Sísmicos Invasivos
description: Técnicas de medición de VS que requieren perforaciones o penetración del terreno (cross-hole, down-hole, SCPT); medición directa de alta resolución pero costosa y puntual
type: reference
---

# Métodos Sísmicos Invasivos (Borehole Methods)

> **Contexto:** Los métodos sísmicos invasivos miden $V_S$ directamente en el subsuelo mediante instrumentación introducida en perforaciones o sondas de penetración. Ofrecen la mayor precisión y resolución vertical de todos los métodos geofísicos de caracterización de sitio, pero su costo es elevado y la medición es puntual (1D). Se usan como referencia de validación para los [[Métodos Sísmicos No Invasivos|métodos no invasivos]] y para proporcionar los parámetros a priori en la inversión de ondas superficiales.
> **Fuente:** Foti et al. (2014), Cap. 1.1, pp. 1–10; referencias a normativas ASTM D4428 y ASTM D7400.

## Fundamento físico común

Todos los métodos invasivos miden el **tiempo de viaje** de ondas elásticas entre una fuente y uno o varios receptores ubicados a profundidades conocidas. La velocidad se calcula como $V = \Delta d / \Delta t$ donde $\Delta d$ es la distancia geométrica entre fuente y receptor y $\Delta t$ es el tiempo de viaje medido. En suelos, se miden principalmente [[S-Waves|ondas S]] (por su relevancia geotécnica) aunque también se pueden medir [[P-waves|ondas P]].

## Técnicas principales

### Cross-Hole Test (CHT)

La fuente y los receptores se instalan a la **misma profundidad** en pozos separados horizontalmente. Se mide el tiempo de viaje directo horizontal entre pozos. Es la medición más directa de $V_S$ a cada profundidad.

- **Geometría**: 2 o más pozos separados 3–5 m; fuente en uno, receptor(es) en otro(s).
- **Ventaja**: Resolución vertical muy alta; mide $V_S$ a cada profundidad sin promediar.
- **Limitación**: Requiere al menos 2 pozos — costo alto; el paralelismo perfecto de los pozos es difícil de garantizar (requiere inclinometría).

### Down-Hole Test

La fuente se ubica en **superficie** y los receptores bajan por un único pozo a diferentes profundidades. Se mide el tiempo de llegada de la primera onda S a cada profundidad.

- **Geometría**: 1 pozo; fuente superficial a ~1 m del borde del pozo.
- **Método**: Se baja el receptor a incrementos de 1–2 m y se mide el tiempo de viaje total (tiempo de llegada desde la fuente).
- **Procesamiento**: El perfil $V_S(z)$ se obtiene por diferenciación: $V_S(z_i) = (z_{i+1} - z_{i}) / (t_{i+1} - t_i)$.
- **Variante SCPT**: los receptores se montan en la sonda del **ensayo de penetración de cono (CPT)**, permitiendo medición sísmica simultánea con la penetración. Es la alternativa más práctica cuando ya se realiza CPT.

### P-S Suspension Logging

Un único instrumento con fuente y dos receptores se suspende en un **pozo lleno de fluido**. El fluido actúa como acoplador mecánico con la pared del pozo. Se generan pulsos de alta frecuencia y se mide el tiempo de viaje entre receptores a distancias de ~1 m.

- **Ventaja**: Alta resolución vertical (~0.5–1 m); puede trabajar en pozos existentes llenos de agua.
- **Aplicación**: Investigación profunda (>100 m); industria del petróleo y gas; obra civil en roca.
- **Limitación**: Requiere pozo de buena calidad; sensible al estado de las paredes.

## Ventajas y limitaciones

| Aspecto | Invasivos | [[Métodos Sísmicos No Invasivos\|No invasivos]] |
|---|---|---|
| Resolución vertical | Alta (0.5–2 m) | Moderada (gradiente suave) |
| Precisión de $V_S$ | Alta (±5–10%) | Moderada–baja (±15–30%) |
| Representatividad espacial | Puntual (1D) | Volumétrica (promedio lateral) |
| Profundidad accesible | Alta (>100 m con perforación) | Limitada por $\lambda_{\max}$ |
| Costo relativo | Alto | Bajo |
| Inversión de velocidades | Detecta directamente | Difícil (no-unicidad) |

## Rol en el contexto de ondas superficiales

Los métodos invasivos cumplen dos roles fundamentales en la práctica de MASW:

1. **Validación**: Los perfiles $V_S(z)$ obtenidos por cross-hole o down-hole son la referencia de oro para evaluar la precisión de los perfiles derivados por inversión de la curva de dispersión.

2. **Parámetros a priori**: El [[Non-uniqueness|problema de no-unicidad]] de la inversión requiere parámetros fijos. El perfil $V_P(z)$ (o el [[Poisson Ratio|coeficiente de Poisson]]) obtenido por refracción sísmica o down-hole se usa como entrada fija en la inversión de la curva de dispersión de [[Rayleigh Waves]].

## Referencias

- Foti et al. (2014), Cap. 1.1, pp. 1–10 — contexto de los métodos invasivos vs. no invasivos en caracterización geotécnica.
- ASTM D4428 — Cross-Hole Seismic Testing.
- ASTM D7400 — Down-Hole Seismic Testing.
