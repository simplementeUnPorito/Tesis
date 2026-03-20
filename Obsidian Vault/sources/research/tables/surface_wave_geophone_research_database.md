# Surface Wave & Geophone Research Database

> Base de datos curada para la tesis. Una entrada por paper, bien analizada.
> Fuente maestra: `surface_wave_geophone_research_database.csv`

**Última actualización:** 2026-03-20

---

## Estadísticas

| Categoría | N |
|-----------|---|
| core | 21 |
| peripheral | 1 |
| reject | 0 |
| Con PDF local | 11 |
| Solo DOI/link | 11 |
| **Total** | **22** |

---

## Entradas

---

### 001 — Park, Miller & Xia (1999) — MASW canónico

| Campo | Valor |
|-------|-------|
| **Título** | Multichannel analysis of surface waves |
| **Autores** | Choon B. Park, Richard D. Miller, Jianghai Xia |
| **Año** | 1999 |
| **Idioma** | Inglés |
| **DOI** | `10.1190/1.1444590` |
| **Landing page** | https://library.seg.org/doi/10.1190/1.1444590 |
| **PDF (KGS, open access)** | https://www.kgs.ku.edu/software/surfseis/Publications/ParkEtAl1999.pdf |
| **PDF local** | `research/papers/pdf/Park1999_MASW.pdf` |
| **Tipo de publicación** | Artículo en revista peer-reviewed (*Geophysics*, Vol. 64, No. 3, pp. 800–808) |
| **Calidad de fuente** | Alta (SEG / CrossRef verificado) |

**Método principal:** MASW (Multistation Analysis of Surface Waves)
**Método secundario:** Análisis f-k
**Sensor:** Geófonos verticales estándar
**Adquisición:** Activa impulsiva (martillo)
**Geometría:** Arreglo lineal multicanal
**Tipo de sitio:** Campo (múltiples sitios Kansas)

**Problema que aborda:** Proponer MASW como alternativa eficiente al SASW, aprovechando el arreglo multicanal y el análisis f-k para extraer la curva de dispersión de manera robusta y rápida desde el ground-roll.

**Método y flujo de trabajo:**
1. Adquisición con arreglo lineal de geófonos (24 canales típico)
2. Transformada f-k del sismograma → identificación de máximos espectrales → curva de dispersión experimental
3. Inversión 1D iterativa (modo fundamental) para obtener Vs(z)

**Instrumentación requerida:** Geófonos verticales 4.5 Hz, sismógrafo de 24 canales, martillo sledge. Equipamiento de bajo a moderado costo, factible en contexto académico.

**Limitaciones reportadas:**
- Asume modo fundamental dominante → puede fallar en perfiles inversamente dispersivos (capa rígida superficial)
- Resolución decrece con profundidad
- El offset mínimo no se sistematiza rigurosamente en este trabajo

**Conclusiones clave para la tesis:**
MASW ofrece tasa de producción de campo muy superior a SASW: con un solo disparo y un arreglo fijo se obtiene la curva de dispersión completa. El análisis f-k separa modos y reduce contaminación por ruido. Define el flujo estándar adquisición → f-k → inversión que es la base de la mayoría de implementaciones actuales.

**Relevancia para tesis:** **Alta** — paper fundacional, lectura obligatoria. Justifica la elección de MASW como método principal. Parámetros de diseño experimental directamente aplicables.

**Factibilidad económica:** Alta — todo el equipamiento es de bajo-moderado costo y disponible comercialmente. Reproducible en contexto como Paraguay.

**Categoría:** core

---

### 002 — Xia, Miller & Park (1999) — Inversión MASW (companion paper)


| Campo | Valor |
|-------|-------|
| **Título** | Estimation of near-surface shear-wave velocity by inversion of Rayleigh waves |
| **Autores** | Jianghai Xia, Richard D. Miller, Choon B. Park |
| **Año** | 1999 |
| **Idioma** | Inglés |
| **DOI** | `10.1190/1.1444578` |
| **Landing page** | https://pubs.geoscienceworld.org/geophysics/article/64/3/691/73487/ |
| **PDF (KGS, open access)** | https://www.kgs.ku.edu/software/surfseis/Publications/XiaEtAl1999.pdf |
| **PDF local** | `research/papers/pdf/Xia1999_MASW_inversion.pdf` |
| **Tipo de publicación** | Artículo en revista peer-reviewed (*Geophysics*, Vol. 64, No. 3, pp. 691–700) |
| **Calidad de fuente** | Alta (SEG / CrossRef verificado) |

**Método principal:** Inversión de ondas de Rayleigh (MASW — algoritmo de inversión)
**Método secundario:** Análisis f-k (referenciado a Park et al. 1999)
**Sensor:** Geófonos verticales estándar
**Adquisición:** Activa impulsiva (martillo)
**Geometría:** Arreglo lineal multicanal
**Tipo de sitio:** Campo + sintético (validación con borehole, sitios en Kansas)

**Problema que aborda:** Presentar el algoritmo de inversión iterativa para obtener el perfil Vs(z) desde la curva de dispersión experimental de ondas de Rayleigh. Companion paper directo de Park et al. (1999): mientras ese paper propone el método de adquisición y extracción de la curva, este define el algoritmo de inversión.

**Método y flujo de trabajo:**
1. Curva de dispersión experimental como input (desde f-k, Park 1999)
2. Linealización iterativa del problema no lineal de inversión
3. Cálculo del Jacobiano (derivadas parciales ∂VR/∂Vs por capa) — computacionalmente eficiente
4. Método del gradiente conjugado para actualizar el modelo
5. Modelo inicial empírico: Vs ≈ 0.9 × VR(f)
6. Validación cruzada vs. borehole en sitios de Kansas; también con datos sintéticos

**Instrumentación requerida:** Misma que Park 1999 (geófonos 4.5 Hz, sismógrafo 24 canales, martillo sledge). La inversión es computacionalmente ligera — corre en cualquier PC moderno.

**Limitaciones reportadas:**
- Sensible al modelo inicial — puede converger a mínimo local si el modelo de partida es muy incorrecto
- Supone estratificación horizontal (1D)
- Vp y densidad fijados a priori (introduce sesgo si son incorrectos, aunque la sensibilidad a estos parámetros es baja comparada con Vs)
- Solo considera modo fundamental de Rayleigh

**Conclusiones clave para la tesis:**
La inversión de ondas de Rayleigh es un problema no lineal que puede linealizarse iterativamente con buena eficiencia. El Jacobiano se puede calcular analíticamente, lo que hace el proceso rápido (convergencia típica en < 10 iteraciones). El acuerdo entre Vs estimado e independiente (borehole) es muy bueno en los sitios de prueba. Este es el algoritmo base implementado en SurfSeis y adoptado por la mayoría de los softwares de procesamiento MASW. Comprenderlo es esencial para justificar las decisiones de inversión en la tesis.

**Relevancia para tesis:** **Alta** — define el algoritmo de inversión estándar. Las ecuaciones del Jacobiano son la base de casi todas las implementaciones locales posteriores. Lectura obligatoria junto con Park 1999.

**Factibilidad económica:** Alta — mismo equipamiento de campo que Park 1999. La inversión es liviana computacionalmente. Totalmente reproducible en contexto académico con recursos básicos.

**Categoría:** core

---

### 003 — Nazarian & Stokoe (1984) — SASW fundacional

| Campo | Valor |
|-------|-------|
| **Título** | In situ shear wave velocities from spectral analysis of surface waves |
| **Autores** | Soheil Nazarian, Kenneth H. Stokoe II |
| **Año** | 1984 |
| **Idioma** | Inglés |
| **DOI** | *(sin DOI — proceedings preDigital)* |
| **Landing page (WorldCat)** | https://search.worldcat.org/title/84257107 |
| **PDF** | *(no disponible en acceso libre)* |
| **PDF local** | *(no descargado)* |
| **Tipo de publicación** | Conference proceedings peer-reviewed (*Proc. 8th World Conference on Earthquake Engineering*, Vol. III, pp. 31–38, Prentice-Hall, 1984, San Francisco) |
| **Calidad de fuente** | Alta (citado >3000 veces; metadatos verificados via WorldCat OCLC 11037839 y múltiples listas de referencias en literatura) |

**Método principal:** SASW (Spectral Analysis of Surface Waves)
**Método secundario:** Análisis espectral cruzado de ondas superficiales
**Sensor:** Geófonos verticales
**Adquisición:** Activa impulsiva (martillo)
**Geometría:** Dos receptores (configuración clásica SASW — distancia variable, múltiples configuraciones)
**Tipo de sitio:** Campo (USA)

**Problema que aborda:** Proponer un método sistemático para obtener velocidades de onda de corte in situ usando análisis espectral de ondas superficiales de Rayleigh. Punto de partida conceptual de todos los métodos SASW y MASW posteriores.

**Método y flujo de trabajo:**
1. Adquisición con dos receptores a distancias crecientes — múltiples configuraciones de separación
2. Cross-power spectrum entre señales → función de coherencia → curva de velocidad de fase vs. frecuencia
3. Inversión iterativa de la curva de dispersión de Rayleigh para obtener Vs(z)
4. Validación en sitios de campo

**Instrumentación requerida:** Geófonos verticales + sismógrafo o analizador espectral + fuente impulsiva. Hardware similar al MASW pero la operación requiere múltiples repeticiones para distintas separaciones.

**Limitaciones reportadas:**
- Requiere múltiples configuraciones de receptor con disparos separados → proceso lento y operacionalmente tedioso
- Intensivo en mano de obra y tiempo de campo
- Asume modo fundamental dominante
- Sin supresión eficiente de ruido coherente (no tiene los beneficios del análisis multicanal de MASW)

**Conclusiones clave para la tesis:**
Paper fundacional del SASW. Primer uso sistemático del análisis espectral para obtener curvas de dispersión in situ. Demostró viabilidad de estimar Vs(z) de manera no invasiva con equipamiento relativamente simple. MASW (Park 1999) fue desarrollado como mejora operativa directa de este método: arreglo multicanal elimina las limitaciones de eficiencia de SASW. Esta comparación es argumento clave para justificar la elección de MASW en la tesis.

**Relevancia para tesis:** **Alta (contexto histórico obligatorio)** — lectura de referencia para la sección de antecedentes. No se usa directamente en diseño experimental pero contextualiza y motiva la elección metodológica.

**Factibilidad económica:** Media — mismo hardware básico que MASW, pero operacionalmente más lento e intensivo. MASW supera estas limitaciones conservando el mismo equipamiento económico.

