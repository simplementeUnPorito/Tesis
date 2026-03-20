# Scraping Worklog — Surface Wave Methods Research Database

## Estadísticas globales

| Categoría | Total |
|-----------|-------|
| core | 21 |
| peripheral | 1 |
| reject | 0 |
| Con PDF descargado | 11 |
| Solo con enlace/DOI | 11 |
| **Total** | **22** |

---

## Fase actual: FASE 2 — Scraping y base de datos

**FASE 1 (auditoría vault):** completa — ver Worklog editorial.

**Estrategia de búsqueda general:**
1. Papers seminales de métodos (Park 1999 MASW, Nazarian 1984 SASW, Aki 1957 SPAC, Louie 2001 ReMi)
2. Aplicaciones de campo con geófonos económicos
3. Estudios en contextos de bajo presupuesto / países en desarrollo
4. Revisiones metodológicas comparativas
5. Papers con validación cruzada vs. borehole
6. Casos de joint inversion económica

**Fuentes a explorar:**
- Google Scholar (via WebSearch/WebFetch)
- Semantic Scholar API
- CrossRef API (DOI resolution)
- ResearchGate (landing pages)
- AGU, SEG, EAGE repositories
- Geophysics, Near Surface Geophysics, Journal of Applied Geophysics

---

## Historial de iteraciones

### 2026-03-19 23:48 -03 — Iteración 1 (setup + paper 001)
- **Estado:** VÁLIDA
- **Acción:** Creación de estructura de directorios y archivos base. Procesado paper 001.
- **Query / estrategia:** Paper canónico MASW — Park, Miller & Xia 1999 (Geophysics). Metadata verificada via CrossRef + SEG Library. PDF descargado desde KGS (acceso libre institucional).
- **Paper procesado:** Park CB, Miller RD, Xia J (1999). "Multichannel analysis of surface waves." *Geophysics*, 64(3), 800–808. DOI: 10.1190/1.1444590
- **PDF obtenido:** Sí — `research/papers/pdf/Park1999_MASW.pdf` (1.9 MB, KGS open access)
- **Clasificación:** core
- **Problemas:** Ninguno — PDF accesible directamente desde KGS.
- **Próximo paso:** Procesar Xia, Miller & Park (1999) — paper complementario de inversión MASW (mismo año, mismo grupo KGS). DOI: 10.1190/1.1444543. Publicado también en Geophysics.

### 2026-03-20 00:05 -03 — Iteración 2 (paper 002)
- **Estado:** VÁLIDA
- **Acción:** Procesado paper 002 — companion paper de inversión al MASW canónico.
- **Query / estrategia:** Paper complementario directo del grupo KGS. Xia, Miller & Park 1999 (Geophysics). Metadata verificada via CrossRef. PDF descargado desde KGS (acceso libre institucional).
- **Paper procesado:** Xia J, Miller RD, Park CB (1999). "Estimation of near-surface shear-wave velocity by inversion of Rayleigh waves." *Geophysics*, 64(3), 691–700. DOI: 10.1190/1.1444578
- **PDF obtenido:** Sí — `research/papers/pdf/Xia1999_MASW_inversion.pdf` (427 KB, KGS open access)
- **Clasificación:** core
- **Problemas:** Ninguno — PDF accesible directamente desde KGS.
- **Próximo paso:** Procesar Nazarian & Stokoe (1984) — paper fundacional del método SASW. Contexto: referencia de comparación obligatoria para justificar MASW como mejora. DOI a verificar; posible acceso a través de TRB (Transportation Research Board) o ResearchGate.

### 2026-03-20 00:10 -03 — Iteración 3 (paper 003)
- **Estado:** VÁLIDA
- **Acción:** Procesado paper 003 — paper fundacional del método SASW (antecedente directo del MASW).
- **Query / estrategia:** Búsqueda via CrossRef API + WorldCat + web. Metadata verificada via múltiples fuentes independientes (OCLC, PMC referencias, Google Scholar citations).
- **Paper procesado:** Nazarian S, Stokoe KH (1984). "In situ shear wave velocities from spectral analysis of surface waves." *Proc. 8th World Conference on Earthquake Engineering*, Vol. III, pp. 31–38. Prentice-Hall, San Francisco.
- **PDF obtenido:** No — proceedings de 1984 sin acceso libre digital. WorldCat confirma disponibilidad solo en bibliotecas físicas. DOI inexistente (proceedings preDigital).
- **Clasificación:** core (referencia histórica obligatoria para contextualizar MASW)
- **Problemas:** Sin DOI. Sin PDF libre. Se registró con WorldCat landing page y trazabilidad completa de metadatos.
- **Nota adicional:** Existe un precursor de 1983 (Nazarian, Stokoe & Hudson, TRR 930) con PDF libre en TRB — candidato para siguiente iteración como entrada complementaria.
- **Próximo paso:** Considerar registrar Nazarian, Stokoe & Hudson (1983) TRR 930 como entrada peripheral (con PDF libre disponible), luego procesar Aki (1957) SPAC o Louie (2001) ReMi.

