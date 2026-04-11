---
name: Métodos Sísmicos No Invasivos
description: Técnicas de medición de VS realizadas íntegramente desde la superficie sin perforaciones; incluyen refracción, reflexión y métodos de ondas superficiales ([[MASW Method|MASW]], [[SASW Method|SASW]], [[ReMi Method|ReMi]], SPAC)
type: reference
---

# Métodos Sísmicos No Invasivos

> [!CONCEPT] Definición
> Los **métodos sísmicos no invasivos** caracterizan el subsuelo midiendo ondas sísmicas desde la superficie del terreno, sin necesidad de perforaciones ni penetración. Son más económicos y representan volúmenes de suelo mucho mayores que los [[Métodos Sísmicos Invasivos|métodos invasivos]]. Los **métodos de ondas superficiales** ([[MASW Method|MASW]], [[SASW Method|SASW]], [[ReMi Method|ReMi]], [[SPAC Method|SPAC]]) son un subconjunto de los no invasivos que explota la [[Wave Dispersion|dispersión]] de las [[Rayleigh Waves|ondas de Rayleigh]] y [[Love Waves|Love]] para inferir el perfil $V_S(z)$ mediante [[Inversión|inversión]] de la [[Dispersion Curve|curva de dispersión]] $c_R(f)$.
>
> — Foti et al. (2018), §1.1, pp. 1–10; Caps. 3–5.

## Clasificación general

Los métodos no invasivos se agrupan por el tipo de onda que aprovechan y la geometría del experimento:

### 1. Sísmica de Refracción

Mide los **tiempos de llegada de primeras ondas** (ondas P refractadas críticamente en interfaces de velocidad creciente con la profundidad). El análisis de los tiempos de viaje permite estimar el contraste de $V_P$ entre capas y la profundidad de cada interfaz.

- **Ventaja**: Sencilla y económica; detecta la tabla de agua (salto de $V_P$ a ~1500 m/s).
- **Limitación crítica**: Falla en presencia de **inversiones de velocidad** (capa blanda bajo capa dura): las ondas no se refractan de vuelta a la superficie, generando un perfil erróneamente simplificado.

### 2. Sísmica de Reflexión de Alta Resolución

Detecta reflexiones de interfaces y construye secciones sísmicas de alta resolución. Requiere procesamiento complejo (NMO, deconvolución, migración). Aplicada a exploración de profundidades medias a grandes.

- **Limitación en geotecnia superficial**: Las reflexiones de los primeros metros son difíciles de separar de la onda directa y el [[Ground Roll|ground-roll]].

### 3. Métodos de Ondas Superficiales

Explotan la **dispersión** de las [[Surface Waves|ondas superficiales]] para inferir el perfil de $V_S$. Son el núcleo de este vault.

| Método | Fuente | Geometría | Observable |
|---|---|---|---|
| [[MASW Method|MASW]] | Activa (martillo/vibrador) | Línea de geófonos | Espectro f-k → [[Dispersion Curve|curva de dispersión]] |
| [[SASW Method|SASW]] | Activa | 2 receptores, offset variable | Función de transferencia → fase |
| [[ReMi Method|ReMi]] | Pasiva (ruido ambiente) | Línea de geófonos | p-f slantstack → [[Dispersion Curve|curva de dispersión]] |
| [[SPAC Method|SPAC]] | Pasiva (ruido ambiente) | Arreglo 2D (triángulo, anillo) | Autocorrelación espacial → $J_0$ |
| [[Seismic Interferometry|Interferometría]] | Pasiva | Cualquier arreglo | Cross-correlación → función de Green |

### 4. [[HVSR|HVSR]] (Microtremores)

El método [[HVSR]] utiliza la razón espectral horizontal/vertical de microtremores para estimar la frecuencia fundamental del sitio $f_0 = V_S / (4H)$. No requiere fuente controlada ni arreglo de múltiples sensores — un único sensor triaxial es suficiente.

## Por qué los métodos de ondas superficiales

Los métodos de ondas superficiales tienen ventajas específicas sobre los otros métodos no invasivos:

1. **No requieren inversión de velocidad**: La refracción sísmica falla en perfiles donde $V_S$ decrece con la profundidad (condición común en depósitos con materiales blandos intercalados). Los métodos de ondas superficiales pueden detectar inversiones, aunque su inversión se complica (ver [[Non-uniqueness]]).

2. **Miden directamente $V_S$**: La [[Dispersion Curve|curva de dispersión]] de Rayleigh es sensible principalmente a $V_S$ (con sensibilidad menor a $V_P$ y $\rho$), y el producto de la inversión es directamente el perfil $V_S(z)$.

3. **Representatividad espacial**: Un arreglo de geófonos de longitud $L$ promedia las propiedades del suelo lateralmente. Esto es una ventaja para heterogeneidades horizontales pero una limitación si el suelo varía significativamente a lo largo del arreglo.

4. **Rango de profundidades**: Ajustando la longitud del arreglo y la fuente se puede investigar desde <1 m hasta >50 m de profundidad en condiciones típicas.

## Comparativa geotécnica

| Aspecto | [[Métodos Sísmicos Invasivos|Invasivos]] | No invasivos (sup. waves) |
|---|---|---|
| Costo | Alto | Bajo |
| Representatividad | Puntual (1D) | Volumétrica (promedio lateral) |
| Resolución vertical | Alta (~0.5 m) | Moderada (gradiente suave) |
| Profundidad | Alta (>100 m) | Moderada (~30–80 m típico) |
| Inversiones de velocidad | Detecta directamente | Detecta con inversión multimodal |
| [[Non-uniqueness|no-unicidad]] | No aplica | Alta (requiere parámetros a priori) |
| Validación necesaria | Referencia de oro | Recomendable vs. invasivo |

> [!EXAMPLE] Evidencia empírica: InterPACIFIC (Garofalo et al. 2016) — comparativa masiva de métodos no invasivos
> **Papers 006+007 (Garofalo et al. 2016a/b)** presentan el estudio InterPACIFIC: 30 equipos internacionales aplican métodos sísmicos no invasivos ([[MASW Method|MASW]], [[ReMi Method|ReMi]], SPAC, [[HVSR|HVSR]]) en 3 sitios de referencia con datos de borehole disponibles. Los resultados muestran que: (1) los métodos de ondas superficiales reproducen el perfil $V_S(z)$ del borehole con acuerdo razonable en todos los sitios; (2) la variabilidad entre operadores es significativa (~15–20% en $[[Vs30|Vs,30]]$) y está dominada por decisiones de procesamiento e inversión, no por el método en sí; (3) la concordancia mejora cuando se usan protocolos estandarizados y parámetros a priori compartidos.
>
> — Research Database, entradas 006, 007 (core).

## Referencias

| Fuente | Sección / Página |
|--------|-----------------|
| Foti et al. (2018), *Surface Wave Methods* | §1.1, pp. 1–10 — clasificación de métodos |
| Foti et al. (2018), *Surface Wave Methods* | Caps. 3–5 — metodologías específicas |
| Garofalo et al. (2016a/b) | Papers 006, 007 — InterPACIFIC |