**Observaciones:** Sin DOI (proceedings de 1984, preDigital). PDF no disponible en acceso libre — volumen en bibliotecas físicas solamente. Ver también precursor: Nazarian, Stokoe & Hudson (1983), *Transportation Research Record* 930, pp. 38–45 — PDF libre en TRB: https://onlinepubs.trb.org/Onlinepubs/trr/1983/930/930-006.pdf

**Categoría:** core

---

### 004 — Louie (2001) — ReMi (Refraction Microtremor)

| Campo | Valor |
|-------|-------|
| **Título** | Faster, Better: Shear-Wave Velocity to 100 Meters Depth from Refraction Microtremor Arrays |
| **Autores** | John N. Louie |
| **Año** | 2001 |
| **Idioma** | Inglés |
| **DOI** | `10.1785/0120000098` |
| **Landing page** | https://pubs.geoscienceworld.org/bssa/article/91/2/347-364/340756 |
| **HTML (mirror U. Memphis)** | http://www.ce.memphis.edu/7137/PDFs/ReMi/1.%20refr.html |
| **PDF local** | *(no descargado — BSSA paywalled)* |
| **Tipo de publicación** | Artículo en revista peer-reviewed (*Bulletin of the Seismological Society of America*, Vol. 91, No. 2, pp. 347–364) |
| **Calidad de fuente** | Alta (DOI verificado CrossRef; >515 citas CrossRef; >1000 citas en literatura) |

**Método principal:** ReMi — Refraction Microtremor
**Método secundario:** Análisis slowness-frequency (p-f) pasivo; ondas de Rayleigh
**Sensor:** Geófonos estándar (arrays de refracción sísmica — los mismos usados en MASW)
**Adquisición:** Pasiva (microtremores ambientales — tráfico, viento, actividad industrial)
**Geometría:** Lineal (arrays de refracción sísmica estándar, 12–48 canales típico)
**Tipo de sitio:** Campo (múltiples sitios en California y Nevada, USA)

**Problema que aborda:** Proponer un método pasivo y económico para obtener Vs hasta 100 m usando arrays de geófonos estándar de refracción sísmica, sin necesidad de fuente activa. El nombre "Refraction Microtremor" proviene de usar el mismo equipamiento y geometría que la sísmica de refracción clásica, pero analizando los microtremores ambientales en el dominio slowness-frecuencia.

**Método y flujo de trabajo:**
1. Adquisición de registros de microtremores con array lineal de geófonos (sin fuente activa)
2. Transformada de Radon → dominio slowness-frecuencia (p-f)
3. Identificación de la curva de dispersión de Rayleigh en el espectro p-f
4. Picking manual de la curva de dispersión experimental
5. Inversión 1D para obtener Vs(z) — compatible con herramientas MASW (ej. SurfSeis)
6. Validación con borehole y SCPT en múltiples sitios de campo

**Instrumentación requerida:** Geófonos estándar (los mismos de sísmica de refracción o MASW) + sismógrafo multicanal. Sin fuente activa → costo operativo muy reducido. Adquisición en pocos minutos.

**Limitaciones reportadas:**
- Depende de ruido ambiental con suficiente energía en la banda de frecuencias de interés (puede fallar en sitios muy silenciosos)
- El análisis p-f puede ser más complejo de interpretar que el f-k activo de MASW
- Menor control sobre la fuente de energía → mayor incertidumbre en picking de curva de dispersión

**Conclusiones clave para la tesis:**
ReMi permite obtener perfiles Vs de buena calidad hasta 100 m con el mismo equipamiento de geófonos de bajo costo usado en MASW, sin necesidad de fuente activa. Validado contra borehole y SCPT en múltiples sitios. La compatibilidad con equipamiento de refracción sísmica estándar es clave: significa que con el mismo arreglo se pueden hacer tanto MASW activo como ReMi pasivo, maximizando la información geotécnica obtenida. Muy útil para situaciones donde la fuente activa no es práctica o accesible.

**Relevancia para tesis:** **Alta** — método pasivo complementario al MASW. Usa mismo equipamiento → sin costo adicional. Permite validación cruzada y extensión de profundidad de investigación. Relevante para diseño experimental en contextos con restricciones.

**Factibilidad económica:** Muy alta — no requiere fuente activa; mismo equipamiento geófonos + sismógrafo que MASW; tiempo de adquisición mínimo (pocos minutos de registro). Ideal para contextos con restricciones presupuestarias.

**Observaciones:** DOI verificado via CrossRef (10.1785/0120000098). PDF no descargado — BSSA requiere suscripción. HTML completo disponible en mirror U. Memphis. ResearchGate tiene PDF pero requiere login.

**Categoría:** core

---

### 005 — Aki (1957) — SPAC fundacional

| Campo | Valor |
|-------|-------|
| **Título** | Space and Time Spectra of Stationary Stochastic Waves, with Special Reference to Microtremors |
| **Autores** | Keiiti Aki |
| **Año** | 1957 |
| **Idioma** | Inglés |
| **DOI (JaLC)** | `10.15083/0000033938` |
| **Landing page (UTokyo)** | https://repository.dl.itc.u-tokyo.ac.jp/records/33938 |
| **PDF (UTokyo, open access)** | https://repository.dl.itc.u-tokyo.ac.jp/record/33938/files/ji0353001.pdf |
| **PDF local** | `research/papers/pdf/Aki1957_SPAC.pdf` |
| **Tipo de publicación** | Artículo en revista peer-reviewed (*Bulletin of the Earthquake Research Institute, University of Tokyo*, Vol. 35, No. 3, pp. 415–456) |
| **Calidad de fuente** | Alta (repositorio institucional UTokyo; DOI JaLC registrado; fundacional del campo) |

**Método principal:** SPAC — Spatial Autocorrelation
**Método secundario:** Análisis espectral espacio-temporal de ondas estocásticas
**Sensor:** Sismómetros / geófonos en arreglo
**Adquisición:** Pasiva (microtremores ambientales)
**Geometría:** Arreglo circular (formulación original) — adaptable a otras geometrías
**Tipo de sitio:** Campo (Japón)

**Problema que aborda:** Desarrollar el marco teórico y experimental para analizar el campo de ondas estocásticas (microtremores) mediante autocorrelación espacial, con el objetivo de extraer la curva de dispersión de ondas de Rayleigh sin fuente activa. Es la piedra fundacional de todos los métodos pasivos basados en coherencia espacial.

**Método y flujo de trabajo:**
1. Registro simultáneo de microtremores en múltiples sensores en arreglo circular
2. Cálculo de la función de autocorrelación espacial ρ(r, ω) entre pares de sensores a distancia r
3. Relación teórica: ρ(r, ω) = J₀(ω·r/c(ω)) donde J₀ es la función de Bessel de orden cero y c(ω) la velocidad de fase
4. Ajuste de la función de Bessel → extracción de c(ω) → curva de dispersión experimental
5. Inversión de la curva de dispersión para obtener Vs(z) (desarrollada en trabajos posteriores)

**Instrumentación requerida:** Sismómetros o geófonos en arreglo (mínimo centro + anillo exterior). Hardware básico de sísmica pasiva. Sin fuente activa — los microtremores ambientales son la señal.

**Limitaciones reportadas:**
- Requiere geometría de arreglo específica para muestrear correctamente la función de coherencia espacial
- Supone isotropía del campo de ruido (microtremores llegando de todas direcciones con igual probabilidad)
- Sensible a condiciones de homogeneidad del campo de ruido → puede fallar en sitios con fuente dominante direccional

**Conclusiones clave para la tesis:**
Establece la base teórica completa del SPAC: la autocorrelación espacial de microtremores está relacionada con la función de Bessel J₀, permitiendo extraer la velocidad de fase de ondas de Rayleigh sin fuente activa. La elegancia matemática del resultado (la curva de coherencia tiene forma de J₀) hace que sea reproducible con equipamiento mínimo. Toda la familia de métodos SPAC, ESAC, MSPAC, ReMi y las versiones modernas de análisis de ruido ambiental derivan directamente de este trabajo.

**Relevancia para tesis:** **Alta (fundacional)** — comprenderlo es esencial para la revisión del estado del arte. Aunque no se use SPAC directamente en el experimento, provee el marco teórico que subyace a todos los métodos pasivos de ondas superficiales.

**Factibilidad económica:** Alta — mismo tipo de sensor que MASW/ReMi. Arreglo circular adaptable con geófonos estándar. No requiere fuente activa → costo operativo mínimo.

**Observaciones:** DOI JaLC: `10.15083/0000033938`. PDF descargado desde repositorio institucional UTokyo (2.2 MB, acceso libre). CiNii Research ID: 1573950399959666816. Paper de 1957 — sin CrossRef DOI. Fundacional del SPAC — citado en prácticamente toda la literatura de métodos pasivos de ondas superficiales.

**Categoría:** core

---

### 006 — Foti et al. (2018) — Guías InterPACIFIC para ondas superficiales

| Campo | Valor |
|-------|-------|
| **Título** | Guidelines for the good practice of surface wave analysis: a product of the InterPACIFIC project |
| **Autores** | S. Foti, F. Hollender, F. Garofalo, D. Albarello, M. Asten, P.-Y. Bard, C. Comina, C. Cornou, B. Cox, G. Di Giulio, T. Forbriger, K. Hayashi, E. Lunedei, A. Martin, D. Mercerat, M. Ohrnberger, V. Poggi, F. Renalier, D. Sicilia, V. Socco |
| **Año** | 2018 |
| **Idioma** | Inglés |
| **DOI** | `10.1007/s10518-017-0206-7` |
| **Landing page** | https://link.springer.com/article/10.1007/s10518-017-0206-7 |
| **PDF (HAL, open access CC BY 4.0)** | https://hal.science/hal-01693204v1/file/10.1007%252Fs10518-017-0206-7.pdf |
| **PDF local** | `research/papers/pdf/Foti2018_InterPACIFIC_guidelines.pdf` |
| **Tipo de publicación** | Artículo en revista peer-reviewed (*Bulletin of Earthquake Engineering*, Vol. 16, No. 6, pp. 2367–2420) |
| **Calidad de fuente** | Alta (open access CC BY 4.0; DOI CrossRef verificado; 405 citas CrossRef) |

**Métodos cubiertos:** MASW activo, SPAC, ESAC, ReMi, beamforming f-k, análisis de elipticidad H/V
**Sensor:** Geófonos, acelerómetros, velocímetros (cualquier sensor de campo estándar)
**Adquisición:** Activa y pasiva (ambas cubiertas)
**Geometría:** Múltiples (lineal, circular, 2D)
**Tipo de sitio:** Campo — múltiples sitios de referencia en Europa, USA y Japón (ejercicio InterPACIFIC)

