# Surface Wave & Geophone Research Database

> Base de datos curada para la tesis. Una entrada por paper, bien analizada.
> Fuente maestra: `surface_wave_geophone_research_database.csv`

**Última actualización:** 2026-03-20

---

## Estadísticas

| Categoría     | N      |
| ------------- | ------ |
| core          | 49     |
| peripheral    | 3      |
| reject        | 0      |
| Con PDF local | 21     |
| Solo DOI/link | 31     |
| **Total**     | **52** |

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


| Campo                      | Valor                                                                         |
| -------------------------- | ----------------------------------------------------------------------------- |
| **Título**                 | Estimation of near-surface shear-wave velocity by inversion of Rayleigh waves |
| **Autores**                | Jianghai Xia, Richard D. Miller, Choon B. Park                                |
| **Año**                    | 1999                                                                          |
| **Idioma**                 | Inglés                                                                        |
| **DOI**                    | `10.1190/1.1444578`                                                           |
| **Landing page**           | https://pubs.geoscienceworld.org/geophysics/article/64/3/691/73487/           |
| **PDF (KGS, open access)** | https://www.kgs.ku.edu/software/surfseis/Publications/XiaEtAl1999.pdf         |
| **PDF local**              | `research/papers/pdf/Xia1999_MASW_inversion.pdf`                              |
| **Tipo de publicación**    | Artículo en revista peer-reviewed (*Geophysics*, Vol. 64, No. 3, pp. 691–700) |
| **Calidad de fuente**      | Alta (SEG / CrossRef verificado)                                              |

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

| Campo                       | Valor                                                                                                                                                  |
| --------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------ |
| **Título**                  | In situ shear wave velocities from spectral analysis of surface waves                                                                                  |
| **Autores**                 | Soheil Nazarian, Kenneth H. Stokoe II                                                                                                                  |
| **Año**                     | 1984                                                                                                                                                   |
| **Idioma**                  | Inglés                                                                                                                                                 |
| **DOI**                     | *(sin DOI — proceedings preDigital)*                                                                                                                   |
| **Landing page (WorldCat)** | https://search.worldcat.org/title/84257107                                                                                                             |
| **PDF**                     | *(no disponible en acceso libre)*                                                                                                                      |
| **PDF local**               | *(no descargado)*                                                                                                                                      |
| **Tipo de publicación**     | Conference proceedings peer-reviewed (*Proc. 8th World Conference on Earthquake Engineering*, Vol. III, pp. 31–38, Prentice-Hall, 1984, San Francisco) |
| **Calidad de fuente**       | Alta (citado >3000 veces; metadatos verificados via WorldCat OCLC 11037839 y múltiples listas de referencias en literatura)                            |

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

---

### 023 — Park, Miller & Xia (1998) — Método phase-shift: fundamento algorítmico del MASW

| Campo | Valor |
|-------|-------|
| **ID** | 023 |
| **DOI** | 10.1190/1.1820161 |
| **Año** | 1998 |
| **Autores** | Choon Byong Park; Richard D. Miller; Jianghai Xia (KGS) |
| **Venue** | SEG Technical Program Expanded Abstracts 1998, pp. 1377–1380 |
| **Categoría** | core |
| **PDF local** | Sí — `research/papers/pdf/Park1998_phase_shift_method.pdf` (142 KB, 4 pp., masw.com) |
| **Relevancia** | Alta |
| **Calidad fuente** | Alta (SEG proceedings, 761 citas, autores KGS) |

**Qué introduce:**
La transformación wavefield **phase-shift** que convierte un shot gather multicanal directamente en imágenes de alta resolución de curvas de dispersión multi-modo. Es el algoritmo central de todo el procesamiento MASW moderno.

**Ecuación clave:**
`A(ω, cT) = Σ [u_norm(xj, ω) · exp(i·ω·xj/cT)]`

Suma de trazas normalizadas con corrección de fase en función de la velocidad de prueba cT. Las crestas de amplitud en el espacio (f, cT) identifican los modos de propagación.

**Ventaja sobre f-k y p-ω:**
- Funciona con número reducido de trazas (no requiere apertura enorme)
- Apto para offsets cercanos a la fuente (condición frecuente en ingeniería)
- Alta resolución multimodal con registros compactos

**Limitaciones:** Asume propagación 1D; sensible a ondas de cuerpo en offsets cercanos; resolución modal limitada por apertura del arreglo.

**Relevancia para la tesis:** Alta — es el fundamento algorítmico de MASWaves (papers 013, 022), Geopsy (014), SurfSeis (016, 021) y cualquier procesamiento MASW. Referencia obligatoria para justificar el paso de extracción de curva de dispersión. Precede directamente a Park et al. 1999 (paper 001).

**Observaciones:** Precursor directo de paper 001 (Park 1999). Junto con papers 001 y 002 (Xia 1999) forma la tríada fundacional del MASW. PDF libre en masw.com (copia autorizada KGS). 761 citas en Semantic Scholar.

---

### 024 — Yoon & Rix (2009) — Efectos near-field en MASW activo [core]

| Campo | Valor |
|-------|-------|
| **Autores** | Yoon S; Rix GJ |
| **Año** | 2009 |
| **Idioma** | Inglés |
| **DOI** | 10.1061/(ASCE)1090-0241(2009)135:3(399) |
| **Landing page** | https://ascelibrary.org/doi/10.1061/%28ASCE%291090-0241%282009%29135%3A3%28399%29 |
| **Tipo publicación** | Journal article (peer-reviewed) — ASCE JGGE Vol.135(3) pp.399–406 |
| **Calidad fuente** | Alta |
| **Categoría** | core |
| **PDF local** | No — ASCE paywalled, sin OA |

**Método principal:** Análisis numérico (simulaciones 2D) de efectos near-field en MASW activo con arrays de geófonos.

**Qué problema aborda:** La contaminación sistemática de las curvas de dispersión MASW cuando el offset fuente–primer receptor es insuficiente respecto de la longitud de onda analizada. Este efecto ("near-field effect") produce estimaciones sesgadas hacia velocidades de fase menores a las reales, afectando la precisión del perfil Vs, especialmente a bajas frecuencias (= profundidades mayores).

**Método e instrumentación:** Simulaciones numéricas 2D (FEM/BEM) con variación paramétrica sistemática del offset fuente-primer receptor (x₁) y del espaciamiento entre geófonos. Análisis de la razón x₁/λ (offset sobre longitud de onda) como variable de control del sesgo. Validación con modelos homogéneo y multicapa.

**Criterio clave establecido:** Offset mínimo fuente–primer receptor: **x₁ ≥ 0.5·λmax** para obtener velocidades de fase sin sesgo significativo. Equivalentemente, la razón x₁/λ debe ser ≥ 0.5 en el rango de frecuencias de interés. Efectos más severos en bajas frecuencias (longitudes de onda largas).

**Factibilidad de replicar:** Alta — el criterio es una guía de diseño de campo aplicable a cualquier equipamiento. No requiere instrumentación especial.

**Limitaciones reportadas:** Análisis principalmente numérico; la generalización a medios fuertemente heterogéneos o sitios con topografía puede requerir verificación adicional.

**Aporte a la tesis:** Fundamento estándar para justificar el diseño del arreglo MASW — elección del offset mínimo fuente–primer receptor. El criterio x₁/λ ≥ 0.5 es el estándar de facto referenciado en revisiones MASW (Foti et al. 2018, paper 012) y en guías de adquisición. Permite evaluar la confiabilidad de curvas de dispersión a bajas frecuencias y la calidad del perfil Vs en profundidad. Necesario para cualquier discusión de limitaciones de adquisición en la tesis.

**Observaciones:** DOI verificado CrossRef. Sin OA (Unpaywall confirmado). G.J. Rix (Georgia Tech) — uno de los investigadores MASW más citados. Companion study: Yoon (2007) PhD thesis Georgia Tech. Referenciado explícitamente en Foti et al. 2018 (paper 012) y en protocolos de adquisición MASW. Existe discusión del paper publicada en JGGE 2010.


---

### 025 — Xia et al. (2003) — Inversión MASW con modo fundamental y modos superiores [core]

| Campo | Valor |
|-------|-------|
| **Autores** | Xia J; Miller RD; Park CB; Tian G |
| **Año** | 2003 |
| **Idioma** | Inglés |
| **DOI** | 10.1016/s0926-9851(02)00239-2 |
| **Landing page** | https://www.sciencedirect.com/science/article/pii/S0926985102002392 |
| **Tipo publicación** | Journal article (peer-reviewed) — J. Appl. Geophys. Vol.52(1) pp.45–57 |
| **Calidad fuente** | Alta |
| **Categoría** | core |
| **PDF local** | No — Elsevier paywalled, sin OA |

**Método principal:** Inversión de curvas de dispersión MASW con modo fundamental y modos superiores de ondas Rayleigh (extensión de Xia et al. 1999).

**Qué problema aborda:** La inversión de solo el modo fundamental de Rayleigh tiene resolución limitada en profundidad y puede fallar al detectar inversiones de velocidad (capa blanda bajo capa rígida). Los modos superiores tienen kernels de sensibilidad distribuidos a mayor profundidad, lo que permite mejorar la resolución del perfil Vs(z) y reducir la no-unicidad del problema inverso.

**Método e instrumentación:** Array multicanal de geófonos verticales (datos sintéticos + campo en Kansas). Extracción de curvas de dispersión para múltiples modos (fundamental + modos superiores 1°, 2°, ...) via imagen f-k o phase-shift. Inversión iterativa por mínimos cuadrados que minimiza simultáneamente el misfit de todas las curvas modales con un modelo de capas planas horizontales. Extensión directa del algoritmo de Xia et al. 1999.

**Hallazgo principal:** La inversión multimodal produce perfiles Vs(z) con mayor resolución en profundidad y mejor detección de inversiones de velocidad que el modo fundamental aislado. Los modos superiores tienen mayor sensibilidad a capas profundas. Validado con datos sintéticos multicapa y datos de campo en Kansas.

**Factibilidad de replicar:** Media — requiere buena relación señal-ruido para identificar modos superiores. Geófonos 4.5 Hz + fuente adecuada ayudan. Implementado en MASWaves (papers 013, 022), Geopsy (014) y SurfSeis.

**Limitaciones reportadas:** Identificación modal en campo más compleja que en datos sintéticos; riesgo de mode misidentification; requiere mayor apertura o densidad de geófonos para resolver modos superiores confiablemente.

**Aporte a la tesis:** Extensión del paper 002 (Xia 1999) para modos superiores. Relevante cuando el modo fundamental no resuelve bien la estructura en profundidad o cuando hay inversiones de velocidad. Justifica el análisis multimodal en la discusión de inversión. 448 citas confirma alta relevancia en la comunidad.

**Observaciones:** DOI verificado CrossRef. 448 citas (Semantic Scholar). Sin OA (Unpaywall + SS confirmados). Companion de paper 002 (Xia 1999). Precede a Xia 2004 (paper 011 — incertidumbre MASW). Autores: grupo KGS fundador del MASW moderno. El concepto de inversión práctica con modos superiores fue introducido en forma sistemática aquí.


---

### 026 — Park, Miller & Miura (2002) — Parámetros óptimos de adquisición MASW [core]

| Campo | Valor |
|-------|-------|
| **Autores** | Park CB; Miller RD; Miura H |
| **Año** | 2002 |
| **Idioma** | Inglés |
| **DOI** | Sin DOI (conference expanded abstract SEG-J) |
| **PDF** | https://www.masw.com/files/PAR-02-03.pdf |
| **Tipo publicación** | Conference expanded abstract — SEG-J Annual Meeting, Tokyo, May 22-23, 2002 |
| **Calidad fuente** | Alta (autores: grupo KGS, inventores del MASW) |
| **Categoría** | core |
| **PDF local** | Sí — `research/papers/pdf/Park2002_optimum_field_parameters_MASW.pdf` (335 KB, 9 pp.) |

**Método principal:** MASW activo — análisis empírico de parámetros óptimos de adquisición de campo: offset mínimo, offset máximo, tipo de geófono y fuente sísmica.

**Qué problema aborda:** La selección de parámetros de campo óptimos para una encuesta MASW: ¿cuánto offset mínimo y máximo usar? ¿qué frecuencia de geófono? ¿qué fuente? Los autores (inventores del MASW) proporcionan criterios empíricos basados en extensas observaciones de campo.

