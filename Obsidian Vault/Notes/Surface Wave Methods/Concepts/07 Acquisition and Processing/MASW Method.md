---
name: MASW Method
description: Multichannel Analysis of Surface Waves — método activo multicanal para estimar perfiles VS a partir de la dispersión de ondas de Rayleigh; estándar de facto en caracterización geotécnica no invasiva
type: reference
---

# MASW Method (Multichannel Analysis of Surface Waves)

> [!CONCEPT] Definición
> El **método MASW** (*Multichannel Analysis of Surface Waves*, Park et al. 1999) estima el perfil de velocidad de onda de corte $V_S(z)$ del subsuelo analizando la [[Wave Dispersion|dispersión]] de las [[Rayleigh Waves|ondas de Rayleigh]] generadas por una fuente activa controlada. El flujo de trabajo es: (1) adquisición con arreglo lineal de geófonos verticales, (2) extracción de la [[Dispersion Curve|curva de dispersión]] $c_R(f)$ por análisis f-k, (3) inversión para obtener $V_S(z)$. Es el estándar de facto en caracterización geotécnica no invasiva para obtención del parámetro $V_{S,30}$.
>
> — Park, Miller & Xia (1999), *Geophysics* 64(3); Foti et al. (2018), Caps. 3–7.

## Principio

El **método MASW** (*Multichannel Analysis of Surface Waves*, Park et al. 1999) estima el perfil de velocidad de onda S del subsuelo ($V_S$ vs. profundidad) analizando la dispersión de las [[Rayleigh Waves|ondas de Rayleigh]] generadas por una fuente activa controlada.

El flujo de trabajo tiene tres etapas:

1. **Adquisición**: registrar un sismograma multicanal con fuente activa (sledgehammer) y un arreglo lineal de geófonos verticales.
2. **Procesamiento**: extraer la [[Dispersion Relation|curva de dispersión]] experimental $c(f)$ a partir del sismograma mediante transformada f-k, beamforming u otras técnicas.
3. **Inversión**: estimar el perfil $V_S(z)$ que mejor reproduce la [[Dispersion Curve|curva de dispersión]] observada.

## Geometría de adquisición

La geometría básica es un **arreglo lineal de receptores uniformemente espaciados** con una fuente en un extremo (*end-off*) o en el centro. Los parámetros de diseño controlan las capacidades del sistema:

| Parámetro | Símbolo | Efecto principal |
|---|---|---|
| Espaciado entre geófonos | $\Delta X$ | Controla longitud de onda mínima (profundidad mínima) |
| Apertura total | $D = N\cdot\Delta X$ | Resolución modal, profundidad máxima |
| Offset de la fuente | $L_s$ | Excluye zona de [[Near-field Effect|campo cercano]] |
| Número de canales | $N$ | Sobredeterminación del sistema |
| Duración del registro | $T$ | Resolución en frecuencia |

**Parámetros recomendados (Park, Miller & Miura 2002 — Tabla 1, Paper 026)**:

| Geófono (Hz) | Prof. máx. (m) | Offset mín. (m) | Offset máx. (m) | Espaciamiento (m) |
|---|---|---|---|---|
| 4.5 | 50 | 10 | 100 | 1 |
| 10 | 30 | 10 | 100 | 1 |
| 40 | 15 | 10 | 100 | 1 |

El **MASW es el método sísmico más tolerante a variaciones de parámetros** — un offset mínimo de 10 m es suficiente para la mayoría de suelos (más tolerante que el criterio $\lambda/2$ del [[SASW Method|SASW]]). La fuente recomendada es un sledgehammer ≥ 10 lb con buena acoplamiento al suelo.

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
| Estima $V_S$ directamente | [[Non-uniqueness|No-unicidad]] de la inversión |
| Compatible con refracción (mismo dataset) | Requiere diseño cuidadoso del arreglo |

## Diferencia con [[SASW Method|SASW]]

El método [[SASW Method|SASW]] (*Spectral Analysis of Surface Waves*) usa solo **dos receptores** y requiere múltiples adquisiciones con diferentes espaciados para cubrir el rango de frecuencias. MASW usa un arreglo multicanal en una sola adquisición, lo que mejora la resolución modal y reduce la ambigüedad en la identificación de modos.

## Extensiones avanzadas

- **Passive MASW**: usa ruido ambiental en lugar de fuente activa; permite bajas frecuencias pero la geometría y el procesamiento son más complejos.
- **Multimodal MASW**: incorpora modos superiores de Rayleigh (y/o Love) en la inversión para mejorar la resolución en profundidad.
- **2D MASW**: ensayos con arreglo deslizante (*rolling array*) para generar secciones pseudo-2D de $V_S$.