**Problema que aborda:** Sistematizar las buenas prácticas para análisis de ondas superficiales a partir de un ejercicio comparativo entre 14 laboratorios internacionales. El proyecto InterPACIFIC (Interpacific project for site characterization) identificó las fuentes principales de incertidumbre en la cadena adquisición → procesamiento → inversión y produjo recomendaciones aplicables a cualquier contexto.

**Contenido principal:**
1. Guías para diseño de arreglos (separación, longitud, geometría)
2. Criterios de calidad para curvas de dispersión experimentales
3. Recomendaciones para picking y estimación de incertidumbre
4. Estrategias de inversión: local vs. global, parametrización del modelo
5. Protocolos para validación cruzada entre métodos
6. Análisis de fuentes de incertidumbre en cada etapa

**Instrumentación requerida:** Cualquier sensor sísmico de campo estándar. Las guías son independientes del nivel de sofisticación del equipo.

**Limitaciones reportadas:**
- La incertidumbre en la inversión está dominada por decisiones del operador (picking, parametrización) más que por ruido instrumental
- La no-unicidad de la inversión 1D es una limitación inherente — múltiples perfiles de Vs pueden ajustar la misma curva de dispersión
- Las diferencias entre laboratorios en el mismo sitio evidencian la subjetividad residual incluso con guías

**Conclusiones clave para la tesis:**
La comparación entre métodos activos y pasivos en los mismos sitios mejora significativamente la confianza en los resultados. Las guías recomiendan explícitamente: (1) múltiples inversiones con diferentes modelos iniciales, (2) análisis de sensibilidad del modelo, (3) validación cruzada entre métodos cuando sea posible. Los principios son aplicables con cualquier nivel de equipamiento y son directamente trasladables a un contexto de bajo presupuesto como Paraguay.

**Relevancia para tesis:** **Alta** — es la referencia metodológica estándar actual para justificar el protocolo de la tesis. Citable directamente para justificar decisiones de diseño experimental, procesamiento e inversión.

**Factibilidad económica:** Alta — las guías son metodológicas, no instrumentales. Aplicables con equipamiento básico.

**Observaciones:** Open access CC BY 4.0. PDF descargado desde HAL archive (8.6 MB, versión publicada). DOI: 10.1007/s10518-017-0206-7. Proyecto InterPACIFIC: 14 laboratorios de Europa, USA y Japón. 405 citas CrossRef.

**Categoría:** core

---

### 007 — Garofalo et al. (2016) — InterPACIFIC Part I: Intra-comparación de métodos de ondas superficiales

| Campo | Valor |
|-------|-------|
| **Título** | InterPACIFIC project: Comparison of invasive and non-invasive methods for seismic site characterization. Part I: Intra-comparison of surface wave methods |
| **Autores** | F. Garofalo, S. Foti, F. Hollender, P.Y. Bard, C. Cornou, B.R. Cox, M. Ohrnberger, D. Sicilia, M. Asten, G. Di Giulio, T. Forbriger, B. Guillier, K. Hayashi, A. Martin, S. Matsushima, D. Mercerat, V. Poggi, H. Yamanaka |
| **Año** | 2016 |
| **Idioma** | Inglés |
| **DOI** | `10.1016/j.soildyn.2015.12.010` |
| **Landing page** | https://www.sciencedirect.com/science/article/pii/S026772611500319X |
| **PDF** | *(no disponible — Elsevier closed)* |
| **PDF local** | *(no descargado)* |
| **Tipo de publicación** | Artículo en revista peer-reviewed (*Soil Dynamics and Earthquake Engineering*, Vol. 82, pp. 222–240) |
| **Calidad de fuente** | Alta (DOI CrossRef verificado; 180 citas CrossRef; Proyecto InterPACIFIC) |

**Métodos comparados:** MASW activo, SPAC, ESAC, MSPAC, ReMi, f-k beamforming
**Sensor:** Geófonos, acelerómetros, velocímetros (diferentes laboratorios usaron diferentes sensores)
**Adquisición:** Activa y pasiva — ambas cubiertas en el ejercicio comparativo
**Tipo de sitio:** Campo — sitios de referencia con mediciones de borehole disponibles (Europa: Italia, Francia, Suiza)

**Problema que aborda:** Cuantificar la variabilidad en los resultados de métodos de ondas superficiales cuando múltiples laboratorios independientes procesan los mismos datos en los mismos sitios. Parte del proyecto InterPACIFIC que usa sitios de referencia con borehole para validación.

**Método y flujo de trabajo:**
1. Adquisición de datos en sitios de referencia por múltiples laboratorios
2. Cada laboratorio aplica su propio flujo de trabajo (procesamiento + inversión)
3. Comparación de curvas de dispersión obtenidas entre laboratorios
4. Comparación de perfiles Vs(z) obtenidos
5. Evaluación de variabilidad inter-laboratorio en cada etapa

**Instrumentación requerida:** Varía por laboratorio — desde geófonos básicos hasta velocímetros de banda ancha. Los resultados muestran que las diferencias entre instrumentos son menores que las diferencias entre operadores.

**Limitaciones reportadas:**
- Variabilidad inter-laboratorio significativa, especialmente en la etapa de inversión
- Las diferencias entre métodos activos y pasivos son mayores para sitios geológicamente complejos
- Mayor dispersión en inversión que en procesamiento → la parametrización del modelo es la principal fuente de incertidumbre

**Conclusiones clave para la tesis:**
Los métodos de ondas superficiales convergen bien entre sí cuando se aplican correctamente. La variabilidad en las inversiones revela que el operador tiene un impacto significativo. MASW activo y métodos pasivos (SPAC, ReMi) dan resultados comparables en sitios simples. **Implicación clave para la tesis:** la incertidumbre instrumental es menor que la incertidumbre del operador → justifica enfocarse en un buen protocolo metodológico más que en equipamiento sofisticado.

**Relevancia para tesis:** **Alta** — permite fundamentar la comparabilidad entre métodos y cuantificar fuentes de incertidumbre. Companion de Foti et al. (2018). Justifica por qué validar contra borehole cuando sea posible y por qué documentar bien el protocolo metodológico.

**Factibilidad económica:** Media para el ejercicio completo (requirió 14 laboratorios); las conclusiones y recomendaciones son aplicables a cualquier configuración de bajo presupuesto.

**Observaciones:** DOI: 10.1016/j.soildyn.2015.12.010. SDEE Vol.82 pp.222-240. 180 citas CrossRef. PDF no disponible (Elsevier closed, Unpaywall confirmado). Ver también Part II: DOI `10.1016/j.soildyn.2015.12.009` (comparación superficie vs. borehole; 138 citas). Companion de entrada 006.

**Categoría:** core

---

### 008 — Socco & Strobbia (2004) — Tutorial de métodos de ondas superficiales

| Campo | Valor |
|-------|-------|
| **Título** | Surface-wave method for near-surface characterization: a tutorial |
| **Autores** | L.V. Socco, C. Strobbia |
| **Año** | 2004 |
| **Idioma** | Inglés |
| **DOI** | `10.3997/1873-0604.2004015` |
| **Landing page (EAGE EarthDoc)** | https://www.earthdoc.org/content/journals/10.3997/1873-0604.2004015 |
| **PDF** | *(no disponible en acceso libre — EAGE paywalled)* |
| **PDF local** | *(no descargado)* |
| **Tipo de publicación** | Artículo en revista peer-reviewed (*Near Surface Geophysics*, Vol. 2, No. 4, pp. 165–185) |
| **Calidad de fuente** | Alta (DOI CrossRef verificado; 306 citas CrossRef; Politecnico di Torino) |

**Método principal:** Tutorial de métodos de ondas superficiales (MASW, SASW, SPAC)
**Método secundario:** Análisis de dispersión de ondas superficiales; inversión 1D
**Sensor:** Geófonos, velocímetros (cualquier sensor de campo estándar)
**Adquisición:** Activa y pasiva — ambas cubiertas
**Geometría:** Múltiples (lineal, circular)
**Tipo de sitio:** Sintético + campo (tutorial)

**Problema que aborda:** Proveer una guía comprehensiva y práctica sobre el método de ondas superficiales para caracterización del subsuelo. Cubre todo el flujo de trabajo desde la teoría básica hasta la implementación experimental, incluyendo criterios para diseño de arreglos, procesamiento de datos, inversión y análisis de incertidumbre.

**Contenido principal:**
1. Marco teórico: ondas de Rayleigh, dispersión, relación con Vs(z)
2. Diseño de arreglo: efectos near-field, far-field, aliasing espacial
3. Parámetros de adquisición: frecuencia de geófonos, separación, longitud del arreglo
4. Procesamiento: f-k, SPAC, análisis de coherencia, picking de curva de dispersión
5. Inversión: métodos locales vs. globales, parametrización del modelo, análisis de sensibilidad
6. Fuentes de error y limitaciones en cada etapa

**Instrumentación requerida:** Cualquier sistema de geófonos estándar. Las guías son independientes del nivel de instrumentación. El tutorial discute qué parámetros mínimos son necesarios para un resultado confiable.

**Limitaciones reportadas:**
- Supone estratificación horizontal 1D (misma limitación que todos los métodos 1D)
- No-unicidad inherente de la inversión
- Dependencia del modelo inicial en inversión local
- Dificultades con perfiles inversamente dispersivos (capa rígida superficial)

**Conclusiones clave para la tesis:**
Tutorial que sistematiza el estado del arte de los métodos de ondas superficiales hasta 2004. Provee criterios cuantitativos para el diseño del arreglo (separación mínima entre geófonos, offset mínimo, longitud del arreglo) que son directamente aplicables al diseño experimental de la tesis. Es una referencia clave para justificar las decisiones de adquisición sin necesidad de citar múltiples papers separados.

**Relevancia para tesis:** **Alta** — tutorial de referencia para la metodología completa. Citable directamente para justificar decisiones de diseño experimental y procesamiento. Complementa y precede a Foti et al. (2018).

**Factibilidad económica:** Alta — las guías son metodológicas e independientes del costo del equipamiento. Aplicable íntegramente a un contexto de bajo presupuesto.

**Observaciones:** DOI corregido durante la búsqueda (DOI incorrecto inicial → verificado como `10.3997/1873-0604.2004015`). Near Surface Geophysics Vol.2 No.4 pp.165-185. 306 citas CrossRef. PDF no disponible — EAGE paywalled. IRIS Polito requiere login institucional. ResearchGate requiere login.

**Categoría:** core

---

### 009 — Xia et al. (2002) — Validación MASW contra borehole