### 2026-03-20 00:21 -03 — Iteración 4 (paper 004)
- **Estado:** VÁLIDA
- **Acción:** Procesado paper 004 — método ReMi, adquisición pasiva con arrays de geófonos estándar.
- **Query / estrategia:** Búsqueda via CrossRef API (DOI corregido de 10.1785/0120000102 → 10.1785/0120000098 confirmado). Metadata verificada via CrossRef. Mirror HTML disponible en U. Memphis.
- **Paper procesado:** Louie JN (2001). "Faster, Better: Shear-Wave Velocity to 100 Meters Depth from Refraction Microtremor Arrays." *Bull. Seismol. Soc. Am.*, 91(2), 347–364. DOI: 10.1785/0120000098
- **PDF obtenido:** No — BSSA paywalled. HTML completo disponible en mirror U. Memphis. ResearchGate requiere login. DOI correcto verificado.
- **Clasificación:** core (método pasivo complementario al MASW; mismo equipamiento; muy relevante para diseño experimental)
- **Problemas:** DOI inicial incorrecto (corregido). PDF no accesible directamente.
- **Próximo paso:** Procesar Aki (1957) — paper fundacional del método SPAC. Contexto: método de autocorrelación espacial para medición pasiva de ondas superficiales; antecedente teórico clave de métodos modernos de ruido ambiental.

### 2026-03-20 00:32 -03 — Iteración 5 (paper 005)
- **Estado:** VÁLIDA
- **Acción:** Procesado paper 005 — paper fundacional del método SPAC (Spatial Autocorrelation).
- **Query / estrategia:** Búsqueda via CrossRef + repositorio UTokyo + CiNii. DOI JaLC encontrado: 10.15083/0000033938. PDF descargado desde repositorio institucional UTokyo.
- **Paper procesado:** Aki K (1957). "Space and Time Spectra of Stationary Stochastic Waves, with Special Reference to Microtremors." *Bull. Earthquake Res. Inst. Univ. Tokyo*, 35(3), 415–456. DOI: 10.15083/0000033938
- **PDF obtenido:** Sí — `research/papers/pdf/Aki1957_SPAC.pdf` (2.2 MB, repositorio institucional UTokyo, acceso libre)
- **Clasificación:** core (fundacional de todos los métodos pasivos basados en autocorrelación espacial)
- **Problemas:** Sin CrossRef DOI (1957), pero DOI JaLC válido encontrado y verificado.
- **Próximo paso:** Procesar Foti et al. (2014) — libro principal de referencia de la tesis ("Surface Wave Methods for Near-Surface Site Characterization", CRC Press). O alternativamente procesar un paper de aplicación de campo con geófonos económicos en contextos de bajo presupuesto.

### 2026-03-20 00:41 -03 — Iteración 6 (paper 006)
- **Estado:** VÁLIDA
- **Acción:** Procesado paper 006 — guías de buenas prácticas InterPACIFIC para análisis de ondas superficiales.
- **Query / estrategia:** Búsqueda via CrossRef API (DOI 10.1007/s10518-017-0206-7). Metadata verificada. PDF open access CC BY 4.0 descargado desde HAL archive.
- **Paper procesado:** Foti S et al. (2018). "Guidelines for the good practice of surface wave analysis: a product of the InterPACIFIC project." *Bull. Earthquake Eng.*, 16(6), 2367–2420. DOI: 10.1007/s10518-017-0206-7
- **PDF obtenido:** Sí — `research/papers/pdf/Foti2018_InterPACIFIC_guidelines.pdf` (8.6 MB, HAL open access CC BY 4.0)
- **Clasificación:** core (referencia metodológica estándar para justificar protocolo de la tesis)
- **Problemas:** Ninguno.
- **Próximo paso:** Considerar un paper de aplicación de campo con MASW en contexto de bajo presupuesto o países en desarrollo, o procesar Garofalo et al. (2016) InterPACIFIC companion paper con resultados del ejercicio comparativo.

### 2026-03-20 01:01 -03 — Iteración 7 (paper 007)
- **Estado:** VÁLIDA
- **Acción:** Procesado paper 007 — Garofalo et al. (2016) InterPACIFIC Part I, intra-comparación de métodos de ondas superficiales.
- **Query / estrategia:** DOI 10.1016/j.soildyn.2015.12.010 verificado via CrossRef. Búsqueda de PDF libre: Unpaywall confirma closed. Elsevier sin OA. IRIS Polito bloqueado.
- **Paper procesado:** Garofalo F et al. (2016). "InterPACIFIC project: Comparison of invasive and non-invasive methods for seismic site characterization. Part I: Intra-comparison of surface wave methods." *Soil Dyn. Earthquake Eng.*, 82, 222–240. DOI: 10.1016/j.soildyn.2015.12.010
- **PDF obtenido:** No — Elsevier closed (Unpaywall confirmado).
- **Clasificación:** core (companion de Foti 2018; comparación cuantitativa inter-laboratorios de métodos de ondas superficiales)
- **Problemas:** PDF no disponible en OA. Se documentó con trazabilidad completa.
- **Próximo paso:** Procesar un paper de aplicación de campo en contexto de bajo presupuesto. Candidatos: (a) Socco & Strobbia (2004) review paper en Near Surface Geophysics, o (b) un paper de MASW en Latinoamérica o contexto similar.

