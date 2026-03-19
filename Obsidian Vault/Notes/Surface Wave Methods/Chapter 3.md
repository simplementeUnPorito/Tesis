# Measurement of Surface Waves

## Introducción

Este capítulo aborda la teoría y práctica de la **adquisición de datos de ondas superficiales**. La medición es un proceso experimental en el que se generan ondas superficiales y se observan sus efectos en el medio. El objetivo final es estimar los **parámetros de propagación** —principalmente la velocidad de fase en función de la frecuencia— que luego se usan para caracterizar el subsuelo.

El capítulo sigue la secuencia real del workflow: adquisición → procesamiento → inversión. Entender las limitaciones de la adquisición es indispensable para diseñar correctamente el procesamiento posterior.

---

## Estructura del capítulo

- **3.1** Principios generales de adquisición sísmica
- **3.2** El campo de ondas como señal multidimensional
- **3.3** Adquisición digital de señales sísmicas
- **3.4** Adquisición específica de ondas superficiales
- **3.5** Equipamiento sísmico

---

## 3.1 Seismic Data Acquisition

### 3.1.1 Datos sísmicos

La adquisición sísmica involucra tres elementos: **fuente**, **receptores** y **sistema de registro**. La fuente genera ondas sísmicas; los receptores detectan el movimiento de partículas (o variación de presión) en posiciones discretas del terreno; el sistema registra la señal en el tiempo.

La unidad elemental de datos sísmicos es la **traza sísmica** (*seismic trace*): una señal en tiempo que describe la respuesta del medio a una fuente en una posición dada. Las trazas se representan como *wiggles* o como gráficos de densidad.

En aplicaciones con múltiples receptores, el conjunto de trazas simultáneas forma un **sismograma multicanal** (*seismic gather*). Esto permite observar la propagación de ondas en espacio y tiempo simultáneamente.

El campo de ondas medido en un registro típico contiene múltiples tipos de ondas:
- ondas refractadas (primeras llegadas)
- ondas reflejadas
- ondas superficiales (dominantes a distancias intermedias)

*(Fuente: Foti Ch. 3, Sec. 3.1.1, p. 122–124)*

### 3.1.2 Adquisición de ondas superficiales

En métodos de ondas superficiales, la adquisición apunta a medir la **velocidad de fase** (o grupo) y su dependencia en frecuencia, sobre un rango amplio de frecuencias. Esto implica registrar longitudes de onda largas (bajas frecuencias → mayor profundidad) y cortas (altas frecuencias → capas superficiales).

La peculiaridad de la adquisición de ondas superficiales respecto a otras metodologías sísmicas es que la **completitud y exactitud de los datos depende de su distribución en el dominio de la frecuencia**, no solo en tiempo y espacio.

Las ondas superficiales son eventos de baja velocidad y muy dispersivos. Su registro requiere trazas largas en tiempo porque el tren de onda puede durar varios segundos incluso a distancias cortas. Son el evento de mayor amplitud en registros de campo de ingeniería.

*(Fuente: Foti Ch. 3, Sec. 3.1.2, p. 125–126)*

---

## 3.2 The Wave Field as a Signal in Time and Space

El campo de ondas es una función continua de espacio y tiempo. Para ondas superficiales planas a lo largo de la superficie libre, puede representarse como una función 2D: $s(x,t)$.

Una traza sísmica es el valor de este campo en una posición fija: $s(x_0, t)$.

En la realidad, la medición no puede hacerse en forma continua ni infinita. El dato adquirido es:

$$
\text{data} = \text{muestreo}\bigl(\text{instrumento}(\bar{s} + n)\bigr)
$$

donde $\bar{s}$ es la señal real de ondas superficiales y $n$ es el ruido. Las limitaciones de muestreo en tiempo y espacio, sumadas al instrumento y al ruido, determinan la calidad y el contenido de información útil del dato.

El objetivo ideal (no alcanzable en la práctica): registrar $s(x,t)$ de manera continua, sin distorsión y libre de ruido, sobre un rango amplio de frecuencias.

*(Fuente: Foti Ch. 3, Sec. 3.2, p. 126–129)*

---

## 3.3 Acquisition of Digital Seismic Signals

### 3.3.1 Análisis espectral y transformadas

El análisis de señales sísmicas se realiza principalmente en el **dominio de la frecuencia**. Descomponer una señal en sus componentes cíclicas (análisis espectral) revela la distribución de energía en frecuencias.