| Campo | Valor |
|-------|-------|
| **Título** | Comparing shear-wave velocity profiles inverted from multichannel surface wave with borehole measurements |
| **Autores** | J. Xia, R.D. Miller, C.B. Park, J.A. Hunter, J.B. Harris, J. Ivanov |
| **Año** | 2002 |
| **Idioma** | Inglés |
| **DOI** | `10.1016/S0267-7261(02)00008-8` |
| **Landing page** | https://linkinghub.elsevier.com/retrieve/pii/S0267726102000088 |
| **PDF** | *(no disponible — Elsevier paywalled)* |
| **PDF local** | *(no descargado)* |
| **Tipo de publicación** | Artículo en revista peer-reviewed (*Soil Dynamics and Earthquake Engineering*, Vol. 22, No. 3, pp. 181–190) |
| **Calidad de fuente** | Alta (DOI CrossRef verificado; 223 citas CrossRef; grupo KGS) |

**Método principal:** MASW — validación contra borehole
**Método secundario:** Rayleigh wave inversion (Xia 1999); comparación con medición invasiva
**Sensor:** Geófonos verticales 4.5 Hz (mismo equipamiento Park 1999)
**Adquisición:** Activa impulsiva (martillo)
**Geometría:** Arreglo lineal multicanal
**Tipo de sitio:** Campo — múltiples sitios en Kansas (USA) y Canadá con borehole disponible

**Problema que aborda:** Validar sistemáticamente la precisión de los perfiles Vs(z) obtenidos por MASW comparando contra mediciones independientes de borehole (crosshole o downhole). El objetivo es cuantificar el acuerdo entre el método no-invasivo (MASW) y la referencia invasiva (borehole).

**Método y flujo de trabajo:**
1. Adquisición MASW en sitios con borehole disponible (mismo sitio o muy cercano)
2. Procesamiento e inversión estándar (Park 1999 + Xia 1999)
3. Comparación directa de perfiles Vs(z) de MASW vs. borehole capa por capa
4. Cuantificación del error relativo por capa

**Instrumentación requerida:** Geófonos 4.5 Hz + sismógrafo 24 canales + martillo — exactamente el mismo equipamiento de los papers fundacionales 001 y 002.

**Limitaciones reportadas:**
- La comparación depende de que el borehole esté en el mismo punto o muy cercano al perfil MASW
- La resolución del MASW decrece con la profundidad → mayor incertidumbre en capas profundas
- Supone estratificación horizontal 1D
- Error crece si el sitio tiene variabilidad lateral

**Conclusiones clave para la tesis:**
Los perfiles Vs de MASW concuerdan bien con los de borehole: errores típicos menores al 15% en la mayoría de las capas. La concordancia es mejor en las capas superficiales y empeora con la profundidad (consecuencia de la resolución decreciente del método). **Implicación directa para la tesis:** MASW produce resultados confiables sin necesidad de perforación previa, lo que lo hace especialmente valioso en contextos donde el borehole no es accesible por costo o logística.

**Relevancia para tesis:** **Alta** — validación directa del método MASW. Citable para justificar que el método produce resultados confiables sin necesidad de borehole, argumento clave para la aplicación en Paraguay.

**Factibilidad económica:** Alta — mismo equipamiento económico de papers 001 y 002. La validación demuestra confiabilidad del método con hardware básico.

**Observaciones:** DOI: `10.1016/S0267-7261(02)00008-8`. SDEE Vol.22 No.3 pp.181-190. 223 citas CrossRef. PDF no disponible (Elsevier paywalled, Unpaywall: closed). Mismo grupo KGS (Xia + Miller + Park). Compañero temático de entradas 001 y 002.

**Categoría:** core

---

### 010 — Park et al. (2007) — MASW activo y pasivo: review práctico

| Campo | Valor |
|-------|-------|
| **Título** | Multichannel analysis of surface waves (MASW)—active and passive methods |
| **Autores** | Choon B. Park, Richard D. Miller, Jianghai Xia, Julian Ivanov |
| **Año** | 2007 |
| **Idioma** | Inglés |
| **DOI** | `10.1190/1.2431832` |
| **Landing page** | https://library.seg.org/doi/10.1190/1.2431832 |
| **PDF (KGS, open access)** | https://www.kgs.ku.edu/software/surfseis/Publications/ParkEtAl2007.pdf |
| **PDF local** | `research/papers/pdf/Park2007_MASW_active_passive.pdf` |
| **Tipo de publicación** | Artículo en revista peer-reviewed (*The Leading Edge*, Vol. 26, No. 1, pp. 60–64) |
| **Calidad de fuente** | Alta (DOI SEG CrossRef verificado; 258 citas CrossRef; KGS open access) |

**Método principal:** MASW activo y pasivo — comparación y complementariedad
**Método secundario:** Análisis f-k (activo); análisis p-f/f-k (pasivo); ondas de Rayleigh
**Sensor:** Geófonos verticales estándar (mismos para ambos modos)
**Adquisición:** Activa impulsiva (martillo) + pasiva (ruido ambiental) — mismo arreglo
**Geometría:** Lineal multicanal estándar
**Tipo de sitio:** Campo (múltiples sitios KGS, Kansas)

**Problema que aborda:** Revisar y comparar las dos variantes del MASW — activo (fuente controlada) y pasivo (ruido ambiental) — describiendo sus diferencias en adquisición, procesamiento, profundidad de investigación y casos de uso. Demostrar que el mismo equipamiento básico sirve para ambos modos.

**Diferencias clave activo vs. pasivo:**

| Característica | MASW activo | MASW pasivo |
|----------------|-------------|-------------|
| Fuente | Martillo / explosivo | Ruido ambiental |
| Profundidad típica | ~30 m | ~100+ m |
| Costo adicional | — | Ninguno |
| Control de fuente | Alto | Ninguno |
| Tiempo adquisición | Rápido (segundos) | Requiere registro (minutos) |
| Procesamiento | f-k estándar | p-f o beamforming |

**Instrumentación requerida:** Exactamente el mismo hardware que MASW activo (geófonos + sismógrafo). Sin costo adicional para agregar medición pasiva a la campaña activa.

**Limitaciones reportadas:**
- Modo pasivo depende de calidad y direccionalidad del ruido ambiental
- Modo activo limitado en profundidad por frecuencias generadas por fuente impulsiva
- Aliasing espacial en arreglos cortos con separación grande entre geófonos

**Conclusiones clave para la tesis:**
MASW activo y pasivo pueden usarse con el mismo arreglo y el mismo equipamiento. Activo: alta resolución superficial (~30 m). Pasivo: mayor profundidad (~100+ m). La combinación de ambos modos maximiza la información obtenida sin costo adicional de hardware. **Implicación directa:** en la tesis se puede justificar la combinación activo+pasivo como estrategia de bajo costo para ampliar el rango de profundidad de investigación.

**Relevancia para tesis:** **Alta** — review práctico clave del grupo KGS. Define claramente las diferencias entre modos activo y pasivo. Justifica diseño experimental combinado con mismo equipo básico.

**Factibilidad económica:** Muy alta — mismo equipamiento geófonos + sismógrafo para ambos modos. Sin inversión adicional para agregar el modo pasivo.

**Observaciones:** DOI: 10.1190/1.2431832. The Leading Edge Vol.26 No.1 pp.60-64. 258 citas CrossRef. PDF KGS open access (643 KB). Mismo grupo KGS: Park + Miller + Xia + Ivanov. Review conciso (5 páginas) de uso práctico. La KGS publica también ParkEtAl2004.pdf y ParkEtAl2005.pdf como candidatos para iteraciones futuras.

**Categoría:** core

---

### 011 — Xia et al. (2004) — MASW: inversión generalizada para mayor resolución horizontal

| Campo | Valor |
|-------|-------|
| **Título** | Increasing horizontal resolution of geophysical models by generalized inversion |
| **Autores** | Jianghai Xia, Richard D. Miller, Chao Chen, Julian Ivanov |
| **Año** | 2004 |
| **Idioma** | Inglés |
| **DOI** | `10.1190/1.1845123` |
| **Landing page** | https://library.seg.org/doi/10.1190/1.1845123 |
| **PDF (KGS, open access)** | https://www.kgs.ku.edu/software/surfseis/Publications/XiaEtAl2004_1.1845123v2.pdf |
| **PDF local** | `research/papers/pdf/Xia2004_MASW_horizontal_resolution.pdf` |
| **Tipo de publicación** | Abstract de proceedings peer-reviewed (SEG Technical Program Expanded Abstracts 2004, pp. 1437–1440) |
| **Calidad de fuente** | Alta (DOI SEG CrossRef verificado; KGS open access) |

**Método principal:** MASW con inversión generalizada 2D para aumentar resolución horizontal del modelo de Vs
**Método secundario:** Inversión generalizada multi-shot; análisis de ondas de Rayleigh
**Sensor:** Geófonos verticales estándar (mismo equipamiento que MASW convencional)
**Adquisición:** Activa impulsiva (martillo), múltiples disparos con arreglo desplazado (roll-along)
**Geometría:** Lineal multicanal — múltiples posiciones de arreglo
**Tipo de sitio:** Sintético + campo (Kansas, KGS)

**Problema que aborda:** El método MASW estándar produce un perfil 1D de Vs por posición de arreglo; la unión lateral de perfiles produce modelos 2D con resolución horizontal limitada. Este trabajo propone una inversión generalizada que usa datos de múltiples disparos simultáneamente para mejorar la resolución horizontal sin cambiar el equipamiento.

**Instrumentación requerida:** Exactamente el mismo hardware que MASW estándar (geófonos verticales + sismógrafo multicanal + martillo). Sin cambio en hardware — solo en el algoritmo de inversión.

**Limitaciones reportadas:**
- Abstract corto (4 páginas) sin validación sistemática contra borehole
- Mayor complejidad computacional que inversión 1D estándar
- Requiere mayor densidad de disparos (roll-along) para buena resolución horizontal
- Sin análisis de sensibilidad o incertidumbre detallado en este formato

**Conclusiones clave para la tesis:**
Con el mismo equipamiento básico de MASW, es posible producir modelos 2D de subsuperficie con mejor resolución horizontal usando inversión generalizada. El cambio es algorítmico, no instrumental. **Implicación:** si el presupuesto de hardware es limitado, el avance hacia caracterización 2D es posible mejorando el software de inversión, sin costo adicional en equipo.

**Relevancia para tesis:** **Media** — no es una referencia primaria de método, sino una extensión metodológica. Útil en sección de perspectivas o discusión de limitaciones de resolución del método básico.

**Factibilidad económica:** Alta en hardware (mismo equipamiento). Mayor esfuerzo computacional y operativo. La inversión 2D no requiere hardware adicional.

**Observaciones:** DOI: `10.1190/1.1845123`. SEG Technical Program Expanded Abstracts 2004, pp. 1437–1440. PDF KGS open access (272 KB). Abstract de 4 páginas. Mismo grupo KGS: Xia + Miller + Chen + Ivanov. El DOI fue inicialmente catalogado en el worklog como posible artículo de revista — CrossRef confirma que corresponde a un SEG expanded abstract. La KGS aloja el PDF bajo su colección de publicaciones de surfseis.