### 2026-03-20 01:21 -03 — Iteración 8 (paper 008)
- **Estado:** VÁLIDA
- **Acción:** Procesado paper 008 — Socco & Strobbia (2004) tutorial completo de métodos de ondas superficiales.
- **Query / estrategia:** DOI verificado via CrossRef (DOI inicial incorrecto — corregido a 10.3997/1873-0604.2004015). Búsqueda PDF: EAGE paywalled, IRIS Polito bloqueado, ResearchGate requiere login.
- **Paper procesado:** Socco LV, Strobbia C (2004). "Surface-wave method for near-surface characterization: a tutorial." *Near Surface Geophysics*, 2(4), 165–185. DOI: 10.3997/1873-0604.2004015
- **PDF obtenido:** No — EAGE paywalled. Sin OA verificado.
- **Clasificación:** core (tutorial de referencia metodológica completa — aplicable íntegramente al diseño experimental de la tesis)
- **Problemas:** DOI inicial incorrecto (corregido). PDF no accesible.
- **Próximo paso:** Pasar a papers de APLICACIÓN DE CAMPO — especialmente MASW en países en desarrollo o con bajo presupuesto. Candidato: Tsuji et al. (2011) MASW en Nepal/Asia, o Garofalo et al. (2016) Part II, o un paper latinoamericano de MASW aplicado.

### 2026-03-20 01:41 -03 — Iteración 9 (paper 009)
- **Estado:** VÁLIDA
- **Acción:** Procesado paper 009 — Xia et al. (2002) validación MASW contra borehole.
- **Query / estrategia:** DOI inicial incorrecto (10.1190/1.1516004) — corregido a 10.1016/S0267-7261(02)00008-8 via CrossRef. Agente también identificó papers KGS con PDF libre aún no procesados: XiaEtAl2004 (DOI 10.1190/1.1845123) y ParkEtAl2007.
- **Paper procesado:** Xia J, Miller RD, Park CB, Hunter JA, Harris JB, Ivanov J (2002). "Comparing shear-wave velocity profiles inverted from multichannel surface wave with borehole measurements." *Soil Dyn. Earthquake Eng.*, 22(3), 181–190. DOI: 10.1016/S0267-7261(02)00008-8
- **PDF obtenido:** No — Elsevier paywalled.
- **Clasificación:** core (validación directa del método — argumento clave para la tesis)
- **Problemas:** PDF no accesible. DOI inicial incorrecto.
- **Próximo paso:** Procesar XiaEtAl2004 desde KGS (DOI 10.1190/1.1845123, PDF libre disponible) o ParkEtAl2007 desde KGS. Alternativamente, buscar paper de MASW en Latinoamérica.

### 2026-03-20 02:01 -03 — Iteración 10 (paper 010)
- **Estado:** VÁLIDA
- **Acción:** Procesado paper 010 — Park et al. (2007) review práctico de MASW activo y pasivo.
- **Query / estrategia:** DOI 10.1190/1.2431832 verificado via CrossRef. PDF descargado desde KGS (open access, 643 KB).
- **Paper procesado:** Park CB, Miller RD, Xia J, Ivanov J (2007). "Multichannel analysis of surface waves (MASW)—active and passive methods." *The Leading Edge*, 26(1), 60–64. DOI: 10.1190/1.2431832
- **PDF obtenido:** Sí — `research/papers/pdf/Park2007_MASW_active_passive.pdf` (643 KB, KGS open access)
- **Clasificación:** core (review práctico directo del diseño experimental activo + pasivo con mismo equipo)
- **Problemas:** Ninguno.
- **Nota:** KGS tiene también ParkEtAl2004.pdf (730K), ParkEtAl2005.pdf (2.1M) y XiaEtAl2004_1.1845123v2.pdf (266K) con PDFs accesibles.
- **Próximo paso:** Cambio de estrategia — procesar XiaEtAl2004 (DOI 10.1190/1.1845123) desde KGS para completar el conjunto de papers KGS open-access. O alternativamente, procesar un paper de aplicación en Latinoamérica o con geófonos de bajo costo para diversificar la base.

### 2026-03-20 02:23 -03 — Iteración 11 (paper 011)
- **Estado:** VÁLIDA
- **Acción:** Procesado paper 011 — Xia et al. (2004) inversión generalizada para mayor resolución horizontal en MASW.
- **Query / estrategia:** DOI 10.1190/1.1845123 verificado via CrossRef API. PDF descargado desde KGS open access (272 KB). DOI identificado en iteración 10 como candidato KGS. CrossRef confirma: SEG Technical Program Expanded Abstracts 2004, pp. 1437–1440 (abstract de 4 páginas, no artículo de revista como se anticipó).
- **Paper procesado:** Xia J, Miller RD, Chen C, Ivanov J (2004). "Increasing horizontal resolution of geophysical models by generalized inversion." *SEG Technical Program Expanded Abstracts 2004*, pp. 1437–1440. DOI: 10.1190/1.1845123
- **PDF obtenido:** Sí — `research/papers/pdf/Xia2004_MASW_horizontal_resolution.pdf` (272 KB, KGS open access)
- **Clasificación:** peripheral (abstract corto de 4 páginas; extensión metodológica de inversión 2D; sin validación sistemática vs. borehole; menos crítico que los core papers)
- **Problemas:** El papel fue inicialmente identificado como candidato "artículo KGS" pero CrossRef confirma que es un SEG expanded abstract. La clasificación se ajustó a peripheral en consecuencia. Sin otros problemas.
- **Próximo paso:** Diversificar la base de datos hacia papers de aplicación de campo en contextos de bajo presupuesto o países en desarrollo. Candidatos: (a) ParkEtAl2004 desde KGS (ParkEtAl2004.pdf, 730 KB), (b) ParkEtAl2005 desde KGS (ParkEtAl2005.pdf, 2.1 MB), o (c) buscar paper de MASW aplicado en Latinoamérica / región comparable. Opción (c) añadiría más diversidad temática y geográfica a la colección actual.

