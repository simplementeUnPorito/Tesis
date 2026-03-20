# MASW Method (Multichannel Analysis of Surface Waves)

> **Contexto:** Método activo multicanal para estimar perfiles Vs a partir de ondas de Rayleigh.
> **Fuente:** Park et al. 1999; Foti et al. (2014), Caps. 3–7.

## Principio

El **método MASW** (*Multichannel Analysis of Surface Waves*, Park et al. 1999) estima el perfil de velocidad de onda S del subsuelo ($V_S$ vs. profundidad) analizando la dispersión de las [[Rayleigh Waves|ondas de Rayleigh]] generadas por una fuente activa controlada.

El flujo de trabajo tiene tres etapas:

1. **Adquisición**: registrar un sismograma multicanal con fuente activa (sledgehammer) y un arreglo lineal de geófonos verticales.
2. **Procesamiento**: extraer la [[Dispersion Relation|curva de dispersión]] experimental $c(f)$ a partir del sismograma mediante transformada f-k, beamforming u otras técnicas.
3. **Inversión**: estimar el perfil $V_S(z)$ que mejor reproduce la curva de dispersión observada.

## Geometría de adquisición

La geometría básica es un **arreglo lineal de receptores uniformemente espaciados** con una fuente en un extremo (*end-off*) o en el centro. Los parámetros de diseño controlan las capacidades del sistema:

| Parámetro | Símbolo | Efecto principal |
|---|---|---|
| Espaciado entre geófonos | $\Delta X$ | Controla longitud de onda mínima (profundidad mínima) |
| Apertura total | $D = N\cdot\Delta X$ | Resolución modal, profundidad máxima |
| Offset de la fuente | $L_s$ | Excluye zona de [[Near-field Effect\|campo cercano]] |
| Número de canales | $N$ | Sobredeterminación del sistema |
| Duración del registro | $T$ | Resolución en frecuencia |

**Reglas prácticas**:
- Espaciado típico: 1–5 m para caracterización de suelos superficiales (<30 m)
- Apertura típica: 20–100 m para aplicaciones de ingeniería
- Offset mínimo de fuente: $\lambda_R/2$ (para excluir campo cercano)

## Relación frecuencia–profundidad

La longitud de onda $\lambda = V_R / f$ determina la profundidad de investigación:
- **Altas frecuencias** (λ corta) → información de capas superficiales
- **Bajas frecuencias** (λ larga) → información de capas profundas

La profundidad máxima de investigación es aproximadamente $\lambda_{max}/2$ a $\lambda_{max}$, donde $\lambda_{max}$ corresponde a la frecuencia mínima registrada con buena SNR.

## Ventajas vs. limitaciones

| Ventaja | Limitación |
|---|---|
| No invasivo (sin sondeos) | Resolución en profundidad limitada por longitud del arreglo |
| Rápido en campo | Sensible a variaciones laterales (modelo 1D) |
| Estima $V_S$ directamente | [[Non-uniqueness\|No-unicidad]] de la inversión |
| Compatible con refracción (mismo dataset) | Requiere diseño cuidadoso del arreglo |

## Diferencia con SASW

El método [[SASW Method|SASW]] (*Spectral Analysis of Surface Waves*) usa solo **dos receptores** y requiere múltiples adquisiciones con diferentes espaciados para cubrir el rango de frecuencias. MASW usa un arreglo multicanal en una sola adquisición, lo que mejora la resolución modal y reduce la ambigüedad en la identificación de modos.

## Extensiones avanzadas

- **Passive MASW**: usa ruido ambiental en lugar de fuente activa; permite bajas frecuencias pero la geometría y el procesamiento son más complejos.
- **Multimodal MASW**: incorpora modos superiores de Rayleigh (y/o Love) en la inversión para mejorar la resolución en profundidad.
- **2D MASW**: ensayos con arreglo deslizante (*rolling array*) para generar secciones pseudo-2D de $V_S$.

## Referencias

- Park, C.B., Miller, R.D., Xia, J. (1999), *Geophysics*.
- Foti et al. (2014), Caps. 3 (adquisición), 4–5 (procesamiento), 6–7 (inversión).