Las herramientas matemáticas centrales son las **transformadas integrales**, que mapean entre dominios:
- dominio tiempo → dominio frecuencia
- dominio espacio → dominio número de onda

*(Fuente: Foti Ch. 3, Sec. 3.3.1, p. 130–131)*

### 3.3.2 Transformada de Fourier

La transformada de Fourier convierte una señal en tiempo $g(t)$ en su representación en frecuencia $G(f)$:

$$
G(f) = \int_{-\infty}^{+\infty} g(t)\,e^{-j2\pi ft}\,dt
$$

La transformada inversa:

$$
g(t) = \int_{-\infty}^{+\infty} G(f)\,e^{j2\pi ft}\,df
$$

No se pierde información en la transformación: las dos representaciones son complementarias.

Para señales en espacio, la variable independiente es $k$ (número de onda):

$$
g(x) \xleftrightarrow{F} G(k)
$$

Propiedades clave utilizadas en este capítulo: linealidad, desplazamiento (produce fase), escalamiento, convolución (multiplicación en tiempo ↔ convolución en frecuencia, y viceversa).

*(Fuente: Foti Ch. 3, Sec. 3.3.2, p. 131–134)*

### 3.3.3 Muestreo y criterio de Nyquist

El muestreo convierte la señal continua en una serie discreta de valores a intervalos $\Delta t$. La frecuencia de muestreo es $F_s = 1/\Delta t$.

El espectro de la señal muestreada es una **repetición periódica** del espectro original, con período igual a $F_s$.

Si la frecuencia máxima del contenido espectral supera $F_s/2$ (frecuencia de Nyquist), las réplicas se superponen: ocurre **aliasing**. Para evitarlo:

$$
F_s > 2 f_{\max}
$$

Este criterio es el **teorema de Nyquist–Shannon**.

En la práctica: filtros antialiasing analógicos (hardware) eliminan componentes de alta frecuencia antes de digitalizar. También pueden usarse filtros digitales tras el muestreo (software), o sobremuestreo espacial seguido de filtrado.

*(Fuente: Foti Ch. 3, Sec. 3.3.3–3.3.4, p. 134–137)*

### 3.3.5 Ventaneo y *spectral leakage*

Cualquier señal medida tiene duración finita → equivale a multiplicar la señal infinita por una **ventana temporal**. La multiplicación en tiempo corresponde a la **convolución** del espectro original con el espectro de la ventana.

Para una ventana boxcar, el espectro resultante presenta:
- reducción de la resolución espectral (lobulo principal finito)
- lóbulos laterales (*side lobes*)

El **spectral leakage** dispersa energía fuera de la frecuencia real y dificulta resolver eventos cercanos en frecuencia o número de onda.

Para reducir los side lobes se usan ventanas suavizadas (Hanning, Hamming), a costa de perder algo de resolución.

En el espacio, la "ventana" es la **apertura del arreglo** $D$: la longitud total cubierta por los receptores. Mayor apertura → mejor resolución en número de onda → mejor capacidad de separar modos.

*(Fuente: Foti Ch. 3, Sec. 3.3.5, p. 137–140)*

### 3.3.6 Cuantización y conversión analógico-digital

La conversión A/D requiere **cuantizar** la amplitud: el valor continuo se redondea al nivel discreto más cercano. El error de cuantización es proporcional al tamaño del paso de cuantización (LSB).

La **resolución dinámica** (en bits) define cuántos niveles distintos puede representar el sistema. Los sistemas sísmicos modernos usan entre 16 y 24 bits, lo que da entre 96 y 144 dB de rango dinámico.

*(Fuente: Foti Ch. 3, Sec. 3.3.6, p. 140–141)*

### 3.3.7 Señales 2D y la transformada f-k

El campo de ondas sísmico es una función 2D: $s(x,t)$. La transformada de Fourier 2D (transformada **f-k**) convierte simultáneamente el dominio tiempo–espacio en el dominio frecuencia–número de onda:

$$
G(f,k) = \int_{-\infty}^{+\infty}\int_{-\infty}^{+\infty} g(t,x)\,e^{-j2\pi(ft+kx)}\,dx\,dt
$$

En el dominio f-k, cada modo de propagación ocupa una posición específica. La pendiente de una línea en f-k corresponde a la **velocidad de fase** de ese modo.

