# ReMi Method (Refraction Microtremor)

> [!CONCEPT] Definición
> El **ReMi** (*Refraction Microtremor*, Louie 2001) es un método pasivo que extrae la [[Dispersion Curve|curva de dispersión]] de [[Rayleigh Waves|ondas de Rayleigh]] desde ruido sísmico ambiental (*microtremores*) usando un arreglo lineal estándar de [[Geophone|geófono]] — el mismo hardware que el [[MASW Method|MASW]] activo. El procedimiento consiste en: (1) registrar ruido ambiental, (2) calcular el espectro f-k o tau-p, (3) identificar el **borde mínimo de velocidad** (lowermost velocity boundary) en el espectrograma como estimador de la [[Dispersion Curve|curva de dispersión]] del modo fundamental. La principal hipótesis es que el campo de ruido es aproximadamente **isotrópico**: si las fuentes dominan en una sola dirección, se produce **sobreestimación de la [[Phase Velocity|velocidad de fase]]** (velocidad aparente > velocidad real). La [[Seismic Interferometry|interferometría sísmica pasiva]] supera esta limitación; ReMi es más simple pero menos riguroso en campos de ruido direccionales.
>
> — Louie (2001), *Seismological Research Letters*; Foti et al. (2018), Cap. 3, §3.4.3.3; Cap. 8, §8.4.

## Principio

El **método ReMi** (*Refraction Microtremor*, Louie 2001) extrae la [[Phase Velocity|velocidad de fase]] de [[Surface Waves|ondas superficiales]] a partir del **ruido sísmico ambiental** (*microtremors*), registrado con un arreglo lineal de [[Geophone|geófono]] estándar de adquisición.

La idea central: el campo de ruido ambiental contiene [[Surface Waves|ondas superficiales]] que se propagan en todas las direcciones. En el espectro f-k de un arreglo lineal, estas ondas producen energía que puede usarse para estimar la [[Dispersion Relation|curva de dispersión]], bajo la hipótesis de que el campo de ruido es **aproximadamente isotrópico** (fuentes distribuidas uniformemente alrededor del arreglo) o que al menos contiene ondas propagándose en la dirección del arreglo.

## Procesamiento

1. Registrar ruido ambiental con un arreglo lineal de [[Geophone|geófono]] (típicamente 24–48 canales).
2. Calcular el espectro f-k de los registros de ruido (típicamente mediante la transformada p-τ o f-k directa).
3. Identificar el **borde mínimo de velocidad** en el espectro f-k: los puntos de mínimo [[Wavenumber|número de onda]] para cada frecuencia corresponden a la [[Phase Velocity|velocidad de fase]] de Rayleigh.
4. Trazar la [[Dispersion Curve|curva de dispersión]] a lo largo de ese borde.
5. Invertir la curva para obtener el perfil Vs(z).

## Hipótesis y limitaciones

- **Hipótesis de isotropía del ruido:** si las fuentes de ruido dominan en una sola dirección, el espectro f-k mostrará la velocidad aparente (proyectada sobre el arreglo) que puede ser mayor que la velocidad real. Esto produce **sobreestimación de la [[Phase Velocity|velocidad de fase]]**.
- **Arreglo lineal:** no permite estimar el vector [[Wavenumber|número de onda]] completo. Solo aprovecha componentes de ruido alineadas con el arreglo.
- **Sin separación modal clara:** el espectro f-k de ruido no tiene la misma definición que el espectro de un experimento activo.

## Ventaja vs. métodos activos y vs. interferometría

| Característica | ReMi | Activo ([[MASW Method|MASW]]) | Interferometría pasiva |
|---|---|---|---|
| Fuente | Ruido ambiental | Fuente controlada | Ruido ambiental |
| Geometría | Lineal | Lineal | 2D/lineal |
| Validación hipótesis | Difícil | No aplica | Por correlogram gather |
| Velocidad aparente | Sí (posible sobrestimación) | No (fuente en extremo) | No (cancelación de contribuciones) |
| Frecuencias bajas | Buenas (ruido natural) | Limitadas por fuente | Buenas |

La **[[Seismic Interferometry|interferometría sísmica]] pasiva** (Cap. 8) supera la limitación de la velocidad aparente: el proceso de cross-correlación cancela las contribuciones de fuentes opuestas y el espectro f-k del interferograma tiene máximos en el [[Wavenumber|número de onda]] verdadero. El ReMi es más simple pero menos riguroso cuando el campo de ruido no es isotrópico.

## Aplicaciones

- Zonas urbanas donde fuentes activas son impracticables.
- Cuando se requieren profundidades de investigación > 30 m y no hay energía suficiente con sledgehammer.
- Ensayos sísmicos de sitio (Vs30) combinados con refracción de primeros arrivals.

