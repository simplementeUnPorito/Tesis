# Worklog de resumen

## Estado general
- Chapter 1: **consolidado (segunda fase)** — secciones 1.3, 1.3.1, 1.4, 1.4.1, 1.4.2, 1.4.3 reescritas con trazabilidad Foti y referencias por página; 1.7.2–1.7.6 y 1.8 presentes desde iteración anterior; capítulo completo y coherente con el resto del vault
- Chapter 2: **consolidado (tercera fase completa)** — Introducción (~95→220p), 2.2.4 (~80→280p), 2.5.1 (~80→220p) expandidas; [[Poisson Ratio]] enlazado
- Chapter 3: **consolidado (tercera fase completa)** — secciones 3.3.2, 3.1.2, 3.3.6, 3.4.3.3 expandidas; ninguna sección queda < 150 palabras
- Chapter 4 y 5: **consolidado (tercera fase completa)** — secciones 4.2 SSRM, 5.5.1, 5.5.2 expandidas en tercera fase
- Chapter 6: **consolidado (tercera fase completa)** — calidad alta desde primera fase; revisado tercera fase, ninguna sección < 150 palabras
- Chapter 7: **consolidado (tercera fase completa)** — sección 7.3 intro expandida de ~80 a ~260 palabras; resto sin cambios necesarios
- Chapter 8: **consolidado (tercera fase completa)** — intro sección 8.3 añadida (~190 palabras); sección 8.3.2 intro expandida de ~80 a ~230 palabras

## Último punto procesado
- Capítulo actual: Chapter 1 — segunda fase (completada)
- Sección actual: todas las secciones del capítulo presentes y con trazabilidad Foti
- Fase actual: segunda (Chapter 1 consolidado)
- PDF fuente utilizado: Sebastiano Foti Chapter 1.pdf, pp. 1–20 (secciones 1.2–1.3.3 del PDF)
- Página inicial aproximada: 5
- Página final aproximada: 20
- Pendiente Chapter 1: ninguno — capítulo en estado comparable al resto del vault

## Conceptos creados o actualizados en la última iteración
- **Tercera fase**: creados 6 conceptos nuevos en Concepts/
  - `Concepts/08 Inversion and Interpretation/HVSR.md` — principio, singularidades f_H/f_V, f₀ = Vs/4H, SESAME 2004, inversión, limitaciones
  - `Concepts/07 Acquisition and Processing/Seismic Interferometry.md` — cross-correlación, función de Green, correlogram gather, puntos estacionarios, interferograma vs ReMi, hipótesis difuso, limitaciones
  - `Concepts/07 Acquisition and Processing/MOPA.md` — formulación matricial, mínimos cuadrados ponderados, test chi-cuadrado, detección campo cercano/variaciones laterales, tabla comparativa con SASW
  - `Concepts/08 Inversion and Interpretation/Non-uniqueness.md` — definición, causas físicas (resolución finita, equivalencia parámetros, insensibilidad a Vp), manifestación práctica (4 regímenes), estrategias de mitigación
  - `Concepts/08 Inversion and Interpretation/Monte Carlo Methods.md` — principio, formulación misfit, test de Fisher, ejemplo La Salle (10⁵ modelos), tabla comparativa LS vs GS, variantes
  - `Concepts/07 Acquisition and Processing/SPAC Method.md` — autocorrelación espacial (Ec. 4.28), cos (Ec. 4.33) y J₀ (Ec. 4.40) para fuente única vs isótropo, ESAC para geometrías arbitrarias, tabla comparativa, limitaciones

## Figuras referenciadas o incorporadas
- Figura 8.1, p. 394 — esquema 3D de propagación de ondas Love con fuente/receptores horizontales
- Figura 8.2, p. 395 — funciones eigendesplazamiento de Love para 5 modos a 80 Hz
- Figura 8.3, p. 396 — curvas modales Love (a) y Rayleigh (b) — diferencias en regularidad y osculación
- Figura 8.4, p. 398 — radiación de una fuente horizontal: Love perpendicular, Rayleigh en dirección de fuerza
- Figura 8.5, p. 399 — ejemplo de dato Love (shot gather, traza única, espectro)
- Figura 8.6, p. 400 — curva de dispersión experimental de ondas Love
- Figura 8.7, p. 401 — Rayleigh: sismograma, f-k, curvas (modo fundamental atenuado + modo superior)
- Figura 8.8, p. 402 — Love: sismograma y curva de dispersión (modo fundamental bien definido)
- Figura 7.30, p. 382 — superficie 3D del misfit por determinante (Maraschini et al. 2010)
- Figura 7.31a, p. 383 — perfiles Vs Monte Carlo con determinant misfit (grayscale por misfit)
- Figura 7.31b, p. 383 — curvas de dispersión teóricas de mejores perfiles vs experimental
- Figura 7.31c, p. 384 — determinante Haskell-Thomson del mejor modelo con puntos experimentales
- Figura 7.32, p. 386 — mapa del sitio La Salle con líneas de reflexión L1 y L2
- Figura 7.33, p. 386 — sismograma de reflexión con representación de ventana deslizante
- Figura 7.34, p. 387 — curvas de dispersión por ventana para L1 y L2
- Figura 7.35, p. 388 — secciones Vs pseudo-2D con inversión con restricciones laterales
- Figura 7.36, p. 389 — modelo Vs de ground-roll superpuesto a secciones de reflexión
- Figura 7.37, p. 390 — pseudosección de velocidad modo fundamental, línea receptora 10km
- Figura 7.38, p. 391 — rebanada de volumen de dispersión λ=130m, ~300 km² Egipto
- Figura 7.39, p. 392 — modelo Vs 2D de inversión modal, línea receptora 10km
- Figura 7.24, p. 376 — regresión de función de transferencia compleja (fase y amplitud) a f=33.78Hz
- Figura 7.25, p. 377 — curvas de dispersión y atenuación Memphis: experimental vs teórica
- Figura 7.26, p. 378 — perfiles Vs y Ds de Memphis vs ensayo SCPT
- Figura 7.27, p. 379 — mapa de ubicación del ensayo en Torre de Pisa + cross-hole
- Figura 7.28, p. 379 — curvas de dispersión y atenuación Pisa: experimental vs teórica
- Figura 7.29, p. 380 — perfiles Vs vs CHT y Ds vs RCT del sitio Pisa
- Figura 7.11, p. 364 — dataset activo: 48 geófonos, 1.5m, 6kg sledgehammer
- Figura 7.12, p. 365 — espectro f-k del dataset activo
- Figura 7.13, p. 365 — análisis pasivo beamformer: espectros 2D para 6 frecuencias (5–17.5 Hz)
- Figura 7.14, p. 367 — curva de dispersión combinada activo+pasivo con incertidumbre
- Figura 7.15, p. 368 — coeficiente de variación activo vs pasivo
- Figura 7.16, p. 369 — pseudo-perfil Vs y modelo inicial para inversión
- Figura 7.17, p. 370 — inversión determinista: ajuste curva dispersión (Herrmann LSM)
- Figura 7.18, p. 370 — perfil Vs con barras de error, comparado con downhole tests
- Figura 7.19, p. 372 — inversión Monte Carlo: familia de perfiles Vs aceptables (grayscale)
- Figura 7.20, p. 372 — curvas de dispersión teóricas de los perfiles seleccionados
- Figura 7.21, p. 373 — espectros de respuesta sísmica 1D para perfiles equivalentes
- Figura 7.22, p. 374 — Vs,30 para cada perfil aceptable del Monte Carlo
- Figura 7.23, p. 375 — comparación perfil por capas vs modelo continuo (Rix & Lai 2013)