Las limitaciones de resolución debidas al ventaneo en tiempo y espacio se extienden al dominio 2D:
- La **resolución en frecuencia** es proporcional a $1/T$ (donde $T$ es la duración del registro)
- La **resolución en número de onda** es proporcional a $1/D$ (donde $D$ es la apertura espacial)

Para resolver dos modos de propagación distintos en el espacio de f-k, la apertura del arreglo debe ser suficientemente grande para que sus wavenumbers queden separados por más de $2\pi/D$ (criterio de Rayleigh).

> **Implicación para la tesis**: la incapacidad de resolver modos en el dominio f-k lleva a una curva de dispersión aparente que mezcla modos. Aumentar la apertura del arreglo mejora la resolución modal.

*(Fuente: Foti Ch. 3, Sec. 3.3.7, p. 141–148)*

---

## 3.4 Acquisition of Surface Waves

### 3.4.1 Ruido sísmico

El dato adquirido contiene señal y **ruido**. En el contexto de ondas superficiales, señal = ondas superficiales planas compatibles con el modelo 1D asumido. Todo lo demás es ruido.

$$
\text{SNR [dB]} = 20\log_{10}\frac{S}{N}
$$

El diseño de la adquisición debe maximizar el SNR para maximizar la exactitud de las propiedades estimadas.

#### Ruido incoherente

El ruido incoherente es no reproducible estadísticamente. Fuentes: tráfico, maquinaria, viento, actividad humana, ruido electrónico. No está correlacionado con el experimento.

Estrategias para aumentar el SNR ante ruido incoherente:
- **Vertical stacking**: repetir el disparo múltiples veces y sumar. El SNR mejora como $\sqrt{n}$ repeticiones (señal crece linealmente, ruido incoherente crece como $\sqrt{n}$).
- Adquirir en horarios de bajo ruido ambiental.
- Aumentar la energía de la fuente.

El ruido incoherente afecta directamente la **incertidumbre en la fase**, que se propaga a la incertidumbre en la velocidad de fase estimada.

*(Fuente: Foti Ch. 3, Sec. 3.4.1.1–3.4.1.2, p. 149–157)*

#### Ruido coherente

El ruido coherente es reproducible determinísticamente. No se puede eliminar con *stacking*. Requiere estrategias de diseño del arreglo o de procesamiento.

Tipos de ruido coherente en adquisición de ondas superficiales:

- **Ondas de cuerpo** (P y S): llegan antes o simultáneamente con las ondas superficiales. En aplicaciones de pequeña escala suelen tener menor amplitud. Pueden identificarse en tiempo-offset y eliminarse o ignorarse.
- **Modos superiores** de propagación: en sitios inversamente dispersivos pueden dominar la respuesta. Si el modelo solo considera el modo fundamental, los modos superiores son ruido coherente. La solución correcta es incluirlos en el modelo (inversión multimodal).
- **Efecto de campo cercano** (*near-field effect*): las Rayleigh waves solo se comportan como ondas planas más allá de cierta distancia de la fuente. Dentro de esa zona, el campo está dominado por contribuciones de ondas de cuerpo y la velocidad aparente no corresponde a la del modo fundamental.
- **Air blast**: la onda de presión acústica en el aire (velocidad ~331–360 m/s) puede ser detectada por los geófonos. Aparece en el dominio f-k como un evento lineal de velocidad constante.
- **Variaciones laterales**: heterogeneidades subsuperficiales hacen que las ondas superficiales no sigan el modelo de propagación plana 1D, generando difracción y distorsión de la velocidad aparente.

*(Fuente: Foti Ch. 3, Sec. 3.4.1.3–3.4.1.6, p. 158–160)*

---

## Conceptos relacionados

- [[Adquisición de Datos]]
- [[Procesamiento de Señales]]
- [[Rayleigh Waves]]
- [[Love Waves]]
- [[Phase Velocity]]
- [[Group Velocity]]
- [[Wave Dispersion]]
- [[Surface Wave Modes]]
- [[Mode Superposition]]
- [[Geometric Dispersion]]
- [[Wavenumber]]
- [[Angular Frequency]]
- [[Fourier Integral]]

---

### 3.4.1.7 Variaciones laterales

El procesamiento asume un modelo 1D: la propagación es lateralmente homogénea. Las variaciones laterales del subsuelo producen efectos que no pueden modelarse correctamente y deben considerarse ruido coherente.