**Hallazgos clave:**
- **Offset mínimo:** 10 m es suficiente para la mayoría de sitios de suelo — más tolerante que el criterio de ½ longitud de onda del SASW. A 10 m offset, las ondas de superficie son planares para λ ≤ 60 m (= profundidad de investigación ~30 m).
- **Offset máximo:** 100 m como criterio empírico general. Limitado por ondas de cuerpo y modos superiores a offsets grandes.
- **Tabla 1 — parámetros recomendados:**

| Geófono (Hz) | Prof. máx. (m) | Offset mín. (m) | Offset máx. (m) | Espaciamiento (m) |
|---|---|---|---|---|
| 4.5 | 50 | 10 | 100 | 1 |
| 10 | 30 | 10 | 100 | 1 |
| 40 | 15 | 10 | 100 | 1 |

- **Geófonos:** 10-Hz puede registrar hasta 5 Hz (igual que 4.5 Hz en la mayoría de sitios); 40-Hz registra hasta ~10 Hz.
- **Fuente:** Sledgehammer ≥ 10 lb. Mayor impacto no siempre = más energía a baja frecuencia; el acoplamiento importa.
- **MASW es el método sísmico más tolerante a variaciones de parámetros** entre todos los métodos sísmicos de exploración.

**Factibilidad de replicar:** Muy alta — guía directa de los inventores del método. Configuración básica (4.5 Hz + 20-lb sledgehammer + offset 10-100 m + dx=1 m) es completamente accesible con presupuesto limitado.

**Limitaciones reportadas:** Criterios establecidos para dos tipos de suelo (suelto húmedo + duro seco en EE.UU.); no incluye todos los escenarios geológicos posibles.

**Aporte a la tesis:** Referencia esencial para justificar el diseño de campo en cualquier estudio MASW. La Tabla 1 es la guía paramétrica estándar del método. Directamente aplicable a la tesis para decisiones de instrumentación (geófonos 4.5 Hz, offset 10-100 m, sledgehammer ≥ 10 lb).

**Observaciones:** Sin DOI (conference abstract). PDF en masw.com (KGS author copy). Tercer autor: H. Miura (Terra Corp., Tokyo) — no Xia. Paper del mismo grupo que papers 001 (Park 1999) y 023 (Park 1998).


---

### 027 — Strobbia & Foti (2006) — Método MOPA para extracción de curvas de dispersión [core]

| Campo | Valor |
|-------|-------|
| **Autores** | Strobbia C; Foti S |
| **Año** | 2006 |
| **Idioma** | Inglés |
| **DOI** | 10.1016/j.jappgeo.2005.10.009 |
| **Landing page** | https://www.sciencedirect.com/science/article/pii/S0926985105001418 |
| **Tipo publicación** | Journal article (peer-reviewed) — J. Appl. Geophys. Vol.59(4) pp.300–313 |
| **Calidad fuente** | Alta |
| **Categoría** | core |
| **PDF local** | No — Elsevier paywalled, sin OA |

**Método principal:** MOPA (Multi-Offset Phase Analysis) — análisis de diferencias de fase entre pares de receptores adyacentes a múltiples offsets para extraer curvas de dispersión de ondas superficiales activas.

**Qué problema aborda:** Los métodos clásicos de extracción de dispersión (f-k, phase-shift) requieren arrays densos y largos. El MOPA propone una alternativa: analizar sistemáticamente las diferencias de fase entre pares de receptores a múltiples offsets, con criterios estadísticos para identificar observaciones válidas (excluyendo near-field e interferencias de ondas de cuerpo).

**Ventajas clave del MOPA:**
- Puede funcionar con pocos receptores (incluso pares de 2 sensores)
- Proporciona estimaciones de incertidumbre estadística de la curva de dispersión de forma natural
- Identifica automáticamente observaciones contaminadas por near-field
- Más robusto a contaminación por ondas de cuerpo en ciertos rangos de offset

**Factibilidad de replicar:** Media-alta — la adquisición es simple (pocos geófonos), pero el procesamiento es más demandante que el MASW estándar. No implementado directamente en Geopsy o MASWaves de forma estándar.

**Limitaciones reportadas:** Mayor complejidad de procesamiento que MASW; requiere análisis cuidadoso de coherencia de fase; puede necesitar más tiros para cubrir múltiples offsets.

**Aporte a la tesis:** Método alternativo al MASW estándar relevante cuando el equipo es limitado. Proporciona incertidumbre estadística de la dispersión (útil para inversión probabilística). Complementa papers 008 (Socco & Strobbia 2004) y 013 (Olafsdottir 2020). 127 citas confirman adopción en la comunidad.

**Observaciones:** DOI correcto: 10.1016/j.jappgeo.2005.10.009 (DOI .10.007 en listas previas era incorrecto — resolvía a paper ERT de Cassiani et al.). Elsevier paywalled. Sin OA. Foti S. es también autor de paper 006 (Foti et al. 2018). Strobbia C. y Foti S. = grupo Politecnico di Torino, Italia.


---

### 028 — Lima Júnior, Prado & Mendes (2012) — MASW en suelos tropicales residuales, Brasil [core]

| Campo | Valor |
|-------|-------|
| **Autores** | Lima Júnior SB; Prado RL; Mendes RM |
| **Año** | 2012 |
| **Idioma** | Inglés / Portugués (bilingüe) |
| **DOI** | 10.22564/rbgf.v30i2.109 |
| **Landing page** | https://sbgf.org.br/revista/index.php/rbgf/article/view/109 |
| **PDF** | https://sbgf.org.br/revista/index.php/rbgf/article/download/109/50 |
| **Tipo publicación** | Journal article (peer-reviewed) — Rev. Brasileira de Geofísica Vol.30(2) pp.213–224 |
| **Calidad fuente** | Media (IAG-USP — grupo de referencia en geofísica aplicada de Brasil; 13 citas) |
| **Categoría** | core |
| **PDF local** | Sí — `research/papers/pdf/LimaJunior2012_MASW_landslide_Brazil.pdf` (7.2 MB, OA) |

**Método principal:** MASW activo 1D en suelos tropicales residuales no saturados (ladera, São Paulo). Evaluación experimental de parámetros de adquisición (frecuencia de geófonos, offsets) y variación estacional (seco vs lluvioso).

**Sitio:** Praia de Maranduba, Ubatuba SP, Brasil. Clima tropical húmedo (25.5°C, >2000 mm/año). Regolito granítico-gnéisico no saturado. Zona de movimientos de masa recurrentes.

**Instrumentación:** Tres Geometrics Geode 24-channel simultáneos con tres frecuencias de geófono: **4.5 Hz, 14 Hz y 28 Hz** (comparación experimental). Martillo ~8 kg sobre placa metálica. Espaciamiento 1 m. Offsets mínimos 1-15 m evaluados. SurfSeis software (Park 1999).

**Hallazgos clave:**
- Vs en temporada seca > temporada lluviosa → atribuido a mayor cohesión por succión capilar en suelos no saturados
- Geófonos **4.5 Hz** dan mejor desempeño a bajas frecuencias (mayor profundidad de investigación)
- Offset mínimo óptimo ~10 m — confirma experimentalmente el criterio de Park et al. 2002 (paper 026) en suelos tropicales
- Resultados MASW coherentes con otros estudios geotécnicos del sitio
- Cita Yoon & Rix (2009) para efectos near-field y Xia et al. 1999/Park 1999 para fundamentos

**Aporte a la tesis:** Referencia directa para MASW en suelo tropical sudamericano. Demuestra que geófonos 4.5 Hz + Geometrics Geode + martillo 8 kg caracteriza suelos residuales tropicales similar a los paraguayos. La variación estacional Vs (seco vs lluvioso) es relevante para zonas con precipitación marcada como Paraguay.

**Observaciones:** DOI verificado CrossRef. OA Bronze (PDF libre RBGf). IAG-USP grupo = referencia en geofísica aplicada de Brasil. Bilingüe (abstract en inglés y portugués). 13 citas (SS). Cita directamente Yoon & Rix 2009 (paper 024). Offsets comparados: 1-15 m.


---

### 029 — Parolai et al. (2005) — Joint inversion H/V + dispersión pasiva con algoritmo genético [core]

| Campo | Valor |
|-------|-------|
| **Autores** | Parolai S; Picozzi M; Richwalski SM; Milkereit C |
| **Año** | 2005 |
| **Idioma** | Inglés |
| **DOI** | 10.1029/2004gl021115 |
| **Landing page** | https://agupubs.onlinelibrary.wiley.com/doi/10.1029/2004GL021115 |
| **Tipo publicación** | Journal article (peer-reviewed) — Geophysical Research Letters Vol.32(1) (2005) |
| **Calidad fuente** | Alta (GRL — una de las revistas de geofísica más prestigiosas; 239 citas) |
| **Categoría** | core |
| **PDF local** | No — AGU/Wiley paywalled, sin OA |

**Método principal:** Inversión conjunta (joint inversion) de curvas de dispersión de velocidad de fase Rayleigh (extraídas de ruido sísmico pasivo) y razones espectrales H/V, considerando modos fundamental y superiores, optimizada con algoritmo genético.

**Qué problema aborda:** La inversión individual de curvas de dispersión o de H/V tienen alta no-unicidad. La inversión conjunta reduce la no-unicidad combinando dos observables complementarios: la dispersión es sensible al contraste de velocidad, mientras que H/V es sensible a la frecuencia fundamental del sitio y a los efectos de amplificación. Usando algoritmo genético se evitan mínimos locales.

**Ventajas clave:**
- Solo requiere ruido sísmico pasivo — sin fuente activa (método económico)
- El AG permite exploración global del espacio de parámetros
- Modos superiores mejoran la resolución en profundidad
- Reduce la no-unicidad respecto a la inversión individual de H/V o dispersión

**Limitaciones reportadas:** Requiere ruido sísmico de buena calidad e isótropo; modelado de H/V es complejo (no es función directa de dispersión); AG puede ser computacionalmente costoso.

**Aporte a la tesis:** Justifica combinar MASW (activo) + HVSR (pasivo) en un esquema de joint inversion para reducir no-unicidad. Relevante si el perfil Vs no puede ser resuelto solo con MASW. Conecta papers 017 (Nakamura 1989), 019 (SESAME 2004) y 014 (Wathelet/Geopsy) con una aplicación metodológica concreta. 239 citas confirma amplia adopción.

**Observaciones:** DOI verificado CrossRef. GRL Vol.32(1) 2005. Paywalled (GFZ repository: acceso bloqueado). 239 citas (SS). Grupo GFZ Potsdam (Parolai). Companion paper: Parolai et al. 2005 GRL 10.1029/2005gl022878. Relacionado: papers 017, 019, 014 de esta base.


---

### 030 — Miller et al. (1999) · *The Leading Edge* · core

**Titulo**: Multichannel analysis of surface waves to map bedrock
**Autores**: Miller RD; Xia J; Park CB; Ivanov JM
**Año**: 1999 · **Idioma**: en
**DOI**: 10.1190/1.1438226
**PDF local**: papers/pdf/Miller1999_MASW_map_bedrock.pdf *(descargado — masw.com KGS author copy, 1.4 MB)*

**Método principal**: MASW (2D con adquisición CMP roll-along)
**Método secundario**: CMP roll-along; sección 2D de Vs
**Sensor**: Geofono 4.5 Hz (Geospace GS11D) — single, espaciado 2 ft
**Adquisición**: Activa — martillo 12 lb sobre placa 1 ft², 4 golpes apilados; 60-ch Geometrics StrataView; 48 canales por registro cada 4 ft
**Geometría del arreglo**: Lineal CMP roll-along
**Tipo de sitio**: Sitio contaminado — parking sobre roca basal
**Contexto geográfico**: Olathe, Kansas, USA
**Profundidad investigada**: 0.6–10.7 m (2–35 ft)

**Objetivo**: Mapeo de superficie de bedrock y detección de fracturas/paleocanal para caracterización hidrológica
**Procesamiento**: Phase-shift estilo CMP-MASW; SurfSeis (KGS)
**Inversión**: 1D Vs por CMP con continuidad lateral → sección 2D
**Variables estimadas**: Vs; profundidad a bedrock; zonas de fractura

**Limitaciones**: Resolución lateral limitada a escala sub-CMP; profundidad máxima ~10 m con setup de martillo y 4.5 Hz
**Conclusiones clave**: 2D-MASW via CMP produce mapa de bedrock con precisión < 1 ft vs. perforaciones; MASW insensible a inversiones de velocidad; ventaja sobre ondas de cuerpo en este tipo de sitio
**Utilidad para tesis**: Introduce 2D-MASW via CMP roll-along con geófonos 4.5 Hz y sismógrafo 60 canales; directamente citado en Park 2002 (paper 026); muestra factibilidad de mapeo de bedrock con equipamiento estándar
**Relevancia**: alta · **Economicidad**: alta — setup completamente reproducible con equipamiento estándar