## Decisiones editoriales vigentes
- La teoría conceptual debe ir en Concepts.
- Los capítulos deben contener síntesis, enlaces a conceptos y contexto narrativo.
- Priorizar PDFs por capítulo antes que el libro completo.
- El resumen debe priorizar comprensión conceptual y física antes que desarrollo matemático extenso.

## Próximos pasos
1. **Chapter 1 consolidado** — todas las secciones presentes con trazabilidad Foti
2. Capítulos 2–8 marcados como "consolidado (tercera fase completa)"; todos los wikilinks activos resueltos
3. Excepción mantenida: [[Refraction Seismics]] (método externo, fuera del alcance del vault)
4. Posible trabajo futuro: revisión de profundidad de conceptos en Concepts/ si hay algo pendiente; si no, marcar Trabajo completo
5. **Candidatos a revisión**: [[Geometric Dispersion]] — el wikilink aparece en Chapter 1.md sección 1.3 (renombrada) pero no existe como archivo de concepto separado (era stub en la sección 1.3.1). Considerar si crear concepto propio o dejar el contenido en el capítulo (actualmente el contenido está en la sección 1.3.1 del capítulo, lo cual es suficiente dada la trazabilidad).

## Historial de iteraciones

### 2026-03-19 — iteración 39 de loop (segunda fase Chapter 1 — secciones 1.3, 1.3.1, 1.4, 1.4.1–1.4.3)
- **Estado:** VÁLIDA.
- **Acción realizada:**
  - Leído Sebastiano Foti Chapter 1.pdf, pp. 5–20 (secciones 1.2 Surface Waves, 1.2.1 Geometric Dispersion, 1.3 Test Methodology, 1.3.1–1.3.3, 1.4 Historical Perspective).
  - **Reescrita sección 1.3 Ondas Superficiales** (~120→420 palabras): eliminadas referencias "[2, 4]" y marcadores de imagen locales; añadida trazabilidad Foti pp.5–6; expansión de atenuación geométrica (punto source 1/√r, línea sin atenuación, Ewing 1957), dominancia campo lejano (Lamb 1904), confinamiento en profundidad (Achenbach 1984), tipos de ondas con wikilinks inline.
  - **Reescrita y expandida sección 1.3.1 Dispersión Geométrica** (~50→400 palabras): intuición física del semiespacio no dispersivo vs. medio heterogéneo dispersivo; mecanismo ilustrado con Figura 1.2 (p.7); relación alta/baja frecuencia con profundidad; curva de dispersión como producto (Figura 1.3, p.8); definición explícita del problema directo (Cap. 2) e inverso (Cap. 6); referencia a Engl (1993).
  - **Reescrita sección 1.4 Metodología** (~120→320 palabras): eliminadas referencias "[1, 2]"; trazabilidad Foti pp.8–9; contexto de variedad de ensayos (SASW, MASW, ReMi, SPAC) con principio común; Figura 1.4 (p.9) marcada.
  - **Reescrita sección 1.4.1 Adquisición** (~100→480 palabras): trazabilidad Foti pp.10–11; geófonos (electriodinámicos, preferidos por sensibilidad/robustez), MEMS, hardware A/D; fuentes impulsivas vs. continuas vs. pasivas (microtremores); Figura 1.5 (p.11) marcada.
  - **Reescrita sección 1.4.2 Procesamiento** (~80→280 palabras): trazabilidad Foti pp.12–13; Fourier + f–k con Figura 1.6 (p.12) marcada; curva de atenuación experimental y inversión conjunta VS+DS.
  - **Reescrita sección 1.4.3 Inversión** (~100→350 palabras): trazabilidad Foti pp.13–15; problema directo como base, función objetivo RMS, LSM vs. GSM, ill-posedness, problema de equivalencia, rol del juicio de ingeniería; Figura 1.7 (p.14) marcada.
- **Archivos modificados:** `Chapter 1.md`
- **Conceptos creados o modificados:** ninguno
- **Figuras referenciadas:**
  - Figura 1.1, p. 5 — patrón de radiación 2D de ondas Rayleigh desde fuente puntual vertical
  - Figura 1.2, p. 7 — dispersión geométrica: movimiento de partícula a alta y baja frecuencia en medio estratificado
  - Figura 1.3, p. 8 — identificación de parámetros desde dispersión geométrica (a–e): perfil → curva de dispersión → problema inverso
  - Figura 1.4, p. 9 — diagrama de flujo de ensayos de ondas superficiales
  - Figura 1.5, p. 11 — combinación de fuentes activas y pasivas
  - Figura 1.6, p. 12 — ejemplo de procesamiento f–k: datos, espectro, curva de dispersión
  - Figura 1.7, p. 14 — ejemplo de proceso de inversión: perfil VS, curvas en λ–V y f–V
- **Fecha y hora:** 2026-03-19 23:10 -03
- **Estado de finalización global:** Chapter 1 consolidado (segunda fase completa). Vault en estado plenamente consolidado. **Trabajo completo: sí**

### 2026-03-19 — iteración 38 de loop (primera fase Chapter 1 — estructura y secciones faltantes)
- **Estado:** VÁLIDA.
- **Acción realizada:**
  - Leído Sebastiano Foti Chapter 1.pdf, pp. 1–30. Identificadas secciones completamente ausentes del vault: 1.4 Historical Perspective (PDF) y 1.5 Challenges (PDF).
  - **Renumeración**: sección existente "1.6 Aplicaciones" → "1.7 Aplicaciones" para hacer espacio.
  - **Añadida sección 1.5 Perspectiva Histórica**: sismología global (grupos velocidad, tomografía, filtrado multimodal) → geofísica de exploración (ground-roll como ruido/señal) → aplicaciones ingeniería (Jones 1958 estado estacionario → SASW Nazarian 1984 → MASW Park 1999 → microtremores SPAC/ReMi/HVSR).
  - **Añadida sección 1.6 Desafíos**: 1.6.1 Superposición modal y velocidad aparente (Fig. 1.9 sitio inversamente dispersivo), 1.6.2 Efectos de campo cercano (interferencia ondas cuerpo + frente cilíndrico, distancia crítica 0.5–2λ, tradeoff offset/resolución), 1.6.3 Errores de modelo (4 parámetros por capa, fijación ρ y ν, coeficiente de Poisson en suelos saturados, variaciones laterales, perfiles suaves), 1.6.4 Resolución y profundidad de investigación (kernels de sensibilidad Fig. 1.11, zmax≈λmax/2, distribución sesgada puntos Fig. 1.12, remuestreo exponencial).
  - **Expandidas secciones thin**: 1.0 Introducción (~60→220 palabras, Lord Rayleigh 1885, flujo 3 pasos), 1.1 Comportamiento del Suelo (~80→280 palabras, pequeñas deformaciones γ<10⁻⁵, VP y VS, por qué VS más relevante, viscoelasticidad y damping ratio), 1.2 Tipos de Ondas de Cuerpo (~30→150 palabras, P/S, SV/SH, génesis Rayleigh y Love).
  - **Expandida sección 1.7.1 Caracterización de sitio** (~100→220 palabras): Gmax, respuesta sísmica, VS30 (Fig. 1.13), amortiguamiento material, ventajas sobre borehole.