> [!EXAMPLE] Evidencia empírica: Stephenson (2005) — comparación ciega ReMi y [[MASW Method|MASW]] vs sondeos a 200 m en Santa Clara Valley
> **Paper 036 (Stephenson 2005, BSSA 95, 141 citas)** realiza una comparación ciega de ReMi y [[MASW Method|MASW]] contra sondeos independientes hasta 200 m de profundidad en el Valle de Santa Clara (California), con 8 sitios con distintas condiciones geológicas. Los resultados muestran que **ReMi y [[MASW Method|MASW]] producen perfiles VS concordantes con los sondeos en la mayoría de los sitios**, con diferencias que el autor atribuye principalmente a la variabilidad lateral del subsuelo y no a limitaciones inherentes de los métodos. El VS30 derivado de ambos métodos es coherente con las clasificaciones de sitio del NEHRP. La comparación ciega es metodológicamente robusta porque los procesadores no tuvieron acceso a los datos de sondeo durante el procesamiento, eliminando el sesgo de confirmación. Implicación: en sitios sin inversiones de velocidad severas y con ruido isotrópico, ReMi es competitivo con [[MASW Method|MASW]] para determinar VS30 hasta profundidades excepcionales.
>
> — Research Database, entrada 036 (core); Stephenson (2005), *Bull. Seismol. Soc. Am.*

> [!EXAMPLE] Evidencia empírica: Park & Miller (2008) — Roadside Passive [[MASW Method|MASW]] con arreglo lineal en entorno urbano
> **Paper 048 (Park & Miller 2008, JEEG 13:1–11, 152 citas)** desarrolla una versión pasiva del [[MASW Method|MASW]] con arreglo lineal convencional en borde de carretera, usando el tráfico vehicular como fuente pasiva distribuida. El método aplica un **escaneo azimutal 0–180°** del wavefield registrado para separar ondas propagadas desde distintos azimuts; sumando trazas por azimut se mejora la relación señal/ruido y se obtiene una [[Dispersion Curve|curva de dispersión]] equivalente a la de fuente activa, con el mismo equipamiento estándar ([[Geophone|geófono]] + sismógrafo multicanal). Los resultados de campo en sitios urbanos de Kansas demuestran que el arreglo roadside es prácticamente viable cuando no es posible desplegar arreglos 2D y la fuente activa no es factible. Conexión directa con ReMi (arreglo lineal, fuente pasiva) pero con separación azimutal explícita que corrige el sesgo de velocidad aparente de fuentes offline.
>
> — Research Database, entrada 048 (core); Park & Miller (2008), *J. Environ. Eng. Geophys.* 13:1–11.

> [!EXAMPLE] Evidencia empírica: Garofalo et al. (2016) — ReMi en InterPACIFIC: limitaciones en campo de ruido no isotrópico
> **Papers 006+007 (Garofalo et al. 2016a/b)** incluyen resultados ReMi para los 3 sitios InterPACIFIC, revelando una limitación sistemática: en el sitio Grenoble (zona alpina con fuentes de ruido predominantemente direccionales), los equipos que usaron ReMi obtuvieron [[Dispersion Curve|curvas de dispersión]] con velocidades de fase **sistematicamente sobreestimadas** (~10–15%) respecto a los métodos activos y los datos de borehole, consistente con la hipótesis de velocidad aparente en campo no isotrópico. En contraste, los equipos que aplicaron [[Seismic Interferometry|interferometría sísmica]] o [[SPAC Method|SPAC]] sobre los mismos datos de ruido reprodujeron las curvas de referencia con mejor acuerdo. La comparación confirma que ReMi es confiable cuando el campo de ruido es globalmente isotrópico, pero debe verificarse con criterios de calidad adicionales antes de usar las curvas en inversión.
>
> — Research Database, entradas 006, 007 (core); Garofalo et al. (2016a/b), *Near Surface Geophysics*.

## Referencias

| Fuente | Sección / Página |
|--------|-----------------|
| Louie (2001), *Seismological Research Letters* | Método ReMi original — borde mínimo de velocidad |
| Foti et al. (2018), *Surface Wave Methods* | Cap. 3, §3.4.3.3; Cap. 8, §8.4 — ReMi y comparativa pasivos |
| Garofalo et al. (2016a/b) | Papers 006, 007 — ReMi vs interferometría en InterPACIFIC |
| Park et al. (2007), *The Leading Edge* 26(1):60–64 | Paper 010 — review [[MASW Method|MASW]] activo+pasivo; complementariedad y flujo combinado; 258 citas |
| Stephenson (2005), *BSSA* | Paper 036 — comparación ciega ReMi+[[MASW Method|MASW]] vs sondeos a 200 m; 141 citas |
| Park & Miller (2008), *JEEG* 13:1–11 | Paper 048 — Roadside Passive [[MASW Method|MASW]] con escaneo azimutal; 152 citas |