> [!EXAMPLE] Evidencia empírica: Park et al. (1999) + Xia et al. (2002) — validación del método MASW
> **Paper 001 (Park, Miller & Xia 1999)** introduce el método MASW moderno con análisis f-k multicanal. Registros de campo en Kansas con 24 geófonos a 1.5 m de espaciado producen espectrogramas f-k donde el modo fundamental de Rayleigh es claramente identificable entre 5 y 30 Hz. La [[Dispersion Curve|curva de dispersión]] extraída muestra reproducibilidad entre ensayos y coherencia con el perfil geológico conocido.
>
> **Paper 009 (Xia et al. 2002)** valida los perfiles $V_S(z)$ obtenidos por MASW contra 14 ensayos de borehole independientes en Kansas: error RMS promedio < 15%, con errores individuales < 5% en sitios homogéneos. Este resultado establece el MASW como herramienta de caracterización geotécnica con precisión comparable a métodos invasivos.
>
> **Paper 035 (Long & Donohue 2007, CGJ, 76 citas)** — 8 sitios de investigación geotécnica en Noruega (arcillas, limos, arenas) con geófonos 4.5 Hz y 10 Hz a 1 m de espaciado (RAS-24 Seistronix, setup equivalente al de la tesis). MASW sobreestima Vs ~10% respecto a SCPT y crosshole en arcillas; en arenas sueltas la sobreestimación puede ser mayor. Los perfiles Gmax = ρVs² tienen buena correlación con contenido de agua e índice de vacíos. Conclusión clave: MASW es rápido, repetible y consistente, con un sesgo sistemático de +10% que debe considerarse en la interpretación.
>
> — Research Database, entradas 001, 009, 035 (core).

> [!EXAMPLE] Evidencia empírica: Lima Júnior et al. (2012) — MASW en suelos tropicales residuales, Brasil
> **Paper 028 (Lima Júnior, Prado & Mendes 2012, Rev. Bras. Geofísica 30(2):213–224)** aplica MASW en suelos tropicales residuales no saturados (regolito granítico-gnéisico) en ladera de Ubatuba, São Paulo (Brasil), con tres frecuencias de geófono simultáneas (4.5 Hz, 14 Hz, 28 Hz) para comparación experimental. Resultado clave: **geófonos de 4.5 Hz proporcionan la mayor profundidad de investigación** y mejor respuesta a bajas frecuencias — validando la elección para la presente tesis. El offset mínimo óptimo (~10 m) confirma experimentalmente el criterio de Park et al. 2002 en contexto tropical. Adicionalmente, los autores documentan una **variación estacional de Vs** (temporada seca > lluviosa) atribuida a la succión capilar en suelos no saturados — resultado directamente relevante para Paraguay con su régimen pluviométrico marcado.
>
> — Research Database, entrada 028 (core); Lima Júnior et al. (2012), *Rev. Bras. Geofísica* 30(2):213–224.

> [!EXAMPLE] Evidencia empírica: Alhuay-León & Trejo-Noreña (2021) — MASW+SPT en arenas eólicas, Perú
> **Paper 016 (Alhuay-León & Trejo-Noreña 2021, DYNA 88(217):247–255, 4 citas)** aplica MASW activo con 24 geófonos de 4.5 Hz (Geometrics Geode 24 canales) y martillo 25 lb en arenas eólicas de Olmos, Lambayeque (Perú) — zona de máxima sismicidad peruana (PGA 0.45g). Los perfiles VS obtenidos generan correlaciones empíricas con el SPT: $V_S = 65.5 \cdot N_{60}^{0.33}$ y $V_S = 21.6 \cdot N_{60}^{0.38} \cdot (\sigma'_v)^{0.24}$. El estudio confirma que con el mismo equipamiento básico candidato para la tesis (Geode 24-ch + 4.5 Hz + martillo) es posible caracterizar sísmicamente suelos granulares secos en contexto latinoamericano de recursos limitados, obteniendo VS30 en el rango Clase D (180–360 m/s). Es un **precedente sudamericano directo** del hardware y protocolo propuesto.
>
> — Research Database, entrada 016 (core); Alhuay-León & Trejo-Noreña (2021), *DYNA* 88(217):247–255.

## Referencias

| Fuente | Sección / Página |
|--------|-----------------|
| Park, Miller & Xia (1999), *Geophysics* 64(3) | Paper 001 — método MASW original |
| Xia et al. (2002), *J. Environ. Eng. Geophys.* | Paper 009 — validación vs borehole, error < 15% |
| Long & Donohue (2007), *Canadian Geotechnical Journal* | Paper 035 — 8 sitios noruegos; sesgo +10% vs SCPT/crosshole |
| Park, Miller & Miura (2002), SEG-J abstract | Paper 026 — guía de parámetros óptimos de campo (Tabla 1) |
| Lima Júnior et al. (2012), *Rev. Bras. Geofísica* 30(2):213–224 | Paper 028 — MASW tropical Brasil; geófonos 4.5 Hz óptimos |
| Alhuay-León & Trejo-Noreña (2021), *DYNA* 88(217):247–255 | Paper 016 — MASW+SPT Perú; precedente sudamericano 4.5 Hz |
| Foti et al. (2018), *Surface Wave Methods* | Caps. 3 (adquisición), 4–5 (procesamiento), 6–7 (inversión) |
