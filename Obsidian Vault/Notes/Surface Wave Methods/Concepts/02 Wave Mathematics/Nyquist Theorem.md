---
name: Nyquist Theorem
description: Condición de muestreo que establece que la frecuencia de muestreo debe ser al menos el doble de la frecuencia máxima de la señal para evitar [[Aliasing|aliasing]] temporal en [[MASW Method|MASW]]
type: reference
---

# Nyquist Theorem — Teorema de Nyquist

> [!CONCEPT] Definición
> El **teorema de Nyquist** (o teorema de Nyquist-Shannon) establece que para reconstruir perfectamente una señal de banda limitada $x(t)$ con frecuencia máxima $f_{max}$ a partir de sus muestras discretas, la **frecuencia de muestreo** $f_s$ debe satisfacer $f_s \geq 2 f_{max}$. La frecuencia límite $f_{Nyquist} = f_s/2$ es la frecuencia máxima representable sin [[Aliasing|aliasing]]. En [[MASW Method|MASW]], el teorema aplica en dos dimensiones: (1) **temporal** — la frecuencia de muestreo $f_s$ (tipicamente 1000–4000 Hz) limita la frecuencia máxima de la señal sísmica; (2) **espacial** — el espaciado entre [[Geophone|geófono]] $\Delta x$ actúa como "muestreo espacial" y el [[Wavenumber|número de onda]] máximo $k_{Nyquist} = \pi/\Delta x$ limita la longitud de onda mínima detectable. El [[Aliasing|aliasing]] espacial ocurre cuando $\lambda < 2\Delta x$, produciendo velocidades de fase aparentes erróneas en el espectrograma f-k.
>
> — Foti et al. (2018), Cap. 3, §3.1; Cap. 4, §4.2; Shannon (1949).

## [[Aliasing|Aliasing]] temporal

Con frecuencia de muestreo $f_s$, la frecuencia máxima representable es $f_{Nyquist} = f_s/2$. Las frecuencias por encima de $f_{Nyquist}$ se "pliegan" alrededor de ella → **[[Aliasing|aliasing]] temporal**:

$$f_{alias} = |f - n \cdot f_s|, \quad n \in \mathbb{Z}$$

Para [[MASW Method|MASW]] con fuentes activas (sledgehammer, rango 5–100 Hz), $f_s = 500$–$1000$ Hz es suficiente ($f_{Nyquist} = 250$–$500$ Hz >> 100 Hz). Los equipos modernos usan $f_s = 2000$–$8000$ Hz.

## [[Aliasing|Aliasing]] espacial

Con espaciado entre [[Geophone|geófono]] $\Delta x$, el [[Wavenumber|número de onda]] máximo representable es:

$$k_{Nyquist} = \frac{\pi}{\Delta x}$$

La longitud de onda mínima libre de [[Aliasing|aliasing]] es $\lambda_{min} = 2\Delta x$. La condición anti-[[Aliasing|aliasing]] para la [[Phase Velocity|velocidad de fase]] es:

$$c_R(f) \geq 2 f \Delta x \quad \Leftrightarrow \quad \lambda \geq 2\Delta x$$

En la práctica, se elige $\Delta x \leq \lambda_{min}/2 = c_{R,min}/(2f_{max})$ donde $c_{R,min}$ es la velocidad de Rayleigh mínima esperada (capa más blanda del perfil).

## Diseño del arreglo [[MASW Method|MASW]] bajo la restricción de Nyquist

Para un sitio con $V_S = 100$ m/s en la capa superficial (caso extremo de suelo blando) y $f_{max} = 50$ Hz:
- $\lambda_{min} = 100/50 = 2$ m
- Anti-[[Aliasing|aliasing]] espacial: $\Delta x \leq 1$ m

Para $V_S = 200$ m/s y $f_{max} = 30$ Hz:
- $\Delta x \leq 200/(2 \times 30) \approx 3.3$ m (típico $\Delta x = 2$–$3$ m)

> [!EXAMPLE] Evidencia empírica: Park et al. (1999) — diseño anti-[[Aliasing|aliasing]] del arreglo [[MASW Method|MASW]]
> **Paper 001 (Park, Miller & Xia 1999)** diseña el arreglo de Kansas con $\Delta x = 1.5$ m con conocimiento previo de que $V_S \approx 150$–$300$ m/s en los primeros metros del sitio. Esto da $k_{Nyquist} = \pi/1.5 \approx 2.1$ rad/m, equivalente a $\lambda_{min} = 3$ m. El espectrograma f-k del paper muestra que las crestas del modo fundamental de Rayleigh permanecen por debajo de $k_{Nyquist}$ en todo el rango de frecuencias útil (5–50 Hz), confirmando que la elección de $\Delta x = 1.5$ m previene el [[Aliasing|aliasing]] espacial para el sitio en cuestión. Los autores identifican el criterio $\Delta x \leq \lambda_{min}/2$ como regla de diseño, lo que se convirtió en la guía estándar de la literatura [[MASW Method|MASW]].
>
> — Research Database, entrada 001 (core); Park, Miller & Xia (1999), *Geophysics* 64(3); Shannon (1949).

## Referencias

| Fuente | Sección / Página |
|--------|-----------------|
| Foti et al. (2018), *Surface Wave Methods* | Cap. 3, §3.1; Cap. 4, §4.2 — [[Aliasing|aliasing]] en [[MASW Method|MASW]] |
| Shannon (1949), *Proc. IRE* | Teorema de muestreo original |
| Park, Miller & Xia (1999), *Geophysics* 64(3) | Paper 001 — anti-[[Aliasing|aliasing]] en diseño del arreglo |
