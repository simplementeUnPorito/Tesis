---
name: Hidden Layer Problem
description: Limitación de la sísmica de refracción por la que una capa de menor velocidad que la superior queda invisble en los tiempos de llegada — produce perfiles VS subestimados si se confía solo en refracción — [[MASW Method|MASW]] no tiene este problema
type: reference
---

# Hidden Layer Problem — Problema de la Capa Oculta

> [!CONCEPT] Definición
> El **problema de la capa oculta** (*hidden layer problem*) es una limitación fundamental de la [[Seismic Refraction|sísmica de refracción** que ocurre cuando una capa con **menor velocidad** que la capa superior produce tiempos de llegada refractada que nunca dominan sobre las llegadas de capas adyacentes — haciendo que la capa quede **"invisible"** en el gráfico tiempo-distancia (*time-distance plot*). Una capa $k$ es oculta cuando su velocidad $V_k < V_{k-1}$ (inversión de velocidad) o cuando es demasiado delgada para generar refractadas distinguibles en la ventana de distancias medida. En términos cuantitativos, la profundidad mínima detectable de una capa es:
> $$h_{min} \approx \frac{x_{cross}}{2} \sqrt{\frac{V_k - V_{k-1}}{V_k + V_{k-1}}}$$
> donde $x_{cross}$ es la distancia de cruce entre la recta de la capa $k-1$ y la recta de la capa $k$ en el gráfico tiempo-distancia. La consecuencia práctica es que el perfil $V_S(z)$ obtenido solo por [[Seismic Refraction|refracción sísmica]] puede **omitir capas** y sobreestimar la profundidad de las capas inferiores. En contraste, el [[MASW Method|MASW]] y otros métodos de ondas superficiales no tienen este problema: las [[Rayleigh Waves|ondas Rayleigh]] son sensibles a la rigidez de todas las capas a través de las que penetran, incluyendo inversiones de velocidad, aunque la [[Non-uniqueness|no-unicidad]] limita la resolución de inversiones bruscas.
>
> — Foti et al. (2018), §8.3.1, pp. 415–420; Sheriff & Geldart (1995), *Exploration Seismology*, §4.3; Palmer (1981).

## Tipos de capas ocultas en refracción

| Tipo | Mecanismo | Detección posible |
|------|----------|------------------|
| **Inversión de velocidad** ($V_k < V_{k-1}$) | La refractada en capa $k$ llega tarde — dominada por las de capas más rápidas | No sin información adicional |
| **Capa delgada** ($h_k \ll \lambda_{P}$) | La refractada en la capa aparece solo en un rango de distancias muy estrecho | Solo si $x_{array}$ muy largo |
| **Capa de baja contraste** ($V_k \approx V_{k-1}$) | Las líneas de tiempo-distancia se confunden | Solo con alta densidad de receptores |

## Implicaciones para la práctica de caracterización de sitios

El escenario más común en geotecnia superficial donde la capa oculta importa:
- **Suelo blando sobre roca**: $V_S$ del suelo < $V_S$ de la roca → refracción funciona normalmente (velocidad creciente)
- **Capa de arena suelta bajo arcilla densa**: $V_S(arena) < V_S(arcilla)$ → **capa oculta** en refracción → [[MASW Method|MASW]] o CPT necesarios
- **Zona no saturada sobre saturada (tabla de agua)**: $V_P$ salta, $V_S$ no → capa visible en refracción de P, invisible en refracción de S

La combinación [[MASW Method|MASW]] + refracción P es la estrategia estándar porque:
- Refracción P: detecta posición de la tabla de agua (salto en $V_P$)
- [[MASW Method|MASW]]: detecta $V_S$ de todas las capas, incluyendo inversiones de velocidad

> [!EXAMPLE] Evidencia empírica: Foti et al. (2018) — capa oculta en sitio La Salle
> Foti et al. (2018, §8.3.1, pp. 415–420) analizan el sitio La Salle con refracción sísmica P y [[MASW Method|MASW]] simultáneamente. El perfil de refracción muestra solo dos capas: suelo no saturado ($V_P \approx 500$ m/s, 0–4 m) y suelo saturado ($V_P \approx 1500$ m/s, >4 m) — resuelve bien la tabla de agua pero no detecta la variación de $V_S$ dentro de cada zona. El perfil [[MASW Method|MASW]] revela que el suelo saturado (4–25 m) contiene en realidad tres unidades con $V_S$ de 150, 210 y 280 m/s — una de las cuales (la capa de 150 m/s a 8–12 m, arena suelta limo-arenosa) es invisible en refracción porque su $V_P \approx 1500$ m/s (dominado por la saturación) es igual al de las unidades adyacentes. Sin [[MASW Method|MASW]], esta capa potencialmente licuable habría pasado inadvertida en la caracterización del sitio.
>
> — Foti et al. (2018), §8.3.1, pp. 415–420; Sheriff & Geldart (1995), *Exploration Seismology*, §4.3.

## Referencias

| Fuente | Sección / Página |
|--------|-----------------|
| Foti et al. (2018), *Surface Wave Methods* | §8.3.1 — capa oculta y combinación con refracción |
| Sheriff & Geldart (1995), *Exploration Seismology* | §4.3 — limitaciones de la sísmica de refracción |
| Palmer, D. (1981), *The Generalized Reciprocal Method* | Método alternativo para capas ocultas en refracción |
