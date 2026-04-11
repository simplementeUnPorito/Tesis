# HVSR (Horizontal-to-Vertical Spectral Ratio)

> [!CONCEPT] Definición
> El **HVSR** (*Horizontal-to-Vertical Spectral Ratio*) es la razón entre la amplitud espectral de las componentes horizontales y la componente vertical del movimiento del terreno medida sobre microtremores (ruido sísmico ambiental). El pico del HVSR ocurre a la **frecuencia fundamental** del sitio $f_0 = V_S/(4H)$, controlada por la velocidad de corte $V_S$ del depósito y su espesor $H$. El origen físico del pico es la **singularidad de la elipticidad horizontal** de las [[Rayleigh Waves|ondas de Rayleigh]] — no una amplificación de ondas S como propuso Nakamura (1989). La técnica requiere solo un sensor triaxial y permite estimar $f_0$ de forma no invasiva, económica y rápida. La curva H/V puede invertirse conjuntamente con la [[Dispersion Curve|curva de dispersión]] ([[MASW Method|MASW]], [[SPAC Method|SPAC]]) para reducir la [[Non-uniqueness|no-unicidad]] del problema inverso.
>
> — Foti et al. (2018), Cap. 8.5.2–8.5.4; Nakamura (1989); SESAME (2004).

## Principio

El **HVSR** (*Horizontal-to-Vertical Spectral Ratio*) es la razón entre la amplitud espectral de las componentes horizontales y la componente vertical del movimiento del terreno, medida sobre registros de **ruido sísmico ambiental** (*microtremores*). La técnica fue introducida por Nogoshi e Igarashi (1971) y popularizada por Nakamura (1989, 1996, 2000).

La interpretación de Nakamura original atribuía el pico H/V directamente a la función de transferencia del sitio para ondas S. El consenso actual en la comunidad sismológica e ingenieril es diferente: **las ondas superficiales dominan la respuesta H/V en la mayoría de los casos**, y el pico observado está relacionado con la **elipticidad horizontal de las [[Rayleigh Waves|ondas de Rayleigh]]** (Horike 1985; Arai y Tokimatsu 1998).

## Fundamento físico

La **elipticidad** de las ondas de Rayleigh depende de la frecuencia en medios estratificados. El ratio H/V del modo fundamental presenta un comportamiento característico (Figura 8.34, p. 432):

- **Singularidad f_H** (*H singularity*): frecuencia a la que la componente vertical se anula y el movimiento es puramente horizontal. El ratio H/V → ∞.
- **Singularidad f_V** (*V singularity*): frecuencia a la que la componente horizontal se anula. H/V → 0.
- **Frecuencia natural f₀**: frecuencia de resonancia fundamental de corte del depósito,

$$f_0 = \frac{V_S}{4H}$$

donde $V_S$ es la velocidad de corte del depósito superficial y $H$ su espesor. El pico H/V (f_H) es aproximadamente igual a f₀ cuando el contraste de impedancia es alto (la capa tiene baja velocidad homogénea):

$$f_H \approx f_0 = \frac{V_S}{4H}$$

> **Implicación práctica**: midiendo el pico H/V se estima f₀; si se conoce H (por ejemplo, de un sondeo), se puede estimar $V_S$, y viceversa.

## Criterios de interpretación

Interpretación de la curva H/V observada (Foti p. 438):

1. **Pico claro y no de origen industrial**: indica un gran contraste de impedancia en el subsuelo; la frecuencia del pico es cercana a f₀. El **valor absoluto del pico no** está relacionado con el factor de amplificación del sitio.
2. **Curva plana** (valores H/V entre 0.5 y 2): el perfil de velocidades local probablemente no tiene contrastes de impedancia significativos.
3. **Ambigüedad**: múltiples perfiles de velocidad pueden producir la misma curva H/V; la [[Non-uniqueness|no-unicidad]] requiere información a priori adicional o [[Joint Inversion|inversión conjunta]].

El **valor del pico** H/V no puede usarse directamente como amplificación sísmica del sitio, aunque ha sido empleado empíricamente con limitaciones reconocidas.

## Adquisición (SESAME 2004)

- **Sensores**: estación multicomponente (al menos 3 componentes) de baja frecuencia natural. El rango dinámico y la respuesta en fase deben ser iguales en todos los canales.
- **Condiciones**: evitar estructuras subterráneas, suelo blando superficial irregular, maquinaria y fuentes transitorias fuertes.
- **Duración del registro**: ≥ 10 minutos para f₀ > 1 Hz; hasta media hora si f₀ < 1 Hz. La duración debe ser al menos 10× el período f₀⁻¹.
- **Procesamiento**: selección de ventanas estacionarias (descartando transitorios), cálculo de espectros de Fourier, suavizado, combinación cuadrática de componentes horizontales, cálculo de H/V, promediado y estimación de varianza.

## Inversión de H/V

La curva H/V puede invertirse formalmente para estimar los parámetros del subsuelo, de forma análoga a la inversión de la [[Dispersion Relation|curva de dispersión]] (Fäh et al. 2001). Las curvas se corrigen por la contaminación de ondas SH y Love antes de invertir. Arai y Tokimatsu (2000) mostraron que los modos superiores de [[Rayleigh Waves|Rayleigh]] y [[Love Waves|Love]] mejoran la reproducción de las curvas observadas.