**Observaciones**: 462 citas (Semantic Scholar). Mismos autores que papers 001, 002, 023, 026. Introduce 2D-MASW estilo CMP. Sitio Olathe Kansas.


---

### 031 — Tokimatsu et al. (1992) · *Journal of Geotechnical Engineering* · core

**Titulo**: Effects of Multiple Modes on Rayleigh Wave Dispersion Characteristics
**Autores**: Tokimatsu K; Tamura S; Kojima H
**Año**: 1992 · **Idioma**: en
**DOI**: 10.1061/(ASCE)0733-9410(1992)118:10(1529)
**Landing page**: https://ascelibrary.org/doi/10.1061/%28ASCE%290733-9410%281992%29118%3A10%281529%29
**PDF**: no disponible — ASCE paywalled, sin OA

**Método principal**: SASW (análisis modal teórico en contexto SASW)
**Método secundario**: Análisis modal Rayleigh multimodal
**Sensor**: No especificado (estudio teórico)
**Adquisición**: No especificada
**Tipo de sitio**: Teórico — perfiles estratificados sintéticos
**Contexto geográfico**: Japón (Kobe University)
**Profundidad investigada**: Variable (perfiles sintéticos ~30 m)

**Objetivo**: Analizar efecto de modos superiores de ondas Rayleigh sobre la curva de dispersión aparente medida; identificar condiciones en que modos superiores dominan
**Procesamiento**: Cálculo de curvas de dispersión multimodal por método de matriz de transferencia
**Inversión**: Comparación de modos calculados con curva de dispersión aparente
**Variables estimadas**: Vs; estructura modal; contribución de modos superiores

**Limitaciones**: No aborda inversión directamente; análisis limitado a perfiles 1D horizontalmente homogéneos
**Conclusiones clave**: Modos superiores pueden dominar la curva de dispersión aparente en perfiles con inversión de velocidad; curva aparente puede seguir modos superiores a bajas frecuencias causando subestimación de Vs en profundidad; propone simulación multimodal para interpretación correcta
**Utilidad para tesis**: Paper teórico fundamental sobre modos superiores en ondas Rayleigh; explica por qué la inversión en modo fundamental puede dar resultados erróneos en ciertos perfiles; motivación directa para inversiones multimodales (ver paper 025)
**Relevancia**: alta · **Economicidad**: alta — paper teórico puro; resultados válidos para cualquier setup MASW/SASW

**Observaciones**: 352 citas (Semantic Scholar). Tokimatsu K (Kobe University). Citado en Xia 2003 (paper 025) y en prácticamente toda la literatura sobre modos superiores MASW.


---

### 032 — Eikmeier (2018) · *Dissertação de Mestrado IAG-USP* · core

**Titulo**: Análise Multicanal de Ondas de Superfície (MASW): um estudo comparativo com fontes ativas e passivas, ondas Rayleigh e Love e diferentes modos de propagação
**Autor**: Eikmeier CN
**Año**: 2018 · **Idioma**: pt
**DOI**: 10.11606/d.14.2018.tde-09042018-164758
**Landing page**: https://teses.usp.br/teses/disponiveis/14/14132/tde-09042018-164758/pt-br.php
**PDF local**: papers/pdf/Eikmeier2018_MASW_comparativo_Brasil.pdf *(descargado — 11 MB, 130 págs)*

**Método principal**: MASW (activo + pasivo, comparativo)
**Método secundario**: f-k beamforming; Passive Roadside MASW; inversión conjunta multimodal; Love waves
**Sensor**: Geofono 10 Hz triaxial (arreglo 2D) + geofono 4.5 Hz vertical (lineal)
**Adquisición**: Activa + pasiva — compactador de suelo, marreta, ruido ambiental, tráfico vehicular
**Geometría**: 2D bidimensional + lineal
**Tipo de sitio**: Campus universitario urbano — USP IAG Butantã, São Paulo
**Contexto geográfico**: São Paulo, Brasil
**Profundidad investigada**: ~10-30 m

**Objetivo**: Comparar sistemáticamente fuentes activas/pasivas, ondas Rayleigh/Love, modo fundamental vs modos superiores; validar contra SPT
**Procesamiento**: f-k transform; f-k beamforming; phase-shift
**Inversión**: Modo fundamental + 1er modo superior (conjunta); Love waves
**Variables estimadas**: Vs; validado contra SPT

**Limitaciones**: Ruido ambiental (180s) insuficiente para procesamiento pasivo; Passive Roadside mejora identificación de modos superiores pero no mejora perfil Vs directamente; método aún dependiente del operador
**Conclusiones clave**: Compactador de suelo es mejor fuente activa que marreta (más energía, mayor banda de frecuencia, mejores espectros); inversión conjunta fundamental + 1er modo superior da mejores resultados; Passive Roadside MASW ayuda a identificar modos superiores en datos activos; todos los resultados convergentes y validados contra SPT
**Utilidad para tesis**: Disertación IAG-USP (orientador: Renato Prado — mismo grupo que Lima Jr 2012, paper 028); compara sistemáticamente fuentes activas/pasivas con geófonos 4.5 Hz y 10 Hz; muestra que inversión multimodal mejora profundidad e incerteza del perfil; contexto Sudamérica tropical
**Relevancia**: alta · **Economicidad**: alta — geófonos 4.5 Hz + compactador de bajo costo + métodos pasivos; replicable con equipamiento académico limitado

**Observaciones**: 0 citas (SS, esperado para disertación). Gold OA CC BY-NC-SA. Sitio: campus CUASO-USP Butantã São Paulo. SPT disponible para validación.


---

### 033 — Socco, Foti & Boiero (2010) · *Geophysics* · core

**Titulo**: Surface-wave analysis for building near-surface velocity models — Established approaches and new perspectives
**Autores**: Socco LV; Foti S; Boiero D
**Año**: 2010 · **Idioma**: en
**DOI**: 10.1190/1.3479491
**PDF local**: papers/pdf/Socco2010_surface_wave_review_Geophysics.pdf *(descargado — IRIS Politecnico di Torino, 1.7 MB)*

**Método principal**: Revisión — ondas superficiales métodos activos y pasivos
**Método secundario**: MASW; SASW; f-k; beamforming; crosscorrelación; SPAC; modos superiores; variaciones laterales
**Sensor**: No especificado (revisión de literatura, múltiples tipos)
**Adquisición**: Activa y pasiva (revisión general)
**Tipo de sitio**: Múltiple (revisión global)
**Contexto geográfico**: Internacional
**Profundidad investigada**: Variable (revisión completa de la literatura)

**Objetivo**: Revisión comprehensiva del análisis de ondas superficiales para construcción de modelos Vs; best-practices guidelines; discussion de modos superiores y variaciones laterales
**Procesamiento**: Phase-shift; f-k; beamforming; crosscorrelación; SPAC; ESAC; MASW; SASW
**Inversión**: Fundamental; multimodal; variaciones laterales; algoritmos globales y locales
**Variables estimadas**: Vs (perfil 1D y variaciones laterales)

**Limitaciones**: Modos superiores difíciles de recuperar experimentalmente (~33% de publicaciones los incluyen); variaciones laterales = área abierta; no-unicidad clásica de la inversión
**Conclusiones clave**: Modos superiores juegan rol significativo en muchos sitios pero solo ~33% de publicaciones los incluyen; la curva de dispersión aparente puede estar dominada por modos superiores en perfiles con inversiones de velocidad; variaciones laterales son el próximo frontier; propone guía de buenas prácticas
**Utilidad para tesis**: Review de referencia de Socco + Foti + Boiero (Politecnico di Torino); cubre toda la cadena metodológica; discusión en profundidad de modos superiores (prioridad 2); best-practices guidelines para adquisición y procesamiento (prioridad 3); companion a Socco & Strobbia 2004 (paper 008)
**Relevancia**: alta · **Economicidad**: alta — paper de revisión; principios válidos para cualquier setup con geófonos estándar

**Observaciones**: 462 citas (Semantic Scholar). Autores: L.V. Socco, S. Foti, D. Boiero — Politecnico di Torino. Companion a papers 008 (Socco & Strobbia 2004), 006 (Foti 2018), 007 (Garofalo 2016).


---

### 034 — Maraschini & Foti (2010) · *Geophysical Journal International* · core

**Titulo**: A Monte Carlo multimodal inversion of surface waves
**Autores**: Maraschini M; Foti S
**Año**: 2010 · **Idioma**: en
**DOI**: 10.1111/j.1365-246x.2010.04703.x
**Landing page**: https://doi.org/10.1111/j.1365-246x.2010.04703.x
**PDF**: no disponible — Bronze OA (GJI Oxford/Wiley), PDF protegido contra descarga automática

**Método principal**: Inversión multimodal Monte Carlo
**Método secundario**: Ondas Rayleigh multimodal; modos superiores
**Sensor**: No especificado (estudio metodológico numérico + campo)
**Adquisición**: Activa (contexto general)
**Tipo de sitio**: Sintético + campo
**Contexto geográfico**: Italia (Politecnico di Torino)
**Profundidad investigada**: Variable (sintético ~10-30 m)

**Objetivo**: Proponer y validar inversión Monte Carlo multimodal que usa todos los modos simultáneamente; cuantificar incertidumbre de parámetros
**Procesamiento**: Espectro f-v multimodal; extracción de curvas de dispersión modales
**Inversión**: Monte Carlo global — muestrea espacio de modelos sin gradientes; minimiza función de ajuste que pondera todos los modos simultáneamente
**Variables estimadas**: Vs (perfil 1D); incertidumbre de parámetros

**Limitaciones**: Costo computacional elevado; requiere identificación previa de modos en espectro experimental; limitado a perfiles 1D
**Conclusiones clave**: Inversión Monte Carlo usando todos los modos simultáneamente mejora la estimación de Vs respecto a modo fundamental solo; reduce la no-unicidad; permite cuantificar incertidumbre; función de ajuste multimodal más robusta
**Utilidad para tesis**: Paper metodológico Maraschini + Foti (Politecnico di Torino) — mismo grupo que papers 008 y 033; introduce inversión Monte Carlo multimodal; implementado en Geopsy/Dinver (paper 014); cubre P2 (modos superiores) y P5 (inversión global estocástica)
**Relevancia**: alta · **Economicidad**: media — Monte Carlo computacionalmente costoso pero implementado en software libre (Geopsy); geófonos estándar suficientes para adquisición

**Observaciones**: 124 citas (Semantic Scholar). Companion a papers 008 (Socco & Strobbia 2004), 033 (Socco 2010), 014 (Wathelet/Geopsy). Ver también Maraschini & Foti (2011) sobre bedrock somero: DOI 10.1016/j.soildyn.2010.10.006.


---

### 035 — Long & Donohue (2007) · *Canadian Geotechnical Journal* · core

**Titulo**: In situ shear wave velocity from multichannel analysis of surface waves (MASW) tests at eight Norwegian research sites
**Autores**: Long MM; Donohue S
**Año**: 2007 · **Idioma**: en
**DOI**: 10.1139/t07-013
**PDF local**: papers/pdf/Long2007_MASW_Norwegian_soft_soils_CGJ.pdf *(descargado — UCD repository, 676 KB)*

**Método principal**: MASW
**Método secundario**: SCPT; crosshole; correlación CPT-Vs
**Sensor**: Geofono 4.5 Hz y 10 Hz — 12 geofonos a 1 m de separación
**Adquisición**: Activa — sledgehammer; RAS-24 seismograph (Seistronix)
**Geometría**: Lineal — 12 geofonos a 1 m
**Tipo de sitio**: Sitios de investigación geotécnica — arcillas blandas a firmes, limos, arenas
**Contexto geográfico**: Noruega (Drammen, Oslo area, Sandvika — sitios NGI/NTNU)
**Profundidad investigada**: ~5-20 m (dependiendo de sitio y frecuencia)

**Objetivo**: Evaluar repetibilidad, precisión y confiabilidad del MASW en 8 sitios noruegos bien caracterizados; comparar con SCPT, crosshole y correlaciones CPT
**Procesamiento**: Phase-shift; SurfSeis (KGS)
**Inversión**: Iterativa least-squares (SurfSeis — Xia et al. 1999)
**Variables estimadas**: Vs; Gmax (vía ρ·Vs²); correlación con SCPT/crosshole/CPT