### 2026-03-20 02:43 -03 — Iteración 12 (paper 012)
- **Estado:** VÁLIDA
- **Acción:** Procesado paper 012 — Ayele et al. (2022) MASW en Etiopía. Diversificación hacia aplicación de campo en país en desarrollo.
- **Query / estrategia:** WebSearch "MASW Latin America / developing country" → resultados no-latinoamericanos pero sí contexto análogo. Artículo Wiley Open Access identificado: Ayele 2022, International Journal of Geophysics. DOI verificado via CrossRef (CC BY 4.0). Metadata completa via Semantic Scholar API. PDF verificado como libre (Hindawi) pero protegido por Cloudflare — sin descarga automática posible.
- **Paper procesado:** Ayele A, Woldearegay K, Meten M (2022). "Multichannel Analysis of Surface Waves (MASW) to Estimate the Shear Wave Velocity for Engineering Characterization of Soils at Hawassa Town, Southern Ethiopia." *International Journal of Geophysics*, 2022, art. 7588306. DOI: 10.1155/2022/7588306
- **PDF obtenido:** No (PDF libre verificado — Gold OA CC BY 4.0 — pero Hindawi/Cloudflare bloquea descarga automática. URL: https://downloads.hindawi.com/journals/ijge/2022/7588306.pdf)
- **Clasificación:** core (caso de campo en país en desarrollo análogo a Paraguay: MASW activo estándar + VES + SPT; Vs30; clasificación sísmica; equipamiento básico; directamente citable)
- **Problemas:** PDF no descargable automáticamente por Cloudflare challenge. Toda la metadata verificada y trazabilidad completa documentada.
- **Próximo paso:** Continuar diversificando la base. Candidatos: (a) Olafsdottir et al. (2018) — MASWaves tool paper, Canadian Geotechnical Journal (DOI: 10.1139/cgj-2016-0302; posiblemente paywalled); (b) buscar otro caso de MASW en Latinoamérica (Brasil, Colombia, Chile, Perú); (c) procesar ParkEtAl2004 o ParkEtAl2005 desde KGS. Para mayor diversidad geográfica: buscar paper latinoamericano específico.

### 2026-03-20 03:01 -03 — Iteración 13 (paper 013)
- **Estado:** VÁLIDA
- **Acción:** Procesado paper 013 — Olafsdottir et al. (2020) herramienta open-source de inversión MASW (MASWaves). Identificado durante búsqueda de papers latinoamericanos — aunque el origen es Islandia, es directamente más útil para la tesis que un paper latinoamericano de aplicación.
- **Query / estrategia:** WebSearch "MASW Latin America developing country" + "Open-Source MASW Inversion Tool". DOI 10.3390/geosciences10080322 verificado via CrossRef y Semantic Scholar. Metadata completa. PDF Gold OA CC BY 4.0 confirmado via CrossRef y DOAJ. PDF no descargable automáticamente (MDPI bloquea con JS challenge + Access Denied).
- **Paper procesado:** Olafsdottir EA, Erlingsson S, Bessason B (2020). "Open-Source MASW Inversion Tool Aimed at Shear Wave Velocity Profiling for Soil Site Explorations." *Geosciences*, 10(8), 322. DOI: 10.3390/geosciences10080322
- **PDF obtenido:** No (Gold OA CC BY 4.0 verificado; MDPI bloquea descarga automática; acceso manual disponible)
- **Clasificación:** core (software open-source directamente utilizable en la tesis; MATLAB + Python; inversión Monte Carlo con cuantificación de incertidumbre)
- **Problemas:** PDF no descargable automáticamente desde MDPI (Access Denied en curl). Sin otros problemas.
- **Próximo paso:** (a) Olafsdottir et al. 2018 (CGJ, companion processing paper — paywalled) — documentar sin PDF; (b) Buscar paper latinoamericano específico; (c) Procesar ParkEtAl2004 o ParkEtAl2005 desde KGS (PDF libre disponible). Opción más valiosa para diversidad: encontrar paper de MASW aplicado en contexto latinoamericano o de ingeniería civil en país en desarrollo.

### 2026-03-20 03:21 -03 — Iteración 14 (paper 014)
- **Estado:** VÁLIDA
- **Acción:** Procesado paper 014 — Wathelet et al. (2020) Geopsy. Iniciada como búsqueda de paper latinoamericano — redirigida tras revisar ParkEtAl2004 (passive 2D cross-layout, periférico) y ParkEtAl2005 (underwater MASW, periférico). Geopsy resultó el hallazgo más valioso de la iteración.
- **Query / estrategia:** WebSearch "MASW Latin America DOI" + "Wathelet Geopsy SRL 2020". DOI 10.1785/0220190360 verificado via CrossRef y Semantic Scholar. HAL versión registrada pero sin PDF depositado. SRL paywalled. Sin PDF disponible.
- **Paper procesado:** Wathelet M, Chatelain J-L, Cornou C, Di Giulio G, Guillier B, Ohrnberger M, Savvaidis A (2020). "Geopsy: A User-Friendly Open-Source Tool Set for Ambient Vibration Processing." *Seismological Research Letters*, 91(3), 1878–1889. DOI: 10.1785/0220190360
- **PDF obtenido:** No (HAL registrado sin archivo; SRL paywalled; 343 citas — paper bien conocido)
- **Clasificación:** core (software gratuito open-source GPL v3 directamente utilizable en la tesis; 343 citas; referencia estándar para métodos pasivos y HVSR)
- **Problemas:** ParkEtAl2004 y ParkEtAl2005 revisados y descartados como periféricos (passive 2D array y underwater MASW respectivamente) — no incluidos en la base esta iteración. PDF de Geopsy no descargable.
- **Próximo paso:** (a) Buscar paper latinoamericano (Colombia, Brasil, Chile, Perú) con DOI verificado y PDF accesible; (b) Procesar Olafsdottir et al. 2018 (CGJ processing companion — paywalled); (c) Considerar paper de HVSR / Nakamura técnica para complementar métodos pasivos; (d) Schwenk 2016 o ParkEtAl2004/2005 como periféricos si hay tiempo. Prioridad: caso latinoamericano o HVSR Nakamura.

### 2026-03-20 03:41 -03 — Iteración 15 (paper 015)
- **Estado:** VÁLIDA
- **Acción:** Procesado paper 015 — Moffat, Correia & Pastén (2016), primer paper latinoamericano con PDF descargado. Validación MASW vs. downhole en Chile central.
- **Query / estrategia:** WebSearch SciELO MASW Latinoamérica → identificados dos candidatos: (a) Alhuay-León 2021 Peru (MASW+SPT Olmos, eolian sand, DOI: 10.15446/DYNA.V88N217.93317) y (b) Moffat 2016 Chile (comparación Vs30 MASW/downhole, DOI: 10.4067/S0718-28132016000200001). Seleccionado Moffat 2016 por mayor detalle metodológico y especificación exacta de hardware. DOI verificado via CrossRef. PDF descargado desde SciELO Chile (3.4 MB, 10 páginas, OA CC BY-NC 4.0). Metadata extraída de PDF con pdftotext.
- **Paper procesado:** Moffat R, Correia N, Pastén C (2016). "Comparison of mean shear wave velocity of the top 30 m using downhole, MASW and bender elements methods." *Obras y Proyectos*, 20, 6–15. DOI: 10.4067/S0718-28132016000200001
- **PDF obtenido:** Sí — `research/papers/pdf/Moffat2016_Vs30_MASW_downhole_Chile.pdf` (3.4 MB, SciELO Chile OA)
- **Clasificación:** core (validación MASW vs. downhole en Chile; 12 geófonos 4.5 Hz especificados; usa Geopsy; contexto latinoamericano; cita Foti 2014 y Park 1999)
- **Problemas:** SciELO Colombia y Chile bloquearon el primer intento de WebFetch (ECONNREFUSED / 403) — resuelto buscando DOIs via WebSearch y descargando PDF directamente.
- **Próximo paso:** (a) Procesar Alhuay-León 2021 Peru (MASW+SPT en Olmos — DOI: 10.15446/DYNA.V88N217.93317 — Redalyc/SciELO, PDF libre) — segundo candidato latinoamericano identificado esta iteración; (b) Paper HVSR Nakamura 1989 (fundacional, muy citado); (c) Olafsdottir et al. 2018 (CGJ companion — paywalled). Prioridad próxima iteración: Alhuay-León 2021 Peru (segundo paper latinoamericano, MASW+SPT).

### 2026-03-20 03:47 -03 — Iteración 16 (paper 016)
- **Estado:** VÁLIDA
- **Acción:** Procesado paper 016 — correlación MASW-SPT en arenas eólicas, Perú.
- **Query / estrategia:** Candidato identificado en iteración 15: Alhuay-León & Trejo-Noreña (2021), DOI: 10.15446/dyna.v88n217.93317. DOI verificado via CrossRef + Semantic Scholar API. PDF obtenido desde UNAL repository (GOLD OA, CC BY-NC-ND 4.0). Contenido extraído con pdftotext.
- **Paper procesado:** Alhuay-León CG & Trejo-Noreña PC (2021). "The empirical correlation between shear wave velocity and penetration resistance for the eolian sand deposits in the city of Olmos-Peru." *DYNA*, 88(217), pp.247–255. DOI: 10.15446/dyna.v88n217.93317
- **PDF obtenido:** Sí — `research/papers/pdf/Alhuay2021_MASW_SPT_Peru.pdf` (1.07 MB, UNAL repository, CC BY-NC-ND 4.0)
- **Clasificación:** core
- **Hallazgos clave:**
  - Instrumentación: Geometrics Geode 24-channel + 24 geófonos verticales 4.5 Hz + martillo 25 lb sobre placa metálica
  - Procesamiento: phase-shift method (Park et al. 1998)
  - Sitio: arenas eólicas cuaternarias secas en Olmos, Lambayeque, Perú
  - Resultados: Vs30 = 180-360 m/s (Tipo D NEHRP); correlaciones Vs=65.5*N60^0.33 y Vs=21.6*N60^0.38*(σ'v)^0.24
  - Calidad imagen de dispersión excelente por bajo ruido ambiental y topografía plana
- **Problemas:** Ninguno — PDF descargado sin problemas desde UNAL repository.
- **Próximo paso:** Opciones identificadas:
  a) Procesar Nakamura (1989) — paper fundacional HVSR (complementa MASW con método pasivo de estación única, muy citado)
  b) Procesar Olafsdottir et al. 2018 — "Tool for analysis of MASW field data" (CGJ, compañero de paper 013; paywalled — buscar vía Sci-Hub o ResearchGate)
  c) Buscar paper de MASW aplicado a Paraguay o países con condiciones similares (Paraguay — río, sedimentos aluviales)
  d) Procesar Dikmen 2009 — correlaciones Vs-N ampliamente citadas; referenciado en Alhuay 2021; journal of Geophysics and Engineering

