---
name: Radon Transform
description: Transformada τ-p (tiempo de intercepción - parámetro de slowness) que mapea el campo de ondas sísmico al dominio de rayos planos — usada en MASW y sísmica de reflexión para separar modos de ondas superficiales y suprimir ruido coherente
type: reference
---

# Radon Transform — Transformada de Radón ($\tau$-$p$)

> [!CONCEPT] Definición
> La **transformada de Radón** (o transformada $\tau$-$p$, con $p$ = *slowness* = $1/V$) mapea una función $u(x, t)$ (campo de ondas sísmico en el dominio espacio-tiempo) al dominio $(\tau, p)$:
> $$U(\tau, p) = \int_{-\infty}^{\infty} u(x, \tau + px) \, dx$$
> donde $\tau$ es el tiempo de intercepción y $p = 1/V$ es el parámetro de *slowness* (inverso de la velocidad aparente). La transformada de Radón lineal (*linear Radon transform* o *slant stack*) suma a lo largo de líneas rectas $t = \tau + px$ en el dominio $x$-$t$. Una onda plana con velocidad aparente $V_a$ (slowness $p = 1/V_a$) y tiempo de intercepción $\tau_0$ produce un **punto concentrado** en $(\tau_0, p)$ en el dominio transformado. En el análisis de [[MASW Method|ondas superficiales]], la transformada $\tau$-$p$ ofrece una alternativa a la transformada $f$-$k$ para extraer la [[Dispersion Curve|curva de dispersión]]: cada modo de Rayleigh aparece como una cresta en el panel $(\tau, p)$ a slowness $p = 1/V_R(f)$. La versión **parabólica** de la transformada (suma a lo largo de parábolas) es más efectiva para suprimir las ondas de cuerpo que tienen moveout hiperbólico en $x$-$t$.
>
> — Foti et al. (2018), §4.3.3, pp. 198–204; Treitel et al. (1982), *Geophysics* 47(10); Tatham (1989), *Geophysics*.

## Propiedades de la transformada τ-p en ondas superficiales

### Separación de modos

En el panel $(\tau, p)$, los distintos modos de Rayleigh aparecen como crestas a diferentes slownesses $p_n = 1/V_{R,n}(f)$. La separación es efectiva cuando las velocidades de fase difieren > 10–15% — similar a la condición para separación en el dominio $f$-$k$.

### Supresión de ondas de cuerpo

Las ondas P y S directas tienen moveout lineal en $x$-$t$ (onda plana) pero a velocidades mucho mayores que las ondas Rayleigh ($V_P \gg V_R$). En el dominio $\tau$-$p$, aparecen a slowness muy pequeña ($p \ll 1/V_R$), fácilmente filtrable. Las ondas de cuerpo refractadas tienen moveout hiperbólico — no se mapean como puntos en $\tau$-$p$ lineal, pero sí en $\tau$-$p$ parabólico.

### Relación con la transformada f-k

La transformada $f$-$k$ es la versión espectral (en frecuencia) de la $\tau$-$p$:
$$F(f, k) = \int\!\int u(x, t) \, e^{-i2\pi(ft - kx)} \, dx \, dt$$

La relación entre ambas: $p = k/f$ — el slowness es la pendiente en $f$-$k$. Los picos del panel $f$-$k$ sobre líneas de velocidad constante $V_a = f/k$ corresponden a puntos en $\tau$-$p$ a $p = 1/V_a$.

> [!EXAMPLE] Evidencia empírica: Foti et al. (2018) — transformada τ-p en análisis MASW vs. f-k
> Foti et al. (2018, §4.3.3, Figs. 4.15–4.17) comparan los paneles $f$-$k$ y $\tau$-$p$ del mismo conjunto de datos MASW en el sitio Mud Island, Memphis. El panel $\tau$-$p$ muestra el modo fundamental de Rayleigh como cresta concentrada en $p = 1/V_R$ para cada frecuencia, con menos contaminación de ondas de cuerpo que el panel $f$-$k$ equivalente (las ondas directas P a $V_P \approx 500$ m/s quedan a $p \approx 0.002$ s/m vs. las ondas Rayleigh a $p \approx 0.005$–$0.01$ s/m). La resolución en slowness es similar: $\Delta p = 1/(N\Delta x \cdot f)$ — para $N = 24$, $\Delta x = 2$ m, $f = 20$ Hz: $\Delta p \approx 0.001$ s/m. La curva de dispersión extraída del panel $\tau$-$p$ coincide con la del panel $f$-$k$ dentro del 2%.
>
> — Foti et al. (2018), §4.3.3, pp. 198–204; Treitel et al. (1982), *Geophysics* 47(10).

## Referencias

| Fuente | Sección / Página |
|--------|-----------------|
| Foti et al. (2018), *Surface Wave Methods* | §4.3.3 — transformada τ-p en MASW |
| Treitel et al. (1982), *Geophysics* 47(10), 1571–1581 | Slant stack y transformada τ-p en sísmica |
| Tatham, R.H. (1989), *Geophysics* | Transformada τ-p parabólica para supresión de ruido |