**Limitaciones**: MASW sobreestima Vs ~10% respecto a SCPT/crosshole; en arenas sueltas puede sobreestimar más; inversión SurfSeis limita flexibilidad; solo modo fundamental
**Conclusiones clave**: MASW es fácil, rápido, consistente y repetible; perfiles Vs en arcillas coinciden bien con SCPT y crosshole (~10% diferencia); buena correlación Gmax con contenido de agua/índice de vacíos; en limos resultados razonables; en arenas sueltas tiende a sobreestimar Vs
**Utilidad para tesis**: Primer estudio comparativo sistemático en suelos blandos con validación rigurosa (SCPT, crosshole, CPT); usa geófonos 4.5 Hz + RAS-24 Seistronix; muestra límites del MASW en arenas sueltas; relevante para suelos aluviales/blandos típicos de Sudamérica
**Relevancia**: alta · **Economicidad**: alta — geofono 4.5 Hz + RAS-24 + martillo; bajo costo reproducible

**Observaciones**: 76 citas (Semantic Scholar). Long MM, Donohue S (University College Dublin). 8 sitios: Drammen clay, Sandvika, etc. (NGI/NTNU). Validación rigorosa contra SCPT, crosshole, correlaciones CPT (Mayne & Rix 1995).


---

### 036 — Stephenson (2005) · *BSSA* · core

**Titulo**: Blind Shear-Wave Velocity Comparison of ReMi and MASW Results with Boreholes to 200 m in Santa Clara Valley: Implications for Earthquake Ground-Motion Assessment
**Autor**: Stephenson WJ
**Año**: 2005 · **Idioma**: en
**DOI**: 10.1785/0120040240
**Landing page**: https://doi.org/10.1785/0120040240
**PDF**: no disponible — BSSA paywalled, sin OA

**Método principal**: MASW; ReMi
**Método secundario**: Comparación ciega contra sondeos a 200 m
**Sensor**: No especificado (varios sitios — típico MASW/ReMi)
**Adquisición**: Activa (MASW) + pasiva (ReMi)
**Tipo de sitio**: Urbano — Valle de Santa Clara, California, USA
**Contexto geográfico**: Santa Clara Valley, California, USA
**Profundidad investigada**: Hasta 200 m (excepcional para MASW/ReMi)

**Objetivo**: Comparación ciega de ReMi y MASW contra sondeos a 200 m; implicaciones para evaluación de movimiento del terreno sísmico (Vs30 y perfiles Vs)
**Procesamiento**: MASW: phase-shift; ReMi: análisis p-f pasivo
**Inversión**: Inversión separada por método; comparación post-hoc con logs de sondeos
**Variables estimadas**: Vs (perfil 1D); Vs30

**Limitaciones**: Profundidad de 200 m requiere configuraciones especiales; métodos pasivos limitados por ruido de fondo; blind comparison no permite optimizar parámetros para maximizar acuerdo
**Conclusiones clave**: ReMi y MASW muestran buena concordancia con sondeos hasta 200 m en sitios apropiados; diferencias atribuibles principalmente a variabilidad lateral y no a limitaciones inherentes; ambos son herramientas útiles para Vs30 en contexto de peligro sísmico
**Utilidad para tesis**: Validación ciega de alta relevancia — compara ReMi (paper 004) y MASW (paper 001) con sondeos independientes a profundidades excepcionales; 141 citas; BSSA alta calidad; USGS autores
**Relevancia**: alta · **Economicidad**: media — 200 m requiere configuraciones especiales; para Vs30 (~30 m) ambos métodos son accesibles con equipamiento estándar

**Observaciones**: 141 citas (Semantic Scholar). Autor: W. Stephenson (USGS Denver). Sitio: Santa Clara Valley California. Puente entre papers 001 (Park 1999 MASW) y 004 (Louie 2001 ReMi) con validación independiente.


### 037 · Bergamo et al. 2011 — Shallow bedrock multimodal Monte Carlo inversion (SDEE)

| Campo | Valor |
|-------|-------|
| **Autores** | Bergamo P; Comina C; Foti S; Maraschini M |
| **Año** | 2011 |
| **Revista** | Soil Dynamics and Earthquake Engineering 31(3):530–534 |
| **DOI** | 10.1016/j.soildyn.2010.10.006 |
| **PDF local** | papers/pdf/Bergamo2011_MASW_multimodal_montecarlo_shallow_bedrock.pdf |
| **Método principal** | Inversión multimodal Monte Carlo en ondas superficiales |
| **Método secundario** | Análisis f-k (paquete SWAT, MATLAB) |
| **Sensor** | Geófono (tipo no especificado); offset inicio arreglo 3 m |
| **Adquisición** | Activa |
| **Tipo de sitio** | Roca superficial / estaciones red acelerométrica italiana |
| **Contexto** | Italia (Liguria, Sicilia) |
| **Objetivo** | Caracterización sísmica de sitios con basamento poco profundo |
| **Profundidad** | Superficial (~5–20 m) |
| **Variables estimadas** | Perfil Vs, profundidad basamento, amplificación sísmica |
| **Limitaciones** | Requiere curvas de dispersión multimodales; sensible a ruido |
| **Conclusiones clave** | Monte Carlo multimodal robusto para sitios con basamento superficial; maneja inversiones de velocidad y no-unicidad; validado con razones espectrales H/V |
| **Utilidad para tesis** | Método de inversión directamente aplicable cuando modos superiores están presentes; muestra cómo incluir todos los modos sin asignarlos a priori |
| **Relevancia** | alta |
| **Categoría** | **core** |


### 038 · Shapiro & Campillo 2004 — Rayleigh waves from ambient noise correlations (GRL)

| Campo | Valor |
|-------|-------|
| **Autores** | Shapiro N M; Campillo M |
| **Año** | 2004 |
| **Revista** | Geophysical Research Letters 31(7) |
| **DOI** | 10.1029/2004gl019491 |
| **PDF local** | no disponible (Wiley bronze OA requiere autenticación) |
| **Landing page** | https://doi.org/10.1029/2004GL019491 |
| **Método principal** | Interferometría sísmica pasiva: extracción de ondas Rayleigh broadband por correlación cruzada de ruido ambiental |
| **Método secundario** | Tomografía de ondas superficiales (velocidad de grupo) |
| **Sensor** | Sismómetros de red regional (100–2000 km entre estaciones) |
| **Adquisición** | Pasiva (ruido sísmico ambiental, días de registro) |
| **Tipo de sitio** | Continental (red sísmica regional, EE.UU.) |
| **Objetivo** | Demostrar que ondas Rayleigh coherentes emergen de correlaciones de ruido ambiental |
| **Profundidad** | Corteza y manto superior (escala km) |
| **Variables estimadas** | Velocidad de grupo de ondas Rayleigh broadband; mapas tomográficos |
| **Limitaciones** | Escala regional (100–2000 km); no directamente aplicable a caracterización de sitio con geófonos |
| **Conclusiones clave** | Paper fundacional: ondas Rayleigh broadband emergen de días de ruido ambiental; velocidades consistentes con tomografía balística; abre camino a mediciones pasivas sin fuente activa |
| **Utilidad para tesis** | Fundamento teórico de ReMi y métodos pasivos; justifica uso de ruido ambiental para extraer Vs; base de interferometría sísmica a escala local |
| **Relevancia** | media |
| **Categoría** | **peripheral** |


### 039 · Luo et al. 2009 — Rayleigh wave mode separation by high-resolution Radon transform (GJI)

| Campo | Valor |
|-------|-------|
| **Autores** | Luo Y; Xia J; Miller R D; Xu Y; Liu J; Liu Q |
| **Año** | 2009 |
| **Revista** | Geophysical Journal International 179(1):254–264 |
| **DOI** | 10.1111/j.1365-246x.2009.04277.x |
| **PDF local** | no disponible (GJI Oxford cerrado) |
| **Landing page** | https://academic.oup.com/gji/article/179/1/254/736500 |
| **Método principal** | Separación de modos Rayleigh por transformada de Radon lineal de alta resolución (inversion de esparsidad) |
| **Método secundario** | MASW multimodal; análisis de dispersión f-v |
| **Sensor** | Geófono vertical 4.5 Hz (espaciado 0.5 m) — igual que equipamiento típico de tesis |
| **Adquisición** | Activa |
| **Tipo de sitio** | Sintético y campo |
| **Objetivo** | Separar y reconstruir modos de dispersión Rayleigh para mejorar precisión en MASW multimodal |
| **Variables estimadas** | Perfil Vs; curvas de dispersión multimodales individualizadas; frecuencias de corte |
| **Limitaciones** | Resolución limitada en LRT estándar (mejora parcial con esparsidad); no evalúa limitaciones por ruido o heterogeneidad lateral |
| **Conclusiones clave** | LRT alta resolución mejora resolución de imágenes >50% vs slant stacking; separa modos exitosamente; amplía rango frecuencia-profundidad usable; reduce número de disparos necesarios |
| **Utilidad para tesis** | Directamente aplicable a datos MASW con modos superiores visibles; usa geófonos 4.5 Hz igual que en tesis; mejora calidad de inversión multimodal |
| **Relevancia** | alta |
| **Categoría** | **core** |


### 040 · Hayashi & Suzuki 2004 — CMP cross-correlation of multi-channel surface wave data (EG)

| Campo | Valor |
|-------|-------|
| **Autores** | Hayashi K; Suzuki H |
| **Año** | 2004 |
| **Revista** | Exploration Geophysics 35:7–13 |
| **DOI** | 10.1071/eg04007 |
| **PDF local** | no disponible (Exploration Geophysics cerrado) |
| **Landing page** | https://doi.org/10.1071/eg04007 |
| **Método principal** | CMP cross-correlation de ondas superficiales multicanal/multishot para perfil 2D de Vs |
| **Método secundario** | Inversión no lineal de mínimos cuadrados; análisis MASW en gathers CMP |
| **Sensor** | Geófono (arreglo multicanal, roll-along tipo sísmica 2D reflexión) |
| **Adquisición** | Activa (múltiples disparos, cobertura CMP) |
| **Tipo de sitio** | Sintético y campo |
| **Objetivo** | Demostrar que análisis CMP de correlaciones cruzadas de ondas superficiales permite reconstruir estructuras 2D de velocidad con alta resolución |
| **Variables estimadas** | Perfil 2D de Vs; curvas de velocidad de fase por punto CMP |
| **Limitaciones** | Requiere múltiples disparos y cobertura CMP (mayor costo que MASW simple) |
| **Conclusiones clave** | CMP cross-correlation mejora precisión y resolución vs métodos estándar; adquisición similar a reflexión 2D; procesamiento en 4 pasos bien definidos |
| **Utilidad para tesis** | Directamente aplicable a reconocimientos 2D con geófonos estándar; permite detectar variaciones laterales; extiende MASW a perfiles continuos de alta resolución |
| **Relevancia** | alta |
| **Categoría** | **core** |


### 041 · Arai & Tokimatsu 2005 — Joint inversion of microtremor dispersion + H/V spectrum (BSSA)

| Campo | Valor |
|-------|-------|
| **Autores** | Arai H; Tokimatsu K |
| **Año** | 2005 |
| **Revista** | Bulletin of the Seismological Society of America 95(5):1766–1778 |
| **DOI** | 10.1785/0120040243 |
| **PDF local** | no disponible (BSSA cerrado) |
| **Landing page** | https://doi.org/10.1785/0120040243 |
| **Método principal** | Inversión conjunta de curva de dispersión de microtremores y espectro H/V para perfil Vs |
| **Método secundario** | Análisis de modos múltiples de Rayleigh y Love en H/V |
| **Sensor** | Sismómetro de microtremores (pasivo; no geófono) |
| **Adquisición** | Pasiva (ruido sísmico ambiental) |
| **Tipo de sitio** | Campo (4 sitios con perfil de pozo de referencia) |
| **Contexto** | Japón |
| **Objetivo** | Estimar perfiles Vs hasta bedrock de ingeniería por inversión conjunta dispersión + H/V |
| **Profundidad** | Hasta bedrock de ingeniería (~30–100 m) |
| **Variables estimadas** | Perfil Vs; Vs de bedrock; profundidad de bedrock |
| **Limitaciones** | Requiere medición de H/V y dispersión en mismo sitio; sensible al número de modos considerados |
| **Conclusiones clave** | Inversión conjunta más consistente con perfiles de pozo que inversión solo de dispersión; H/V más sensible a Vs de bedrock que velocidad de fase |
| **Utilidad para tesis** | Marco teórico para joint inversion dispersión + H/V; directamente relevante si se combina MASW con H/V Nakamura en mismos sitios; extiende Tokimatsu 1992 al caso pasivo + H/V |
| **Relevancia** | alta |
| **Categoría** | **core** |