### 2026-03-20 04:01 -03 — Iteración 17 (paper 017)
- **Estado:** VÁLIDA
- **Acción:** Procesado paper 017 — Nakamura 1989, paper fundacional de la técnica HVSR.
- **Query / estrategia:** Candidato identificado desde iteraciones anteriores. Búsqueda via Semantic Scholar + CrossRef + TRID (Transportation Research International Documentation). Confirmación de ausencia de DOI (reporte técnico pre-digital). Verificación de disponibilidad de PDF — no existe versión digital libre (RTRI digitaliza desde vol.35/1994; vol.30 no accesible).
- **Paper procesado:** Nakamura Y (1989). "A method for dynamic characteristics estimation of subsurface using microtremor on the ground surface." *Quarterly Report of the Railway Technical Research Institute (RTRI)*, 30(1), pp. 25–33.
- **PDF obtenido:** No — reporte técnico pre-digital. RTRI archivo online comienza en vol.35 (1994). Acceso posible solo vía ILL o contacto directo con RTRI (ISSN 0033-9008, TRID accession 00480707).
- **Clasificación:** core (miles de citas; método HVSR complementario al MASW; extremadamente económico; vault ya tiene HVSR.md)
- **Problemas:** Ninguno técnico. Sin PDF disponible por limitación estructural (pre-digital). Rate limit 429 en Semantic Scholar API — resuelto con subagente.
- **Próximo paso:** Opciones para iteración 18:
  a) Procesar Lermo & Chávez-García (1993) — "Site effect evaluation using spectral ratios with only one station" (BSSA) — primer paper que valida y populariza la técnica de Nakamura con datos de terremoto; DOI disponible; más accesible que el paper original de 1989.
  b) Olafsdottir et al. 2018 — "Tool for analysis of MASW field data" (CGJ DOI:10.1139/cgj-2016-0302) — paywalled, companion de paper 013.
  c) Buscar paper de MASW aplicado en Paraguay directamente o en contextos de cuencas sedimentarias aluviales similares.