La **[[Joint Inversion|inversión conjunta]] de [[Dispersion Curve|curvas de dispersión]] + H/V** es más robusta que cada inversión individual porque los dos datos tienen diferente sensibilidad a los parámetros del modelo (Parolai et al. 2005). La [[Dispersion Curve|curva de dispersión]] es más sensible a la distribución vertical de Vs; la curva H/V es más sensible al contraste de impedancia en la interfaz. La combinación mejora el condicionamiento del problema inverso.

## Limitaciones

- La curva H/V no es equivalente a la función de amplificación del sitio.
- La interpretación asume dominancia de ondas de Rayleigh; en sitios con alta contribución de Love, la curva es más compleja.
- La hipótesis de campo difuso isótropo puede no cumplirse en entornos urbanos con fuentes de ruido direccionales.
- La identificación del pico requiere criterios de calidad (SESAME 2004): al menos dos picos claros en la mitad del rango de frecuencias de interés.

> [!EXAMPLE] Evidencia empírica: Lermo & Chávez-García (1993) — validación HVSR con registros de terremoto
> **Paper 018 (Lermo & Chávez-García 1993, BSSA 83(5):1574–1594, 1103 citas)** proporciona la primera validación sistemática del método HVSR usando registros reales de terremoto en tres ciudades mexicanas (Oaxaca, Acapulco y Ciudad de México). Aplicando la razón H/V a la fase S de los registros, los autores reproducen cuantitativamente la función de transferencia empírica del sitio (*Standard Spectral Ratio*, SSR) obtenida con estación de referencia en roca — sin necesidad de dicha referencia. La concordancia entre H/V y SSR en los tres sitios valida que la técnica captura la respuesta fundamental del sitio de forma fiable. En Ciudad de México (zona lacustre, suelo muy blando), el pico H/V a ~0.5 Hz coincide con el período dominante de amplificación conocido. El estudio establece que la razón H/V de la onda S puede sustituir al SSR para evaluación rápida de efecto de sitio de primer orden, siendo particularmente valioso en regiones sin estación de referencia en roca.
>
> — Research Database, entrada 018 (core); Lermo & Chávez-García (1993), *Bull. Seismol. Soc. Am.* 83(5):1574–1594.

> [!EXAMPLE] Evidencia empírica: Bonnefoy-Claudet et al. (2009) — HVSR en cuenca sedimentaria de Santiago de Chile
> **Paper 049 (Bonnefoy-Claudet et al. 2009, GJI 176(3):925–937, 132 citas)** realiza mediciones extensas de HVSR en toda la cuenca sedimentaria urbana de Santiago de Chile. Las razones H/V analizadas según criterios SESAME revelan tres patrones espaciales: picos nítidos (zonas con alto contraste de impedancia suelo/roca), curvas planas (zonas sin contraste significativo) y picos anchos (variaciones laterales de estructura). Las frecuencias de resonancia $f_0$ cartografiadas desde 0.5 Hz (zona central, sedimentos profundos) hasta >5 Hz (borde oriente, roca próxima a superficie) coinciden con el patrón de daños históricos en terremotos. El estudio demuestra que HVSR es una herramienta confiable para microzonificación sísmica en cuencas sedimentarias urbanas complejas de Sudamérica, con instrumentación mínima y sin fuente activa.
>
> — Research Database, entrada 049 (core); Bonnefoy-Claudet et al. (2009), *Geophys. J. Int.* 176(3):925–937.

> [!EXAMPLE] Evidencia empírica: Garofalo et al. (2016) — HVSR como dato complementario en InterPACIFIC
> **Papers 006+007 (Garofalo et al. 2016a/b)** incluyen mediciones HVSR en los 3 sitios del estudio InterPACIFIC como dato complementario a los métodos de ondas superficiales ([[MASW Method|MASW]], ReMi, SPAC). Los resultados muestran que el pico H/V coincide con la frecuencia fundamental inferida de los perfiles $V_S(z)$ del borehole en los sitios donde el contraste de impedancia es alto (Mirandola: $f_0 \approx 0.5$ Hz, sedimentos blandos sobre roca a >150 m). La concordancia confirma el uso de HVSR para verificar independientemente la frecuencia de resonancia del sitio. Sin embargo, la [[Joint Inversion|inversión conjunta]] HVSR + [[Dispersion Curve|curva de dispersión]] muestra mejora en el condicionamiento del problema inverso en los sitios con alta [[Non-uniqueness|no-unicidad]], consistente con el resultado de Parolai et al. (2005).
>
> — Research Database, entradas 006, 007 (core); Garofalo et al. (2016a/b), *Near Surface Geophysics*.

## Referencias

| Fuente | Sección / Página |
|--------|-----------------|
| Foti et al. (2018), *Surface Wave Methods* | Cap. 8.5.2–8.5.4, pp. 430–440 — HVSR e [[Joint Inversion|inversión conjunta]] |
| Nakamura (1989), *QR of RTRI* | Propuesta original HVSR como función de transferencia |
| Lermo & Chávez-García (1993), *BSSA* 83(5):1574–1594 | Paper 018 — validación HVSR con terremotos; 1103 citas |
| SESAME Project (2004) | Guías para implementación del método H/V |
| Bonnefoy-Claudet et al. (2009), *GJI* 176(3):925–937 | Paper 049 — HVSR cuenca sedimentaria Santiago de Chile; 132 citas |
| Garofalo et al. (2016a/b) | Papers 006, 007 — HVSR en InterPACIFIC |
