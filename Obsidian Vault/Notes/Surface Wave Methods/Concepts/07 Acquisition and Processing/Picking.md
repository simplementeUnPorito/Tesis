---
name: Picking
description: Proceso de identificación manual o automática de la [[Phase Velocity|velocidad de fase]] en el espectrograma f-k o p-f para construir la [[Dispersion Curve|curva de dispersión]] experimental en [[MASW Method|MASW]]/[[SASW Method|SASW]]
type: reference
---

# Picking — Extracción de la Curva de Dispersión

> [!CONCEPT]
> El **picking** (selección de picos) es el procedimiento por el cual el analista extrae la [[Dispersion Curve|curva de dispersión experimental]] a partir del espectrograma de velocidad (panel f-k, f-v o τ-p). Para cada frecuencia f, se identifica la [[Phase Velocity|velocidad de fase]] V_R(f) que corresponde al máximo de energía espectral en el panel transformado:
>
> $$V_R(f) = \underset{V}{\arg\max}\; |S(f,V)|^2$$
>
> La calidad del picking determina directamente la fiabilidad de la inversión posterior: un error de ±5% en V_R(f) produce un error de ±10–15% en el perfil Vs(z) resultante (Foti et al. 2018, §3.4).

## Tipos de picking

### Manual
El analista selecciona visualmente la cresta del modo fundamental en el panel f-k. Es el estándar en [[MASW Method|MASW]]:
1. Visualizar el espectrograma normalizado en escala de color
2. Identificar la cresta continua del modo fundamental
3. Marcar puntos (f_i, V_i) a lo largo de la cresta
4. Verificar coherencia con velocidades de grupo esperadas

### Automático
Algoritmos de extracción automática del máximo (útil en procesamiento masivo):
- **Búsqueda de máximo por columna**: para cada f, encontrar V de máxima amplitud
- **Rastreo de contorno**: seguir la cresta con algoritmos de snake/active contour
- **Umbral de amplitud**: descartar puntos con amplitud < X% del máximo global

## Criterios de aceptación

- **Ancho de la cresta (resolución f-k)**: la cresta debe ser estrecha y continua — cretas anchas indican mezcla de modos o campo cercano
- **Coherencia interciclo**: el picking debe ser consistente entre disparos del mismo ensayo
- **Rango frecuencial válido**: típicamente [f_min, f_max] donde f_min ≈ VS_min/(L_array) y f_max < 1/(2·Δt·geophone)
- **Límites de campo cercano y lejano**: excluir frecuencias donde x_min/λ < 0.5 (campo cercano) o x_max/λ > 2 (campo lejano)

## Incertidumbre del picking

La incertidumbre en la [[Dispersion Curve|curva de dispersión]] experimental se estima estadísticamente cuando se dispone de múltiples realizaciones (disparos o ventanas):

$$\sigma_{V_R}(f) = \text{std}[V_R^{(k)}(f)]$$

Esta incertidumbre se propaga a la inversión como peso en el funcional de mínimos cuadrados: puntos de picking con alta incertidumbre contribuyen menos al ajuste (Foti et al. 2018, §6.2).

> [!EXAMPLE] Evidencia empírica (Park et al. 1999, Foti et al. 2018)
> - **Park et al. (1999)** — Kansas field test (19 geófonos, 1.5 m, fuente sledgehammer): el picking manual del modo fundamental en el panel f-k produjo la [[Dispersion Curve|curva de dispersión]] en el rango 5–50 Hz. La ventana de Hann previa al picking redujo la contaminación de lóbulos laterales ~18 dB, permitiendo identificar el modo fundamental sin ambigüedad hasta 50 Hz (longitudes de onda 1–15 m, sondeo efectivo 0.5–7.5 m).
> - **Foti et al. (2018, §7.3)** — Sitio Memphis, TN: picking combinado activo (5–70 Hz) + pasivo (0.5–10 Hz) produciendo [[Dispersion Curve|curva de dispersión]] en 0.5–70 Hz. La zona de solapamiento (5–10 Hz) mostró consistencia entre activo y pasivo dentro de ±3%, validando la concatenación de curvas.
> - **Xia et al. (1999)** — Lawrence, Kansas: picking automático con búsqueda de máximo en 19 columnas del panel f-v (5–50 Hz). Error de picking ≈ ±2 m/s (±1% a 200 m/s), propagado a error de inversión ±8% en Vs.

## Referencias

| Autor | Año | Contribución |
|-------|-----|--------------|
| Park, Miller & Xia | 1999 | Picking manual del modo fundamental en f-k [[MASW Method|MASW]] |
| Xia, Miller & Park | 1999 | Picking automático en panel f-v y propagación de error |
| Foti et al. | 2018 | §3.4, §7.3: criterios de calidad y combinación activo+pasivo |
| Herrmann | 2013 | Software CPS: herramientas de picking interactivo |
