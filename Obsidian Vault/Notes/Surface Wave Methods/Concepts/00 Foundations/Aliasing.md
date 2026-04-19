---
name: Aliasing
description: Distorsión de la señal por muestreo insuficiente — en [[MASW Method|MASW]] ocurre tanto en el dominio temporal (frecuencias altas) como en el dominio espacial (longitudes de onda cortas)
type: reference
---

# Aliasing — Aliasing Temporal y Espacial

> [!CONCEPT] Definición
> El **aliasing** es la distorsión que ocurre cuando una señal se muestrea a una frecuencia insuficiente ([[Nyquist Theorem]]): las componentes de frecuencia que superan $f_{Nyquist} = f_s/2$ se "pliegan" y aparecen como frecuencias más bajas en el espectro, produciendo artefactos. En [[MASW Method|MASW]] hay dos tipos: (1) **aliasing temporal** — ocurre si la frecuencia de muestreo del sismógrafo $f_s$ es menor que $2f_{max}$ (poco común con equipos modernos de 2000+ Hz); (2) **aliasing espacial** — ocurre si el espaciado entre [[Geophone|geófono]] $\Delta x$ es mayor que $\lambda_{min}/2 = c_{R,min}/(2f_{max})$, produciendo crestas espectrales aparentes a velocidades erróneas en el espectrograma f-k. El aliasing espacial es el más crítico en diseño de campo: si se elige $\Delta x$ muy grande (para cubrir más terreno con menos [[Geophone|geófono]]), las ondas de Rayleigh de [[Wavelength|longitud de onda]] corta se aliasen y producen velocidades de fase aparentes mayores que las reales.
>
> — Foti et al. (2018), Cap. 3, §3.1; Cap. 4, §4.2; [[Nyquist Theorem]].

## Aliasing temporal

Si $f_s < 2f_{max}$, las componentes $f > f_{Nyquist}$ se pliegan:

$$f_{alias} = |f_{real} - n \cdot f_s|, \quad \text{con } f_{alias} \leq f_s/2$$

**Consecuencia en [[MASW Method|MASW]]**: si el sledgehammer genera energía hasta 100 Hz y $f_s = 500$ Hz, $f_{Nyquist} = 250$ Hz → sin aliasing. Con $f_s = 100$ Hz, $f_{Nyquist} = 50$ Hz → las frecuencias 50–100 Hz se aliasen entre 0–50 Hz → la [[Dispersion Curve|curva de dispersión]] a altas frecuencias se contamina.

## Aliasing espacial

Con espaciado $\Delta x$, las ondas con $k > k_{Nyquist} = \pi/\Delta x$ (equivalente $\lambda < 2\Delta x$) se pliegan en el espectrograma f-k:

$$k_{alias} = |k_{real} - n \cdot 2\pi/\Delta x|, \quad k_{alias} \leq \pi/\Delta x$$

**Consecuencia en [[MASW Method|MASW]]**: si el suelo superficial tiene $V_S = 100$ m/s y $f = 30$ Hz → $\lambda = 3.3$ m. Si $\Delta x = 3$ m > $\lambda_{min}/2 = 1.65$ m → aliasing espacial → esa [[Wavelength|longitud de onda]] aparece en el espectrograma con un [[Wavenumber|número de onda]] aliaseado → [[Phase Velocity|velocidad de fase]] aparente incorrecta.

## Detección del aliasing espacial en el espectrograma f-k

En el espectrograma f-k, el aliasing espacial produce crestas "fantasma" que son imágenes especulares de la cresta real reflejadas alrededor de $k_{Nyquist}$. A frecuencias altas con $\Delta x$ grande, pueden aparecer múltiples crestas — una real y una o más aliaseadas — confundiendo la identificación modal.

**Regla de diseño**: verificar en el espectrograma que todas las crestas del modo fundamental de Rayleigh están bien por debajo de $k_{Nyquist}$ en todo el rango de frecuencias útil.

> [!EXAMPLE] Evidencia empírica: Park et al. (1999) — diseño sin aliasing en [[MASW Method|MASW]] Kansas
> **Paper 001 (Park, Miller & Xia 1999)** diseña el arreglo con $\Delta x = 1.5$ m para el sitio de Kansas con $V_S$ superficial ~100–200 m/s (capa de suelo no consolidado). Esto da $\lambda_{min} = 2\Delta x = 3$ m → $f_{Nyquist,espacial} \approx 100/3 \approx 33$ Hz para la capa más blanda. El espectrograma f-k del paper muestra las crestas modales por debajo de $k_{Nyquist}$ en todo el rango 5–50 Hz, sin crestas aliaseadas visibles. Los autores establecen que elegir $\Delta x \leq V_{S,min}/(2f_{max})$ donde $V_{S,min}$ es la velocidad mínima esperada en el sitio es la condición anti-aliasing espacial para [[MASW Method|MASW]] — regla que se convirtió en el estándar de diseño de campo.
>
> — Research Database, entrada 001 (core); Park, Miller & Xia (1999), *Geophysics* 64(3).

## Referencias

| Fuente | Sección / Página |
|--------|-----------------|
| Foti et al. (2018), *Surface Wave Methods* | Cap. 3, §3.1; Cap. 4, §4.2 — aliasing en [[MASW Method|MASW]] |
| Park, Miller & Xia (1999), *Geophysics* 64(3) | Paper 001 — diseño anti-aliasing |