**Categoría:** peripheral

---

### 012 — Ayele, Woldearegay & Meten (2022) — MASW en Etiopía: caso en país en desarrollo

| Campo | Valor |
|-------|-------|
| **Título** | Multichannel Analysis of Surface Waves (MASW) to Estimate the Shear Wave Velocity for Engineering Characterization of Soils at Hawassa Town, Southern Ethiopia |
| **Autores** | Alemayehu Ayele, Kifle Woldearegay, Matebie Meten |
| **Año** | 2022 |
| **Idioma** | Inglés |
| **DOI** | `10.1155/2022/7588306` |
| **Landing page** | https://onlinelibrary.wiley.com/doi/10.1155/2022/7588306 |
| **PDF (OA, CC BY 4.0)** | https://downloads.hindawi.com/journals/ijge/2022/7588306.pdf |
| **PDF local** | No descargado (Cloudflare en Hindawi — PDF libre verificado, disponible manualmente) |
| **Tipo de publicación** | Artículo peer-reviewed (*International Journal of Geophysics*, 2022, art. 7588306, Hindawi/Wiley) |
| **Calidad de fuente** | Alta (Gold OA CC BY 4.0 verificado via CrossRef y Semantic Scholar; 14 citas) |

**Método principal:** MASW activo — estimación de Vs30 para clasificación sísmica de sitio
**Método secundario:** VES (Vertical Electrical Sounding) + SPT (Standard Penetration Test) — caracterización complementaria
**Sensor:** Geófonos verticales estándar (tipo y frecuencia no especificados en abstract — ver paper completo)
**Adquisición:** Activa impulsiva (martillo)
**Geometría:** Lineal multicanal estándar (múltiples perfiles en zona urbana)
**Tipo de sitio:** Campo — zona urbana (Hawassa Town, Etiopía del Sur)

**Problema que aborda:** Caracterización geotécnica de suelos urbanos en Hawassa Town (Etiopía del Sur) para diseño seguro de cimentaciones. El objetivo es obtener Vs30 y clasificar sísmicamente el sitio según normativas internacionales (NEHRP/ASCE 7), en un contexto de recursos limitados.

**Contexto geográfico y económico:** Hawassa Town, Etiopía del Sur — país en desarrollo. Directamente comparable al contexto de Paraguay: clima tropical/subtropical, limitaciones presupuestarias, necesidad de métodos no invasivos y accesibles para estudios geotécnicos urbanos.

**Instrumentación requerida:** Equipamiento MASW activo estándar:
- Geófonos verticales (estándar de campo)
- Sismógrafo multicanal
- Fuente impulsiva (martillo)
- Complementado con resistivímetro (VES) para correlación litológica

**Resultados principales:**
- Vs30 rango: 248.9 a 371.3 m/s
- Clasificación sísmica: Clase C y D (NEHRP)
- Near-surface soils: arenas limosas y arenas (variantes)
- Zonas de baja velocidad superficial identificadas como críticas para diseño de fundaciones

**Limitaciones reportadas:**
- Sin validación directa vs. borehole profundo
- Asume estratificación horizontal 1D
- Especificaciones detalladas de instrumentación no reportadas en abstract

**Conclusiones clave para la tesis:**
El estudio demuestra que MASW es aplicable y efectivo en contextos de países en desarrollo con recursos limitados. La metodología joint MASW+VES+SPT es completamente reproducible con equipamiento estándar y presupuesto acotado. **Implicación directa:** valida el enfoque metodológico de la tesis en un contexto socioeconómico análogo al de Paraguay. Vs30 + clasificación sísmica son resultados directamente relevantes para el objetivo de la tesis.

**Relevancia para tesis:** **Alta** — caso análogo al contexto de la tesis (país en desarrollo, MASW estándar, objetivo Vs30). Directamente citable como antecedente de aplicación del método en contextos similares al de Paraguay.

**Factibilidad económica:** Muy alta — el mismo equipamiento básico (geófonos + sismógrafo + martillo) fue usado exitosamente en Etiopía. La replicabilidad en Paraguay con el mismo setup está demostrada.

