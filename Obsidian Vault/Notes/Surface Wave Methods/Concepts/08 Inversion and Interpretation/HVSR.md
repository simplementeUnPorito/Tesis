# HVSR (Horizontal-to-Vertical Spectral Ratio)

> **Contexto:** Técnica pasiva monoestación para la caracterización de sitio sísmica basada en la polarización de las ondas superficiales.
> **Fuente:** Foti et al. (2014), Cap. 8.5.2–8.5.4; Nakamura (1989); SESAME (2004).

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
3. **Ambigüedad**: múltiples perfiles de velocidad pueden producir la misma curva H/V; la no-unicidad requiere información a priori adicional o inversión conjunta.

El **valor del pico** H/V no puede usarse directamente como amplificación sísmica del sitio, aunque ha sido empleado empíricamente con limitaciones reconocidas.

## Adquisición (SESAME 2004)

- **Sensores**: estación multicomponente (al menos 3 componentes) de baja frecuencia natural. El rango dinámico y la respuesta en fase deben ser iguales en todos los canales.
- **Condiciones**: evitar estructuras subterráneas, suelo blando superficial irregular, maquinaria y fuentes transitorias fuertes.
- **Duración del registro**: ≥ 10 minutos para f₀ > 1 Hz; hasta media hora si f₀ < 1 Hz. La duración debe ser al menos 10× el período f₀⁻¹.
- **Procesamiento**: selección de ventanas estacionarias (descartando transitorios), cálculo de espectros de Fourier, suavizado, combinación cuadrática de componentes horizontales, cálculo de H/V, promediado y estimación de varianza.

## Inversión de H/V

La curva H/V puede invertirse formalmente para estimar los parámetros del subsuelo, de forma análoga a la inversión de la [[Dispersion Relation|curva de dispersión]] (Fäh et al. 2001). Las curvas se corrigen por la contaminación de ondas SH y Love antes de invertir. Arai y Tokimatsu (2000) mostraron que los modos superiores de [[Rayleigh Waves|Rayleigh]] y [[Love Waves|Love]] mejoran la reproducción de las curvas observadas.

La **inversión conjunta de curvas de dispersión + H/V** es más robusta que cada inversión individual porque los dos datos tienen diferente sensibilidad a los parámetros del modelo (Parolai et al. 2005). La curva de dispersión es más sensible a la distribución vertical de Vs; la curva H/V es más sensible al contraste de impedancia en la interfaz. La combinación mejora el condicionamiento del problema inverso.

## Limitaciones

- La curva H/V no es equivalente a la función de amplificación del sitio.
- La interpretación asume dominancia de ondas de Rayleigh; en sitios con alta contribución de Love, la curva es más compleja.
- La hipótesis de campo difuso isótropo puede no cumplirse en entornos urbanos con fuentes de ruido direccionales.
- La identificación del pico requiere criterios de calidad (SESAME 2004): al menos dos picos claros en la mitad del rango de frecuencias de interés.

## Referencias

- Nakamura, Y. (1989), *QR of RTRI*.
- SESAME Project (2004), *Guidelines for the implementation of the H/V spectral ratio technique*.
- Foti et al. (2014), Cap. 8.5.2–8.5.4, pp. 430–440.
