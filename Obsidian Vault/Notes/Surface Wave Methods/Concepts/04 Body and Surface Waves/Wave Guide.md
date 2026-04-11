---
name: Wave Guide
description: Guía de ondas — mecanismo de atrapamiento de ondas SH en una capa superficial más lenta que el sustrato por reflexión total interna — condición necesaria para la existencia de Love waves en medios estratificados
type: reference
---

# Wave Guide — Guía de Ondas

> [!CONCEPT] Definición
> Una **guía de ondas** (*wave guide*) es una estructura estratificada que confina y propaga energía ondulatoria a lo largo de una dirección (tipicamente horizontal en geofísica) mediante reflexiones múltiples en sus interfaces. En el contexto de ondas superficiales, el mecanismo de guiado aplica a las **[[Love Waves|ondas Love]]**: una capa superficial con velocidad de corte $V_{S1}$ menor que el sustrato ($V_{S2} > V_{S1}$) actúa como guía de ondas SH por reflexión total interna en la interfaz. La condición de corte (*cut-off*) para el modo fundamental de Love es:
> $$c_L = \omega/k < V_{S2}$$
> con [[Phase Velocity|velocidad de fase]] $c_L$ entre $V_{S1}$ y $V_{S2}$. Las ondas SH se reflejan totalmente en la base de la capa superior cuando el ángulo de incidencia supera el ángulo crítico $\theta_c = \arcsin(V_{S1}/V_{S2})$, quedando **atrapadas** en la guía. Si $V_{S2} \leq V_{S1}$ (sin guía), las Love waves no existen — condición física necesaria para el transporte de energía lateral dispersivo. Las ondas de Rayleigh no requieren una guía de ondas en sentido estricto: existen en un semiespacio homogéneo, pero la estratificación aumenta su amplitud superficial y genera la [[Geometric Dispersion|dispersión geométrica]] observable en [[MASW Method|MASW]].
>
> — Foti et al. (2018), §2.3.2, pp. 85–92; Ewing et al. (1957), *Elastic Waves in Layered Media*.

## Mecanismo físico en ondas Love

Para una capa de espesor $H$ con $V_{S1} < V_{S2}$:

1. **Incidencia oblicua** de ondas SH en la interfaz inferior al ángulo $\theta$
2. **Reflexión total** cuando $\theta > \theta_c = \arcsin(V_{S1}/V_{S2})$: sin energía transmitida al sustrato
3. **Interferencia constructiva** entre ondas SH ascendentes y descendentes: modos propios con condición de resonancia:
$$\frac{2\omega H \sqrt{1/V_{S1}^2 - 1/c_L^2}}{2} = n\pi - \phi_R, \quad n = 1, 2, 3, \ldots$$
donde $\phi_R$ es el desfase en reflexión. Esto genera la **ecuación de dispersión de Love** (Foti Ec. 2.46):
$$\tan\left(\omega H \sqrt{1/V_{S1}^2 - 1/c_L^2}\right) = \frac{\mu_2 \sqrt{1/c_L^2 - 1/V_{S2}^2}}{\mu_1 \sqrt{1/V_{S1}^2 - 1/c_L^2}}$$
4. **Decaimiento evanescente** en el sustrato: la energía decae exponencialmente por debajo de la interfaz a profundidades $> \lambda_{S2}/2$

## Comparación: Love waves vs. Rayleigh waves como guías

| Aspecto | Love waves | Rayleigh waves |
|---------|-----------|----------------|
| Condición de guía | Requiere $V_{S2} > V_{S1}$ | No requerida (existen en semiespacio homogéneo) |
| Profundidad de sensibilidad | ~$\lambda/3$ (onda SH) | ~$\lambda/3$ (onda P+SV) |
| Componente de movimiento | Transversal horizontal (SH) | Elíptica en plano vertical (P+SV) |
| Presencia de modo fundamental | Siempre existe para $f > f_c$ | Siempre existe (sin cut-off) |
| Frecuencia de corte modo 1 | $f_c = V_{S1}/(4H)$ | Sin frecuencia de corte |

## Frecuencias de corte y modos superiores

El modo $n$ (con $n = 1$ para el fundamental) existe para frecuencias:
$$f > f_{c,n} = \frac{(2n-1)V_{S1}}{4H} \left(1 - \frac{V_{S1}^2}{V_{S2}^2}\right)^{-1/2}$$

A frecuencias muy altas ($\lambda \ll H$), todos los modos convergen a $c_L \to V_{S1}$ — las ondas muestrean solo la capa superficial. A $c_L \to V_{S2}$, el modo abandona la guía (ángulo de incidencia → $\theta_c$).

> [!EXAMPLE] Evidencia empírica: Foti et al. (2018) — Love waves como guía en sitio Hveragerdi (Islandia)
> Foti et al. (2018, §2.3.2) ilustran el mecanismo de guía de ondas con la dispersión de Love waves en el sitio geotérmico Hveragerdi (Islandia). El perfil de $V_S$ muestra $V_{S1} \approx 280$ m/s en los primeros 15 m y $V_{S2} \approx 900$ m/s en el sustrato — contraste de ~3.2x que crea una guía de ondas muy eficiente. La [[Dispersion Curve|curva de dispersión]] observada va de $c_L = 290$ m/s a 30 Hz hasta $c_L = 850$ m/s a 3 Hz, con modos superiores bien separados en frecuencia. La velocidad de grupo de cada modo exhibe un mínimo (punto de Airy) donde la energía se concentra — producible como señal impulsiva intensa en el sismograma. La presencia simultánea de modos propios de Love (guía de ondas SH) y de modos de Rayleigh permite la inversión conjunta para mejor determinación de $V_P$ y $\nu$ (véase [[Joint Inversion]]).
>
> — Foti et al. (2018), §2.3.2, pp. 85–92, Figs. 2.26–2.28.

## Referencias

| Fuente | Sección / Página |
|--------|-----------------|
| Foti et al. (2018), *Surface Wave Methods* | §2.3.2 — dispersión de Love waves, guía de ondas |
| Ewing, Jardetzky & Press (1957), *Elastic Waves in Layered Media* | Teoría clásica de guías de ondas elásticas |
| Aki & Richards (2002), *Quantitative Seismology* | §7 — Love waves y modos propios en guías |