Implicaciones prácticas:
- Evitar ubicar el arreglo en zonas con discontinuidades litológicas conocidas o capas buzantes.
- Arrays más cortos reducen el riesgo de variaciones laterales pero también la resolución espectral (trade-off apertura vs. homogeneidad lateral).
- Las variaciones laterales pueden identificarse comparando curvas de dispersión extraídas de diferentes segmentos del arreglo.

*(Fuente: Foti Ch. 3, Sec. 3.4.1.7, p. 162)*

### 3.4.1.8 Modos superiores

La propagación de ondas superficiales es inherentemente multimodal. En sitios inversamente dispersivos, los modos superiores pueden dominar la respuesta sobre el modo fundamental. Los modos superiores deben considerarse **información útil**, no ruido, a menos que el sistema de adquisición o inversión no pueda manejarlos.

Consecuencias de no resolver modos:
- La apertura insuficiente hace que los modos se superpongan en el dominio f-k → curva de dispersión aparente que no corresponde a ningún modo individual.
- La inversión del modo fundamental cuando domina un modo superior lleva a perfiles $V_S(z)$ sistemáticamente erróneos.

La adquisición multicanal con apertura suficiente es la única forma de identificar y separar modos.

*(Fuente: Foti Ch. 3, Sec. 3.4.1.8, p. 162–164)*

---

### 3.4.2 Sampling: limitaciones del muestreo espacial y temporal

El campo de ondas sísmico es muestreado con una ventana 2D en tiempo (duración $T$) y espacio (apertura $D$, espaciado $\Delta X$). Esto introduce cuatro limitaciones fundamentales:

#### 3.4.2.1 Muestreo discreto y finito

La ventana 2D en tiempo-offset actúa como multiplicación por una función boxcar 2D → en el dominio f-k es una convolución con la transformada de esa ventana (función sinc 2D). El efecto:
- Resolución limitada en frecuencia y en número de onda.
- Dispersión de energía (spectral leakage) fuera del pico real.

La curva de dispersión experimental es siempre una **curva aparente** que depende de los parámetros de adquisición, no solo de las propiedades del subsuelo.

*(Fuente: Foti Ch. 3, Sec. 3.4.2.1, p. 165–168)*

#### 3.4.2.2 Wavenumber máximo y aliasing espacial

El espaciado entre receptores $\Delta X$ determina el **número de onda de Nyquist**:

$$
k_{Nyq} = \frac{1}{2\Delta X}
$$

Para velocidades bajas (wavenumbers altos), ocurre aliasing espacial: el wavenumber verdadero $k_{true} > k_{Nyq}$ aparece como $k_{alias} = k_{true} - 2k_{Nyq}$ con velocidad aparente negativa. En arreglos end-off, la información aliasada en el cuadrante negativo puede recuperarse, extendiendo el wavenumber máximo efectivo a $2k_{Nyq}$ (longitud mínima igual al espaciado).

**Regla práctica**: espaciado de 1–5 m para caracterización de suelos superficiales.

*(Fuente: Foti Ch. 3, Sec. 3.4.2.2, p. 168–171)*

#### 3.4.2.3 Resolución espectral y apertura

La **apertura** del arreglo $D$ determina la resolución en número de onda:

$$
\Delta k_{Rayleigh} = \frac{2\pi}{D}
$$

Para separar dos modos con wavenumbers $k_1$ y $k_2$, se requiere $D > 2\pi / |k_1 - k_2|$.

Arrays más largos → mayor resolución modal → mejor identificación de modos superiores y mayor exactitud en la estimación de velocidad. Pero arrays más largos aumentan el riesgo de variaciones laterales.

**Longitudes típicas**: 20–100 m para aplicaciones de ingeniería superficiales.

*(Fuente: Foti Ch. 3, Sec. 3.4.2.3, p. 171–173)*

#### 3.4.2.4 Efectos de lóbulos laterales

La ventana boxcar produce lóbulos laterales en el dominio f-k que pueden confundirse con modos de propagación. El *tapering* espacial (ventana Hanning) reduce los lóbulos laterales a costa de una pequeña pérdida de resolución.

*(Fuente: Foti Ch. 3, Sec. 3.4.2.4, p. 173)*

---

### 3.4.3 Survey Design

