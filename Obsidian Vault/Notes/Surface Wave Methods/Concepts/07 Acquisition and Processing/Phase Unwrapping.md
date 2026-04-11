---
name: Phase Unwrapping
description: Proceso de corrección de saltos de 2π en la fase del espectro cruzado — limitación principal del método [[SASW Method|SASW]] con dos receptores
type: reference
---

# Phase Unwrapping — Desenrollamiento de Fase

> [!CONCEPT] Definición
> El **phase unwrapping** (o desenrollamiento de fase) es el proceso de corregir los saltos de $\pm2\pi$ en la fase del [[Cross-Power Spectrum|espectro cruzado]] $\phi_{12}(f) = \angle[G_{12}(f)]$ para obtener una función de fase continua. El problema surge porque la DFT produce fases en el intervalo $(-\pi, \pi]$: cuando la fase acumulada real supera $\pi$ (para grandes separaciones $\Delta x$ o bajas frecuencias), se produce un salto artificial de $2\pi$ en el espectro (el *phase wrapping*). Si no se corrige, la [[Phase Velocity|velocidad de fase]] calculada $c_R(f) = 2\pi f \Delta x / \phi_{12}(f)$ contendrá errores sistemáticos. Es la **limitación principal del [[SASW Method|método SASW]]** con dos receptores: en la práctica, se recomienda elegir separaciones $\Delta x$ tales que $\phi_{12}(f) < \pi$ para todo $f$ útil (condición de campo cercano), pero esto entra en conflicto con la necesidad de separaciones grandes para medir bajas frecuencias. El análisis multicanal ([[MASW Method|MASW]], f-k) evita este problema porque identifica el número de onda directamente como máximo espectral sin unwrapping.
>
> — Foti et al. (2018), Cap. 4, §4.2; Nazarian & Stokoe (1984), Paper 003.

## Por qué ocurre el phase wrapping

La DFT produce $\phi_{12}(f) \in (-\pi, \pi]$. La fase real acumulada es:

$$\phi_{12}^{real}(f) = -k(f) \cdot \Delta x = -\frac{2\pi f}{c_R(f)} \cdot \Delta x$$

Cuando $|\phi_{12}^{real}| > \pi$ (es decir, cuando el retardo de fase supera medio ciclo), la DFT reporta $\phi_{12}(f) = \phi_{12}^{real}(f) \pm n \cdot 2\pi$ con $n$ entero — produciendo un salto en la curva de fase.

La condición de no-wrapping: $\Delta x < c_R(f) / (2f)$ — equivale a que la separación entre receptores sea menor que la mitad de la longitud de onda.

## Algoritmo de unwrapping 1D

El unwrapping estándar en 1D (rango de frecuencias):
1. Calcular $\Delta\phi = \phi(f_{i+1}) - \phi(f_i)$ entre frecuencias consecutivas
2. Si $|\Delta\phi| > \pi$ → detectar salto → añadir $\pm2\pi$ para suavizar la fase
3. Acumular las correcciones para obtener la fase continua

El algoritmo es frágil en presencia de ruido: si la SNR es baja ($\gamma^2 < 0.9$), los saltos de fase pueden ser reales (ruido) o aparentes (wrapping) — el algoritmo puede hacer correcciones erróneas.

## Ventaja del [[MASW Method|MASW]] sobre el [[SASW Method|SASW]]

En el análisis f-k del [[MASW Method|MASW]], la [[Phase Velocity|velocidad de fase]] se identifica como la posición del **máximo espectral** en el espectrograma $|U(\omega, k)|$. Este procedimiento no requiere unwrapping porque:
- El espectrograma siempre tiene máximos no-negativos (no ambigüedad de signo)
- La resolución $\Delta k$ permite identificar el número de onda verdadero directamente
- Múltiples receptores promedian los efectos del ruido, reduciendo falsas detecciones

Esta ventaja del análisis f-k sobre el espectro cruzado [[SASW Method|SASW]] fue uno de los argumentos principales de Park et al. (1999) para proponer el [[MASW Method|MASW]] como sucesor del [[SASW Method|SASW]].

> [!EXAMPLE] Evidencia empírica: Nazarian & Stokoe (1984) — phase unwrapping como operación esencial en [[SASW Method|SASW]]
> **Paper 003 (Nazarian & Stokoe 1984)** documenta el problema del phase wrapping y el procedimiento de unwrapping en el contexto del [[SASW Method|SASW]]. Los autores identifican que para separaciones $\Delta x$ grandes (necesarias para investigar profundidades >10 m con un sledgehammer estándar), la fase del espectro cruzado a bajas frecuencias supera $\pi$ y produce saltos. El unwrapping se realiza manualmente en el paper original (inspección visual de la curva de fase) — una operación que requiere experiencia y juicio del operador. El paper establece que los errores de unwrapping no detectados producen errores directos de velocidad y son la principal fuente de inconsistencias entre pares de receptores con distintas separaciones. Este problema motivó el desarrollo posterior del [[MASW Method|MASW]] multicanal donde el unwrapping no es necesario.
>
> — Research Database, entrada 003 (core); Nazarian & Stokoe (1984), *8th WCEE*.

## Referencias

| Fuente | Sección / Página |
|--------|-----------------|
| Foti et al. (2018), *Surface Wave Methods* | Cap. 4, §4.2 — phase unwrapping en [[SASW Method|SASW]] |
| Nazarian & Stokoe (1984), *8th WCEE* | Paper 003 — [[SASW Method|SASW]] con unwrapping manual |
