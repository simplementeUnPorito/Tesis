---
name: Dirac Delta
description: Distribución generalizada δ(t) con integral unitaria y soporte puntual — modelo ideal de fuente impulsiva en sísmica y núcleo de la convolución para la función de Green del medio
type: reference
---

# Dirac Delta — Distribución Delta de Dirac

> [!CONCEPT] Definición
> La **distribución delta de Dirac** $\delta(t)$ es la distribución generalizada con las propiedades:
> $$\delta(t) = 0 \text{ para } t \neq 0, \qquad \int_{-\infty}^{\infty} \delta(t) \, dt = 1$$
> Propiedad de muestreo (*sifting property*): $\int_{-\infty}^{\infty} f(t) \, \delta(t - t_0) \, dt = f(t_0)$ para cualquier función continua $f$. En procesamiento sísmico, $\delta(t)$ representa la **fuente ideal impulsiva**: una descarga de energía infinitamente corta en el tiempo que contiene energía uniforme en todas las frecuencias ($\mathcal{F}\{\delta(t)\} = 1$). La respuesta del medio a esta fuente ideal es la **[[Green Function|función de Green]]** $G(t, r)$, que codifica la propagación dispersiva de [[Rayleigh Waves|ondas Rayleigh]] desde la fuente hasta el receptor. La señal real observada en [[MASW Method|MASW]] es la convolución de la función de Green con la señal de la fuente real: $u(t,r) = s(t) * G(t,r)$. El [[Dirac Comb|tren de deltas]] (Dirac comb) $\sum_n \delta(t - n\Delta t)$ modela el **muestreo temporal discreto** de las señales sísmicas.
>
> — Foti et al. (2018), §3.3.1, pp. 124–128; Bracewell (2000), *The Fourier Transform*, §5.

## Transformada de Fourier de la delta

$$\mathcal{F}\{\delta(t)\} = 1, \qquad \mathcal{F}\{\delta(t - t_0)\} = e^{-i\omega t_0}$$

Esta propiedad implica que una fuente impulsiva ideal emite energía con amplitud **uniforme en todas las frecuencias** y con **fase lineal** proporcional al retardo $t_0$. En MASW, el pico de energía de la fuente martillo se aproxima como una delta desplazada: $s(t) \approx A_0 \, \delta(t - t_s)$.

## Relación con el kernel de la convolución

La [[Convolution Theorem|convolución]] con la delta actúa como **identidad**: $f(t) * \delta(t - t_0) = f(t - t_0)$. Esto permite expresar la respuesta de cualquier sistema lineal como:
$$u(t, r) = \int_{-\infty}^{\infty} G(t - \tau, r) \, s(\tau) \, d\tau = s(t) * G(t, r)$$

donde $G(t, r)$ es la función de Green del medio — respuesta al impulso unitario $\delta(t)$ en $\tau = 0$.

## Dirac comb y muestreo

El **tren de deltas** $\text{III}(t) = \sum_{n=-\infty}^{\infty} \delta(t - n\Delta t)$ modela el muestreo a frecuencia $F_s = 1/\Delta t$. Su transformada de Fourier también es un tren de deltas: $\mathcal{F}\{\text{III}(t)\} = \Delta t \cdot \text{III}(f \cdot \Delta t)$, lo que genera la periodicidad del espectro discreto responsable del [[Spectral Leakage|aliasing]] cuando $f_{\max} > F_s/2$ (ver [[Dirac Comb]]).

> [!EXAMPLE] Evidencia empírica: Park et al. (1998) — respuesta impulsiva en adquisición MASW
> Park et al. (1998, *SEG Technical Program Expanded Abstracts*) analizan la respuesta espectral de diferentes fuentes en ensayos MASW: martillo de 4.5 kg (≈0.5 ms de contacto), vibrador controlado (barrido 1–100 Hz) y carga explosiva. El espectro de amplitud del martillo muestra energía casi plana de 1 a 80 Hz — aproximando la delta de Dirac ideal en el rango sísmico superficial. La correspondencia entre el espectro de la fuente y el espectro de la función de Green (curva de dispersión de Rayleigh) permite extraer $V_R(f)$ directamente de la razón espectral entre receptores, sin necesidad de deconvolución explícita. Foti et al. (2018, §3.4.1) adoptan este modelo convolucional como base del análisis espectral en MASW.
>
> — Foti et al. (2018), §3.3.1, §3.4.1; Park et al. (1998), *SEG Expanded Abstracts*.

## Referencias

| Fuente | Sección / Página |
|--------|-----------------|
| Foti et al. (2018), *Surface Wave Methods* | §3.3.1 — modelo de fuente y función de Green |
| Bracewell, R.N. (2000), *The Fourier Transform* | §5 — delta de Dirac y sus propiedades |
| Lighthill, M.J. (1958), *Introduction to Fourier Analysis* | Distribuciones generalizadas y delta de Dirac |
