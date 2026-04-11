---
name: P-waves
description: Ondas de cuerpo de compresión (longitudinales); las más rápidas en sólidos; su velocidad en suelos saturados es dominada por la compresibilidad del agua, limitando su utilidad geotécnica
type: reference
---

# Ondas P (P-waves / Compressional Waves)

> [!CONCEPT] Definición
> Las **ondas P** (Primary / Pressure / Compressional) son ondas de cuerpo donde el movimiento de la partícula es **paralelo** a la dirección de propagación — deformación volumétrica alternante sin corte puro. Son las ondas más rápidas en sólidos y viajan también en fluidos ($\mu = 0$). En el contexto de [[MASW Method|MASW]], $V_P$ es un **parámetro a priori** de baja sensibilidad en la inversión de la [[Dispersion Curve|curva de dispersión]] de [[Rayleigh Waves]], pero crítico en suelos saturados donde $V_P \approx 1500$ m/s (dominado por el agua poral) y puede afectar el perfil $V_S$ si se ignora.
>
> — Foti et al. (2018), §2.1.3, pp. 43–50.

## Intuición física

Las ondas P producen una secuencia alterna de compresión y dilatación del medio en la dirección de propagación. Es análogo al sonido en el aire: la perturbación se transmite como una variación de presión que viaja hacia adelante, comprimiendo y expandiendo el volumen local del material.

En sólidos, la energía se transmite tanto por la rigidez de corte $\mu$ como por la rigidez volumétrica $K = \lambda + 2\mu/3$. En fluidos, donde $\mu = 0$, solo existe la componente compresional: las ondas P viajan en agua y aire, mientras que las ondas S no lo hacen.

## Formulación matemática

La velocidad de propagación de las ondas P en un medio elástico isótropo es:

$$V_P = \sqrt{\frac{\lambda + 2\mu}{\rho}} = \sqrt{\frac{M}{\rho}}$$

donde:
- $\lambda$, $\mu$ — constantes de Lamé
- $M = \lambda + 2\mu$ — módulo confinado (P-wave modulus)
- $\rho$ — densidad

En términos del [[Poisson Ratio|coeficiente de Poisson]] $\nu$:

$$\frac{V_P}{V_S} = \sqrt{\frac{2(1-\nu)}{1-2\nu}}$$

Para $\nu = 0.25$: $V_P/V_S = \sqrt{3} \approx 1.73$.

## Polarización y movimiento de partícula

Las ondas P tienen **polarización longitudinal**: el vector de desplazamiento de las partículas es paralelo al vector de propagación $\hat{k}$. No existe componente transversal. Esto contrasta con las [[S-Waves|ondas S]] (polarización transversal).

Consecuencia: las ondas P no producen deformación de corte pura. Son sensibles al módulo volumétrico del material.

## Comportamiento en geomateriales saturados

En suelos saturados bajo carga no drenada, la compresibilidad del material está dominada por la compresibilidad del agua poral ($K_{agua} \approx 2.2\,\text{GPa}$). Esto hace que $V_P$ aumente fuertemente y tienda a la velocidad del sonido en agua (~1500 m/s), independientemente de la rigidez del esqueleto sólido.

**Consecuencia crítica**: en suelos saturados, $V_P$ no es un buen indicador de la rigidez geotécnica del suelo. La [[S-Waves|velocidad de onda S]] ($V_S$) sí refleja la rigidez del esqueleto y tiene mejor correlación con propiedades geotécnicas. Esto es la razón fundamental por la que los métodos de caracterización geotécnica se centran en $V_S$.

## Valores típicos

| Material | $V_P$ (m/s) | $V_S$ (m/s) |
|---|---|---|
| Arcilla blanda saturada | 1400–1600 | 50–200 |
| Arena suelta seca | 200–500 | 100–300 |
| Arena densa saturada | 1500–2000 | 200–400 |
| Roca sedimentaria | 2000–4000 | 1000–2000 |
| Roca cristalina | 4000–7000 | 2000–4000 |

## Relevancia en métodos de ondas superficiales

En la inversión de la [[Dispersion Curve|curva de dispersión]] de [[Rayleigh Waves]], $V_P$ (o equivalentemente $\nu$) es un **parámetro a priori** — se fija basándose en información independiente (refracción P, nivel freático, ensayos SPT) y no se invierte directamente. La sensibilidad de la [[Dispersion Curve|curva de dispersión]] a $V_P$ es baja comparada con $V_S$, pero no despreciable: un $V_P$ incorrecto (especialmente ignorar el nivel freático) puede introducir errores sistemáticos en el perfil $V_S$ invertido.

En el método de **refracción sísmica**, las ondas P son el observable primario: los tiempos de llegada de los primeros arrivals se usan para inferir el contraste de $V_P$ entre capas, incluyendo la detección de la tabla de agua.

> [!EXAMPLE] Evidencia empírica: Foti et al. (2018) — impacto de VP y nivel freático en la inversión [[MASW Method|MASW]]
> Foti et al. (2018, §7.1.3) documentan que ignorar la posición del nivel freático (que produce un salto de $V_P$ de ~300 m/s a ~1500 m/s) puede introducir errores sistemáticos en el perfil $V_S$ invertido, especialmente en el rango de frecuencias bajas donde la onda de Rayleigh penetra hasta la zona saturada. En los casos estudiados (sitios de Bélgica e Italia), el error en $V_S$ por $V_P$ incorrecto fue de 5–10% — significativo pero menor que el error por $V_S$ incorrecto. Este resultado justifica la recomendación de medir $V_P$ por refracción P como dato a priori de la inversión de ondas superficiales.
>
> — Foti et al. (2018), §7.1.3, pp. 361–363.

## Referencias

| Fuente | Sección / Página |
|--------|-----------------|
| Foti et al. (2018), *Surface Wave Methods* | §2.1.3, pp. 43–50 — derivación de $V_P$ desde ecuaciones de Navier |
| Foti et al. (2018), *Surface Wave Methods* | §7.1.3, pp. 361–363 — impacto de $V_P$ y nivel freático en inversión |