### 042 · Wathelet et al. 2004 — Surface wave inversion by neighbourhood algorithm (NSG)

| Campo | Valor |
|-------|-------|
| **Autores** | Wathelet M; Jongmans D; Ohrnberger M |
| **Año** | 2004 |
| **Revista** | Near Surface Geophysics 2:211–221 |
| **DOI** | 10.3997/1873-0604.2004018 |
| **PDF local** | no disponible (Wiley/EAGE bronze OA requiere autenticación) |
| **Landing page** | https://doi.org/10.3997/1873-0604.2004018 |
| **Método principal** | Inversión de curva de dispersión por algoritmo de vecindad (neighbourhood algorithm, búsqueda estocástica global) |
| **Método secundario** | Complementariedad activo+pasivo; inserción de información a priori |
| **Sensor** | Arreglo de sismómetros (activo y pasivo) |
| **Adquisición** | Pasiva + activa (complementarias) |
| **Tipo de sitio** | Sintético + campo (Bruselas, Bélgica) |
| **Contexto** | Bélgica (~115 m arenas/arcillas sobre basamento Paleozoico) |
| **Objetivo** | Invertir curva de dispersión 1D incluyendo no-unicidad e incertidumbre mediante búsqueda estocástica global |
| **Profundidad** | ~115 m (caso Bruselas) |
| **Variables estimadas** | Perfil Vs 1D; incertidumbre de inversión; rango de modelos aceptables |
| **Limitaciones** | Solución no única (inherente a problema no lineal); requiere parametrización cuidadosa |
| **Conclusiones clave** | Neighbourhood algorithm eficiente para inversión 1D de ondas superficiales; activo+pasivo complementarios; validado con pozo en Bruselas |
| **Utilidad para tesis** | Paper fundacional del algoritmo implementado en Geopsy/Dinver (paper 014); directamente relevante para uso de Geopsy en tesis; precede y motiva Wathelet 2020 |
| **Relevancia** | alta |
| **Categoría** | **core** |


### 043 · Forbriger 2003 — Inversion of shallow-seismic wavefields: I. Wavefield transformation (GJI)

| Campo | Valor |
|-------|-------|
| **Autor** | Forbriger T |
| **Año** | 2003 |
| **Revista** | Geophysical Journal International 153(3):719–734 |
| **DOI** | 10.1046/j.1365-246x.2003.01929.x |
| **PDF local** | no disponible (OUP requiere autenticación pese a bronze OA) |
| **Landing page** | https://academic.oup.com/gji/article/153/3/719/611543 |
| **Método principal** | Transformación de Fourier-Bessel discreta para representación completa del campo de onda sísmico superficial (primer paso de inversión de campo completo) |
| **Método secundario** | Inversión 1D por ajuste de coeficientes sintéticos (Part II como companion) |
| **Sensor** | Geófonos (sísmica superficial) |
| **Objetivo** | Calcular coeficientes de Bessel para inversión completa de campo de onda sin separación de modos |
| **Limitaciones** | Computacionalmente intensivo; requiere software especializado; no trivialmente aplicable con herramientas de MASW estándar |
| **Conclusiones clave** | Método evita separación de modos (inseparables en dominio temporal); robusto sin a priori; aplicable en campo cercano; más eficiente que inversión directa de sismogramas |
| **Utilidad para tesis** | Fundamento teórico para entender cuándo métodos de dispersión estándar fallan; contextualiza limitaciones del MASW por interferencia de modos |
| **Relevancia** | media |
| **Categoría** | **peripheral** |


### 044 · Boore 2004 — Estimating Vs(30) from Shallow Velocity Models (BSSA)

| Campo | Valor |
|-------|-------|
| **ID** | 044 |
| **Autores** | Boore D.M. |
| **Año** | 2004 |
| **Journal** | Bulletin of the Seismological Society of America |
| **Vol/Pág** | 94(2), 591–597 |
| **DOI** | `10.1785/0120030105` |
| **Landing page** | https://doi.org/10.1785/0120030105 |
| **PDF local** | *(no disponible — BSSA closed access)* |
| **Tipo fuente** | journal |
| **Calidad fuente** | alta |
| **Citas** | 285 (Semantic Scholar) |
| **Categoría** | core |

**Problema abordado:** En muchos sitios, los perfiles de velocidad de onda de corte sólo llegan a profundidades menores de 30 m, imposibilitando el cálculo directo de Vs30. El trabajo evalúa métodos de extrapolación para estimar Vs30 a partir de modelos incompletos.

**Método:** Se evalúan cuatro métodos de extrapolación de velocidad usando datos de 135 sondeos en California con modelos que alcanzan al menos 30 m. Los métodos incluyen asumir velocidad constante, correlaciones empíricas entre velocidad superficial y Vs30, y ajustes de tendencia.

**Instrumentación:** Datos de perfiles de velocidad de sondeos geotécnicos (borehole). No requiere adquisición sísmica activa.

**Factibilidad con presupuesto limitado:** Alta — la metodología es puramente analítica/estadística sobre datos existentes. No requiere equipo nuevo.

**Limitaciones reportadas:** La incertidumbre aumenta para perfiles muy superficiales; el rendimiento depende del método y del sitio. Los errores de clasificación NEHRP persisten incluso con los mejores métodos.

**Conclusiones clave:** Los métodos basados en correlación entre velocidad superficial y Vs30 reducen significativamente el sesgo respecto a asumir velocidad constante. Permite aprovechar datos de perfiles someros sin descartar sitios con información incompleta.

**Utilidad para tesis:** Referencia fundamental para la evaluación de perfiles Vs estimados mediante MASW/inversión cuando la profundidad de investigación es menor a 30 m; directamente útil para discutir la validez de los resultados de inversión y la clasificación de sitios.

**Relevancia:** alta


### 045 · Dal Moro & Ferigo 2011 — Joint Rayleigh+Love Dispersion Inversion (J. Appl. Geophys.)

| Campo | Valor |
|-------|-------|
| **ID** | 045 |
| **Autores** | Dal Moro G.; Ferigo F. |
| **Año** | 2011 |
| **Journal** | Journal of Applied Geophysics |
| **Vol/Pág** | 75, 573–589 |
| **DOI** | `10.1016/j.jappgeo.2011.09.008` |
| **Landing page** | https://doi.org/10.1016/j.jappgeo.2011.09.008 |
| **PDF local** | *(no disponible — Elsevier closed access)* |
| **Tipo fuente** | journal |
| **Calidad fuente** | alta |
| **Citas** | 58 (Semantic Scholar) |
| **Categoría** | core |

**Problema abordado:** La inversión individual de ondas Rayleigh o Love presenta no-unicidad y ambigüedad en la identificación de modos. El trabajo evalúa cómo la inversión conjunta de ambos tipos de ondas reduce estos problemas.

**Método:** Inversión conjunta de curvas de dispersión de ondas Rayleigh y Love usando algoritmos evolutivos multiobjetivo (MOEA) con análisis de modelos óptimos de Pareto. Se valida con datos sintéticos y dos sitios de campo.

**Instrumentación:** Geófonos triaxiales 4.5 Hz (componentes vertical + horizontal). Se requieren dos tipos de fuente: impacto vertical en placa (Rayleigh) e impacto lateral en viga horizontal (Love). Mayor complejidad que MASW estándar.

**Factibilidad con presupuesto limitado:** Media — requiere geófonos horizontales y doble fuente; la adquisición es más compleja y costosa que MASW puro, pero no prohibitiva para contexto académico equipado.

**Limitaciones reportadas:** Mayor complejidad logística de adquisición; requiere identificación correcta de modos en ambas ondas para que la inversión conjunta sea válida.

**Conclusiones clave:** La inversión conjunta Rayleigh+Love reduce significativamente la ambigüedad de solución y mejora la determinación del perfil Vs. Propone procedimiento de adquisición eficiente en campo para capturar ambas ondas.

**Utilidad para tesis:** Justifica enfoque multicomponente si se cuenta con geófonos triaxiales; contextualiza las limitaciones de la inversión unimodal (solo Rayleigh); relevante para discusión sobre no-unicidad.

**Relevancia:** media


### 046 · Garofalo et al. 2016 — InterPACIFIC Part II: MASW vs Borehole (Soil Dyn. Earthq. Eng.)

| Campo | Valor |
|-------|-------|
| **ID** | 046 |
| **Autores** | Garofalo F.; Foti S.; Hollender F.; Bard P.Y.; Cornou C.; Cox B.R. et al. |
| **Año** | 2016 |
| **Journal** | Soil Dynamics and Earthquake Engineering |
| **Vol/Pág** | 82, 241–254 |
| **DOI** | `10.1016/j.soildyn.2015.12.009` |
| **Landing page** | https://doi.org/10.1016/j.soildyn.2015.12.009 |
| **PDF local** | *(no disponible — Elsevier closed; HAL/OSTI sin PDF directo)* |
| **Tipo fuente** | journal |
| **Calidad fuente** | alta |
| **Citas** | 153 (Semantic Scholar) |
| **Categoría** | core |

**Problema abordado:** Evaluar la confiabilidad de los métodos sísmicos no invasivos (ondas superficiales) comparándolos con métodos invasivos (borehole) para la caracterización de sitios sísmicos, especialmente para la estimación de Vs30.

**Método:** Ejercicio ciego multi-equipo: múltiples grupos independientes procesaron el mismo dataset (Rayleigh + Love waves, MASW, SPAC, f-k) y comparan los perfiles Vs resultantes con datos de downhole/crosshole en 3 sitios europeos (Italia y Francia).

**Instrumentación:** Geófonos en arreglos superficiales + perforaciones de referencia (downhole/crosshole). Distintos grupos usaron distintos equipamientos y estrategias.

**Factibilidad con presupuesto limitado:** Alta — el paper valida el uso de métodos superficiales (MASW) como alternativa económica confiable a las perforaciones para obtener Vs30.

**Limitaciones reportadas:** Métodos superficiales con menor resolución para capas delgadas y contrastes de velocidad abruptos vs. borehole; variabilidad entre equipos de procesamiento.

**Conclusiones clave:** Vs30 estimado por métodos superficiales (MASW, SPAC, f-k) es comparable al obtenido por borehole; las diferencias son mayores en la resolución de capas delgadas. Valida el uso de MASW para clasificación sísmica en ingeniería.

**Utilidad para tesis:** Benchmark de referencia para justificar el uso de MASW como método de bajo costo comparado con borehole; soporte para validar resultados de inversión; relevante para discusión sobre limitaciones y confiabilidad de los métodos no-invasivos.

**Relevancia:** alta


### 047 · Griffiths, Cox, Rathje & Teague 2016 — Uncertainty in Vs Profiles vs Site Response (JGGE/ASCE)

| Campo | Valor |
|-------|-------|
| **ID** | 047 |
| **Autores** | Griffiths S.C.; Cox B.R.; Rathje E.M.; Teague D.P. |
| **Año** | 2016 |
| **Journal** | Journal of Geotechnical and Geoenvironmental Engineering (ASCE) |
| **Vol/Pág** | 142 |
| **DOI** | `10.1061/(asce)gt.1943-5606.0001553` |
| **Landing page** | https://doi.org/10.1061/(asce)gt.1943-5606.0001553 |
| **PDF local** | *(no disponible — ASCE closed access)* |
| **Tipo fuente** | journal |
| **Calidad fuente** | alta |
| **Citas** | 63 (Semantic Scholar) |
| **Categoría** | core |

**Problema abordado:** La incertidumbre en los perfiles Vs derivados de la inversión de ondas superficiales se propaga a las estimaciones de respuesta sísmica de sitio. El trabajo evalúa qué enfoques estadísticos para representar esa incertidumbre son más realistas.

**Método:** Se comparan perfiles Vs obtenidos directamente de inversión de ondas superficiales (MASW) contra perfiles estadísticos indirectos (bounding, percentiles, aleatorios) para evaluar su efecto en respuestas de sitio calculadas. Datos de dos sitios de estudio ciego internacional (InterPACIFIC).

**Instrumentación:** Datos MASW preexistentes (arreglos superficiales activos). No requiere adquisición nueva.