#### 3.4.3.1 Diseño para ensayos activos

La geometría básica es un **arreglo lineal de receptores uniformemente espaciados** con fuente en uno de los extremos (end-off) o en el centro. Los parámetros de diseño son:

| Parámetro | Efecto principal |
|---|---|
| Espaciado $\Delta X$ | $k_{max}$ → profundidad mínima / longitud de onda mínima |
| Apertura $D = N \cdot \Delta X$ | Resolución modal, profundidad máxima |
| Offset fuente $L_s$ | Excluye zona de campo cercano |
| Duración del registro $T$ | Resolución en frecuencia |

**Reglas empíricas para el offset de fuente**:
- Offset mínimo: $\lambda_R/2$ (Stokoe et al. 1994)
- Para estratigrafías complejas: hasta $\lambda_R$–$2\lambda_R$
- Excluir los primeros receptores afectados por campo cercano en el procesamiento si es necesario.

**Extensión del arreglo** mediante:
- Combinar disparos con la misma fuente moviendo los receptores (aumenta apertura virtual → "walkaway test").
- *Common receiver gather*: fuente se mueve, receptor fijo. Equivalente al sismograma de disparo común por reciprocidad.

*(Fuente: Foti Ch. 3, Sec. 3.4.3.1, p. 174–178)*

#### 3.4.3.2 Método de dos estaciones (SASW)

El método SASW (*Spectral Analysis of Surface Waves*) es un caso especial con solo dos receptores. Su ventaja es la simplicidad logística; su limitación es la mayor vulnerabilidad al aliasing espacial y a la superposición de modos.

Para cubrir un rango amplio de frecuencias, se repite la medición con diferentes espaciados (short → alta frecuencia; long → baja frecuencia), usando el esquema de punto medio común (*common midpoint*) para mejorar la representatividad.

*(Fuente: Foti Ch. 3, Sec. 3.4.3.2, p. 178–179)*

#### 3.4.3.3 Métodos pasivos

Los métodos pasivos aprovechan el **ruido sísmico ambiental** (*microtremors*, frecuencia típica > 1 Hz) como fuente de ondas superficiales. Son útiles cuando:
- Se necesita investigar grandes profundidades (baja frecuencia → longitudes de onda largas).
- No es posible generar ondas superficiales con la energía requerida con fuentes activas.
- El ruido ambiental en el sitio es elevado.

Diferencias con la adquisición activa:
- La posición de la fuente es desconocida y cambiante → se requiere procesamiento 2D.
- Se prefieren arreglos 2D (círculo, triángulo, L, T) para estimar el vector número de onda.
- La técnica ReMi (*Refraction Microtremor*) usa un arreglo lineal y funciona asumiendo isotropía del campo de ruido.

*(Fuente: Foti Ch. 3, Sec. 3.4.3.3, p. 179–181)*

---

## 3.5 Equipment

### 3.5.1 Fuentes sísmicas

La fuente debe generar ondas superficiales con suficiente SNR en el rango de frecuencias de interés. Los parámetros clave son **energía** y **contenido espectral** (especialmente a baja frecuencia, para mayor profundidad).

#### Fuentes impulsivas

Son las más utilizadas en aplicaciones de ingeniería superficiales. Inputan energía con una aplicación corta de fuerza.

| Fuente | Energía | Frecuencias | Ventajas |
|---|---|---|---|
| Sledgehammer (1–15 kg) | Baja–media | 5–200 Hz | Portátil, barato, fácil apilado |
| Weight drop / thumper | Media–alta | 2–50 Hz | Buena energía a baja frecuencia |
| Seismic gun | Media | 5–200 Hz | Más energía que sledgehammer |
| Explosivos | Alta | 5–150 Hz | Broadband, escalable; requiere autorización |

El **sledgehammer** es la fuente más común en ensayos geotécnicos de pequeña escala. Permite fácil *vertical stacking* con interruptor de inercia. Genera suficiente energía para arreglos de 50–100 m.

*(Fuente: Foti Ch. 3, Sec. 3.5.1.1, p. 183–186)*

#### Fuentes vibratorias

Las fuentes vibratorias (vibradores electromecánicos, vibroseis) inputan energía con señales controladas de larga duración. Ventajas: SNR alto mediante correlación (*sweep*), control del contenido espectral. Desventajas: mayor complejidad logística.

La señal de barrido lineal varía la frecuencia con el tiempo:

$$
f(t) = c \cdot t + f_0
$$

La correlación cruzada del registro con la señal de sweep produce un sismograma equivalente al de una fuente impulsiva de alta SNR.

*(Fuente: Foti Ch. 3, Sec. 3.5.1.2–3.5.1.3, p. 186–191)*

### 3.5.2 Receptores

Los receptores transducen el movimiento del terreno en una señal eléctrica. En aplicaciones de campo sobre suelo, los tipos principales son:

#### Geófonos

Los **geófonos** son velocímetros electrodinámicos (bobina móvil en campo magnético). Se comportan como osciladores de un grado de libertad con frecuencia natural $f_n$ y amortiguamiento $D$.

Consideraciones críticas para ondas superficiales:
- La amplitud se atenúa fuertemente **por debajo** de $f_n$. Para medir frecuencias bajas se necesitan geófonos con $f_n$ baja (1–4.5 Hz).
- La **respuesta en fase** afecta la estimación de velocidad. Geófonos no idénticos introducen diferencias de fase espurias.
- Geófonos verticales: capturan la componente vertical del movimiento → sensibles a Rayleigh waves.
- Geófonos horizontales transversales: sensibles a Love waves.

La sensibilidad de fase del geófono introduce incertidumbre en la velocidad estimada. En mediciones de dos estaciones (SASW), este efecto puede ser crítico. En arrays multicanal el efecto es mitigado si todos los receptores son idénticos.

*(Fuente: Foti Ch. 3, Sec. 3.5.2.1, p. 193–197)*

#### Acelerómetros y MEMS

Los acelerómetros son útiles en aplicaciones de alta frecuencia (ensayos de pavimentos, NDT). Los sensores MEMS permiten alta frecuencia, bajo ruido y grabación hasta DC (aceleración estática). Están siendo adoptados progresivamente para aplicaciones de baja frecuencia.

*(Fuente: Foti Ch. 3, Sec. 3.5.2.2, p. 197–198)*

#### Acoplamiento y receptores de dos componentes

El acoplamiento receptor–suelo es fundamental. Los receptores se plantan con espiga de acero o se entierran para maximizar el contacto. Los land streamers ofrecen ventajas logísticas pero menor calidad de acoplamiento.

Los receptores de dos componentes (vertical + horizontal radial) permiten medir la polarización elíptica de las Rayleigh waves y separar modos. Son útiles para inversión conjunta o aplicaciones de caracterización avanzada.

*(Fuente: Foti Ch. 3, Sec. 3.5.2.3–3.5.2.4, p. 198–199)*

---

## Síntesis del capítulo

El flujo de trabajo completo de adquisición de ondas superficiales involucra:

1. **Diseño del arreglo**: espaciado $\Delta X$ (controla $k_{max}$), apertura $D$ (controla resolución modal), offset de fuente (controla campo cercano), duración de registro (controla resolución en frecuencia).

2. **Fuente**: generar suficiente energía a baja frecuencia para la profundidad objetivo. Sledgehammer para aplicaciones de ingeniería (<100 m); fuentes más energéticas para mayor profundidad.

3. **Receptores**: geófonos verticales de baja frecuencia natural (1–4.5 Hz) para capturar Rayleigh waves sobre un rango amplio de frecuencias.

4. **Control de ruido**: maximizar SNR (stacking, adquisición nocturna), identificar y mitigar ruido coherente (campo cercano, modos superiores, variaciones laterales).

La limitación fundamental es que la **curva de dispersión experimental es siempre una curva aparente**: depende de los parámetros de adquisición, no solo del subsuelo. El proceso de inversión debe tener esto en cuenta.

---

## Conceptos relacionados

- [[Adquisición de Datos]]
- [[Procesamiento de Señales]]
- [[Rayleigh Waves]]
- [[Love Waves]]
- [[Phase Velocity]]
- [[Group Velocity]]
- [[Wave Dispersion]]
- [[Surface Wave Modes]]
- [[Mode Superposition]]
- [[Geometric Dispersion]]
- [[Wavenumber]]
- [[Angular Frequency]]
- [[Fourier Integral]]
- [[Lamb's Problem]]

---

## Fuentes

- PDF: Sebastiano Foti Chapter 3 (book pages 121–200, secciones 3.1–3.5.2.5)
- Capítulo completado en esta iteración.