- **Próximo paso:** Leer páginas 30+ del PDF Cap. 1 para completar sección 1.7 Aplicaciones (subsecciones: NDT, caracterización offshore, expansiones Chapter 2+). También expandir sección 1.3 Ondas Superficiales y subsecciones 1.4.1–1.4.3.

### 2026-03-19 — iteración 37 de loop (cuarta fase — expansión Procesamiento de Señales y Dispersion Relation)
- **Estado:** VÁLIDA.
- **Acción realizada:**
  - Reescrito `Concepts/07 Acquisition and Processing/Procesamiento de Señales.md` (~200→560 palabras): producto (curva dispersión experimental), análisis f-k (DFT 2D, máximos en k), análisis tau-p (slantstack, equivalencia con f-k), SASW (desfase espectral, aliasing fase), identificación de modos (fundamental vs superiores), incertidumbre de la curva (variabilidad entre disparos, anchura pico, ruido).
  - Reescrito `Concepts/03 Wave Propagation/Dispersion Relation.md` (~230→580 palabras): intuición (filtro modal del medio), forma general ω(k) con cp y cg como derivadas, ecuación secular de Rayleigh para semiespacio homogéneo (no dispersivo), Thomson-Haskell det=0 para medios estratificados (implícita, numérica), modos múltiples como soluciones discretas, dispersión normal vs inversa, función de misfit χ² en inversión.
- **Próximo paso:** Cuarta fase completada para todos los conceptos activos. Solo quedan stubs huérfanos sin wikilinks.

### 2026-03-19 — iteración 36 de loop (cuarta fase — expansión 9 conceptos thin/borderline)
- **Estado:** VÁLIDA.
- **Acción realizada:**
  - Auditoría completa de todos los archivos Concepts/ (~45 archivos): 5 stubs vacíos huérfanos (sin wikilinks — no expandidos), 8 stubs (<200p), 4 borderline (~200p).
  - Reescrito `Concepts/04 Body and Surface Waves/S-Waves.md` (~175→520 palabras): intuición (corte puro sin cambio de volumen, insensibilidad al agua), VS=sqrt(μ/ρ), polarización SV/SH con tabla, Gmax=ρVS², VS vs VP en suelos saturados, tabla de valores típicos, aplicaciones geotécnicas (VS30, licuefacción).
  - Reescrito `Concepts/04 Body and Surface Waves/Surface Waves.md` (~180→530 palabras): intuición (confinamiento por condición de esfuerzo libre), tipos tabla (Rayleigh/Love/Scholte), decaimiento expo con profundidad, dispersión en estratificados, partición energía Lamb (~67% Rayleigh), modos múltiples.
  - Reescrito `Concepts/01 Elasticity and Continuum Mechanics/Strain Tensor.md` (~160→520 palabras): intuición (normal vs corte), definición εij=(∂ui/∂xj+∂uj/∂xi)/2, componentes tabla, cambio volumétrico traza=∇·u, ley de Hooke σ=λ(∇·u)I+2με, ecuaciones de Navier, descomposición VP/VS.
  - Reescrito `Concepts/01 Elasticity and Continuum Mechanics/Stress Tensor.md` (~155→530 palabras): intuición (tracción en plano), tensor Cauchy 3×3, componentes tabla, teorema de Cauchy t=σn, ecuación de movimiento ∇·σ=ρü, condición de esfuerzo libre en z=0 (génesis Rayleigh), condiciones de interfaz (Thomson-Haskell).
  - Reescrito `Concepts/07 Acquisition and Processing/Métodos Sísmicos Invasivos.md` (~180→500 palabras): fundamento (tiempo de viaje), CHT/Down-hole/SCPT/P-S Logging descritos, tabla comparativa invasivos vs no invasivos, rol como validación y parámetros a priori para inversión MASW.
  - Reescrito `Concepts/07 Acquisition and Processing/Métodos Sísmicos No Invasivos.md` (~155→520 palabras): refracción (limitación inversión velocidades), reflexión, tabla de métodos de ondas superficiales (MASW/SASW/ReMi/SPAC/Interferometría/HVSR), ventajas vs invasivos, tabla comparativa geotécnica.
  - Reescrito `Concepts/02 Wave Mathematics/Wavenumber.md` (~200→480 palabras): k=2π/λ, variación espacial de fase, k complejo (atenuación α), rol en espectrograma f-k (eje horizontal, cp=ω/k), resolución Δk=2π/L, aliasing k>π/Δx.
  - Reescrito `Concepts/00 Foundations/Wave.md` (~180→450 palabras): intuición (transporte energía sin materia), onda armónica, tabla de clasificación por tipo (P/S/Rayleigh/Love), por confinamiento (cuerpo vs superficie), por dispersividad, dominio de superficiales (1/√r vs 1/r), geófonos miden velocidad de partícula.
  - Reescrito `Concepts/04 Body and Surface Waves/SV-wave.md` (~200→450 palabras): polarización en plano sagital, tabla P/SV/SH, acoplamiento P-SV→génesis Rayleigh (condición σzz=σxz=0), conversión de modos (Zoeppritz), SV como ruido pre-ground-roll en MASW.
- **Próximo paso:** Vault en estado muy consolidado. Considerar revisión de la Chapter 2 y conceptos borderline restantes, o dar cuarta fase por completada.

### 2026-03-19 — iteración 35 de loop (cuarta fase — expansión 6 conceptos thin)
- **Estado:** VÁLIDA.
- **Acción realizada:**
  - Reescrito `Concepts/03 Wave Propagation/Lamb's Problem.md` (~100→550 palabras, Unicode apostrophe manejado via Python): Lamb 1904, formulación (carga puntual en semiespacio), tabla de partición de energía (~67% Rayleigh, ~26% S, ~7% P), decaimiento 1/√r vs 1/r, campo cercano vs lejano, regla x_min ≈ λmax/2 para MASW, extensiones históricas.
  - Reescrito `Concepts/04 Body and Surface Waves/Body Waves.md` (~180→550 palabras): intuición (frente esférico vs cilíndrico), VP y VS desde constantes de Lamé, tabla SV/SH y desacoplamiento, decaimiento geométrico tabla, partición de energía (Lamb), role de P como ruido en MASW, uso en refracción sísmica.
  - Reescrito `Concepts/04 Body and Surface Waves/SH-wave.md` (~150→650 palabras): polarización horizontal, desacoplamiento P-SV geométrico, ecuación escalar independiente, condiciones de frontera SH vs P-SV, reflexión total y Love waves como guía SH, ecuación de dispersión Love, excitación con fuentes horizontales, simplificación matricial 2×2 vs 4×4.
  - Reescrito `Concepts/02 Wave Mathematics/Angular Frequency.md` (~170→500 palabras): ω=2πf, onda armónica, relación de dispersión ω(k), cp=ω/k, análisis f-k como extracción de crestas en espectrograma, límites instrumentales tabla (Nyquist temporal y espacial, resolución f y k), conversión práctica f↔ω.
  - Reescrito `Concepts/02 Wave Mathematics/Wavelength.md` (~130→500 palabras): λ=c/f, k=2π/λ, regla z_max≈λ/2, resolución vertical Δz_min≈λmin/2, tabla diseño (Δx→λmin, L→λmax), aliasing espacial λ>2Δx, tabla de valores típicos MASW a 5/20/50 m de profundidad.
  - Reescrito `Concepts/02 Wave Mathematics/Fourier Integral.md` (~160→600 palabras): superposición de ondas monocromáticas, dispersión como no-linealidad de ω(k), fase estacionaria → velocidad de grupo = velocidad de transporte, f-k 2D como DFT discreta del sismograma, extracción de curva de dispersión, tabla de limitaciones (Nyquist, resolución), Parseval.