**Factibilidad con presupuesto limitado:** Media — el análisis de respuesta de sitio requiere software específico, pero los conceptos son aplicables con perfiles MASW obtenidos en campo.

**Limitaciones reportadas:** Los perfiles estadísticos simples pueden subestimar o sobreestimar la variabilidad real; el resultado depende fuertemente de la calidad de la inversión original.

**Conclusiones clave:** Los perfiles Vs directos de inversión MASW producen variabilidad más realista en la respuesta de sitio que los métodos estadísticos indirectos. La elección del perfil Vs representativo tiene impacto significativo en el resultado de la respuesta sísmica.

**Utilidad para tesis:** Cuantifica las consecuencias prácticas de la incertidumbre en la inversión MASW; útil para discutir la no-unicidad de la inversión y sus implicaciones en la clasificación sísmica del sitio.

**Relevancia:** alta


### 048 · Park & Miller 2008 — Roadside Passive MASW (JEEG)

| Campo | Valor |
|-------|-------|
| **ID** | 048 |
| **Autores** | Park C.B.; Miller R.D. |
| **Año** | 2008 |
| **Journal** | Journal of Environmental and Engineering Geophysics |
| **Vol/Pág** | 13, 1–11 |
| **DOI** | `10.2113/jeeg13.1.1` |
| **Landing page** | https://doi.org/10.2113/jeeg13.1.1 |
| **PDF local** | *(no disponible — JEEG closed access)* |
| **Tipo fuente** | journal |
| **Calidad fuente** | alta |
| **Citas** | 152 (Semantic Scholar) |
| **Categoría** | core |

**Problema abordado:** En entornos urbanos frecuentemente no es posible desplegar un arreglo 2D para MASW pasivo. El trabajo desarrolla una versión pasiva del MASW con arreglo lineal convencional en borde de carretera.

**Método:** Escaneo azimutal 0–180° del wavefield registrado con arreglo lineal para separar ondas propagadas desde distintos azimuts (fuentes de tráfico vehicular). Las trazas se suman por azimut para mejorar la señal. Resulta en curva de dispersión equivalente a la de fuente activa.

**Instrumentación:** Geófonos estándar en arreglo lineal convencional. Usa el tráfico vehicular como fuente pasiva. Equipamiento idéntico al MASW activo.

**Factibilidad con presupuesto limitado:** Alta — mismo equipamiento que MASW activo; no requiere fuente artificial; aplica en entornos urbanos donde hay tráfico.

**Limitaciones reportadas:** Requiere tráfico activo como fuente; las fuentes offline introducen sesgo si no se corrige el azimut; penetración en profundidad limitada por la frecuencia del ruido de tráfico.

**Conclusiones clave:** El arreglo lineal roadside es prácticamente viable en zonas urbanas donde no se puede desplegar arreglo 2D; el escaneo azimutal compensa la geometría lineal permitiendo obtener curvas de dispersión comparables al MASW activo.

**Utilidad para tesis:** Extiende la aplicabilidad del MASW estándar a entornos urbanos sin necesidad de fuente activa ni arreglo 2D; directamente reproducible con geófonos estándar de 4.5 Hz.

**Relevancia:** alta


### 049 · Bonnefoy-Claudet et al. 2009 — HVSR Santiago de Chile Basin (GJI) [P4]

| Campo | Valor |
|-------|-------|
| **ID** | 049 |
| **Autores** | Bonnefoy-Claudet S.; Baize S.; Bonilla L.F.; Berge-Thierry C.; Pasten C.; Campos J.; Volant P.; Verdugo R. |
| **Año** | 2009 |
| **Journal** | Geophysical Journal International |
| **Vol/Pág** | 176(3), 925–937 |
| **DOI** | `10.1111/j.1365-246x.2008.04020.x` |
| **Landing page** | https://doi.org/10.1111/j.1365-246x.2008.04020.x |
| **PDF URL (bronze OA — inaccessible vía curl)** | https://academic.oup.com/gji/article-pdf/176/3/925/6087245/176-3-925.pdf |
| **PDF local** | *(no descargado — OUP retorna 403)* |
| **Tipo fuente** | journal |
| **Calidad fuente** | alta |
| **Citas** | 132 (Semantic Scholar) |
| **Categoría** | core |

**Problema abordado:** Evaluar la confiabilidad del método H/V (HVSR) para caracterizar los efectos de sitio sísmico en la cuenca sedimentaria de Santiago de Chile, identificando frecuencias de resonancia del suelo.

**Método:** Mediciones extensas de vibración ambiental (microtremores) distribuidas en toda la cuenca urbana de Santiago. Las razones H/V se analizan según criterios SESAME. Se identifican tres patrones en las curvas H/V: picos nítidos (contraste fuerte), curvas planas (contraste débil) y picos anchos (variaciones laterales).

**Instrumentación:** Sensores de vibración ambiental (acelerómetros/geófonos de velocidad). No requiere fuente activa. Equipamiento mínimo.

**Factibilidad con presupuesto limitado:** Alta — sólo se necesitan medidores de vibración ambiental; el método H/V es de los más económicos para caracterización sísmica de sitios.

**Limitaciones reportadas:** H/V tiene limitaciones para cuantificar la amplificación absoluta; las variaciones laterales de estructura complican la interpretación directa; las frecuencias de resonancia del suelo no siempre coinciden con las de los edificios.

**Conclusiones clave:** HVSR es confiable para mapear frecuencias de resonancia del suelo en cuenca sedimentaria compleja; se identifican zonas con contraste fuerte (f₀ claro), débil y con estructuras lateralmente variables. Relevante para planificación urbana y evaluación sísmica de sitios.

**Utilidad para tesis:** Estudio HVSR en ciudad sudamericana (Santiago de Chile); contextualiza la aplicación de métodos pasivos en cuencas sedimentarias urbanas latinoamericanas; complementa perfiles MASW para caracterización de sitio en contexto P4. **Nota:** Este paper usa HVSR (no MASW directamente), pero es el primer paper P4 de Sudamérica con HVSR — extensión directa de métodos no invasivos.

**Relevancia:** alta


### 050 · Wald & Allen 2007 — Vs30 from Topographic Slope (BSSA)

| Campo | Valor |
|-------|-------|
| **ID** | 050 |
| **Autores** | Wald D.J.; Allen T.I. |
| **Año** | 2007 |
| **Journal** | Bulletin of the Seismological Society of America |
| **Vol/Pág** | 97(5), 1379–1395 |
| **DOI** | `10.1785/0120060267` |
| **Landing page** | https://doi.org/10.1785/0120060267 |
| **PDF local** | *(no disponible — BSSA closed access)* |
| **Tipo fuente** | journal |
| **Calidad fuente** | alta |
| **Citas** | 861 (Semantic Scholar) |
| **Categoría** | core |

**Problema abordado:** En la mayoría de sitios no existen mediciones directas de Vs30. Se necesita una técnica de primer orden para estimar condiciones de sitio sísmico a escala regional cuando no hay datos de campo.

**Método:** Correlación estadística entre pendiente topográfica (gradiente de DEM global a 30 arcsec) y valores de Vs30 medidos en campo (USA, Taiwan, Italia, Australia). Se desarrollan dos conjuntos de parámetros: regiones tectónicas activas (alto relieve) y escudos estables (bajo relieve).

**Instrumentación:** No requiere equipamiento de campo — usa datos topográficos públicos globales (SRTM u otros DEM) y bases de datos de Vs30 existentes.

**Factibilidad con presupuesto limitado:** Alta — totalmente basado en datos públicos gratuitos; no requiere campaña de campo.

**Limitaciones reportadas:** Aproximación de primer orden con alta dispersión estadística; no reemplaza mediciones directas en sitios críticos o de ingeniería; correlación más débil en zonas de baja pendiente.

**Conclusiones clave:** La pendiente topográfica es un proxy estadísticamente significativo para Vs30 a escala regional; los mapas resultantes capturan tendencias espaciales importantes para clasificación sísmica de sitios. Herramienta complementaria cuando no existen datos directos.

**Utilidad para tesis:** Permite estimar Vs30 aproximado para sitios sin mediciones previas; útil para contextualizar resultados MASW/HVSR en el marco de clasificación sísmica regional; complementa paper 044 (Boore 2004) sobre extrapolación de Vs30.

**Relevancia:** alta


### 051 · Cox & Teague 2016 — Layering Ratios for Surface Wave Inversion without A Priori (GJI)

| Campo | Valor |
|-------|-------|
| **ID** | 051 |
| **Autores** | Cox B.R.; Teague D.P. |
| **Año** | 2016 |
| **Journal** | Geophysical Journal International |
| **Vol/Pág** | 207(1), 422–438 |
| **DOI** | `10.1093/gji/ggw282` |
| **Landing page** | https://doi.org/10.1093/gji/ggw282 |
| **PDF URL (bronze OA — inaccessible vía curl)** | https://academic.oup.com/gji/article-pdf/207/1/422/7967122/ggw282.pdf |
| **PDF local** | *(no descargado — OUP retorna 403)* |
| **Tipo fuente** | journal |
| **Calidad fuente** | alta |
| **Citas** | 115 (Semantic Scholar) |
| **Categoría** | core |

**Problema abordado:** La inversión de curvas de dispersión de ondas superficiales es inherentemente no única y requiere definir a priori el número de capas y sus rangos de espesor. Sin información de borehole, esta elección es subjetiva y puede afectar significativamente el resultado.

**Método:** Se propone el concepto de "layering ratios" — relaciones sistemáticas entre los espesores de capas sucesivas — como guía para definir la parametrización del modelo de inversion sin requerir a priori. Se valida con datos sintéticos y reales.

**Instrumentación:** Datos MASW/SASW (cualquier fuente de curva de dispersión). No añade requisitos de campo.

**Factibilidad con presupuesto limitado:** Alta — es un enfoque analítico/metodológico que se aplica sobre los datos de dispersión existentes; no requiere equipamiento adicional.

**Limitaciones reportadas:** Sin información a priori los layering ratios pueden no capturar heterogeneidades reales; la elección de la relación entre capas sigue siendo una decisión del analista.

**Conclusiones clave:** Los layering ratios proporcionan un enfoque sistemático y reproducible para definir el modelo de capas en inversión sin a priori. Reduce la subjetividad del analista y mejora la trazabilidad del proceso de inversión. Directamente aplicable en "análisis ciego".

**Utilidad para tesis:** Guía práctica para la parametrización del modelo de capas en la inversión MASW cuando no hay datos de borehole disponibles; directamente aplicable con cualquier dato MASW; mejora la reproducibilidad del análisis.

**Relevancia:** alta


### 052 · Kafadar 2020 — Low-Cost Geophone System for Microtremor/HVSR (Geoscient. Instrum.)

| Campo | Valor |
|-------|-------|
| **ID** | 052 |
| **Autores** | Kafadar O. |
| **Año** | 2020 |
| **Journal** | Geoscientific Instrumentation, Methods and Data Systems |
| **Vol/Pág** | 9(2), 365–373 |
| **DOI** | `10.5194/gi-9-365-2020` |
| **Landing page** | https://doi.org/10.5194/gi-9-365-2020 |
| **PDF URL (Gold OA — CC-BY)** | https://gi.copernicus.org/articles/9/365/2020/gi-9-365-2020.pdf |
| **PDF local** | `research/papers/pdf/Kafadar2020_low_cost_geophone_microtremor_HVSR.pdf` |
| **Tipo fuente** | journal |
| **Calidad fuente** | media |
| **Citas** | 6 (Semantic Scholar) |
| **Categoría** | core |

**Problema abordado:** Los equipos comerciales para medición de microtremores de tres componentes son costosos, lo que limita su uso en contextos académicos y países con recursos limitados. Se diseña un sistema alternativo de bajo costo basado en geófonos.

**Método:** Sistema integrado de adquisición y análisis de microtremores construido con geófonos triaxiales, amplificadores y convertidor ADC de bajo costo. Incluye software embebido para calcular H/V automáticamente sin software externo. Se valida comparando con equipos comerciales.

**Instrumentación:** Geófonos de tres componentes (horizontal x2 + vertical x1). Hardware de bajo costo; replicable en laboratorio académico.

**Factibilidad con presupuesto limitado:** Alta — el sistema completo es de bajo costo y el diseño es replicable. El artículo describe el hardware con suficiente detalle para reproducirlo.

**Limitaciones reportadas:** Solo mide en punto único (no genera arreglo para curvas de dispersión completas); limitado a HVSR puntual, no a MASW lineal.

