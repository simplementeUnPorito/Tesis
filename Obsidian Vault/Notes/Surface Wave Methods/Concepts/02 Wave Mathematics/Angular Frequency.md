---
name: Angular Frequency
description: ω = 2πf; frecuencia de oscilación en radianes por segundo; aparece en la [[Dispersion Relation|relación de dispersión]] ω(k) que codifica la física de propagación en medios dispersivos
type: reference
---

# Frecuencia Angular (Angular Frequency)

> [!CONCEPT] Definición
> La **frecuencia angular** $\omega = 2\pi f$ es la forma natural de expresar la frecuencia en el formalismo matemático de ondas. Aparece directamente en la representación de ondas armónicas ($e^{i(kx-\omega t)}$) y en la [[Dispersion Relation|relación de dispersión]] $\omega(k)$ — la función central que codifica la física de propagación en el medio. En [[MASW Method|MASW]], $\omega$ vincula el dominio temporal del sismograma con el dominio espacial mediante la [[Phase Velocity|velocidad de fase]] $c_p = \omega/k$, y la [[Group Velocity|velocidad de grupo]] $c_g = d\omega/dk$ controla el *moveout* temporal del [[Ground Roll|ground-roll]].
>
> — Foti et al. (2018), §2.1.1, pp. 39–41.

## Intuición física

Una onda periódica completa un ciclo de $2\pi$ radianes por período $T = 1/f$. La frecuencia $f$ mide ciclos por segundo (Hz), pero en ecuaciones de onda la unidad natural es **radianes por segundo** porque el argumento de las funciones trigonométricas está en radianes. La frecuencia angular $\omega$ simplifica las expresiones al eliminar los factores $2\pi$ recurrentes.

La diferencia entre $f$ y $\omega$ es puramente de escala: $\omega = 2\pi f$. En la práctica, los instrumentos y los datos sísmicos reportan $f$ en Hz, mientras que los desarrollos matemáticos usan $\omega$ en rad/s. La conversión es inmediata.

## Definición y rol en una onda armónica

La representación canónica de una onda plana armónica es:

$$\phi(x, t) = A\,e^{i(kx - \omega t)}$$

donde:
- $k = 2\pi/\lambda$ — [[Wavenumber|número de onda]] (rad/m): controla la variación **espacial**.
- $\omega$ — frecuencia angular (rad/s): controla la variación **temporal**.
- $A$ — amplitud compleja (incluye fase inicial).

La relación entre $\omega$, $k$, y la [[Phase Velocity|velocidad de fase]] $c_p$ es:

$$c_p = \frac{\omega}{k}$$

Esta ecuación es la definición operativa de [[Phase Velocity|velocidad de fase]]: la rapidez a la que una cresta de fase (frente de onda de igual $\omega t - kx$) se propaga en el espacio.

## La [[Dispersion Relation|relación de dispersión]] ω(k)

La **[[Dispersion Relation|relación de dispersión]]** $\omega(k)$ es la función que determina el comportamiento ondulatorio del medio. Se obtiene sustituyendo la onda armónica en la ecuación de onda del medio:

- **Medio no dispersivo** (velocidad constante $c$): $\omega = ck$ — relación lineal, $c_p = c_g = c$ constantes.
- **Medio dispersivo** (velocidad dependiente de $k$ o $\omega$): $\omega(k)$ es no lineal. La [[Phase Velocity|velocidad de fase]] $c_p = \omega/k$ y la [[Group Velocity|velocidad de grupo]] $c_g = d\omega/dk$ difieren.

Para [[Rayleigh Waves]] en un [[Layered Media|medio estratificado]], la [[Dispersion Relation|relación de dispersión]] se obtiene del sistema de ecuaciones de frontera (método de la matriz de transferencia de Thomson-Haskell) y es implícita: no tiene forma analítica cerrada en general, pero puede evaluarse numéricamente para cada par $(\omega, k)$.

## [[Dispersion Relation|relación de dispersión]] y análisis f-k

En [[MASW Method|MASW]], el análisis f-k (transformada de Fourier 2D del sismograma) transforma el registro $u(x, t)$ al dominio $(\omega, k)$. La amplitud en cada punto $({\omega, k})$ del espectrograma f-k es proporcional a la energía de la onda con esa frecuencia y [[Wavenumber|número de onda]]. Los modos de Rayleigh aparecen como **crestas** en el espectro f-k, cuya pendiente $\omega/k$ da la [[Phase Velocity|velocidad de fase]]:

$$c_p(f) = \frac{\omega}{k}\bigg|_{\text{cresta}} = \frac{2\pi f}{k_{\text{cresta}}}$$

La [[Dispersion Curve|curva de dispersión]] experimental es la imagen de estas crestas en el plano $(f, c_p)$.

## Límites instrumentales en frecuencia

La frecuencia angular (y su análogo $f$) está limitada en la práctica por:

| Límite | Expresión | Controlado por |
|---|---|---|
| $f_{\max}$ (temporal) | $f_{\max} = 1/(2\Delta t)$ | Intervalo de muestreo $\Delta t$ (Nyquist) |
| $f_{\max}$ (espacial) | $f_{\max} = c_p/(2\Delta x)$ | Espaciado entre geófonos $\Delta x$ |
| $f_{\min}$ | $f_{\min} \approx c_p/L$ | Longitud total del arreglo $L$ |

Donde $\Delta x$ es el espaciado entre geófonos y $L$ es la apertura total. La frecuencia mínima determina la máxima longitud de onda accesible y, por tanto, la [[Skin Depth|profundidad de investigación]].

## Notación y conversión práctica

En los resultados experimentales y en el diseño del arreglo se trabaja con $f$ (Hz) por convención instrumental. En la teoría y en las ecuaciones de inversión se usa $\omega$ (rad/s). La conversión:

$$\omega = 2\pi f, \quad T = \frac{1}{f} = \frac{2\pi}{\omega}$$

Algunos autores (incluyendo Foti et al.) alternan entre $f$ y $\omega$ según el contexto; es esencial verificar cuál se usa en cada ecuación para evitar errores de un factor $2\pi$.

> [!EXAMPLE] Evidencia empírica: Park et al. (1999) — análisis f-k como operación en el dominio ω-k
> **Paper 001 (Park, Miller & Xia 1999)** implementa el análisis f-k como una transformada 2D que opera en el dominio $(\omega, k)$. La conversión de frecuencia angular a [[Phase Velocity|velocidad de fase]] $c_p = \omega/k$ es directa en el espectrograma: cada cresta del espectro f-k a un par $(\omega_i, k_i)$ corresponde a la [[Phase Velocity|velocidad de fase]] $c_p(f_i) = \omega_i/k_i$. El proceso no requiere conocer $\omega$ en radianes explícitamente porque los instrumentos reportan $f$ en Hz, pero la matemática subyacente usa $\omega$ para mantener la consistencia con la teoría de ondas elásticas.
>
> — Research Database, entrada 001 (core).

## Referencias

| Fuente | Sección / Página |
|--------|-----------------|
| Foti et al. (2018), *Surface Wave Methods* | §2.1.1, pp. 39–41 — representación de ondas armónicas |
| Foti et al. (2018), *Surface Wave Methods* | §2.1.2, pp. 41–43 — [[Dispersion Relation|relación de dispersión]] y velocidades de fase/grupo |
| Park, Miller & Xia (1999), *Geophysics* 64(3) | Paper 001 — análisis f-k en dominio ω-k |