### 2026-03-20 04:21 -03 — Iteración 18 (paper 018)
- **Estado:** VÁLIDA
- **Acción:** Procesado paper 018 — Lermo & Chávez-García (1993), primera validación sistemática del H/V con registros de terremoto.
- **Query / estrategia:** Candidato identificado en iteración 17 como companion de Nakamura 1989. DOI verificado via CrossRef (10.1785/bssa0830051574). Citas verificadas via Semantic Scholar (1103). Intentos de acceso a PDF: GeoScienceWorld (403 bloqueado), ResearchGate (403 bloqueado), WebSearch (sin resultado OA). Registrado como no_descargado con DOI y landing page trazable.
- **Paper procesado:** Lermo J & Chávez-García FJ (1993). "Site effect evaluation using spectral ratios with only one station." *Bulletin of the Seismological Society of America*, 83(5), pp. 1574–1594. DOI: 10.1785/bssa0830051574
- **PDF obtenido:** No — paywalled en GeoScienceWorld; sin versión OA identificada.
- **Clasificación:** core (1103 citas; valida Nakamura 1989; fundacional para HVSR; contexto latinoamericano México)
- **Problemas:** PDF no accesible libremente. GeoScienceWorld y ResearchGate bloquearon acceso automatizado.
- **Próximo paso:** Opciones para iteración 19:
  a) Buscar un paper de MASW aplicado a contextos de cuencas sedimentarias o suelos aluviales sudamericanos (Paraguay no tiene papers directos — buscar en Argentina, Brasil, Bolivia).
  b) Procesar Bonnefoy-Claudet et al. (2006) — "The nature of noise wavefield and its applications for site effects studies" (Earth-Science Reviews) — revisión del campo difuso y fundamentos teóricos del HVSR; muy citada.
  c) Procesar SESAME guidelines (2004) — "Guidelines for the implementation of the H/V spectral ratio technique" — documento de referencia técnica para aplicación práctica de HVSR.
  d) Procesar Dikmen (2009) — correlaciones Vs-N para suelos (DOI: 10.1088/1742-2132/6/1/007) — referenciado en Alhuay 2021.
  Prioridad: SESAME 2004 (muy citable, referencia práctica directa; posiblemente disponible como OA).