**Conclusiones clave:** El sistema de bajo costo con geófonos produce resultados de HVSR comparables a equipos comerciales. Demuestra la factibilidad técnica y económica de construir instrumentos sísmicos de bajo costo para caracterización de sitios.

**Utilidad para tesis:** Referencia directa para justificar el uso de sistemas de bajo costo con geófonos estándar; apoya la factibilidad del enfoque hardware de la tesis; aunque es HVSR puntual, el diseño del sistema es transferible al contexto MASW.

**Relevancia:** alta



### 053 · Xu, Xia & Miller 2006 — Minimum Offset MASW (J. Appl. Geophys.)

| Campo | Valor |
|-------|-------|
| **ID** | 053 |
| **Autores** | Xu Y; Xia J; Miller R.D. |
| **Año** | 2006 |
| **Journal** | Journal of Applied Geophysics |
| **Vol/Pág** | 59(2), 117–125 |
| **DOI** | `10.1016/j.jappgeo.2005.08.002` |
| **Landing page** | https://doi.org/10.1016/j.jappgeo.2005.08.002 |
| **PDF URL** | sci-hub (descargado) |
| **PDF local** | `research/papers/pdf/Xu2006_MASW_minimum_offset_JAG.pdf` |
| **Tipo fuente** | journal_article |
| **Calidad fuente** | alta |
| **Citas** | 141 (OpenAlex) |
| **Categoría** | core |

**Problema abordado:** El offset mínimo fuente-primer receptor en MASW activo generalmente se determina de forma empírica o semi-cuantitativa, sin base analítica sólida. La contaminación de la curva de dispersión por efectos near-field depende de este parámetro.

**Método:** Se desarrolla una fórmula analítica para estimar el offset mínimo en un modelo elástico estratificado homogéneo. Se valida con datos sintéticos y experimentales de campo.

**Instrumentación:** Cualquier configuración MASW activa con geófonos estándar; el método es agnóstico al hardware específico.

**Factibilidad con presupuesto limitado:** Alta — es un análisis teórico; la fórmula resultante es aplicable directamente al diseño de campo con cualquier equipamiento MASW estándar.

**Limitaciones reportadas:** La fórmula se derivó para modelo estratificado homogéneo; su generalización a modelos heterogéneos requiere validación adicional.

**Conclusiones clave:** El offset mínimo puede estimarse analíticamente a partir de la longitud de onda máxima y las propiedades del sitio. El criterio propuesto es más riguroso que los empíricos previos y reduce la contaminación por near-field en la curva de dispersión.

**Utilidad para tesis:** Directamente aplicable al diseño de adquisición MASW en campo; proporciona justificación cuantitativa para la elección del offset mínimo; complementa el análisis de Yoon & Rix 2009 (paper 024) sobre efectos near-field.

**Relevancia:** alta


### 054 · Xia et al. 2006 — Simple Equations for Surface-Wave Survey Design (Soil Dyn.)

| Campo | Valor |
|-------|-------|
| **ID** | 054 |
| **Autores** | Xia J; Xu Y; Chen C; Kaufmann R.D.; Luo Y |
| **Año** | 2006 |
| **Journal** | Soil Dynamics and Earthquake Engineering |
| **Vol/Pág** | 26(5), 395–403 |
| **DOI** | `10.1016/j.soildyn.2005.11.001` |
| **Landing page** | https://doi.org/10.1016/j.soildyn.2005.11.001 |
| **PDF local** | `research/papers/pdf/Xia2006_simple_equations_surface_wave.pdf` |
| **Tipo fuente** | journal_article |
| **Calidad fuente** | alta |
| **Citas** | 91 (OpenAlex) |
| **Categoría** | core |

**Problema abordado:** Los parámetros de adquisición en surveys de ondas superficiales de alta frecuencia (MASW) suelen determinarse de forma empírica. Se carece de guías analíticas simples y unificadas.

**Método:** Se discuten cinco ecuaciones analíticas derivadas de la literatura y se validan con datos de campo: (1) selección de fuente superficial; (2-3) offset óptimo más cercano; (4) resolución de imagen de dispersión; (5) frecuencia de corte de modos superiores.

**Instrumentación:** Aplicable a cualquier arreglo MASW activo con geófonos estándar; no añade requerimientos de hardware.

**Factibilidad con presupuesto limitado:** Alta — las ecuaciones son fórmulas de papel/lápiz aplicables en cualquier contexto sin software adicional.

**Conclusiones clave:** Las 5 ecuaciones permiten diseñar un survey MASW de forma cuantitativa: offset mínimo, longitud de arreglo para la resolución deseada, e identificación de modos superiores vs. artefactos numéricos.

**Utilidad para tesis:** Referencia directa para justificar cuantitativamente los parámetros de campo del survey MASW de la tesis; complementa papers 024 (Yoon & Rix 2009) y 053 (Xu et al. 2006) sobre offset mínimo.

**Relevancia:** alta


### 055 · Dikmen 2009 — Vs-SPT Correlations for Soils (J. Geophys. Eng.)

| Campo | Valor |
|-------|-------|
| **ID** | 055 |
| **Autores** | Dikmen Ü |
| **Año** | 2009 |
| **Journal** | Journal of Geophysics and Engineering |
| **Vol/Pág** | 6(1), 61–72 |
| **DOI** | `10.1088/1742-2132/6/1/007` |
| **Landing page** | https://doi.org/10.1088/1742-2132/6/1/007 |
| **PDF local** | `research/papers/pdf/Dikmen2009_Vs_SPT_correlations.pdf` |
| **Tipo fuente** | journal_article |
| **Calidad fuente** | alta |
| **Citas** | 233 (Semantic Scholar) |
| **Categoría** | core |

**Problema abordado:** Las correlaciones entre velocidad de onda de corte (Vs) y resistencia a la penetración estándar (SPT-N) son esenciales para validar perfiles MASW en sitios donde hay sondeos geotécnicos. Las correlaciones existentes provienen de distintos contextos y hay disparidad entre ellas.

**Método:** Se recopilan datos de ensayos sísmicos activos + pasivos y SPT en Eskisehir (Turquía). Se desarrollan nuevas fórmulas empíricas de regresión para todos los suelos, arena, limo y arcilla. Se compara con correlaciones previas de la literatura usando el mismo dataset.

**Instrumentación:** MASW activo + pasivo para medición de Vs. SPT convencional para N.

**Factibilidad con presupuesto limitado:** Alta — las correlaciones son fórmulas analíticas que solo requieren datos SPT (ya disponibles en la mayoría de sitios geotécnicos) y el perfil Vs del MASW.

**Conclusiones clave:** N sin corrección como variable principal. El tipo de suelo tiene influencia secundaria. Las correlaciones son prácticas pero específicas al contexto geológico de derivación; deben verificarse con Vs medido.

**Utilidad para tesis:** Permite cruzar validar perfiles Vs obtenidos por MASW con ensayos SPT disponibles en el sitio de estudio; referenciado en Alhuay 2021 (paper 016); proporciona tabla comparativa de correlaciones de la literatura.

**Relevancia:** alta


### 056 · Bonnefoy-Claudet, Cotton & Bard 2006 — Seismic Noise Wavefield Review (Earth-Sci. Rev.)

| Campo | Valor |
|-------|-------|
| **ID** | 056 |
| **Autores** | Bonnefoy-Claudet S; Cotton F; Bard P-Y |
| **Año** | 2006 |
| **Journal** | Earth-Science Reviews |
| **Vol/Pág** | 79(3-4), 205–227 |
| **DOI** | `10.1016/j.earscirev.2006.07.004` |
| **Landing page** | https://doi.org/10.1016/j.earscirev.2006.07.004 |
| **PDF local** | `research/papers/pdf/BonnefoyClaudet2006_seismic_noise_review.pdf` |
| **Tipo fuente** | journal_article |
| **Calidad fuente** | alta |
| **Citas** | 652 (Semantic Scholar) |
| **Categoría** | core |

**Problema abordado:** Las técnicas basadas en ruido sísmico ambiental (HVSR, SPAC, passive MASW) asumen que el campo de ruido consiste predominantemente en ondas de Rayleigh de modo fundamental. Esta asunción no ha sido evaluada sistemáticamente en la literatura.

**Método:** Revisión bibliográfica exhaustiva de estudios sobre origen y naturaleza del campo de ondas de ruido sísmico en rangos de frecuencia relevantes para la ingeniería geotécnica.

**Hallazgos clave:** >1 Hz: ruido dominado por actividad humana (variaciones diarias/semanales). 0.005–0.3 Hz: actividad natural (oceánica, meteorológica). El origen superficial soporta la presencia de ondas superficiales, pero la asunción de modo fundamental dominante de Rayleigh NO está universalmente soportada — la proporción entre tipos de onda es altamente variable según las condiciones del sitio.

**Utilidad para tesis:** Base teórica obligatoria para justificar el uso de HVSR y MASW pasivo; también proporciona las advertencias sobre limitaciones que un análisis riguroso debe reconocer. Autor Bard = coordinador del proyecto SESAME (paper 019).

**Relevancia:** alta


### 057 · Neducza 2007 — Stacking of Surface Waves (Geophysics)

| Campo | Valor |
|-------|-------|
| **ID** | 057 |
| **Autores** | Neducza B |
| **Año** | 2007 |
| **Journal** | Geophysics |
| **Vol/Pág** | 72(2), V51–V58 |
| **DOI** | `10.1190/1.2431635` |
| **Landing page** | https://doi.org/10.1190/1.2431635 |
| **PDF local** | `research/papers/pdf/Neducza2007_stacking_surface_waves.pdf` |
| **Tipo fuente** | journal_article |
| **Calidad fuente** | alta |
| **Citas** | 68 (Semantic Scholar) |
| **Categoría** | core |

**Problema abordado:** SASW requiere múltiples disparos pero tiene poca resolución horizontal; MASW tiene mejor resolución pero a veces SNR insuficiente con un solo disparo. Se busca un compromiso entre ambos métodos.

**Método:** SSW (Stacking of Surface Waves) — apilado del espectro de amplitud f-k de múltiples disparos con ventaneo espacial. Mejora la relación señal/ruido y la resolución horizontal de la imagen de dispersión.

**Instrumentación:** Cualquier arreglo MASW activo estándar; no añade requerimientos de hardware. Solo requiere múltiples disparos en el mismo punto.

**Factibilidad con presupuesto limitado:** Alta — no añade costo de equipamiento; solo requiere tiempo adicional de adquisición en campo.

**Conclusiones clave:** SSW mejora la calidad de imagen de dispersión combinando las ventajas de SASW y MASW. Directamente aplicable para sitios con ruido ambiental alto o señal débil.

**Utilidad para tesis:** Justifica protocolo de múltiples disparos para mejorar calidad de datos MASW; aplicable en contextos con equipamiento básico donde el SNR puede ser limitante.

**Relevancia:** media-alta


### 058 · Foti et al. 2009 — Non-Uniqueness in Surface-Wave Inversion (Soil Dyn.)

| Campo | Valor |
|-------|-------|
| **ID** | 058 |
| **Autores** | Foti S; Comina C; Boiero D; Socco L.V. |
| **Año** | 2009 |
| **Journal** | Soil Dynamics and Earthquake Engineering |
| **Vol/Pág** | 29(6), 982–993 |
| **DOI** | `10.1016/j.soildyn.2008.11.004` |
| **Landing page** | https://doi.org/10.1016/j.soildyn.2008.11.004 |
| **PDF local** | `research/papers/pdf/Foti2009_non_uniqueness_surface_wave_inversion.pdf` |
| **Tipo fuente** | journal_article |
| **Calidad fuente** | alta |
| **Citas** | 172 (OpenAlex) |
| **Categoría** | core |

**Problema abordado:** La no-unicidad en la inversión de ondas superficiales es criticada como limitación fundamental: distintos perfiles Vs pueden ajustar igualmente bien la curva de dispersión medida. ¿Invalida esto el uso ingenieril del MASW?

**Método:** Inversión Monte Carlo para obtener el conjunto completo de perfiles Vs equivalentes, basado en test estadístico que incorpora incertidumbre en datos y parametrización del modelo. Cada perfil equivalente se usa para calcular la respuesta sísmica 1D.

**Resultado clave:** Los perfiles Vs equivalentes respecto a la inversión de ondas superficiales son también equivalentes respecto a la amplificación de sitio. Esto contraargumenta directamente la crítica sobre la no-unicidad para el uso ingenieril del MASW.