**Observaciones:** DOI: `10.1155/2022/7588306`. International Journal of Geophysics (Hindawi/Wiley) 2022, art. 7588306. Gold OA CC BY 4.0 — PDF libre disponible pero protegido por Cloudflare (no descargable automáticamente; acceso manual en https://downloads.hindawi.com/journals/ijge/2022/7588306.pdf). 14 citas Semantic Scholar. Autores afiliados a Mekelle University y Addis Ababa University (Etiopía). Primera entrada de la base de datos en contexto africano / país en desarrollo.

**Categoría:** core

---

### 013 — Olafsdottir, Erlingsson & Bessason (2020) — MASWaves: inversión Monte Carlo open-source

| Campo | Valor |
|-------|-------|
| **Título** | Open-Source MASW Inversion Tool Aimed at Shear Wave Velocity Profiling for Soil Site Explorations |
| **Autores** | Elin Asta Olafsdottir, Sigurdur Erlingsson, Bjarni Bessason |
| **Año** | 2020 |
| **Idioma** | Inglés |
| **DOI** | `10.3390/geosciences10080322` |
| **Landing page** | https://www.mdpi.com/2076-3263/10/8/322 |
| **PDF (OA, CC BY 4.0)** | https://www.mdpi.com/2076-3263/10/8/322/pdf?version=1597666181 |
| **PDF local** | No descargado (MDPI bloquea descarga automática; PDF libre CC BY 4.0 disponible manualmente) |
| **Tipo de publicación** | Artículo peer-reviewed (*Geosciences*, MDPI, Vol. 10, No. 8, art. 322) |
| **Calidad de fuente** | Alta (Gold OA CC BY 4.0 verificado via CrossRef y DOAJ; 14 citas) |

**Método principal:** Inversión Monte Carlo de curvas de dispersión MASW — herramienta open-source MASWaves (MATLAB)
**Método secundario:** Análisis de curvas de dispersión de ondas de Rayleigh; validación con datos sintéticos y de campo
**Sensor:** Geófonos verticales (campo); datos sintéticos para validación
**Adquisición:** Activa impulsiva — lineal multicanal estándar
**Tipo de sitio:** Sintético + campo (sitio geotécnico de referencia, Islandia)

**Problema que aborda:** La inversión de curvas de dispersión MASW es un problema no-único y mal condicionado: múltiples modelos de velocidad pueden ajustar los datos. El trabajo presenta una herramienta de inversión open-source basada en búsqueda Monte Carlo global que permite: (1) encontrar perfiles de Vs que ajustan las curvas de dispersión observadas, y (2) cuantificar la incertidumbre del resultado.

**Componentes del software MASWaves:**
- **MASWaves (2018, CGJ):** Procesamiento de datos de campo — extracción de imágenes de dispersión y picking de curvas
- **MASWaves Inversion (2020, este paper):** Inversión Monte Carlo — determina Vs(z) y cuantifica incertidumbre
- **maswavespy (Python, GitHub):** Versión Python open-source

**Instrumentación requerida:** Cualquier sistema MASW estándar (geófonos + sismógrafo). El software procesa datos adquiridos con cualquier configuración compatible. Sin requerimiento de hardware especializado.

**Metodología de inversión:**
- Búsqueda Monte Carlo: muestreo aleatorio sobre el espacio de parámetros del modelo
- Modela curvas de dispersión teóricas para cada modelo candidato
- Selecciona modelos cuyas curvas teóricas ajustan la curva observada
- Resultado: distribución de perfiles aceptables → cuantificación de incertidumbre

**Limitaciones reportadas:**
- Monte Carlo puede ser computacionalmente intensivo para espacios de búsqueda grandes
- Requiere parametrización inicial del modelo (número de capas, rangos de Vs)
- No aborda heterogeneidad lateral (modelo 1D)
- Necesita curva de dispersión bien definida como entrada

**Conclusiones clave para la tesis:**
La herramienta MASWaves es directamente utilizable en la tesis para procesamiento e inversión de datos MASW. Es gratuita, open-source, e implementada en MATLAB (entorno compatible con la tesis). Permite abordar la no-unicidad de la inversión de manera rigurosa. El enfoque Monte Carlo proporciona no solo el perfil de Vs sino también una medida de la incertidumbre — componente esencial para una tesis defensible. **Implicación directa:** citable como herramienta de procesamiento de datos y como referencia para el tratamiento de la no-unicidad en la inversión.

**Relevancia para tesis:** **Alta** — software directamente utilizable + referencia metodológica para la inversión. Compañero del paper 2018 (procesamiento). Justifica decisiones de implementación en la tesis.

**Factibilidad económica:** Muy alta — completamente gratuito. Disponible en MATLAB (licencia académica) y Python (maswavespy en PyPI + GitHub, sin costo).

**Observaciones:** DOI: `10.3390/geosciences10080322`. Geosciences MDPI Vol.10 No.8 art.322. Gold OA CC BY 4.0 (CrossRef + DOAJ). PDF disponible en MDPI (acceso manual) — no descargable automáticamente. 14 citas Semantic Scholar. Universidad de Islandia. **Compañero:** Olafsdottir et al. 2018, Canadian Geotechnical Journal, DOI 10.1139/cgj-2016-0302 (procesamiento MASW — paywalled, ver iteración futura). **Software:** https://uni.hi.is/eao4/ (MATLAB) y https://github.com/Mazvel/maswavespy (Python/PyPI).

**Categoría:** core

---

### 014 — Wathelet et al. (2020) — Geopsy: software open-source para vibraciones ambientales

| Campo | Valor |
|-------|-------|
| **Título** | Geopsy: A User-Friendly Open-Source Tool Set for Ambient Vibration Processing |
| **Autores** | Marc Wathelet, Jean-Luc Chatelain, Cécile Cornou, Giuseppe Di Giulio, Bertrand Guillier, Matthias Ohrnberger, Alexandros Savvaidis |
| **Año** | 2020 |
| **Idioma** | Inglés |
| **DOI** | `10.1785/0220190360` |
| **Landing page** | https://pubs.geoscienceworld.org/ssa/srl/article-abstract/91/3/1878/583456/ |
| **PDF** | No disponible (HAL registrado pero sin PDF depositado; paywalled en SRL) |
| **PDF local** | — |
| **Tipo de publicación** | Artículo peer-reviewed (*Seismological Research Letters*, Vol. 91, No. 3, pp. 1878–1889) |
| **Calidad de fuente** | Alta (DOI CrossRef verificado; 343 citas Semantic Scholar; referencia estándar del software) |

**Método principal:** Procesamiento completo de vibraciones ambientales — HVSR, arrays, curvas de dispersión — software open-source Geopsy
**Método secundario:** SPAC, ESAC, f-k beamforming, inversión de curvas de dispersión (neighbourhood algorithm)
**Sensor:** Velocímetros / geófonos / acelerómetros 3C (desde estación única hasta arrays)
**Adquisición:** Pasiva (ruido ambiental) — sin fuente activa
**Geometría:** Estación única (HVSR) o arrays (circular, lineal, 2D)

**Problema que aborda:** Proveer una herramienta de software unificada, gratuita y de código abierto para el procesamiento completo de datos de vibraciones ambientales en caracterización de sitio. Cubre desde la adquisición de datos hasta la producción de figuras de publicación, integrando todos los módulos de análisis (HVSR, array processing, inversión).

**Funcionalidades de Geopsy:**

| Módulo | Función |
|--------|---------|
| HVSR | H/V spectral ratio — frecuencia de resonancia fundamental |
| SPAC/ESAC | Spatial Autocorrelation — dispersión Rayleigh/Love |
| f-k beamforming | Análisis frecuencia-wavenumber — curvas de dispersión |
| Inversión | Neighbourhood algorithm — Vs(z) + incertidumbre |
| Exportación | Figuras de calidad de publicación |

**Instrumentación requerida:** Cualquier sensor 3C (velocímetro, geófono, acelerómetro). Para HVSR: 1 sensor 3C solo. Para arrays: múltiples sensores en configuración circular/lineal/2D. Compatible con cualquier sistema de adquisición que produzca datos en formato estándar (SEG-Y, MiniSEED, etc.).

**Limitaciones reportadas:**
- Requiere arrays para obtener curvas de dispersión (no aplica a estación única)
- Calidad del resultado depende de la calidad del ruido ambiental en el sitio
- Más enfocado en procesamiento pasivo que activo
- La inversión con neighbourhood algorithm requiere parametrización inicial

**Conclusiones clave para la tesis:**
Geopsy es el software de referencia para métodos pasivos de caracterización de sitio. Es gratuito, multiplataforma, y tiene una comunidad activa. Complementa MASWaves (entrada 013): mientras MASWaves es más específico para MASW activo en MATLAB, Geopsy cubre el espectro pasivo (ReMi, SPAC, HVSR) con una interfaz más amplia. **Implicación directa:** citable como herramienta de software para el procesamiento de datos pasivos si la tesis incluye mediciones de ruido ambiental además del MASW activo.

**Relevancia para tesis:** **Alta** — software directamente utilizable + referencia obligada para citar en metodología de procesamiento. 343 citas confirma su posición como estándar del campo.

**Factibilidad económica:** Muy alta — completamente gratuito (GPL v3), multiplataforma (Windows, Linux, macOS), sin requerimiento de hardware adicional. Disponible en https://www.geopsy.org.

**Observaciones:** DOI: `10.1785/0220190360`. Seismological Research Letters 91(3):1878-1889. Paywalled en SRL — HAL registrado pero sin archivo PDF depositado. 343 citas Semantic Scholar. Geopsy en desarrollo desde 2005, originado en ISTerre Grenoble + proyecto europeo SESAME/NERIES. **Compañero funcional:** MASWaves (entrada 013 — más enfocado en MASW activo con MATLAB). **Software:** https://www.geopsy.org. Descargar manualmente el paper desde https://pubs.geoscienceworld.org (requiere suscripción) o solicitar a autores vía HAL.

**Categoría:** core

---

### 015 — Moffat, Correia & Pastén (2016) — MASW vs. downhole en Chile: validación Vs30

| Campo | Valor |
|-------|-------|
| **Título** | Comparison of mean shear wave velocity of the top 30 m using downhole, MASW and bender elements methods |
| **Título (español)** | Comparación del promedio de la velocidad de onda de corte en los primeros 30 m usando ensayos downhole, MASW y bender elements |
| **Autores** | Ricardo Moffat (UAI), Nicolle Correia (U. Chile), César Pastén (U. Chile) |
| **Año** | 2016 |
| **Idioma** | Bilingüe (español + inglés) |
| **DOI** | `10.4067/S0718-28132016000200001` |
| **Landing page** | https://www.scielo.cl/scielo.php?pid=S0718-28132016000200001&script=sci_arttext |
| **PDF (SciELO OA)** | https://www.scielo.cl/pdf/oyp/n20/art01.pdf |
| **PDF local** | `research/papers/pdf/Moffat2016_Vs30_MASW_downhole_Chile.pdf` (3.4 MB) |
| **Tipo de publicación** | Artículo peer-reviewed (*Obras y Proyectos*, No. 20, pp. 6–15, UCSC Chile) |
| **Calidad de fuente** | Alta (OA CC BY-NC 4.0 SciELO Chile; DOI CrossRef verificado; revista arbitrada indexada) |

**Método principal:** MASW activo — validación de perfiles Vs30 contra ensayo downhole invasivo
**Método secundario:** Bender elements (laboratorio); análisis f-k con Geopsy; inversión de curva de dispersión
**Sensor:** **12 geófonos verticales de 4.5 Hz** — configuración estándar y económica
**Adquisición:** Activa impulsiva (martillo); 5 repeticiones por sitio
**Geometría:** Lineal multicanal — 12 receptores
**Tipo de sitio:** Campo — estaciones sísmicas en Chile central con datos de sondaje existentes

**Problema que aborda:** ¿Puede el MASW reemplazar al ensayo downhole (invasivo y costoso) para la clasificación sísmica de suelos mediante Vs30? Compara los tres métodos en sitios reales de Chile central donde existe información de sondaje como referencia independiente.

**Configuración de campo (Tabla 1 del paper):**
- **Geófonos:** 12 sensores verticales de 4.5 Hz de frecuencia
- **Análisis:** f-k con Geopsy
- **Repeticiones:** 5 ensayos MASW por sitio
- **Profundidad objetivo:** zmax ~20–30 m
- **Software:** Geopsy (ver entrada 014) para curvas de dispersión

**Sitios estudiados:** Maipú, Peñalolén, Casablanca, Melipilla, Llolleo — Chile central

**Resultados clave:**

| Sitio | Vs30 MASW | Vs30 Downhole | Diferencia |
|-------|-----------|---------------|------------|
| Llolleo | ~265 m/s | ~227 m/s | ~17% |
| Maipú | Similar | Similar | Baja |
| Melipilla | Mayor diferencia (alto contraste impedancia) | — | Mayor |

**Limitaciones reportadas:**
- Mayor discrepancia en sitios con alto contraste de impedancia entre capas (Melipilla)
- No especifica número de capas del modelo de inversión
- Bender elements solo en laboratorio — no siempre disponible

**Conclusiones clave para la tesis:**
Los perfiles Vs de MASW activo y ensayos downhole son similares hasta 30 m. Con buena metodología, MASW produce la misma clasificación sísmica del suelo que el ensayo invasivo. **Implicación directa:** justifica usar MASW como método no-invasivo de bajo costo en lugar de perforación + downhole. Validación en contexto latinoamericano (Chile), con geófonos 4.5 Hz y Geopsy — exactamente el setup más accesible para la tesis en Paraguay.

**Relevancia para tesis:** **Alta** — validación regional directamente citable, datos de configuración específicos (12 geófonos 4.5 Hz), uso de Geopsy, contexto sudamericano. Primer paper latinoamericano con PDF en la base.

**Factibilidad económica:** Muy alta — 12 geófonos 4.5 Hz (bajo costo), martillo, Geopsy (libre). Configuración completamente replicable en Paraguay.

**Observaciones:** DOI: `10.4067/S0718-28132016000200001`. Obras y Proyectos No.20 pp.6-15. UCSC Chile. OA CC BY-NC 4.0 vía SciELO Chile. PDF descargado (3.4 MB, 10 pp). 1 cita Semantic Scholar (normal para revista regional latinoamericana). Autores: U. Adolfo Ibáñez + U. Chile. Bilingüe. Cita Park et al. 1999 y Foti et al. 2014. Usa **Geopsy** para análisis f-k — **ver entrada 014**.

**Categoría:** core

---

### 016 — Alhuay-León & Trejo-Noreña (2021) — MASW-SPT Perú (arenas eólicas) [core]

| Campo | Valor |
|-------|-------|
| **Título** | The empirical correlation between shear wave velocity and penetration resistance for the eolian sand deposits in the city of Olmos-Peru |
| **Autores** | Alhuay-León CG; Trejo-Noreña PC |
| **Año** | 2021 |
| **Idioma** | Inglés/Español (bilingüe) |
| **DOI** | 10.15446/dyna.v88n217.93317 |
| **Publicación** | DYNA (Universidad Nacional de Colombia), Vol.88, No.217, pp.247-255 |
| **Tipo** | Artículo de revista peer-reviewed |
| **PDF** | ✓ Descargado — `research/papers/pdf/Alhuay2021_MASW_SPT_Peru.pdf` (1.07 MB) |
| **Licencia** | CC BY-NC-ND 4.0 (GOLD OA) |
| **Calidad fuente** | Alta |

**Método principal:** MASW activo + correlación empírica con SPT

**Instrumentación:**
- Sismógrafo Geometrics Geode de 24 canales
- 24 geófonos verticales de 4.5 Hz (arreglo lineal)
- Fuente activa: martillo de 25 lb (11.3 kg) sobre placa metálica

**Procesamiento:** Phase-shift method (Park et al. 1998) para imagen de dispersión y extracción de curva de dispersión fundamental

**Sitio:** Olmos, Lambayeque, Perú — arenas eólicas cuaternarias secas (Qr-e), sin nivel freático, Vs < 280 m/s (depósito reciente); Qp-e subyacente más denso con Vs > 280 m/s. Zona de máxima sismicidad peruana (acc. 0.45g en suelo rígido).

**Objetivo:** Correlaciones empíricas Vs-N60 para arenas eólicas de la costa norte peruana. Las correlaciones obtenidas son: Vs = 65.5·N₆₀^0.33 y Vs = 21.6·N₆₀^0.38·(σ'v)^0.24

**Profundidad investigada:** 7–12 m (SPT); Vs30 = 180–360 m/s → Suelo Tipo D (NEHRP)

**Limitaciones:** Válida solo para arenas eólicas del área de Olmos; extrapolación limitada; muestra de un solo sitio geológicamente homogéneo.

**Conclusiones clave:** MASW con 24 geófonos de 4.5 Hz entrega perfiles Vs de alta calidad en arenas eólicas secas. La calidad de la imagen de dispersión es excelente con condiciones favorables (bajo ruido, topografía plana <10°). El MASW es alternativa económica viable al SPT para caracterización sísmica preliminar.

**Relevancia para la tesis:** Alta — precedente sudamericano (Perú) con el mismo hardware candidato (24 geófonos 4.5 Hz). Demuestra viabilidad del método en contexto de recursos limitados y condiciones geológicas similares a Paraguay (suelos granulares secos, poca cobertura vegetal).

**Factibilidad económica:** Muy alta — Geometrics Geode + 24 geófonos 4.5 Hz + martillo estándar. Configuración económica reproducible.

**Observaciones:** DOI verificado CrossRef + Semantic Scholar (4 citas). UNAL repository. Único estudio MASW-SPT para arenas eólicas peruanas al conocimiento de los autores. Procesamiento phase-shift (Park 1998). Proyecto de aplicación real: La Nueva Ciudad de Olmos (urbanización planificada). Referencia directa a Park et al. 1999 [3,41] — confirma linaje metodológico.


---

### 017 — Nakamura (1989) — Técnica HVSR (microtremores) [core]

| Campo | Valor |
|-------|-------|
| **Título** | A method for dynamic characteristics estimation of subsurface using microtremor on the ground surface |
| **Autor** | Nakamura Y |
| **Año** | 1989 |
| **Idioma** | Inglés |
| **DOI** | Ninguno (reporte técnico pre-digital) |
| **Publicación** | Quarterly Report of the Railway Technical Research Institute (RTRI), 30(1), pp. 25–33 |
| **Tipo** | Reporte técnico institucional |
| **PDF** | No disponible digitalmente (RTRI archivo digital comienza en vol.35, 1994) |
| **Landing page** | TRID: https://trid.trb.org/View/294184 |
| **Calidad fuente** | Alta (miles de citas; referencia fundacional en sismología de ingeniería) |

**Método principal:** HVSR — razón espectral H/V (técnica de Nakamura)

**Instrumentación:**
- 1 sensor triaxial / sismógrafo 3C (estación única)
- Sin fuente activa; sin array multicanal
- Equipo mínimo posible para caracterización de sitio

**Procesamiento:** Cálculo de espectros de Fourier de componentes H (horizontales promediadas) y V (vertical); razón H/V; identificación del pico de resonancia fundamental

**Sitio:** Japón (desarrollo conceptual / RTRI); aplicación universal a cualquier tipo de suelo

**Objetivo:** Estimar la frecuencia fundamental de resonancia f₀ del sitio y la amplificación relativa del suelo respecto a la roca, usando únicamente microtremores registrados en superficie con un sensor 3C.

**Variables estimadas:** f₀ (frecuencia fundamental); amplificación relativa H/V; estimación cualitativa de profundidad a contraste de impedancia principal.

**Limitaciones:** La interpretación física del pico H/V es debatida (no siempre = amplificación real en campo libre); sin inversión adicional no entrega perfil Vs; sensible a fuentes de ruido polarizadas; supuesto de campo difuso no siempre válido.

**Conclusiones clave:** El cociente H/V del ruido ambiental muestra un pico claro en la frecuencia fundamental del sitio. Este pico permite estimar f₀ y amplificación relativa sin necesidad de fuente activa ni array. Fundamento del análisis de microtremores de estación única en todo el mundo.

**Relevancia para la tesis:** Alta — método complementario extremadamente económico al MASW. La f₀ del sitio estimada por HVSR es comparable con la profundidad del contraste de impedancia del perfil Vs(z) de MASW. Combinación MASW+HVSR es práctica común para mejor resolución de modelos 1D. Vault ya tiene nota conceptual en [[HVSR]].

**Factibilidad económica:** Extremadamente alta — requiere solo 1 sensor 3C + grabador básico. Sin fuente activa, sin array, sin logística compleja. Método de máxima relación costo-beneficio en caracterización de sitio.

**Observaciones:** Sin DOI. TRID accession 00480707. Una de las referencias más citadas en sismología de ingeniería (miles de citas en Google Scholar/WoS). Introduce la "técnica de Nakamura". Geopsy (entrada 014) implementa HVSR y lo cita como paper fundacional. Semantic Scholar corpus ID: eb38ef39e815c7bdc82397197d72832768ccd546. Acceso físico posible via ILL o contacto directo con RTRI (OCLC 3127232, ISSN 0033-9008).


---

### 018 — Lermo & Chávez-García (1993) — Validación HVSR con terremotos [core]

| Campo | Valor |
|-------|-------|
| **Título** | Site effect evaluation using spectral ratios with only one station |
| **Autores** | Lermo J; Chávez-García FJ |
| **Año** | 1993 |
| **Idioma** | Inglés |
| **DOI** | 10.1785/bssa0830051574 |
| **Publicación** | Bulletin of the Seismological Society of America, 83(5), pp. 1574–1594 |
| **Tipo** | Artículo de revista peer-reviewed |
| **PDF** | No disponible libremente (paywalled en GeoScienceWorld) |
| **Landing page** | https://pubs.geoscienceworld.org/ssa/bssa/article-abstract/83/5/1574/119767/ |
| **Calidad fuente** | Alta (BSSA — revista de primer nivel; 1103 citas) |

**Método principal:** HVSR con registros de terremoto — validación de la técnica de Nakamura

**Instrumentación:**
- 1 sensor triaxial / sismógrafo 3C (estación única)
- Sin array, sin fuente activa
- Registros de terremotos regionales (S-wave coda)

**Procesamiento:** Cálculo de espectros de Fourier de componentes triaxiales; razón H/V del período dominante de la onda S; comparación con función de transferencia empírica SSR (Standard Spectral Ratio) con estación de referencia

**Sitios estudiados:** Oaxaca, Acapulco y Ciudad de México — zonas con fuerte contraste de impedancia suelo/roca, alta sismicidad.

**Objetivo:** Demostrar que la razón H/V aplicada a la fase S de registros de terremoto reproduce la función de transferencia empírica del sitio sin necesitar una estación de referencia en roca.

**Variables estimadas:** f₀ (frecuencia fundamental); amplificación relativa H/V; comparación cuantitativa con SSR.

**Limitaciones:** Tiende a subestimar la amplificación real en algunos casos; requiere terremotos con buena SNR; sensible a fuentes de ruido polarizadas; supuesto de campo difuso.

**Conclusiones clave:** La razón H/V de la onda S reproduce razonablemente bien la función de transferencia empírica del sitio. Valida la técnica de Nakamura (1989) con datos reales de terremoto en tres ciudades mexicanas. Establece que no se necesita estación de referencia para evaluar efecto de sitio de primer orden.

**Relevancia para la tesis:** Alta — companion directo de Nakamura 1989 (paper 017). Proporciona base científica para usar HVSR en evaluación rápida de sitio. Relevante si la tesis combina MASW + HVSR para mejor resolución del modelo de subsuelo. Autores mexicanos: referencia regional Latinoamérica.

**Factibilidad económica:** Muy alta — mismo equipo que Nakamura (1 sensor 3C). En zonas sísmicamente activas permite evaluar sitio con registros de terremotos. En Paraguay (sismicidad moderada), complementar con microtremores siguiendo Nakamura.

**Observaciones:** DOI verificado CrossRef + Semantic Scholar (1103 citas). BSSA Vol.83 No.5. Paywalled. Instituto de Ingeniería UNAM (México). Companion directo de Nakamura 1989 — primera validación sistemática H/V con terremotos. Citado en SESAME guidelines y en la mayoría de publicaciones HVSR posteriores. Junto con Nakamura 1989, forma el par fundacional del método HVSR.


---

### 019 — SESAME (2004) — Guías técnicas H/V [core]

| Campo | Valor |
|-------|-------|
| **Título** | Guidelines for the Implementation of the H/V Spectral Ratio Technique on Ambient Vibrations Measurements, Processing and Interpretation |
| **Autores** | SESAME European Research Project WP12 (coord. Bard P-Y et al.) |
| **Año** | 2004 (diciembre) |
| **Idioma** | Inglés |
| **DOI** | Ninguno (entregable proyecto EU EVG1-CT-2000-00026) |
| **Deliverable** | D23.12, WP12 |
| **Publicación** | European Commission – Research General Directorate, Project No. EVG1-CT-2000-00026 SESAME |
| **PDF** | ✓ Descargado — `research/papers/pdf/SESAME2004_HV_Guidelines.pdf` (1.1 MB, 63 pp.) |
| **URL** | https://sesame.geopsy.org/Papers/HV_User_Guidelines.pdf (acceso libre) |
| **Calidad fuente** | Alta (miles de citas; consenso europeo de 15+ institutos; estándar de referencia) |

**Método:** HVSR — guías de implementación práctica cuantitativa

**Contenido principal:**
- **Parte I:** Quick field reference — duración de registro, espaciado de mediciones, condiciones de campo
- **Parte II:** Requisitos técnicos detallados (instrumentación, condiciones experimentales), procesamiento estándar (J-SESAME), interpretación
- **Criterios de confiabilidad:** f₀ > 10/lw; nc(f₀) > 200; σA(f) < 2 (para f₀ > 0.5 Hz)
- **Criterios de pico claro:** al menos 5 de 6 condiciones cuantitativas

**Instrumentación recomendada:**
- Sensor 3C (velocímetro de banda ancha o acelerómetro)
- Frecuencia de corte ≤ f₀ esperada
- Duración mínima: 30 min para f₀ < 0.2 Hz; 3–5 min para f₀ > 5 Hz

**Recomendaciones clave de campo:**
- Sensor directo sobre el suelo (sin platos de materiales blandos)
- Evitar viento > 5 m/s, fuentes de ruido monochromáticas
- En microzonificación: empezar con grilla de 500 m y densificar según variación lateral

**Relevancia para la tesis:** Alta — guía de referencia estándar si la tesis incluye HVSR como método complementario. Provee criterios cuantitativos directamente aplicables. Explícitamente recomienda el método H/V para zonas de **sismicidad baja y moderada** (como Paraguay). Sugiere combinar con MASW y datos geotécnicos existentes.

**Factibilidad económica:** Extremadamente alta — documento gratuito, software J-SESAME gratuito, sensor 3C básico + grabador. Geopsy (paper 014) implementa exactamente estas guías.

**Observaciones:** Sin DOI. Deliverable D23.12 SESAME. Coordinador: P-Y Bard (ISTerre Grenoble). Marc Wathelet (Geopsy, paper 014) es co-participante. Cita Nakamura 1989 (paper 017) y Lermo & Chávez-García 1993 (paper 018) como fundamentos. Miles de citas (API rate-limited). Estándar de facto internacional para aplicación del método H/V.


---

### 020 — Moya-Gutiérrez et al. (2020) — MASW+TRS+SEV+SPT Colombia [core]

| Campo | Valor |
|-------|-------|
| **Título** | Site characterization using geophysical and geotechnical Prospecting. Case study main road North Central Trunk (Route 55) at Km 68+500, Pamplona, Norte de Santander, Colombia |
| **Autores** | Moya-Gutiérrez AJ; Torres-Peña JA; Contreras-Martínez M |
| **Año** | 2020 |
| **Idioma** | Español/Inglés (bilingüe) |
| **DOI** | 10.15446/rbct.n48.85411 |
| **Publicación** | Boletín de Ciencias de la Tierra (UNAL), No.48, pp. 30–45 |
| **Tipo** | Artículo de revista peer-reviewed |
| **PDF** | ✓ Descargado — `research/papers/pdf/MoyaGutierrez2020_MASW_TRS_Colombia.pdf` (5.3 MB, 16 pp.) |
| **Licencia** | CC BY-NC-ND 4.0 (OA) |
| **Calidad fuente** | Media (revista regional colombiana; peer-reviewed) |

**Métodos usados:**
- MASW 1D y 2D (análisis de ondas Rayleigh)
- TRS — Tomografía de Refracción Sísmica (ondas P)
- SEV — Sondeo Eléctrico Vertical (método Schlumberger)
- SPT — Ensayo de Penetración Estándar

**Instrumentación MASW:**
- Sismógrafo Geometrics Geode 24 canales
- 24 geófonos verticales de **14 Hz** (limitación: menor profundidad vs. 4.5 Hz)
- Martillo de 12 lb sobre placa metálica
- 2 líneas de 80.5 m, espaciamiento 3.5 m
- Software: SeisImager/SW + Seismic Unix (CWP)

**Sitio:** Pamplona, Norte de Santander, Colombia (2322 m snm). Depósitos cuaternarios fluvio-lacustres sobre gneis cuarzomonzonítico (Ortoneis). Contexto de ingeniería vial (NSR-10).

**Resultados:**
- Vp = 499–1714 m/s; Vs = 210–466 m/s; Resistividades 6.06–581.05 Ω-m
- Perfil de suelo Tipo D (según NSR-10)
- Parámetros dinámicos: ν (Poisson), E (Young), G (corte), densidad

**Limitaciones:** Geófonos de 14 Hz limitan profundidad a ~20–30 m (4.5 Hz alcanzaría 30–40 m). No discute incertidumbre de inversión. Correlación geofísica-geotécnica cualitativa.

**Relevancia para la tesis:** Alta — ejemplo de workflow multi-método (MASW+TRS+SEV+SPT) con equipamiento básico Geometrics Geode en contexto latinoamericano de recursos limitados. Muestra que el método es reproducible en proyectos de ingeniería civil. Proporciona parámetros dinámicos adicionales más allá de Vs30.

**Factibilidad:** Alta — setup básico + SeisImager (o alternativa libre: SurfSeis, MASWaves). Para Paraguay se recomendaría usar 4.5 Hz para mayor profundidad.

**Observaciones:** DOI verificado CrossRef. UNAL Colombia, Boletín de Ciencias de la Tierra. Bilingüe. Universidad de Pamplona (Colombia). PDF obtenido de Dialnet. 14 Hz geophones = subóptimo para MASW profundo. Geología: depósitos fluvio-lacustres sobre cristalino (diferente de Paraguay — aluvial profundo). Contexto NSR-10 (norma sismoresistente colombiana).


---

### 021 — Uma Maheswari, Boominathan & Dodagoudar (2010) — MASW+SPT Chennai, India

| Campo | Valor |
|-------|-------|
| **ID** | 021 |
| **DOI** | 10.1007/s10706-009-9285-9 |
| **Año** | 2010 |
| **Autores** | R. Uma Maheswari; A. Boominathan; G. R. Dodagoudar |
| **Revista** | Geotechnical and Geological Engineering, Vol. 28(2), pp. 119–137 |
| **Categoría** | core |
| **PDF local** | No — Springer paywalled, sin OA |
| **Relevancia** | Alta |
| **Calidad fuente** | Alta (Springer, peer-reviewed, 30 sitios, validación crosshole) |

**Métodos usados:**
- MASW activo (Rayleigh waves, Phase-shift, modo fundamental)
- SPT — Standard Penetration Test (correlación Vs-N)
- Crosshole sísmico (validación en sitio Adyar, ASTM D4428)
- Bender element (validación en laboratorio)

**Instrumentación MASW:**
- Sismógrafo Geometrics Geode 24 canales
- 24 geófonos verticales de **4.5 Hz**
- Martillo 8 kg sobre placa metálica
- Espaciamiento 1 m, apertura activa 23 m, offset fuente 5–15 m
- Software: SurfSeis (SurfSeis v1.x)

**Sitio:** 30 sitios en Chennai, India (metrópoli costera, ~1177 km²). Arcilla marina blanda y rígida, arenas fluviales sueltas, sedimentos aluviales. Geología: suelos hasta 50 m de espesor (norte) a afloramiento metamórfico (sur). Contexto urbano densamente poblado.

**Resultados:**
- 200 pares (Vs, N) derivados de MASW+SPT en 30 sitios
- Correlación global: **Vs = 95.64·N^0.301** (r² = 0.83, todos los suelos)
- Ecuaciones separadas para arcilla y arena (con SPT corregido por energía)
- NEHRP: parte significativa de Chennai en Clase D (Vs30 = 180–360 m/s)
- Período fundamental del sitio: 0.03–0.6 s (amenaza a edificaciones <6 pisos)
- MASW detecta inversiones de velocidad (ventaja vs. refracción)

**Limitaciones:** Correlaciones específicas de Chennai (arcilla marina + arena fluvial litoral sur de India); extrapolación cautelosa a otros contextos. Sin análisis de incertidumbre en inversión MASW. El paper precursor de conferencia (WCEE 2008) tiene PDF libre en IITK.

**Relevancia para la tesis:** Alta — protocolo completo Vs-SPT con equipo estándar (Geometrics Geode + geófonos 4.5 Hz) en país en desarrollo. Directamente replicable para validar perfiles MASW con datos SPT preexistentes. Ecuación Vs = f(N) útil para estimación en sitios con SPT histórico. Mapeo NEHRP a escala ciudad como objetivo metodológico alcanzable.

**Factibilidad:** Alta — configuración idéntica a paper 016 (Alhuay 2021): Geode 24-channel + 4.5 Hz + martillo. Espaciamiento 1 m = arreglo compacto apto para entorno urbano. SurfSeis comercial; Geopsy o SurfSeis free edition como alternativas.

**Observaciones:** DOI correcto: 10.1007/s10706-009-9285-9. ATENCIÓN: DOI 10.1007/s10706-010-9334-4 = discusión publicada por Gulerce (2010), NO el paper original. Springer paywalled, sin OA (Unpaywall confirmado). Referenciado en Alhuay-León & Trejo-Noreña 2021 (paper 016). Precursor WCEE 2008 disponible en https://www.iitk.ac.in/nicee/wcee/article/14_04-01-0090.PDF

---

### 022 — Ólafsdóttir, Erlingsson & Bessason (2018) — MASWaves: herramienta open-source MASW

| Campo | Valor |
|-------|-------|
| **ID** | 022 |
| **DOI** | 10.1139/cgj-2016-0302 |
| **Año** | 2018 |
| **Autores** | Elín Ásta Ólafsdóttir; Sigurdur Erlingsson; Bjarni Bessason (U. Iceland) |
| **Revista** | Canadian Geotechnical Journal, Vol. 55(2), pp. 217–233 |
| **Categoría** | core |
| **PDF local** | Sí — `research/papers/pdf/Olafsdottir2018_MASWaves_field_tool.pdf` (9.2 MB, CC BY 4.0) |
| **Relevancia** | Alta |
| **Calidad fuente** | Alta (Canadian Geotechnical Journal, peer-reviewed, validación inter-software) |

**Métodos usados:**
- MASW activo — flujo completo: adquisición → dispersión → inversión
- Phase-shift method (Park et al. 1998) para análisis de dispersión
- Backcálculo iterativo (mínimos cuadrados) para inversión
- Comparación con Geopsy (dispersión) y WinSASW (inversión)
- SASW histórico en sitio Arnarbæli (comparación)

**Software presentado — MASWaves:**
- **Completamente gratuito, open-source (MATLAB)**
- Descargable en: https://uni.hi.is/eao4/ (también datos de muestra y guía de usuario)
- **Módulo 1: MASWaves Dispersion** — procesa registros sísmicos → imagen de dispersión → curva experimental con bandas de incertidumbre
- **Módulo 2: MASWaves Inversion** — invierte curva de dispersión → perfil Vs(z) 1D
- Resultados equivalentes a Geopsy en todos los sitios de prueba

**Instrumentación de campo:**
- 24 geófonos verticales GS-11D (Geospace Technologies, Houston TX), **4.5 Hz**
- Fuente: sledgehammer (activo)
- Arnarbæli: dx = 1 m, x1 = 10 m; Bakkafjara: dx = 2 m, x1 = 15 m; Hella: dx = 1 m, x1 = 10 m

**Sitios de campo (3 sitios en sur de Islandia, 2013–2015):**
- **Arnarbæli** — arena glaciofluvial Holocénica (SW-SM), tabla freática en superficie
- **Bakkafjara** — arena litoral moderna
- **Hella** — arena limosa cementada (MH-ML)
- Vs varía desde ~100 m/s (arena suelta saturada) hasta ~300+ m/s (arena cementada)

**Limitaciones:** Versión 2018 = inversión determinista sin cuantificación de incertidumbre probabilística (esto se añade en el paper 013 — versión Monte Carlo 2020). Software limitado al modo fundamental en la versión original. Suelos islandeses (granulares volcánicos) difieren de suelos aluviales/arcillosos tropicales de Paraguay.

**Relevancia para la tesis:** Alta — **referencia fundacional del toolbox MASWaves**: herramienta libre MATLAB para el flujo MASW completo. Usar junto con paper 013 (MC inversion) para implementación práctica. Permite procesar datos MASW sin software comercial. Guía de usuario incluida. 4.5 Hz geophones = mismo hardware candidato para la tesis.

**Factibilidad:** Extremadamente alta — software gratuito con guía y datos de muestra. Geófonos 4.5 Hz estándar. Flujo documentado paso a paso. Alternativa académica a SurfSeis/SeisImager.

**Observaciones:** Companion de paper 013 (Olafsdottir et al. 2020 — Monte Carlo). PDF descargado desde Opin visindi (repositorio U. Iceland). Geófonos GS-11D Geospace Technologies ≈ similar costo a geófonos serie Mark L-28LB o SM-24 usados en otras tesis. Python port disponible: MASWavesPy (https://github.com/eao4/MASWavesPy).