### 2026-03-20 04:41 -03 — Iteración 19 (paper 019)
- **Estado:** VÁLIDA
- **Acción:** Procesado paper 019 — SESAME 2004 guidelines, guías de referencia estándar para implementación práctica del método H/V.
- **Query / estrategia:** Candidato identificado en iteración 18 como prioridad (guía técnica de implementación HVSR). Búsqueda via WebSearch confirmó URL directa: sesame.geopsy.org/Papers/HV_User_Guidelines.pdf. PDF descargado exitosamente (1.1 MB, 63 pp.). Contenido extraído con pdftotext: tabla de contenidos completa, criterios cuantitativos de confiabilidad, requisitos de instrumentación, condiciones de campo.
- **Paper procesado:** SESAME European Research Project WP12 (coord. Bard P-Y et al.) (2004). "Guidelines for the Implementation of the H/V Spectral Ratio Technique on Ambient Vibrations — Measurements, Processing and Interpretation." Deliverable D23.12. EU Project EVG1-CT-2000-00026. 63 pp.
- **PDF obtenido:** Sí — `research/papers/pdf/SESAME2004_HV_Guidelines.pdf` (1.1 MB, sesame.geopsy.org, libre)
- **Clasificación:** core (miles de citas; guía estándar internacional; criterios cuantitativos directamente aplicables; indica explícitamente que H/V es especialmente recomendado en sismicidad baja/moderada como Paraguay)
- **Hallazgos clave del documento:**
  - Duración mínima de registro: 30 min para f0 < 0.2 Hz; 3-5 min para f0 > 5 Hz
  - Criterio de confiabilidad: f0 > 10/lw; nc(f0) > 200; σA(f) < 2
  - Criterio de pico claro: 5 de 6 condiciones cuantitativas
  - Instrumento: sensor 3C con frecuencia de corte ≤ f0 esperada
  - "The method is especially recommended in areas of low and moderate seismicity"
  - Coordinador P-Y Bard, co-participante Marc Wathelet (Geopsy, paper 014)
- **Problemas:** Semantic Scholar API rate-limited (429). Sin DOI (entregable EU).
- **Próximo paso:** Opciones para iteración 20:
  a) Pivotar a papers de MASW en contextos sudamericanos de cuencas sedimentarias — Argentina, Brasil o Bolivia. Paraguay no tiene papers directos de MASW publicados en revistas indexadas.
  b) Procesar Maheswari et al. (2010) — "Use of surface waves in statistical correlations of shear wave velocity and penetration resistance of Chennai soils" (Geotech Geol Eng, DOI:10.1007/s10706-010-9334-4) — referenciado en Alhuay 2021; MASW para correlaciones Vs-N en India.
  c) Procesar un paper de MASW con joint inversion MASW+HVSR (doble método, económico).
  Prioridad: buscar paper de cuenca aluvial sudamericana con MASW (Argentina o Bolivia — sedimentos similares a Paraguay).

### 2026-03-20 05:01 -03 — Iteración 20 (paper 020)
- **Estado:** VÁLIDA
- **Acción:** Procesado paper 020 — caso de estudio colombiano de caracterización multi-método con MASW 1D+2D, TRS, SEV y SPT.
- **Query / estrategia:** Búsqueda de papers MASW en cuencas sedimentarias sudamericanas (Argentina, Bolivia). No se encontraron papers directos de esas regiones. Resultado encontrado: artículo del Boletín de Ciencias de la Tierra (UNAL Colombia) sobre caracterización de sitio multi-método en Pamplona, Colombia. PDF descargado via Dialnet (ya disponible como descarga del WebFetch anterior). DOI verificado via CrossRef (10.15446/rbct.n48.85411). Contenido extraído con pdftotext.
- **Paper procesado:** Moya-Gutiérrez AJ, Torres-Peña JA & Contreras-Martínez M (2020). "Site characterization using geophysical and geotechnical Prospecting. Case study main road North Central Trunk (Route 55) at Km 68+500, Pamplona, Norte de Santander, Colombia." *Boletín de Ciencias de la Tierra*, 48, pp. 30–45. DOI: 10.15446/rbct.n48.85411
- **PDF obtenido:** Sí — `research/papers/pdf/MoyaGutierrez2020_MASW_TRS_Colombia.pdf` (5.3 MB, 16 pp., Dialnet OA CC BY-NC-ND 4.0)
- **Clasificación:** core (workflow multi-método con Geometrics Geode; contexto Latinoamérica; parámetros dinámicos; OA con PDF)
- **Hallazgos clave:**
  - Equipamiento: Geometrics Geode 24-channel + geófonos 14 Hz + martillo 12 lb
  - Limitación: 14 Hz geophones = menor profundidad vs. 4.5 Hz (subóptimo para MASW profundo)
  - Procesamiento: SeisImager/SW + Seismic Unix (CWP)
  - Resultados: Vs = 210-466 m/s; suelo Tipo D; parámetros dinámicos ν, E, G, densidad
  - Contexto: caracterización vial NSR-10 (norma colombiana), 2322 msnm
- **Problemas:** Argentina/Bolivia MASW papers no encontrados en búsquedas web (probablemente publicados en congresos locales o repositorios nacionales no indexados internacionalmente).
- **Próximo paso:** Opciones para iteración 21:
  a) Procesar Maheswari et al. 2010 (DOI: 10.1007/s10706-010-9334-4) — MASW + correlaciones Vs-N en Chennai, India; referenciado en Alhuay 2021.
  b) Buscar papers de MASW en Brasil o Colombia aplicados a suelos aluviales/tropicales (más similares a Paraguay).
  c) Evaluar si la base de datos ya tiene cobertura suficiente para la tesis y considerar cerrar FASE 2.
  Nota: Con 20 entradas (19 core, 1 peripheral) y 10 PDFs, la base es sólida. Evaluar si conviene continuar o declarar completitud.