**Utilidad para tesis:** Argumento directo para defender la validez metodológica del MASW en la tesis frente a la crítica de no-unicidad; proporciona marco teórico para reportar incertidumbre en resultados de inversión.

**Relevancia:** alta


### 059 · Park et al. 2005 — Combined Active & Passive Surface Waves (JEEG)

| Campo | Valor |
|-------|-------|
| **ID** | 059 |
| **Autores** | Park C.B.; Miller R.D.; Ryden N; Xia J; Ivanov J |
| **Año** | 2005 |
| **Journal** | Journal of Environmental and Engineering Geophysics |
| **Vol/Pág** | 10(3), 323–334 |
| **DOI** | `10.2113/JEEG10.3.323` |
| **Landing page** | https://doi.org/10.2113/JEEG10.3.323 |
| **PDF local** | `research/papers/pdf/Park2005_MASW_active_passive_comparison.pdf` |
| **Tipo fuente** | journal_article |
| **Calidad fuente** | alta |
| **Citas** | 181 (OpenAlex) |
| **Categoría** | core |

**Problema abordado:** La combinación de MASW activo (>20 Hz, poca profundidad) y pasivo (<20 Hz, mayor profundidad) permite extender el rango de investigación, pero la identificación modal de la curva pasiva es crítica y normalmente se asume erróneamente como modo fundamental.

**Método:** Dos campañas de campo en el mismo sitio con MASW activo y pasivo. Combinación de imágenes de dispersión f-k. En la segunda campaña se re-identificó la curva pasiva como primer modo superior (en lugar de fundamental). La clave fue usar un dataset activo de pequeño espaciado receptor para anclar la identificación modal.

**Resultado clave:** La asunción de modo fundamental en la curva pasiva puede ser incorrecta. La validación con datos activos de pequeño espaciado es esencial para correcta identificación modal.

**Utilidad para tesis:** Guía práctica para protocolo activo+pasivo; advierte sobre la trampa del modo superior en curvas pasivas; directamente aplicable al diseño del experimento MASW de la tesis.

**Relevancia:** alta


### 060 · Asten & Henstridge 1984 — Array Estimators & Microseisms (Geophysics)

| Campo | Valor |
|-------|-------|
| **ID** | 060 |
| **Autores** | Asten M.W.; Henstridge J.D. |
| **Año** | 1984 |
| **Journal** | Geophysics |
| **Vol/Pág** | 49(11), 1828–1837 |
| **DOI** | `10.1190/1.1441596` |
| **Landing page** | https://doi.org/10.1190/1.1441596 |
| **PDF local** | `research/papers/pdf/Asten1984_array_microseisms_sedimentary_basins.pdf` |
| **Tipo fuente** | journal_article |
| **Calidad fuente** | alta |
| **Citas** | 204 (OpenAlex) |
| **Categoría** | peripheral |

**Nota de clasificación:** Paper fundacional para arrays pasivos (f-k en microtremores), pero la aplicación es reconocimiento de cuencas a escala regional, no caracterización Vs para geotecnia. Es un precursor conceptual, no una referencia metodológica directa para el MASW de la tesis.

**Método:** Array de 5-7 sismómetros en configuración de cruz expandible. Análisis f-k de registros de microtremores para medir velocidades de fase de ondas Rayleigh. Estimación de profundidad al basamento.

**Utilidad para tesis:** Precursor histórico de los métodos modernos de array pasivo (conecta con Aki 1957, ReMi 2001, passive MASW); citable en la introducción histórica de métodos pasivos.

**Relevancia:** media (histórico-conceptual)


### 061 · Andrus & Stokoe 2000 — Liquefaction Resistance from Vs (JGGE)

| Campo | Valor |
|-------|-------|
| **ID** | 061 |
| **Autores** | Andrus R.D.; Stokoe K.H. II |
| **Año** | 2000 |
| **Journal** | Journal of Geotechnical and Geoenvironmental Engineering |
| **Vol/Pág** | 126(11), 1015–1025 |
| **DOI** | `10.1061/(ASCE)1090-0241(2000)126:11(1015)` |
| **Landing page** | https://doi.org/10.1061/(ASCE)1090-0241(2000)126:11(1015) |
| **PDF local** | `research/papers/pdf/Andrus2000_liquefaction_Vs_JGGE.pdf` |
| **Tipo fuente** | journal_article |
| **Calidad fuente** | alta |
| **Citas** | 867 (Semantic Scholar) |
| **Categoría** | core |

**Problema abordado:** La evaluación de potencial de licuación requiere parámetros de resistencia cíclica del suelo. El Vs, medible por MASW, es una alternativa directa al SPT/CPT con ventajas (mínimamente invasivo, rápido, aplicable a gravas).

**Método:** Procedimiento simplificado (estilo Seed-Idriss) usando Vs1 normalizado. Validado con base de datos de 26 terremotos (arena fina a gravas con bolones). Curvas CRR vs. Vs1 para diferentes contenidos de finos.

**Resultado:** Predice correctamente potencial de licuación moderado-alto en >95% de casos históricos. Consistente con métodos SPT y CPT.

**Utilidad para tesis:** Referencia estándar para usar el perfil Vs del MASW en evaluación de licuación; conecta directamente el output del método sísmico con la práctica geotécnica; Stokoe (co-inventor del SASW, paper 003) es co-autor.

**Relevancia:** alta


### 062 · Comina et al. 2011 — Reliability of Vs30 from Surface-Wave Tests (JGGE)

| Campo | Valor |
|-------|-------|
| **ID** | 062 |
| **Autores** | Comina C; Foti S; Boiero D; Socco L.V. |
| **Año** | 2011 |
| **Journal** | Journal of Geotechnical and Geoenvironmental Engineering |
| **Vol/Pág** | 137(6), 579–586 |
| **DOI** | `10.1061/(ASCE)GT.1943-5606.0000452` |
| **Landing page** | https://doi.org/10.1061/(ASCE)GT.1943-5606.0000452 |
| **PDF local** | `research/papers/pdf/Comina2011_Vs30_reliability_surface_waves.pdf` |
| **Tipo fuente** | journal_article |
| **Calidad fuente** | alta |
| **Citas** | 83 (OpenAlex) |
| **Categoría** | core |

**Problema abordado:** ¿Qué tan confiable es el Vs30 obtenido desde ondas superficiales? Se evalúa tanto la incertidumbre (dispersión de resultados) como la precisión (sesgo respecto a métodos invasivos).

**Método:** Inversión Monte Carlo de curvas de dispersión experimentales. Selección estadística de perfiles Vs equivalentes. Comparación de Vs30 resultante con valores de referencia de técnicas invasivas.

**Resultado clave:** Con profundidad de investigación adecuada, los métodos de ondas superficiales producen estimaciones de Vs30 comparables en precisión a crosshole y downhole. La no-unicidad no implica inprecisión en Vs30.

**Utilidad para tesis:** Argumento directo para defender la validez del Vs30 obtenido por MASW frente a la comunidad geotécnica; companion del paper 058 (Foti 2009 no-unicidad → no invalida aplicación ingenieril). Grupo Polito (Foti, Socco).

**Relevancia:** alta


### 063 · Borcherdt 1994 — Site-Dependent Response Spectra / NEHRP Vs30 (Earthq. Spectra)

| Campo | Valor |
|-------|-------|
| **ID** | 063 |
| **Autores** | Borcherdt R.D. |
| **Año** | 1994 |
| **Journal** | Earthquake Spectra |
| **Vol/Pág** | 10(4), 617–653 |
| **DOI** | `10.1193/1.1585791` |
| **Landing page** | https://doi.org/10.1193/1.1585791 |
| **PDF local** | `research/papers/pdf/Borcherdt1994_site_response_Vs30_NEHRP.pdf` |
| **Tipo fuente** | journal_article |
| **Calidad fuente** | alta |
| **Citas** | 1060 (Semantic Scholar) |
| **Categoría** | core |

**Problema abordado:** Los códigos sísmicos de construcción necesitan parámetros de sitio simples y medibles para estimar la amplificación del movimiento sísmico. Se busca establecer clases de sitio y factores de amplificación empíricos basados en datos reales.

**Método:** Análisis de registros de movimiento sísmico fuerte del terremoto de Loma Prieta (1989) correlacionados con datos geotécnicos de sondeos y mediciones de Vs. Derivación de factores de amplificación Fa y Fv como función de Vs30.

**Resultado:** Establece las clases de sitio NEHRP A–E (A: roca dura, B: roca, C: suelo muy denso, D: suelo rígido, E: suelo blando) basadas en Vs30. Proporciona factores de amplificación empíricos. Se convirtió en la base del NEHRP, UBC e IBC modernos.

**Utilidad para tesis:** Justifica por qué el Vs30 obtenido por MASW es el parámetro estándar para clasificación sísmica de sitios; hace explícita la cadena MASW → Vs30 → clase NEHRP → amplificación de diseño → criterios de ingeniería.

**Relevancia:** alta


### 064 · Castellaro, Mulargia & Rossi 2008 — Vs30: Proxy for Seismic Amplification? (SRL)

| Campo | Valor |
|-------|-------|
| **ID** | 064 |
| **Autores** | Castellaro S; Mulargia F; Rossi P.L. |
| **Año** | 2008 |
| **Journal** | Seismological Research Letters |
| **Vol/Pág** | 79(4), 540–543 |
| **DOI** | `10.1785/gssrl.79.4.540` |
| **Landing page** | https://doi.org/10.1785/gssrl.79.4.540 |
| **PDF local** | `research/papers/pdf/Castellaro2008_Vs30_proxy_amplification.pdf` |
| **Tipo fuente** | journal_article |
| **Calidad fuente** | alta |
| **Citas** | 236 (Semantic Scholar) |
| **Categoría** | core |

**Problema abordado:** Vs30 se usa universalmente en códigos sísmicos como proxy de amplificación de sitio, pero ¿tiene base física rigurosa? ¿La correlación entre Vs30 y amplificación es realmente robusta?

**Argumento:** Vs30 es un proxy de conveniencia, no de rigor físico. La amplificación sísmica depende de toda la columna de suelo, incluyendo la profundidad al basamento. Un sitio con Vs30 idéntico puede tener amplificaciones muy diferentes según el perfil completo. La correlación estadística es débil en muchos contextos.

**Implicación para tesis:** Refuerza el valor de reportar el **perfil Vs completo** (obtenido por MASW) en lugar de solo el valor escalar Vs30; argumenta que la tesis debe ir más allá del mero Vs30 y discutir el perfil de velocidades como resultado primario.

**Nota:** Companion crítico de Borcherdt 1994 (paper 063). Ambos deben citarse juntos para una discusión equilibrada del rol de Vs30.

**Relevancia:** alta


### 065 · Scherbaum, Hinzen & Ohrnberger 2003 — Vs Profiles from Ambient Vibrations, Cologne (GJI)

| Campo | Valor |
|-------|-------|
| **ID** | 065 |
| **Autores** | Scherbaum F; Hinzen K-G; Ohrnberger M |
| **Año** | 2003 |
| **Journal** | Geophysical Journal International |
| **Vol/Pág** | 152(3), 597–612 |
| **DOI** | `10.1046/j.1365-246x.2003.01856.x` |
| **Landing page** | https://doi.org/10.1046/j.1365-246x.2003.01856.x |
| **PDF local** | `research/papers/pdf/Scherbaum2003_ambient_noise_Vs_Cologne.pdf` |
| **Tipo fuente** | journal_article |
| **Calidad fuente** | alta |
| **Citas** | 356 (Semantic Scholar) |
| **Categoría** | core |

**Problema abordado:** ¿Se pueden obtener perfiles Vs fiables desde vibraciones ambientales (sin fuente activa) combinando análisis de array y H/V en un entorno urbano con geología sedimentaria conocida?

**Método:** Array de sismómetros + análisis f-k (dispersión) + H/V (elipticidad). Inversión conjunta: la curva de dispersión constrain los valores absolutos de velocidad; la elipticidad H/V constrain los espesores de capa. Validado contra sondeos downhole en 3 sitios.

**Resultado clave:** La inversión conjunta dispersión + elipticidad es más robusta que la individual. Las curvas de dispersión proveen las velocidades; el H/V provee los espesores. Amplificación SH predicha ~5-6 a la frecuencia fundamental.

**Utilidad para tesis:** Template práctico para joint inversion; justifica teóricamente el vínculo H/V – elipticidad de Rayleigh; muestra la complementariedad entre array pasivo y H/V; Ohrnberger co-participa en el proyecto SESAME (paper 019).

**Relevancia:** alta
