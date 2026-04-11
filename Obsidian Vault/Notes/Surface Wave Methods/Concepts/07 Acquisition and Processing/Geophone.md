---
name: Geophone
description: Sensor sísmico electromagnético de velocidad — transductor estándar en [[MASW Method|MASW]]; convierte movimiento del suelo en señal eléctrica proporcional a la velocidad de partícula
type: reference
---

# Geophone — Geófono

> [!CONCEPT] Definición
> El **geófono** es el sensor sísmico estándar en métodos de exploración superficial ([[MASW Method|MASW]], [[SASW Method|SASW]], [[ReMi Method|ReMi]]). Es un transductor electromagnético que convierte el movimiento del suelo en una señal eléctrica proporcional a la **velocidad de partícula**: una masa-resorte inercial (bobina) se mueve relativa a un imán fijo al suelo, generando una FEM $V(t) = S \cdot \dot{u}(t)$ donde $S$ es la sensibilidad (V·s/m) y $\dot{u}$ la velocidad de partícula. Su comportamiento es el de un oscilador de segundo orden con **frecuencia natural** $f_n$ (tipicamente 4.5, 10, 14 o 28 Hz) y factor de amortiguamiento $\xi$ (típicamente 0.7 para respuesta plana). Por encima de $f_n$, la respuesta es plana en velocidad. Por debajo, la sensibilidad decae con la frecuencia — limitando el rango de bajas frecuencias accesible sin corrección de respuesta instrumental.
>
> — Foti et al. (2018), Cap. 3, §3.2; Sheriff & Geldart (1995), *Exploration Seismology*.

## Principio de funcionamiento

El geófono es un sistema masa-resorte con la bobina como masa inercial:

$$m\ddot{x} + c\dot{x} + kx = -m\ddot{u}_{suelo}$$

donde $x$ es el desplazamiento relativo bobina-imán. La FEM generada es:

$$V(t) = S \cdot \dot{x}(t)$$

En el dominio de la frecuencia, la función de transferencia del geófono (velocidad relativa / velocidad del suelo) es:

$$H(\omega) = \frac{\omega^2}{\omega^2 - \omega_n^2 + 2i\xi\omega\omega_n}$$

Para $\omega \gg \omega_n$: $H \approx 1$ → respuesta plana → el geófono mide fielmente la velocidad del suelo.

## Tipos según frecuencia natural

| $f_n$ (Hz) | Aplicación típica | Rango útil | Uso en ondas superficiales |
|---|---|---|---|
| 4.5 Hz | Exploración profunda, pasiva | 3–200 Hz | Pasivo (microtremores, bajas frecuencias) |
| 10 Hz | Multiusos | 8–200 Hz | Activo + pasivo |
| 14 Hz | [[MASW Method|MASW]] estándar | 12–200 Hz | Activo (sledgehammer) |
| 28 Hz | Alta resolución superficial | 22–200 Hz | Activo, capas muy superficiales |

Para [[MASW Method|MASW]] estándar con sledgehammer (fuente activa, 5–80 Hz), los geófonos de 14 Hz son los más comunes. Para pasivo ([[ReMi Method|ReMi]], SPAC), se recomiendan ≤4.5 Hz para capturar el rango de 1–5 Hz necesario para profundidades >30 m.

## Acoplamiento suelo-geófono

El geófono debe estar mecánicamente acoplado al suelo para que $\dot{u}_{suelo} \approx \dot{u}_{geófono}$. Un acoplamiento deficiente (por superficie dura, geófono inclinado, o suelo blando no compactado) introduce una resonancia espuria en la respuesta y puede alterar la amplitud y la fase de la señal registrada — crítico para la estimación del [[Shear Damping Ratio|coeficiente de amortiguamiento]] $D_s$ desde la curva de atenuación.

## MEMS Accelerometer como alternativa

Los **acelerómetros MEMS** ([[MEMS Accelerometer]]) son sensores de estado sólido que miden aceleración (no velocidad) y tienen respuesta plana desde DC hasta frecuencias altas. Son digitales, robustos y de bajo costo. Limitación: mayor ruido de piso en bajas frecuencias comparado con geófonos de alta calidad. Para [[MASW Method|MASW]] activo (5–100 Hz) son equivalentes en la práctica.

> [!EXAMPLE] Evidencia empírica: Park et al. (1999) — geófonos de 14 Hz como estándar [[MASW Method|MASW]]
> **Paper 001 (Park, Miller & Xia 1999)** utiliza 24 geófonos verticales de **14 Hz** de frecuencia natural en el estudio de Kansas — lo que se convirtió en la configuración estándar de facto para [[MASW Method|MASW]]. En el rango de trabajo (5–50 Hz, dominado por el sledgehammer), la respuesta de los geófonos de 14 Hz es plana con variaciones <1% en amplitud y <2° en fase — sin necesidad de corrección instrumental. Los autores señalan que la elección de geófonos verticales (no horizontales) es específica para ondas de Rayleigh, cuya componente de movimiento dominante es vertical. Para ondas de Love, se requerirían geófonos horizontales transversales, lo que haría el ensayo más complejo.
>
> — Research Database, entrada 001 (core); Park, Miller & Xia (1999), *Geophysics* 64(3).

## Referencias

| Fuente | Sección / Página |
|--------|-----------------|
| Foti et al. (2018), *Surface Wave Methods* | Cap. 3, §3.2 — sensores y sistema de adquisición |
| Sheriff & Geldart (1995), *Exploration Seismology*, 2nd ed. | Cap. 7 — geófonos y respuesta instrumental |
| Park, Miller & Xia (1999), *Geophysics* 64(3) | Paper 001 — geófonos 14 Hz en [[MASW Method|MASW]] estándar |