### 2026-03-20 05:23 -03 — Iteración 21 (paper 021)
- **Estado:** VÁLIDA
- **Acción:** Procesado paper 021 — Uma Maheswari et al. (2010), MASW+SPT correlaciones Vs-N en Chennai, India.
- **Query / estrategia:** Paper referenciado en Alhuay 2021 (paper 016). DOI inicial incorrecto (10.1007/s10706-010-9334-4 = discusión de Gulerce). DOI correcto verificado via CrossRef: 10.1007/s10706-009-9285-9. Unpaywall confirma sin OA. Conference paper precursor WCEE 2008 localizado en IITK (PDF libre), usado para reconstruir contenido metodológico del journal paper. Metadata verified via CrossRef + Springer + secondary sources.
- **Paper procesado:** Uma Maheswari R, Boominathan A, Dodagoudar GR (2010). "Use of Surface Waves in Statistical Correlations of Shear Wave Velocity and Penetration Resistance of Chennai Soils." *Geotechnical and Geological Engineering*, 28(2), 119–137. DOI: 10.1007/s10706-009-9285-9
- **PDF obtenido:** No — Springer paywalled, sin OA. Conference paper precursor (WCEE 2008) tiene PDF libre en IITK: https://www.iitk.ac.in/nicee/wcee/article/14_04-01-0090.PDF
- **Clasificación:** core
- **Contenido clave:** 30 sitios urbanos en Chennai. Geometrics Geode 24-channel + geófonos 4.5 Hz + martillo 8 kg. Espaciamiento 1 m, apertura 23 m. SurfSeis software. 200 pares Vs-N. Correlación: Vs = 95.64·N^0.301 (r²=0.83, todos los suelos); separada para arcilla y arena. Validación por crosshole sísmico (Adyar) y bender element. NEHRP Clase D predominante. Período fundamental 0.03–0.6 s.
- **Problemas:** DOI incorrecto en referencia original (el DOI dado correspondía a la discusión publicada, no al paper original). PDF no disponible OA. Semantic Scholar rate-limited — no se verificaron citas.
- **Próximo paso:** Evaluar si la base de datos ya tiene cobertura suficiente para declarar FASE 2 completa. Con 21 entradas (20 core + 1 peripheral), 10 PDFs locales y cobertura de todos los métodos principales, la base es sólida. Alternativas de continuación: (a) Procesar Olafsdottir et al. (2018) — MASWaves tool companion, CGJ DOI 10.1139/cgj-2016-0302, aún sin procesar; (b) Buscar papers MASW en Brasil (suelos tropicales residuales — contexto similar a Paraguay); (c) Declarar FASE 2 completa y registrar cierre.

### 2026-03-20 05:41 -03 — Iteración 22 (paper 022)
- **Estado:** VÁLIDA
- **Acción:** Procesado paper 022 — Ólafsdóttir, Erlingsson & Bessason (2018), herramienta open-source MASWaves para análisis MASW completo.
- **Query / estrategia:** Paper identificado como companion de paper 013 (Olafsdottir et al. 2020), aún sin procesar. DOI: 10.1139/cgj-2016-0302 verificado via CrossRef. Unpaywall confirma OA híbrido (CC BY 4.0). PDF descargado desde Opin visindi (repositorio institucional Universidad de Islandia): https://opinvisindi.is/bitstream/20.500.11815/755/1/cgj-2016-0302.pdf (9.23 MB).
- **Paper procesado:** Ólafsdóttir EÁ, Erlingsson S, Bessason B (2018). "Tool for analysis of multichannel analysis of surface waves (MASW) field data and evaluation of shear wave velocity profiles of soils." *Canadian Geotechnical Journal*, 55(2), 217–233. DOI: 10.1139/cgj-2016-0302
- **PDF obtenido:** Sí — `research/papers/pdf/Olafsdottir2018_MASWaves_field_tool.pdf` (9.23 MB, CC BY 4.0, Opin visindi)
- **Clasificación:** core
- **Contenido clave:** MASWaves = software open-source MATLAB gratuito con dos módulos: MASWaves Dispersion (phase-shift, Park 1998) + MASWaves Inversion (backcálculo LS). Validado contra Geopsy (dispersión) y WinSASW (inversión). 3 sitios campo Islandia sur (arena glaciofluvial, arena litoral moderna, arena limosa cementada): 24 geófonos verticales GS-11D 4.5 Hz + sledgehammer. Datos de muestra + guía de usuario incluidos. Descargable en uni.hi.is/eao4/.
- **Problemas:** Ninguno. PDF disponible OA en repositorio institucional. Paper claramente distinguible del paper 013 (2020 = versión Monte Carlo de la inversión).
- **Próximo paso:** Con 22 entradas (21 core + 1 peripheral), 11 PDFs y cobertura completa de: métodos principales (MASW, SASW, ReMi, SPAC, HVSR), software libre (MASWaves 2018+2020, Geopsy), directrices de calidad (InterPACIFIC, SESAME), casos de campo en países en desarrollo (Perú, Colombia, India, Chile, Etiopía, Islandia), la base de datos ha alcanzado un nivel sólido y suficiente para la tesis. **Evaluar cierre de FASE 2 en la próxima iteración.**