- **Próximo paso:** Auditar conceptos que aún no han sido revisados en cuarta fase para detectar stubs residuales.

### 2026-03-19 — iteración 34 de loop (cuarta fase — expansión P-waves y Mode Conversion)
- **Estado:** VÁLIDA.
- **Acción realizada:**
  - Auditados 18 conceptos restantes: 8 thin, 1 inexistente (Lamb's Problem en realidad existe con apostrofe Unicode).
  - Reescrito `Concepts/04 Body and Surface Waves/P-waves.md` (~70→560 palabras): intuición (compresión/dilatación longitudinal), VP=sqrt(M/ρ), polarización, comportamiento en suelos saturados (VP→1500m/s no indica rigidez), tabla valores típicos, relevancia como parámetro a priori en inversión de Rayleigh.
  - Reescrito `Concepts/03 Wave Propagation/Mode Conversion.md` (~80→500 palabras): intuición (condiciones de frontera acopladas), tabla P/SV/SH de conversiones, relación con formación de Rayleigh (acoplamiento P-SV), Love (SH independiente), modos superiores, contaminación en adquisición, separación f-k.
- **Próximo paso:** Expandir Lamb's Problem (~100p), Body Waves (~180p), SH-wave (~150p), y los thin matemáticos (Angular Frequency, Wavelength, Fourier Integral).

### 2026-03-19 — iteración 33 de loop (cuarta fase — expansión Skin Depth y Group Velocity)
- **Estado:** VÁLIDA.
- **Acción realizada:**
  - Reescrito `Concepts/03 Wave Propagation/Skin Depth.md` (~100→580 palabras): intuición (confinamiento superficial), definición δ=1/e, z_95%=0.94λ, regla práctica z_max≈λ/2, tabla relaciones diseño de arreglo, limitaciones de la regla del skin depth.
  - Reescrito `Concepts/03 Wave Propagation/Group Velocity.md` (~280→550 palabras): intuición (envolvente vs portadora), derivación superposición dos ondas, relación cg vs cp en curva de dispersión, tabla comparativa sismología global vs MASW, implicaciones para diseño y ventana de análisis.
- **Próximo paso:** Revisar Dispersion Relation.md (~280p) y Mode Superposition.md, y otros conceptos que puedan necesitar mejora.

### 2026-03-19 — iteración 32 de loop (cuarta fase — expansión Attenuation y Phase Velocity)
- **Estado:** VÁLIDA.
- **Acción realizada:**
  - Reescrito `Concepts/00 Foundations/Attenuation.md` (~180→580 palabras): intuición (geométrica vs material), número de onda complejo, Ec. 2.133 de Foti (integral de DS vs αR), ley 1/√r de Rayleigh, procedimiento experimental de regresión ln[A√r] vs r, correcciones necesarias, implicaciones para la tesis.
  - Reescrito `Concepts/03 Wave Propagation/Phase Velocity.md` (~250→720 palabras): intuición (seguir la cresta), definición ω/k, curva de dispersión experimental, medición f-k/τ-p/SASW, velocidad de Rayleigh en semiespacio vs estratificado, velocidad aparente (Ec. 2.93), relación con inversión (función misfit, sensibilidad λ/3), implicaciones para diseño del arreglo.
- **Próximo paso:** Revisar otros conceptos: Dispersion Relation (~280p), Group Velocity (~?), Skin Depth (~?), Mode Superposition (~290p) para ver si necesitan expansión.

### 2026-03-19 — iteración 31 de loop (cuarta fase — completar stubs de Concepts)
- **Estado:** VÁLIDA.
- **Acción realizada:**
  - Creado `Concepts/04 Body and Surface Waves/Surface Wave Modes.md` (~650 palabras): intuición (guía de ondas estratificada), tabla modo/velocidad/penetración, frecuencias de corte modales, eigenfunciones, curva de dispersión aparente, implicaciones para MASW (identificación de modos, offset, longitud, inversión multimodal y determinant misfit).
  - Creado `Concepts/06 Media and Stratification/Vertically Inhomogeneous Media.md` (~600 palabras): intuición (gradiente de compactación), definición matemática (Ecs. 2.56, 2.65–2.66), sistemas EDO para Love y Rayleigh, estrategias numéricas (discretización en capas finas, integración directa), tabla comparativa con modelo de capas, criterio de selección, ejemplo La Salle Fig. 7.23, no-unicidad en modelo continuo.
  - Los 4 stubs vacíos detectados (Layered Media, Elastic Half Space, Surface Wave Modes, Vertically Inhomogeneous Media) han sido completamente desarrollados.
- **Próximo paso:** Expandir Attenuation.md (~180p) y Phase Velocity.md (~250p) que están por debajo del umbral.

### 2026-03-19 — iteración 30 de loop (cuarta fase — auditoría y desarrollo de Concepts stubs)
- **Estado:** VÁLIDA.
- **Acción realizada:**
  - Auditoría de calidad de 10 archivos de concepto: 4 stubs completamente vacíos detectados (Layered Media, Elastic Half Space, Vertically Inhomogeneous Media, Surface Wave Modes).
  - Creado `Concepts/06 Media and Stratification/Layered Media.md` (~700 palabras): intuición física (dispersión por estratificación), tabla de parámetros por capa, condiciones de borde en interfaces, método Thomson-Haskell, tipos de perfil (normalmente/inversamente dispersivo, velocity reversal), sensibilidad a parámetros, implicaciones para MASW, relaciones con otros conceptos.
  - Creado `Concepts/01 Elasticity and Continuum Mechanics/Elastic Half Space.md` (~700 palabras): intuición (no-dispersividad), tabla VP/VS vs ν para VR/VS, ecuación secular, movimiento de partícula elíptico, decaimiento profundidad (~Skin Depth), decaimiento geométrico 1/√r vs 1/r², relación con medios reales.
- **Próximo paso:** Desarrollar Vertically Inhomogeneous Media y Surface Wave Modes (stubs vacíos).

### 2026-03-19 — iteración 29 de loop (tercera fase Chapter 2 — cierre + Poisson Ratio)
- **Estado:** VÁLIDA.
- **Acción realizada:**
  - Inventario de conceptos: detectado único concepto faltante con wikilink en capítulos pero sin archivo: [[Poisson Ratio]].
  - Creado `Concepts/01 Elasticity and Continuum Mechanics/Poisson Ratio.md`: definición, tabla VP/VS vs ν, relación con VR, comportamiento en suelos secos vs saturados, implicación para inversión (nivel freático), referencias a Foti Cap. 2 y 7.
  - Revisión tercera fase Chapter 2: identificadas 3 secciones < 150 palabras.
  - Expandida **Introducción**: justificación del dominio de ondas superficiales (67% energía, decaimiento r^-0.5 vs r^-2), arco argumental del capítulo. ~95→220 palabras.
  - Expandida **sección 2.2.4** (No-dispersividad): razón física (ausencia de longitud de escala), comparación con dispersión geométrica por estratificación, límites asintóticos de alta/baja frecuencia. ~80→280 palabras.
  - Expandida **sección 2.5.1** (Marco constitutivo viscoelástico): significado físico de DS, rango de deformación lineal (~1–5%), cuatro hipótesis del modelo, diferencia con plasticidad/histéresis no lineal. ~80→220 palabras.
  - Añadidos wikilinks [[Poisson Ratio]] en dos lugares del texto de Ch.2.
  - Chapter 2 marcado como **consolidado (tercera fase completa)**.
  - Chapter 6 marcado como **consolidado (tercera fase completa)** (revisado sin cambios en iteración anterior).
  - **VAULT PLENAMENTE CONSOLIDADO**: todos los capítulos 2–8 en tercera fase completa; todos los conceptos referenciados con wikilink tienen archivo correspondiente.
- **Próximo paso:** Ninguno en el pipeline actual. Vault en estado final consolidado.

### 2026-03-19 — iteración 28 de loop (tercera fase Chapters 7 y 8 — cierre)
- **Estado:** VÁLIDA.
- **Acción realizada:**
  - Revisión de control de calidad de Chapters 7 y 8: identificadas 3 secciones < 150 palabras.
  - Expandida sección **7.3 intro**: importancia de Ds en ingeniería sísmica, limitaciones de laboratorio (columna resonante, volúmenes pequeños, nivel de deformación), corrección de atenuación geométrica y campo cercano necesaria para extraer αR(ω), referencia a metodología Sección 6.4.3.4. ~80→260 palabras.
  - Añadida intro de **8.3** (era 0 palabras): motivación para inversión conjunta, sensibilidad limitada de ondas superficiales a Vp/ν, principio físico de compartir fronteras litológicas, preview de subsecciones. ~0→190 palabras.
  - Expandida sección **8.3.2 intro**: objetivo doble (Vp y reducir no-unicidad), argumento de fronteras litológicas compartidas, organización en 3 bloques (eléctrico, sísmico, refracción+superficie). ~80→230 palabras.
  - Chapters 7 y 8 marcados como **consolidado (tercera fase completa)**.
  - **VAULT PLENAMENTE CONSOLIDADO** (tercera fase): todos los capítulos 2–8 con ninguna sección < 150 palabras.
- **Próximo paso:** Ninguno en el pipeline actual. Vault en estado final.

### 2026-03-19 — iteración 27 de loop (tercera fase Chapter 4 y 5 — cierre)
- **Estado:** VÁLIDA.
- **Acción realizada:**
  - Expandida sección 4.2 SSRM: contexto histórico (Jones 1958/1962, Ballard 1964), procedimiento paso a paso (Fig. 4.5), determinación robusta de λ por múltiples posiciones (Fig. 4.6) con ejemplo numérico 3 frecuencias, variante CSW, limitaciones. ~70→500 palabras.
  - Expandida sección 5.5.1 (Half-power bandwidth): principio físico del ancho de banda a mitad de potencia, problema del ventaneo espacial y corrección Badsar et al. 2010, capacidad multimodal, ejemplo Fig. 5.10 (3 modos, D=1-4%). ~80→400 palabras.
  - Expandida sección 5.5.2 (Arias intensity): concepto de intensidad de Arias, procedimiento de inversión directa, limitación fundamental (requiere modelo elástico preciso de Vs/Vp). ~60→300 palabras.
  - Chapter 4 y 5 marcado como **consolidado (tercera fase completa)**.
- **Próximo paso:** Revisar Chapters 6, 7, 8 para detectar secciones < 150 palabras.

### 2026-03-19 — iteración 26 de loop (tercera fase Chapter 3 — cierre)
- **Estado:** VÁLIDA.
- **Acción realizada:**
  - Expandida sección 3.1.2 (adquisición de ondas superficiales): dominio frecuencial como eje central, relación λ=V/f → profundidad, características del tren de ondas (duración, superposición eventos), requerimientos de medición. ~80→450 palabras.
  - Expandida sección 3.3.6 (cuantización): resolución en bits, tabla dB por nivel, error de cuantización RMS = LSB/√12, Fig. 3.14, implicación para detección de modos débiles. ~60→350 palabras.
  - Expandida sección 3.4.3.3 (métodos pasivos): fuentes naturales vs. humanas, microtremores de período corto, campo dominado por ondas superficiales, arrays 2D vs. lineales, diseño de apertura, geometrías típicas (Fig. 3.44), ReMi y su limitación severa ante campo anisotrópico. ~90→500 palabras.
  - Chapter 3 marcado como **consolidado (tercera fase completa)**.
- **Próximo paso:** Revisar Chapter 4 y 5 para detectar secciones < 150 palabras.

### 2026-03-19 — iteración 25 de loop (tercera fase Chapter 3 — sección 3.3.2)
- **Estado:** VÁLIDA.
- **Acción realizada:**
  - Revisión de control de calidad de Chapter 3: identificadas secciones < 150 palabras: 3.3.2 (~80 p.), 3.1.2 (~80 p.), 3.3.6 (~60 p.), 3.4.3.3 (~90 p.).
  - Leído Sebastiano Foti Chapter 3.pdf pp. 11–16 (libro pp. 131–136): sección 3.3.2.
  - Expandida sección 3.3.2 de ~80 a ~550 palabras: origen de la transformada (serie de Fourier → señales no periódicas), Ecs. 3.3–3.6, propiedades completas (linealidad Ecs. 3.7–3.8, escalamiento Ec. 3.9, desplazamiento Ec. 3.10, convolución Ecs. 3.11–3.12), conexión con dominio f-k y estimación de velocidad de fase.
  - Chapter 3 marcado como "en revisión profunda (tercera fase)".
- **Próximo paso:** Expandir sección 3.1.2 (adquisición de ondas superficiales, ~80 palabras).

### 2026-03-19 — iteración 24 de loop (segunda fase Chapter 2 — cierre)
- **Estado:** VÁLIDA.
- **Acción realizada:**
  - Leído Sebastiano Foti Chapter 2.pdf pp. 21–40 (libro pp. 57–76): secciones 2.2.3–2.4.1.
  - Corregido rango $V_R/V_S$ de "0.87–0.96" a **0.862–0.955** (Foti p. 59, Fig. 2.15).
  - Añadidas eigenfunciones de desplazamiento (Foti Ecs. 2.43–2.45) en sección 2.2.2: expresiones completas de $u_1$ y $u_2$, ecuación de la elipse (Ec. 2.44), relación amplitud vertical/horizontal ~1.5:1 en superficie.
  - Añadida profundidad crítica retrógrado→prógrado (Foti Ec. 2.46) en sección 2.2.3 con fórmula completa y referencia a Fig. 2.16.
  - Añadido ejemplo numérico en sección 2.4.1: Tabla 2.4 (sistema de 4 capas con Vp/Vs/ρ), descripción Fig. 2.20 (función secular Rayleigh), Fig. 2.21 (24 modos de dispersión), Fig. 2.22 (eigenfunciones de desplazamiento a f=16 Hz).
  - Chapter 2 marcado como **consolidado (segunda fase completa)**.
  - **VAULT PLENAMENTE CONSOLIDADO**: todos los capítulos 2–8 en estado "consolidado (segunda fase completa)"; todas las fases finalizadas.
- **Próximo paso:** Ninguno en el pipeline actual.



### 2026-03-18 18:34 -03
- **Estado:** BLOQUEADA por regla horaria (hora local 18:34, posterior a 08:00).
- **Acción realizada:** Creación del archivo de estado inicial. No se realizó trabajo editorial.

### 2026-03-18 18:36 -03
- **Estado:** VÁLIDA (hora local 18:36, dentro del rango 18:30–08:00).
- **Acción realizada:**
  - Leído Chapter 2.md → confirmado completo (secciones 2.1–2.5).
  - Leído Sebastiano Foti Chapter 3.pdf (pp. 121–160).
  - Escrito Chapter 3.md con síntesis de secciones 3.1–3.4.1.6.
- **Próximo paso:** Continuar Chapter 3 desde sección 3.4.2 (p. 160+).

### 2026-03-18 19:05 -03
- **Estado:** VÁLIDA (hora local 19:05, dentro del rango 18:30–08:00).
- **Acción realizada:**
  - Leído Sebastiano Foti Chapter 3.pdf (pp. 161–200).
  - Completado Chapter 3.md con secciones 3.4.1.7–3.5.2.5 (variaciones laterales, modos superiores, sampling, survey design, fuentes, geófonos, acelerómetros).
  - Creado concepto [[Near-field Effect]] en Concepts/03 Wave Propagation/.
  - Chapter 3 marcado como completado.
- **Próximo paso:** Iniciar Chapter 4 (procesamiento de señales).

### 2026-03-18 19:29 -03
- **Estado:** VÁLIDA (hora local 19:29, dentro del rango 18:30–08:00).
- **Acción realizada:**
  - Leído Sebastiano Foti Chapter 4.pdf completo (pp. 205–254, 50 páginas del PDF).
  - Leído Sebastiano Foti Chapter 5.pdf completo (pp. 255–271, 18 páginas del PDF).
  - Creado Chapter 4 y 5.md con síntesis completa: secciones 4.1–4.8 (SSRM, SASW, MOPA, SPAC, f-k, τ-p/MASW, ReMi, incertidumbre) y 5.1–5.6 (atenuación, regresión amplitud-offset, función de transferencia, MUSIC multimodal, media potencia, incertidumbre).
  - Chapter 4 y 5 marcados como completados.
- **Próximo paso:** Iniciar Chapter 6 (Inversion).

### 2026-03-19 — iteración 1 de loop
- **Estado:** VÁLIDA.
- **Acción realizada:**
  - Leído Worklog → identificado que Chapter 6 era el próximo paso.
  - Leído Sebastiano Foti Chapter 6.pdf pp. 1–20 (libro pp. 273–292).
  - Creado Chapter 6.md con síntesis de secciones 6.1–6.3.
  - Actualizado concepto [[Inversión]] con condiciones de Hadamard, SVD, Tikhonov, Occam.
  - Worklog actualizado.
- **Próximo paso:** Continuar Chapter 6 desde sección 6.4.

### 2026-03-19 — iteración 2 de loop
- **Estado:** VÁLIDA.
- **Acción realizada:**
  - Leído Sebastiano Foti Chapter 6.pdf pp. 21–75 (libro pp. 293–347): secciones 6.4.1–6.5.4 completas.
  - Completado Chapter 6.md con secciones 6.4 (SVD, Moore-Penrose, Tikhonov, Occam, no lineal LS/GS, Jacobiano, info a priori) y 6.5 (incertidumbre: gaussiana, FOSM, curvas de dispersión/atenuación, trade-off resolución/varianza).
  - Creado concepto [[Tikhonov Regularization]] en Concepts/08 Inversion and Interpretation/.
  - Chapter 6 marcado como completado (primera fase).
- **Próximo paso:** Iniciar Chapter 7.

### 2026-03-19 — iteración 3 de loop
- **Estado:** VÁLIDA.
- **Acción realizada:**
  - Leído Sebastiano Foti Chapter 7.pdf pp. 1–30 (libro pp. 351–380): secciones 7.1–7.3 intro.
  - Creado Chapter 7.md con síntesis de intro del capítulo y sección 7.1 completa (7.1.1 SASW, 7.1.2 f-k, 7.1.3 nivel freático). Sitio Saluggia, comparación de técnicas de procesamiento.
  - Creado concepto [[SASW Method]] en Concepts/07 Acquisition and Processing/.
  - Chapter 7 marcado como en progreso (sección 7.1 completa).
- **Próximo paso:** Sección 7.2 (pp. 363–375, La Salle — comparación de estrategias de inversión).

### 2026-03-19 — iteración 4 de loop
- **Estado:** VÁLIDA.
- **Acción realizada:**
  - Usando material ya leído (pp. 363–375): secciones 7.2.1–7.2.5 completas.
  - Ampliado Chapter 7.md con sección 7.2 completa: dataset activo+pasivo (La Salle), inversión empírica, determinista LSM, Monte Carlo, medio continuo.
  - Creado concepto [[Vs30]] en Concepts/08 Inversion and Interpretation/.
  - Chapter 7 actualizado a secciones 7.1–7.2 completadas.
- **Próximo paso:** Secciones 7.3–7.5 (pp. 375–fin, Memphis/Pisa Vs+Ds, higher modes, ground-roll).

### 2026-03-19 — iteración 5 de loop
- **Estado:** VÁLIDA.
- **Acción realizada:**
  - Leído Sebastiano Foti Chapter 7.pdf pp. 31–35 (libro pp. 381–385): secciones 7.4 y 7.5 intro.
  - Leído Sebastiano Foti Chapter 7.pdf pp. 36–42 (libro pp. 386–392): secciones 7.5.1 y 7.5.2.
  - Ampliado Chapter 7.md con sección 7.3 completa (7.3.1 Memphis y 7.3.2 Pisa — inversión conjunta Vs+Ds).
  - Creado concepto [[Shear Damping Ratio]] en Concepts/08 Inversion and Interpretation/.
  - Chapter 7 actualizado a secciones 7.1–7.3 completadas.
- **Próximo paso:** Secciones 7.4 (higher modes, pp. 380–383) y 7.5 (ground-roll, pp. 384–392).

### 2026-03-19 — iteración 6 de loop
- **Estado:** VÁLIDA.
- **Acción realizada:**
  - Usando material ya leído (pp. 380–392): secciones 7.4 y 7.5 completas.
  - Ampliado Chapter 7.md con sección 7.4 (determinant misfit, higher modes, Monte Carlo multimodal) y sección 7.5 completa (7.5.1 engineering 2D / 7.5.2 exploration 3D ground-roll).
  - Creado concepto [[Ground Roll]] en Concepts/07 Acquisition and Processing/.
  - Chapter 7 marcado como completado (primera fase) — secciones 7.1–7.5.
- **Próximo paso:** Iniciar Chapter 8 (último capítulo de primera fase).

### 2026-03-19 — iteración 7 de loop
- **Estado:** VÁLIDA.
- **Acción realizada:**
  - Leído Sebastiano Foti Chapter 8.pdf pp. 1–20 (libro pp. 393–412): secciones 8.1 y 8.2 parcial.
  - Creado Chapter 8.md con introducción del capítulo y sección 8.1 completa (8.1.1 naturaleza Love waves, 8.1.2 configuraciones experimentales, 8.1.3 ejemplo Terceira Island).
  - Ampliado concepto [[Love Waves]] en Concepts/04 Body and Surface Waves/ con adquisición, polarity reversal, resonancias SH, ventaja inversión conjunta.
  - Chapter 8 marcado como en progreso (sección 8.1 completa).
- **Próximo paso:** Sección 8.2 (Scholte waves + guided P-waves, pp. 402–412).

### 2026-03-19 — iteración 8 de loop
- **Estado:** VÁLIDA.
- **Acción realizada:**
  - Ampliado Chapter 8.md con sección 8.2 completa: 8.2.1 Scholte waves (soft-bottom condition, movimiento elíptico, sin corte en modo fundamental, efecto de capa de agua hasta ~18%, Fig. 8.9–8.12), 8.2.2 P-guided waves (modos fugantes, dependencia de Vp, aproximación acústica, inversión conjunta con Scholte, Fig. 8.13–8.14), 8.2.3 ejemplo marino (12 hidrófonos a 2m, speargun, filtro pasa-bajo para Scholte, adquisición en orilla tierra+mar, Fig. 8.15–8.17).
  - Reescrito completamente concepto [[Scholte Waves]] en Concepts/04 Body and Surface Waves/ con motivación marina (Vp/Vs en sedimentos), características físicas, efecto cuantitativo de la capa de agua, generación/registro, tabla comparativa Scholte vs P-guiadas, flujo de trabajo, shoreline.
  - Chapter 8 actualizado a secciones 8.1–8.2 completadas (pp. 393–412).
- **Próximo paso:** Sección 8.3 (inversión conjunta con refracción de ondas P, pp. 412+).

### 2026-03-19 — iteraciones 16–18 de loop (segunda fase)
- **Estado:** VÁLIDA.
- **Acción realizada:**
  - Evaluado Chapter 6: todas las secciones 6.1–6.5 tienen 200–400 palabras c/u con profundidad técnica adecuada. Sin cambios. Marcado consolidado.
  - Evaluado Chapter 7: todas las secciones 7.1–7.5 tienen 500–700 palabras c/u con casos reales detallados. Sin cambios. Marcado consolidado.
  - Evaluado Chapter 8: todas las secciones 8.1–8.5 tienen 200–600 palabras c/u con contenido técnico y figuras. Sin cambios. Marcado consolidado.
  - **SEGUNDA FASE COMPLETA**: todos los capítulos 2–8 están consolidados.
- **Próximo paso:** revisar conceptos en Concepts/ para identificar ficheros incompletos o sin crear.

### 2026-03-19 — iteración 15 de loop (segunda fase)
- **Estado:** VÁLIDA.
- **Acción realizada:**
  - Leído Sebastiano Foti Chapter 4.pdf pp. 27–40 (libro pp. 231–244): secciones 4.5 SPAC y 4.6 transform-based (beamforming, τ-p).
  - Expandido Section 4.5 "Autocorrelación espacial (SPAC/ESAC)" en Chapter 4 y 5.md: añadida derivación matemática de la autocorrelación espacial (Ec. 4.28), caso de fuente única (ρ = cos(k₀·χ), Ec. 4.33), estimación experimental via espectros cruzados normalizados (Ec. 4.34), caso isótropo (ρ = J₀(k₀r), Ec. 4.39–4.40), referencia a Ec. 4.41, receptor de referencia, ESAC para geometrías arbitrarias, limitaciones completas. De ~180 a ~550 palabras.
  - Chapter 4 y 5 marcado como consolidado.
- **Próximo paso:** Iniciar segunda fase Chapter 6.

### 2026-03-19 — iteración 14 de loop (segunda fase)
- **Estado:** VÁLIDA.
- **Acción realizada:**
  - Leído Sebastiano Foti Chapter 4.pdf pp. 1–20 (libro pp. 205–224): secciones 4.1 y 4.3–4.4.
  - Expandido Section 4.1 "Velocidad de fase y velocidad de grupo" en Chapter 4 y 5.md: añadida distinción física cresta vs. paquete, Fig. 4.2, relación Ec. 4.2 (Vg = Vph + k·dVph/dk), caso normalmente dispersivo (Vg < Vph), representación en f-k (posición = Vph, tangente = Vg), Fig. 4.4, caso multimodal con curvas propias por modo, razón por la que se usa Vph en inversión. De ~130 a ~450 palabras.
- **Próximo paso:** Expandir Section 4.5 SPAC/ESAC (~180 palabras).

### 2026-03-19 — iteración 13 de loop (segunda fase)
- **Estado:** VÁLIDA.
- **Acción realizada:**
  - Leído Sebastiano Foti Chapter 3.pdf pp. 21–40 (libro pp. 141–160): secciones 3.3.7 completa y 3.4.1 intro.
  - Expandido Section 3.3.7 "Señales 2D y la transformada f-k" en Chapter 3.md: añadidos definición formal de la transformada f-k 2D (Ecs. 3.17–3.18), onda plana ideal en f-k (delta de Dirac, Ec. 3.19–3.20, Fig. 3.15), efecto del muestreo temporal finito (sinc en frecuencia, Ec. 3.21–3.22, Fig. 3.16), ventana 2D combinada temporal+espacial (Ecs. 3.25–3.29, Fig. 3.17), análisis de resolución multimodal con cuatro casos (Fig. 3.18a-d), condición cuantitativa D > 2π/|k₁-k₂|. De ~170 a ~700 palabras.
  - [[MASW Method]] wikilink añadido en la implicación final de la sección.
- **Próximo paso:** Evaluar si Chapter 3 puede marcarse "consolidado" o si hay secciones adicionales que requieren expansión; luego iniciar segunda fase Chapter 4 y 5.

### 2026-03-19 — iteración 12 de loop (segunda fase)
- **Estado:** VÁLIDA.
- **Acción realizada:**
  - Expandido Section 3.3.3 "Muestreo y criterio de Nyquist" en Chapter 3.md: añadidos modelo de función comb para el muestreo (Ec. 3.13, repetición periódica del espectro, Fig. 3.9), frecuencia de Nyquist $F_{Nyq} = F_s/2$, teorema de Nyquist–Shannon Fs > 2fmax (Ec. 3.14, Figs. 3.10–3.11), mecanismo de aliasing (componentes ficticias a frecuencias menores), protección por hardware (filtros antialiasing) y software (sobremuestreo), extensión al dominio espacial (kNyq = 1/(2ΔX)), aliasing espacial en arreglos end-off, regla práctica MASW ΔX < λmin/2. De ~130 a ~450 palabras.
- **Próximo paso:** Expandir sección 3.3.7 (f-k 2D, ~170 palabras).

### 2026-03-19 — iteración 11 de loop (segunda fase)
- **Estado:** VÁLIDA.
- **Acción realizada:**
  - Expandido Section 3.3.5 "Ventaneo y spectral leakage" en Chapter 3.md: añadido modelo de ventana temporal z(t) = w(t)·s(t), Ecs. 3.15–3.16, efecto en espectro (convolución → lóbulo principal finito + side lobes), spectral leakage, enmascaramiento de modos débiles, ventanas Hanning/Hamming vs. boxcar, extensión al dominio espacial (apertura D → resolución Δk), implicación crítica para diseño MASW. De ~110 a ~450 palabras.
  - Añadido [[MASW Method]] wikilink en síntesis del capítulo (Chapter 3.md).
  - Añadido [[Inversión]] wikilink en síntesis.
  - Creado concepto [[MASW Method]] en Concepts/07 Acquisition and Processing/.
- **Próximo paso:** Continuar segunda fase Chapter 3 — expandir sección 3.3.3 (sampling/aliasing, ~130 palabras) y revisar sección 3.3.7 (f-k transform).

### 2026-03-19 — iteración 10 de loop (segunda fase)
- **Estado:** VÁLIDA.
- **Acción realizada:**
  - Evaluado Chapter 2: calidad alta (todo detallado), no requiere mejoras inmediatas.
  - Leído Sebastiano Foti Chapter 3.pdf pp. 1–20 (libro pp. 121–140): secciones 3.2 y 3.3.1.
  - Expandido Section 3.2 "The Wave Field as a Signal" en Chapter 3.md: añadidos naturaleza 4D→2D del campo, experimento ideal vs. real, cadena de medición, Ecs. 3.1–3.2 (señal + ruido), figura 3.3 y 3.5, rol crítico del muestreo espacial. De ~150 a ~450 palabras.
  - Expandido Section 3.3.1 "Análisis espectral" en Chapter 3.md: añadidos principio de descomposición en componentes cíclicas, espectro de amplitud y fase, tabla dominio tiempo→frecuencia y espacio→número de onda, por qué el dominio f-k es el dominio natural para ondas superficiales, figuras 3.6 y 3.7. De ~80 a ~350 palabras.
  - Añadido [[ReMi Method]] wikilink en sección 3.4.3.3.
  - Creado concepto [[ReMi Method]] en Concepts/07 Acquisition and Processing/.
  - Chapter 3 marcado como en revisión profunda (segunda fase).
- **Próximo paso:** Continuar segunda fase Chapter 3 — revisar secciones restantes aún superficiales (3.3.5 windowing, 3.3.7 f-k transform implicaciones, 3.4.3.3 passive methods).

### 2026-03-19 — iteración 23 de loop (tercera fase — cierre)
- **Estado:** VÁLIDA.
- **Acción realizada:**
  - Escaneados todos los wikilinks activos en Chapter 3, 4 y 5, 6, 7, 8 → identificados 3 wikilinks sin archivo de concepto: `[[SPAC]]`, `[[Dispersion Curve]]`, `[[Refraction Seismics]]`.
  - Creado concepto [[SPAC Method]] en Concepts/07 Acquisition and Processing/: autocorrelación espacial (Ec. 4.28), caso fuente única (ρ = cos(k₀·χ), Ec. 4.33), estimación experimental (Ec. 4.34), caso isótropo (ρ = J₀(k₀r), Ec. 4.40–4.41), ESAC para geometrías arbitrarias, tabla SPAC vs f-k/beamformer, limitaciones (no separa modos, isotropía, campo cercano).
  - Corregido wikilink `[[Dispersion Curve|...]]` → `[[Dispersion Relation|...]]` en Chapter 7.md (misma entidad conceptual, nombre alternativo).
  - Corregido wikilink `[[SPAC]]` → `[[SPAC Method|SPAC]]` en Chapter 7.md línea 85.
  - `[[Refraction Seismics]]` dejado sin concepto propio (método externo, fuera del alcance del vault).
  - **TERCERA FASE COMPLETA**: todos los wikilinks de los capítulos 2–8 resueltos en conceptos propios.
- **Próximo paso:** Ninguno en el pipeline actual. Vault en estado consolidado.

### 2026-03-19 — iteraciones 21–22 de loop (tercera fase)
- **Estado:** VÁLIDA.
- **Acción realizada:**
  - Creado concepto [[Non-uniqueness]] en Concepts/08 Inversion and Interpretation/: definición Hadamard, causas físicas (resolución finita/equivalencia parámetros/insensibilidad a Vp), 4 regímenes de misfit (Fig. 6.11), estrategias de mitigación (a priori, regularización, búsqueda global, inversión conjunta), implicación práctica Vs,30.
  - Creado concepto [[Monte Carlo Methods]] en Concepts/08 Inversion and Interpretation/: principio de muestreo aleatorio, función de desajuste E(m) (Ec. 6.34), test de Fisher para selección, ejemplo La Salle (10⁵ modelos, Socco & Boiero 2008, Fig. 7.19–7.22), tabla comparativa LS vs GS, variantes (algoritmos genéticos, simulated annealing, Neighbourhood Algorithm).
  - Añadidos wikilinks [[Non-uniqueness]] y [[Monte Carlo Methods]] en Chapter 6.md y Chapter 7.md en las menciones relevantes.
  - **Tercera fase sustancialmente completa**: todos los conceptos con wikilinks activos en los capítulos tienen archivos propios.
- **Próximo paso:** Verificar si quedan wikilinks rotos o conceptos secundarios pendientes. Considerar Poisson Ratio si es pertinente.

### 2026-03-19 — iteraciones 19–20 de loop (tercera fase)
- **Estado:** VÁLIDA.
- **Acción realizada:**
  - Leído Chapter 8.md sección 8.4 (interferometría sísmica, pp. 427–430).
  - Leído Chapter 4 y 5.md sección 4.4 (MOPA, pp. 220–230).
  - Creado concepto [[Seismic Interferometry]] en Concepts/07 Acquisition and Processing/: principio de cross-correlación, función de Green (Weaver, Snieder, Wapenaar), correlogram gather, puntos estacionarios, fuente virtual, interferograma vs ReMi (números de onda verdadero vs aparente, Figs. 8.28–8.32), hipótesis de campo difuso, relación con SPAC/ESAC, limitaciones.
  - Creado concepto [[MOPA]] en Concepts/07 Acquisition and Processing/: derivación fase lineal en posición (Ec. φ = -k·x + φ₀), formulación matricial (Φ = G·M), solución mínimos cuadrados ponderados con σ_V directo, test chi-cuadrado de linealidad (Ecs. 4.26–4.27), detección campo cercano y variaciones laterales (Vignoli 2009), tabla comparativa SASW vs MOPA, limitaciones.
  - **Tres conceptos principales de tercera fase completados**: HVSR, Seismic Interferometry, MOPA.
- **Próximo paso:** Evaluar si se requieren conceptos adicionales (Non-uniqueness, Poisson Ratio, Monte Carlo) o si la tercera fase puede considerarse completa.

### 2026-03-19 — iteración 9 de loop
- **Estado:** VÁLIDA.
- **Acción realizada:**
  - Leído Sebastiano Foti Chapter 8.pdf pp. 21–48 (libro pp. 413–440): secciones 8.3–8.5 completas.
  - Escrito Section 8.3 en Chapter 8.md: inversión conjunta con otros datos geofísicos — conceptos single/multiple-domain, cooperative vs simultaneous, geometrical (cross-gradient, Gallardo & Meju 2003, Eq. 8.1) y petrophysical (Archie, Wyllie, Gardner); joint inversion con eléctrico/EM (VES, Jacobiano combinado, Comina 2004, Fig. 8.20); con datos sísmicos (Love+Rayleigh, Rayleigh+guided, +refracción P); ejemplo hidden layer (Piatti 2013, Monte Carlo, Fig. 8.21–8.25); aplicación gran escala 3D Gulf of Suez (Strobbia 2010, Fig. 8.26–8.27).
  - Escrito Section 8.4 en Chapter 8.md: interferometría sísmica pasiva — principio de cross-correlación, función de Green, correlogram gather, puntos estacionarios, fuente virtual; interferograma vs ReMi (Fig. 8.28–8.32).
  - Escrito Section 8.5 en Chapter 8.md con subsecciones 8.5.1–8.5.4: polarización y H/V — elipticidad en estratificado, ratio H/V, singularidades f_H y f_V, frecuencia natural f_0 = Vs/4H (Fig. 8.33–8.35); identificación de modos con alto contraste, osculación (Fig. 8.36–8.38); H/V pasivo (HVSR, Nakamura 1989, dominancia ondas superficiales); adquisición y procesamiento (SESAME 2004); interpretación H/V (Fig. 8.39), inversión conjunta dispersión + H/V.
  - Creado concepto [[P-guided Waves]] en Concepts/04 Body and Surface Waves/.
  - Chapter 8 marcado como COMPLETADO (primera fase) — pp. 393–440.
  - **Primera fase completada: capítulos 2–8 todos completados.**
- **Próximo paso:** Iniciar segunda fase comenzando desde Chapter 2.
