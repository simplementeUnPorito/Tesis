---
name: Mode Superposition
description: El campo sísmico registrado es la suma de múltiples modos de Rayleigh/Love; si modos superiores son activos pero se asume modo fundamental, el perfil VS invertido es erróneo
type: reference
---

# Superposición de Modos (Mode Superposition)

> [!CONCEPT] Definición
> La **superposición de modos** describe el hecho de que el campo sísmico registrado en un arreglo de geófonos es, en general, la suma de múltiples modos de propagación de [[Rayleigh Waves]] y/o [[Love Waves]]. El campo total es $u(x,t) = \sum_n A_n\,e^{i(k_n x - \omega t)}$, donde cada $n$ corresponde a un modo con su propio número de onda $k_n$ y eigenfunción. Si el procesamiento asume modo fundamental pero hay contribuciones significativas de modos superiores (ver [[Surface Wave Modes]]), la curva de dispersión aparente será una mezcla y el perfil $V_S$ invertido será erróneo.
>
> — Foti et al. (2018), §2.4, pp. 64–95.

## Contexto físico

En medios [[Layered Media|estratificados]], la [[Dispersion Relation|relación de dispersión]] del [[Rayleigh Eigenproblem]] admite múltiples soluciones para una misma frecuencia — cada una es un modo de propagación con:
- Su propio número de onda $k_n(\omega)$
- Su propia velocidad de fase $c_n = \omega/k_n$
- Su propio patrón de desplazamiento con la profundidad (eigenfunción)

El modo fundamental ($n=0$) existe para todas las frecuencias; los modos superiores tienen frecuencias de corte mínimas.

## Formulación matemática

El campo de desplazamiento total en superficie:

$$u(x,t) = \sum_{n=0}^{N} A_n(x)\,e^{i(k_n x - \omega t)}$$

donde el índice $n$ identifica el modo. La velocidad de fase **aparente** medida por el análisis f-k estándar es una media ponderada por las amplitudes:

$$c_{app}(\omega) = \frac{\omega}{\partial\psi/\partial x}\bigg|_{\text{campo total}}$$

que no coincide con ningún $c_n$ individual si hay mezcla modal.

## Implicaciones para el procesamiento

| Situación | Consecuencia |
|---|---|
| Modo fundamental dominante | $c_{app} \approx c_0$ — inversión correcta |
| Modos superiores con alta energía | $c_{app}$ es una media de modos — inversión errónea |
| Fuerte contraste de velocidad (suelo blando/roca) | Modos superiores son energéticamente comparables al fundamental |
| Inversión de velocidad en el perfil | Modos superiores pueden dominar en ciertas frecuencias |

## Estrategias de mitigación

- **Verificación del espectro f-k**: identificar visualmente si hay múltiples ramas
- **Análisis multimodal**: incluir varias curvas modales en la función de desajuste
- **Determinant misfit** (Paper 034): evita asignación modal previa
- **Arreglos largos**: mejoran la resolución en $k$ para separar modos
- **Diversidad de offset**: diferentes distancias excitan modos con diferentes amplitudes relativas

> [!EXAMPLE] Evidencia empírica: Tokimatsu et al. (1992) + Xu et al. (2006)
> **Paper 031 (Tokimatsu, Tamura & Kojima 1992, ASCE JGGE, 352 citas)** — análisis teórico pionero: en perfiles con inversión de velocidad (capa blanda bajo capa rígida), los modos superiores de Rayleigh dominan la curva de dispersión aparente a bajas frecuencias, causando subestimación sistemática de Vs en profundidad si se invierte solo el modo fundamental. Propone la simulación multimodal para interpretación correcta. Fundamento directo de la inversión multimodal (Xia et al. 2003, Paper 025).
>
> **Paper 014 (Xu et al. 2006)** documenta errores sistemáticos de hasta **50%** en el perfil $V_S$ cuando se invierte la curva de dispersión asumiendo modo fundamental en presencia de una capa blanda intercalada (inversión de velocidad). En estos sitios, los modos superiores dominan el espectro f-k a frecuencias intermedias, pero la curva aparente parece continua — sin indicación visual de la confusión modal. El trabajo establece criterios para identificar cuándo la hipótesis de modo fundamental es insegura, y recomienda la inversión multimodal o el determinant misfit como alternativas robustas.
>
> — Research Database, entradas 031 y 014 (core).

## Relaciones con otros conceptos

- [[Surface Wave Modes]] — definición formal de cada modo
- [[Rayleigh Eigenproblem]] — formulación matemática del problema de valores propios modal
- [[Phase Velocity]] — cada modo tiene su propia curva de dispersión
- [[Layered Media]] — la estratificación es la causa de la existencia de múltiples modos
- [[MASW Method]] — el procesamiento f-k estándar puede verse afectado por superposición modal
- [[Love Waves]] — también exhiben superposición modal, aunque sin osculaciones

## Fuentes

| Fuente | Sección / Página |
|--------|-----------------|
| Foti et al. (2018), *Surface Wave Methods* | §2.4, pp. 64–95 — modos y superposición modal |
| Tokimatsu et al. (1992), *ASCE JGGE* 118(10) | Paper 031 — modos superiores dominan curva aparente en perfiles con inversión Vs; 352 citas |
| Xu et al. (2006) | Paper 014 — error por confusión de modos en inversión |
