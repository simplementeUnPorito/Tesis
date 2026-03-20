# Measurement of Surface Waves

## Introducción

Este capítulo aborda la teoría y práctica de la **adquisición de datos de [[Surface Waves|ondas superficiales]]**. La medición es un proceso experimental en el que se generan ondas superficiales y se observan sus efectos en el medio. El objetivo final es estimar los **parámetros de propagación** —principalmente la [[Phase Velocity|velocidad de fase]] en función de la frecuencia— que luego se usan para caracterizar el subsuelo.

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

#### El dominio de la frecuencia como eje central

A diferencia de la sísmica de refracción (que trabaja en tiempo–offset con primeras llegadas) o de la reflexión (que trabaja con reflexiones en tiempo), la adquisición de ondas superficiales opera fundamentalmente en el **dominio de la frecuencia**. La caracterización del subsuelo se realiza resolviendo un problema inverso (ver Capítulo 6) en el que las **propiedades de ondas de diferentes longitudes de onda** se asignan a parámetros del subsuelo a diferentes profundidades. Por eso, registrar y generar un rango amplio de longitudes de onda es crítico: cada longitud de onda "muestrea" una profundidad diferente.

#### El vínculo entre frecuencia, longitud de onda y profundidad

La longitud de onda depende de dos factores:

$$\lambda = \frac{V}{f}$$

donde $V$ es la velocidad de fase de la onda superficial y $f$ la frecuencia. La velocidad $V$ es función de las propiedades mecánicas del subsuelo — que son precisamente el objetivo del experimento y no pueden controlarse a priori. Por eso, el parámetro controlable es la **frecuencia**: **a menor frecuencia, mayor longitud de onda, mayor profundidad de investigación**.

Esta relación tiene una consecuencia práctica directa: para explorar hasta 30 m de profundidad (objetivo típico en $V_{S,30}$) se necesitan [[Rayleigh Waves|ondas de Rayleigh]] con longitudes de onda del orden de 30–60 m, lo que corresponde a frecuencias de 2–10 Hz para velocidades de corte típicas de suelos (~100–300 m/s). Estas frecuencias bajas exigen fuentes energéticas y geófonos de baja frecuencia natural.

#### Características físicas del registro

Las ondas superficiales son **eventos de baja velocidad** y altamente dispersivos. Esto tiene consecuencias concretas en el registro:

- **Duración del tren de ondas**: en medios dispersivos, las distintas componentes de frecuencia viajan a distintas velocidades y se separan espacialmente. El tren de onda puede durar varios segundos incluso a distancias relativamente cortas (< 100 m). Para capturar la dispersión completa, los registros deben ser suficientemente largos en tiempo.

- **Superposición con otros eventos**: no es posible generar exclusivamente ondas superficiales. Una fuente sísmica genera simultáneamente ondas P, ondas S y ondas superficiales. Las ondas de cuerpo llegan antes (mayor velocidad), pero las ondas superficiales dominan por amplitud: en registros de ingeniería activos, las ondas superficiales son los **eventos de mayor energía** y se identifican fácilmente por su alta amplitud, baja velocidad aparente y tren de onda prolongado.

- **Separación en frecuencia**: la identificación y separación de los diferentes eventos se realiza en el dominio f-k, donde cada tipo de onda ocupa una región característica del plano frecuencia–número de onda.

#### Requerimientos específicos de la medición

La medición de ondas superficiales requiere estimar con precisión las propiedades de propagación — principalmente la velocidad de fase como función de la frecuencia — sobre un rango amplio de frecuencias. Esto impone exigencias que no son intuitivas desde la experiencia con otras técnicas sísmicas:

- Los datos están contaminados por **ruido incoherente** (ambiental, electrónico) y **ruido coherente** (ondas de cuerpo, modos superiores, efectos de campo cercano). El diseño de la adquisición debe minimizar ambos.
- Las limitaciones del muestreo espacial y temporal afectan la **exactitud y el ancho de banda** de las propiedades estimadas — no solo la resolución espacial.
- La medición puede modelarse como un problema de **muestreo de señal multidimensional**: las restricciones del teorema de Nyquist–Shannon se aplican tanto en el dominio del tiempo como en el del espacio.

> **Por qué el dominio frecuencial es peculiar a las ondas superficiales**: en la sísmica de refracción, la información útil está en los tiempos de llegada de las primeras ondas. En la sísmica de reflexión, en los tiempos de reflexión de interfaces. En ondas superficiales, la información útil está en la **distribución de energía en el plano f-k** a lo largo de toda la duración del registro. Esto hace que las relaciones entre los dominios tiempo–frecuencia y espacio–número de onda sean **esenciales para entender las limitaciones de la adquisición** — lo que motiva la sección 3.3 sobre señales digitales.

*(Fuente: Foti Ch. 3, Sec. 3.1.2, pp. 125–126)*

---

## 3.2 The Wave Field as a Signal in Time and Space

### Naturaleza del campo de ondas

La propagación del campo de ondas en un medio continuo produce vibraciones: el movimiento de las partículas respecto a su posición de equilibrio. El campo de ondas completo puede describirse con una función 4D continua del espacio y el tiempo que representa, por ejemplo, la velocidad de partícula vectorial.

Para el caso relevante en la adquisición de ondas superficiales —ondas planas a lo largo de la superficie libre de un medio 1D— el campo se reduce a una **función 2D continua de distancia $x$ y tiempo $t$**:

$$s(x, t)$$

La Figura 3.3 (p. 127) ilustra esta función: en la vista superior se muestra una instantánea vertical del campo de deformación a tiempo constante; en la vista inferior, la componente vertical de la velocidad de partícula en función de offset y tiempo (la representación típica del sismograma multicanal). Una **traza sísmica** es el valor del campo en posición fija: $s(x_0, t)$; un corte a offset constante representa la velocidad de partícula de ese punto en el tiempo.

### Experimento ideal vs. experimento real

El experimento ideal generaría exclusivamente ondas superficiales en un entorno libre de ruido, registrando el campo de forma continua e infinita en espacio y tiempo, sin distorsión introducida por el sistema de adquisición. La señal ideal $\bar{s}(x,t)$ debería medirse sobre un rango amplio de frecuencias para capturar la dispersión completa.

En la práctica esto no es posible. Una fuente sísmica real genera un **campo de ondas de banda limitada** con múltiples tipos de ondas superpuestas (refractadas, reflejadas, ondas superficiales). La presencia de variaciones laterales, efectos de campo cercano y ruido ambiental afecta la naturaleza del campo propagante y debe considerarse en el diseño de la adquisición.

El campo medido es la suma de la señal deseada y el ruido:

$$w(x,t) = \bar{s}(x,t) + n(x,t) \tag{3.1}$$

La **cadena de medición** transforma la magnitud física (velocidad de partícula) en una traza sísmica digital mediante: transductor (geófono) → amplificación y acondicionamiento → digitalización → registro. Esta cadena introduce distorsión instrumental, ruido electrónico y muestreo discreto.

El dato efectivamente adquirido queda expresado como (Foti Ec. 3.2):

$$\text{data} = \text{sampling}\bigl(\text{instrument}(\bar{s} + n)\bigr) \tag{3.2}$$

La Figura 3.5 (p. 129) compara el experimento ideal (campo continuo de ondas superficiales puras) con el experimento real (muestreo espacialmente discreto, varios tipos de ruido, efectos de campo cercano visibles en los receptores próximos a la fuente).

### Rol del muestreo espacial

En los métodos de ondas superficiales, el **muestreo en espacio** es incluso más crítico que el muestreo en tiempo. El efecto de la propagación de ondas es detectado por un número finito de receptores: el campo se registra en un conjunto finito y discreto de puntos en tiempo y espacio. Las limitaciones del muestreo espacial y temporal se suman al ruido físico y determinan qué información útil puede extraerse del dato.

> **Implicación para la tesis**: el geófono no registra el campo continuo, sino su versión muestreada, filtrada por el instrumento y contaminada por ruido. La resolución en frecuencia y en número de onda del dato experimental es siempre limitada. Entender estas limitaciones es previo a cualquier interpretación de la curva de dispersión.

*(Fuente: Foti Ch. 3, Sec. 3.2, p. 126–129, Ecs. 3.1–3.2)*

---

## 3.3 Acquisition of Digital Seismic Signals

### 3.3.1 Análisis espectral y transformadas de campo de ondas

El concepto de **frecuencia** es intuitivo para procesos cíclicos: indica el número de ocurrencias de un evento por unidad de tiempo. Para una señal armónica, la frecuencia es el inverso de la duración de un ciclo (el período). Las señales no cíclicas pueden descomponerse en suma de funciones cíclicas simples — esta es la idea central del análisis espectral.

La Figura 3.6 (p. 130) ilustra este principio: una señal no periódica genérica (Fig. 3.6a) puede representarse exactamente como la suma de funciones cíclicas de distintas frecuencias, amplitudes y fases (Fig. 3.6b). La serie de amplitudes y fases de esas funciones elementales es la **representación en el dominio de la frecuencia** de la señal, también llamada su **espectro**, y consiste en un espectro de amplitudes (Fig. 3.6c) y un espectro de fases (Fig. 3.6d).

El **análisis espectral** es el proceso de encontrar la amplitud y la fase de las componentes cíclicas elementales de una señal. La Figura 3.7 (p. 131) muestra dos trazas sísmicas reales con diferente contenido espectral: la traza de la izquierda tiene mayor energía en frecuencias bajas, mientras que la de la derecha tiene componentes de mayor frecuencia más prominentes. Esta diferencia es inmediatamente visible en sus espectros de amplitud.

Los operadores matemáticos que realizan esta descomposición se denominan **transformadas integrales**. Mapean entre dos dominios complementarios:

| Dominio original | Dominio transformado | Variable transformada |
|---|---|---|
| Tiempo $t$ | Frecuencia $f$ | Ciclos por segundo [Hz] |
| Espacio $x$ | Número de onda $k$ | Ciclos por metro [1/m] |

Esta dualidad tiempo–frecuencia y espacio–número de onda es fundamental en el análisis de ondas superficiales porque:
- La **velocidad de fase** se estima directamente como la razón $c = f/k$ en el dominio transformado 2D
- La distribución de energía en el plano $f$–$k$ revela los modos de propagación y sus velocidades
- Las limitaciones del muestreo en tiempo y espacio se traducen directamente en resolución en frecuencia y en número de onda

> **Por qué el dominio frecuencial es el dominio natural de las ondas superficiales**: a diferencia de los métodos de refracción (que trabajan en tiempo–offset), los métodos de ondas superficiales trabajan en el dominio frecuencia–número de onda porque la propiedad que se estima (velocidad de fase) es inherentemente frecuencia-dependiente. La caracterización del subsuelo require estimar la [[Dispersion Relation|curva de dispersión]] $c(f)$, que es justamente la relación entre $f$ y $k$.

*(Fuente: Foti Ch. 3, Sec. 3.3.1, p. 130–131)*

### 3.3.2 Transformada de Fourier y sus propiedades

#### De la serie de Fourier a la transformada

La **serie de Fourier** establece que cualquier señal **periódica** de período $T$ puede descomponerse exactamente en una suma infinita de funciones armónicas (senos o cosenos):

$$
g(t) = \sum_{n=-\infty}^{+\infty} A_n \, e^{j 2\pi f_n t}, \qquad f_n = \frac{n}{T}
$$

donde $A_n$ es la amplitud compleja (que codifica amplitud y fase) del $n$-ésimo armónico. El espectro de frecuencias es **discreto**: solo están presentes las frecuencias $f_n = n/T$, múltiplos enteros de la frecuencia fundamental $1/T$.

La **transformada de Fourier** es la extensión al caso de señales no periódicas: cuando el período $T \to \infty$, las frecuencias discretas se convierten en un continuo, y la suma discreta se convierte en una integral. El resultado es la **transformada de Fourier** (Foti Ec. 3.3):

$$
G(f) = \int_{-\infty}^{+\infty} g(t)\,e^{-j2\pi ft}\,dt \tag{3.3}
$$

$G(f)$ es la **representación en el dominio de la frecuencia** de la señal: asigna una amplitud compleja (módulo = amplitud, argumento = fase) a cada frecuencia $f$. La señal original se recupera sin pérdida mediante la transformada inversa (Foti Ec. 3.4):

$$
g(t) = \int_{-\infty}^{+\infty} G(f)\,e^{+j2\pi ft}\,df \tag{3.4}
$$

El par $(g, G)$ recibe el nombre de **par de Fourier** y se denota $g(t) \xleftrightarrow{F} G(f)$ (Foti Ec. 3.5). Las dos representaciones son **complementarias**: contienen exactamente la misma información sobre la señal, solo organizada de diferente manera.

#### Transformada en el dominio espacial: el número de onda

El mismo concepto se aplica cuando la variable independiente es el **espacio** $x$ en lugar del tiempo $t$. La variable dual del espacio es el **número de onda** $k$ (ciclos por metro), y la transformada de Fourier espacial es (Foti Ec. 3.6):

$$
g(x) \xleftrightarrow{F} G(k) \tag{3.6}
$$

El número de onda $k$ es el análogo espacial de la frecuencia temporal: mide cuántos ciclos por unidad de distancia contiene la señal. En muchos textos se usa el **número de onda circular** $\kappa = 2\pi k$ (radianes por metro), análogo a $\omega = 2\pi f$.

> **Por qué esto importa para ondas superficiales**: la velocidad de fase de una onda es $c = f/k$. Al aplicar la transformada de Fourier 2D (espacio + tiempo) a un sismograma multicanal, cada modo de propagación aparece como un punto (o pico) en el plano $f$–$k$ con coordenadas $(f_0, k_0)$. La velocidad de fase se lee directamente como la pendiente $c = f_0/k_0$ de la recta que une ese punto con el origen.

#### Propiedades fundamentales de la transformada de Fourier (Sec. 3.3.2.1)

Las propiedades siguientes son esenciales para entender cómo el muestreo y la ventana afectan al espectro:

**Linealidad** (Ecs. 3.7–3.8): la transformada de una combinación lineal es la misma combinación lineal de las transformadas:
$$a\,g(t) \xleftrightarrow{F} a\,G(f), \qquad g(t)+h(t) \xleftrightarrow{F} G(f)+H(f)$$

**Escalamiento** (Ec. 3.9): si la señal se comprime en tiempo por un factor $s$, su espectro se estira en frecuencia por el mismo factor (y viceversa):
$$g(t/s) \xleftrightarrow{F} s\,G(s \cdot f) \tag{3.9}$$
Esta propiedad implica que señales cortas (impulsivas) tienen espectros anchos, y señales largas tienen espectros estrechos.

**Desplazamiento temporal** (Ec. 3.10): retrasar una señal por $t_0$ no cambia su amplitud espectral, pero introduce una **fase lineal** proporcional a la frecuencia:
$$g(t - t_0) \xleftrightarrow{F} e^{-j2\pi f t_0}\,G(f) \tag{3.10}$$
En el análisis de ondas superficiales, el tiempo de arribo de una onda a cada geófono produce una diferencia de fase en el espectro cruzado entre trazas. Esta diferencia de fase es la base de la estimación de velocidad de fase.

**Convolución** (Ecs. 3.11–3.12): la convolución de dos señales en tiempo equivale a la **multiplicación** de sus espectros en frecuencia, y la multiplicación en tiempo equivale a la convolución en frecuencia:
$$g(t) * h(t) \xleftrightarrow{F} G(f) \cdot H(f) \tag{3.12a}$$
$$g(t) \cdot h(t) \xleftrightarrow{F} G(f) * H(f) \tag{3.12b}$$

Esta propiedad, el **teorema de la convolución**, es el puente que conecta el muestreo (multiplicación en tiempo) con el aliasing (convolución en frecuencia), y la ventana temporal (multiplicación) con el spectral leakage (convolución con una sinc). Sin entender el teorema de convolución, no puede entenderse por qué el muestreo finito degrada el espectro de la manera que lo hace.

> **Implicación para la tesis**: el análisis f-k de sismogramas de geófonos depende enteramente de estas propiedades. La conversión de una traza en su espectro (Ec. 3.3), la relación entre apertura del arreglo y resolución espectral (Ec. 3.9), y el efecto de la ventana temporal sobre el leakage (Ec. 3.12b) son todos consecuencia directa de las propiedades de la transformada de Fourier. El dominio f-k es el espacio donde la [[Dispersion Relation|curva de dispersión]] de las [[Rayleigh Waves|ondas de Rayleigh]] se hace visible como un patrón de energía cuya pendiente revela la velocidad de fase.

*(Fuente: Foti Ch. 3, Sec. 3.3.2–3.3.2.1, pp. 131–134, Ecs. 3.3–3.12)*

### 3.3.3 Muestreo, criterio de Nyquist y aliasing

#### El proceso de muestreo

La adquisición digital de señales involucra una conversión analógico-digital: la señal continua se reemplaza por una **serie discreta de valores a intervalos de tiempo fijos** $\Delta t$. La frecuencia de muestreo es $F_s = 1/\Delta t$.

Matemáticamente, el muestreo equivale a la **multiplicación** de la señal continua $y(t)$ por una función *comb*: una sucesión infinita de impulsos de Dirac regularmente espaciados por $\Delta t$. El espectro de la señal muestreada es entonces la **convolución** del espectro original con el espectro de la comb (Foti Ec. 3.13):

$$F(\text{comb} \cdot y) = F(\text{comb}) * F(y) \tag{3.13}$$

El resultado es que el espectro de la señal muestreada es una **repetición periódica** del espectro original, con período igual a $F_s$ (Figura 3.9, p. 135). Las réplicas están centradas en los múltiplos de $F_s$.

#### Frecuencia de Nyquist y el teorema de Nyquist–Shannon

Las réplicas del espectro **no se superponen** siempre que la frecuencia máxima del contenido de la señal $f_{\max}$ sea menor que la mitad de la frecuencia de muestreo (Figura 3.10a, p. 136). La **frecuencia de Nyquist** es el umbral máximo observable en la señal muestreada:

$$F_{Nyq} = \frac{F_s}{2}$$

El **teorema de Nyquist–Shannon** establece que no se pierde información si (Foti Ec. 3.14):

$$F_s > 2 f_{\max} \tag{3.14}$$

Es decir: la frecuencia de muestreo debe ser al menos el doble de la frecuencia máxima del contenido espectral de la señal.

#### Aliasing: consecuencias de muestreo insuficiente

Si $f_{\max} > F_s/2$, las réplicas espectrales se superponen (Figura 3.10b, p. 136). En este caso el espectro original **no puede recuperarse**: las componentes de alta frecuencia que exceden $F_{Nyq}$ aparecen en el espectro como **componentes ficticias a frecuencias menores** — este error se denomina **aliasing** (Figura 3.11, p. 137).

El aliasing genera distorsiones y artefactos irreversibles en la señal reconstruida. Un ejemplo cotidiano: las ruedas de los automóviles en películas aparecen girando en sentido contrario cuando la frecuencia de rotación supera la de muestreo del video.

#### Protección contra aliasing en la práctica

- **Filtros antialiasing por hardware** (analógicos, previos a la digitalización): eliminan todas las componentes de frecuencia superior a $F_{Nyq}$ antes de convertir la señal. Son la solución más eficaz porque actúan sobre la señal analógica real.
- **Filtros digitales + sobremuestreo** (*software antialiasing*): muestrear a frecuencia mayor que la necesaria y luego aplicar filtro digital para eliminar las réplicas. Requiere mayor capacidad de almacenamiento.
- Para la **dimensión espacial** (muestreo del array), la protección equivalente es el sobremuestreo espacial o el uso de arrays de receptores analógicos combinados en una sola traza.

#### Aliasing espacial en arreglos de geófonos

El mismo mecanismo se aplica al **muestreo espacial** del array: el espaciado $\Delta X$ entre geófonos define el número de onda de Nyquist:

$$k_{Nyq} = \frac{1}{2\Delta X}$$

Las ondas con $k > k_{Nyq}$ (velocidades de fase muy bajas) aparecen como componentes ficticias de número de onda negativo. En arreglos *end-off*, esta información aliasada puede recuperarse extendiendo el análisis al cuadrante negativo del dominio f-k, aumentando el número de onda máximo efectivo a $2k_{Nyq}$.

> **Regla práctica para MASW**: el espaciado entre geófonos debe ser menor que la mitad de la longitud de onda mínima de interés: $\Delta X < \lambda_{min}/2$. Para frecuencias altas (alta resolución superficial) se requieren espaciados más pequeños; para profundidades mayores se pueden usar espaciados más grandes.

*(Fuente: Foti Ch. 3, Sec. 3.3.3–3.3.4, p. 134–137, Ecs. 3.13–3.14, Figs. 3.8–3.11)*

### 3.3.5 Ventaneo y *spectral leakage*

#### Principio físico

Las secciones anteriores tratan las señales como si fueran de duración infinita. En la realidad, cualquier señal adquirida está limitada a un intervalo finito de tiempo. Este truncamiento puede describirse formalmente como la **multiplicación** de la señal infinita por una **función de ventana** (*window function*), que vale 1 dentro del intervalo de adquisición y 0 fuera de él.

La ventana rectangular más simple (*boxcar*) se define como (Foti Ec. 3.15–3.16):

$$z(t) = w(t) \cdot s(t)$$

$$w(t) = \begin{cases} 1 & -T/2 < t < T/2 \\ 0 & \text{en otro caso} \end{cases}$$

donde $T$ es la duración del registro.

#### Efecto en el espectro: *spectral leakage*

Por la propiedad de convolución de la transformada de Fourier, la **multiplicación en el tiempo** equivale a la **convolución en el dominio de la frecuencia**:

$$Z(f) = W(f) * S(f)$$

La transformada de la ventana boxcar es una función sinc. Esto tiene dos consecuencias directas (Figura 3.12, pp. 138–139):

1. **Lóbulo principal de ancho finito**: la resolución espectral queda limitada a $\Delta f \approx 1/T$. Dos frecuencias separadas por menos de $1/T$ no pueden distinguirse.
2. **Lóbulos laterales** (*side lobes*): el espectro de la ventana boxcar tiene lóbulos que decaen lentamente. Su efecto es que la energía de una componente real "se derrama" hacia las frecuencias vecinas — este fenómeno se llama **spectral leakage**.

El leakage tiene dos consecuencias prácticas graves (Figura 3.13, p. 140):
- **Enmascaramiento de modos débiles**: un modo de alta amplitud puede esconder un modo de baja amplitud próximo en frecuencia mediante sus lóbulos laterales.
- **Imposibilidad de resolver modos cercanos**: dos eventos con amplitudes similares y pequeña diferencia de frecuencia (o número de onda) no pueden separarse cuando sus lóbulos principales se superponen.

#### Ventanas suavizadas

Para reducir los lóbulos laterales se usan ventanas con transición suave de 0 a 1, como las ventanas de **Hanning** o **Hamming**. Su espectro tiene lóbulos laterales mucho menores, lo que aumenta el rango dinámico (capacidad de detectar modos débiles junto a modos fuertes). El costo es una ligera pérdida de resolución espectral (lóbulo principal algo más ancho).

#### Extensión al dominio espacial: apertura del arreglo

El concepto de ventana se aplica directamente al **dominio espacial**: la longitud observada es la **apertura del arreglo** $D = N \cdot \Delta X$. La ventana espacial tiene el mismo efecto en el dominio del número de onda:

$$\Delta k = \frac{2\pi}{D}$$

- Mayor apertura $D$ → mayor resolución en número de onda → mayor capacidad de separar modos con valores de $k$ cercanos.
- Apertura insuficiente → los modos se superponen en el espacio f-k → la curva de dispersión extraída es una "curva aparente" que mezcla contribuciones de varios modos.

> **Implicación crítica para la tesis**: la resolución modal en la estimación de la [[Dispersion Relation|curva de dispersión]] está directamente controlada por la apertura del arreglo de geófonos. Para sitios donde los [[Surface Wave Modes|modos superiores]] son relevantes (inversión de velocidad en subsuelo), la apertura insuficiente es la principal fuente de error en el perfil $V_S(z)$. Este es uno de los criterios de diseño más importantes en ensayos MASW.

*(Fuente: Foti Ch. 3, Sec. 3.3.5, p. 137–140, Ecs. 3.15–3.16, Figs. 3.12–3.13)*

### 3.3.6 Cuantización y conversión analógico-digital

#### El problema fundamental de la cuantización

La conversión analógico-digital involucra dos operaciones distintas: el **muestreo** (discretización en tiempo) y la **cuantización** (discretización en amplitud). Mientras el muestreo se abordó en la sección anterior, la cuantización introduce un tipo diferente de limitación.

Una señal física real puede asumir, entre su valor máximo y mínimo, cualquier valor real — es decir, un conjunto infinito de valores posibles. El dato digital, en cambio, tiene un número **finito** de niveles discretos. El valor verdadero debe redondearse o truncarse al nivel más cercano. Esta diferencia irreducible entre la señal continua y su representación digital constituye el **error de cuantización** (o distorsión de cuantización).

#### Resolución y rango dinámico

La resolución del convertidor se expresa en **bits** ($Q$): un convertidor de $Q$ bits puede representar $2^Q$ niveles distintos dentro del rango de entrada. La relación entre resolución y rango dinámico es:

$$\text{Rango dinámico [dB]} = 20\log_{10}(2^Q) \approx 6.02 \times Q$$

Los convertidores de sistemas sísmicos modernos tienen típicamente entre **16 y 24 bits**:

| Resolución (bits) | Niveles ($2^Q$) | Rango dinámico (dB) |
|---|---|---|
| 16 | 65 536 | 96 dB |
| 20 | 1 048 576 | 120 dB |
| 24 | 16 777 216 | 144 dB |

El **LSB** (*Least Significant Bit*) es el voltaje mínimo que produce un cambio en la salida digital:

$$\text{LSB} = \frac{\text{Rango completo}}{2^Q}$$

#### Error de cuantización como ruido estadístico

Cuando la señal tiene amplitud mucho mayor que el LSB (caso habitual en señales sísmicas bien ajustadas al rango del convertidor), el error de cuantización se comporta como **ruido no correlacionado con la señal**, con distribución uniforme entre $-\text{LSB}/2$ y $+\text{LSB}/2$. El valor RMS del ruido de cuantización es (Foti p. 141):

$$\sigma_q = \frac{\text{LSB}}{\sqrt{12}}$$

La **Fig. 3.14** (p. 141) ilustra una conversión de 4 bits: la parte superior muestra la señal escalada y su versión digitalizada en escalera; la parte inferior muestra el error de cuantización, que oscila dentro de $\pm\text{LSB}/2$ y crece relativamente en las regiones de baja amplitud.

#### Implicación práctica

El rango dinámico del convertidor debe ser suficiente para capturar tanto los eventos de pequeña amplitud (reflexiones débiles, modos superiores de ondas superficiales) como los de gran amplitud (ondas superficiales dominantes a offsets cortos) sin saturación ni excesivo error de cuantización. Para este motivo, los sistemas sísmicos usan 24 bits: la diferencia de amplitud entre la onda superficial directa y un reflector profundo puede superar 100 dB.

> **Para la tesis**: al seleccionar el sistema de adquisición, la resolución del ADC determina la capacidad de capturar modos de pequeña amplitud que de otro modo quedarían sumergidos en el ruido de cuantización. En sistemas de bajo costo (como los basados en geófonos MEMS o tarjetas de audio), la resolución del ADC es una limitación real que afecta el rango de frecuencias y la detección de modos superiores.

*(Fuente: Foti Ch. 3, Sec. 3.3.6, pp. 140–141, Fig. 3.14)*

### 3.3.7 Señales 2D y la transformada f-k

#### Naturaleza 2D de los datos sísmicos

Los datos sísmicos de un arreglo lineal son señales **bidimensionales**: el campo de ondas se representa como $s(x,t)$, donde $x$ es el offset y $t$ el tiempo. Para analizar este dato es necesario extender el análisis espectral al dominio 2D.

La **transformada de Fourier 2D** (transformada **f-k**) aplica simultáneamente una transformada temporal y una espacial (Foti Ec. 3.17):

$$G(f,k) = \int_{-\infty}^{+\infty}\int_{-\infty}^{+\infty} g(t,x)\,e^{-j2\pi(ft+kx)}\,dx\,dt \tag{3.17}$$

La transformada inversa recupera el dato original (Foti Ec. 3.18):

$$g(t,x) = \int_{-\infty}^{+\infty}\int_{-\infty}^{+\infty} G(f,k)\,e^{j2\pi(ft+kx)}\,dk\,df \tag{3.18}$$

Las variables conjugadas son $t \leftrightarrow f$ y $x \leftrightarrow k$. El plano $f$–$k$ es el **dominio natural para el análisis de ondas superficiales**: la [[Phase Velocity|velocidad de fase]] de un modo es la razón $c = f/k$, que en f-k corresponde a la pendiente de la línea que une el origen con el pico espectral de ese modo.

#### Onda plana armónica en f-k: el caso ideal

Una onda plana armónica unitaria con número de onda circular $k_0$ y frecuencia angular $\omega_0$ se escribe (Foti Ec. 3.19):

$$s(x,t) = e^{i(\omega_0 t - k_0 x)} \tag{3.19}$$

Su espectro f-k ideal es (Foti Ec. 3.20):

$$S(k,\omega) = 4\pi^2\,\delta(k - k_0)\,\delta(\omega - \omega_0) \tag{3.20}$$

Un **impulso de Dirac** perfectamente localizado en $(k_0, \omega_0)$ del plano f-k (Figura 3.15, p. 143). En muestreo ideal e infinito, la onda plana aparece como un punto exacto: no hay ambigüedad en su velocidad de fase.

#### Efecto del muestreo temporal finito

Con registro de duración finita $T$ (ventana boxcar $u(t)$), la señal muestreada es $z(x,t) = u(t)\,s(x,t)$. Su espectro f-k resulta (Foti Ec. 3.21–3.22):

$$Z(k,\omega) = 2\pi|T|\,\delta(k - k_0)\,\text{sinc}\!\left[\frac{T}{2}(\omega - \omega_0)\right] \tag{3.22}$$

La delta de Dirac en frecuencia queda **reemplazada por una sinc**: el pico tiene ancho finito $\Delta\omega_{Rayleigh} = 2\pi/T$ con lóbulos laterales en la dimensión de frecuencia (Figura 3.16, p. 145). La resolución en frecuencia queda limitada a $\Delta f \approx 1/T$.

#### Muestreo espacio-temporal finito: ventana 2D

Cuando el campo se muestrea con apertura $D$ (ventana espacial $v(x)$) y duración $T$, la ventana 2D combinada es (Foti Ec. 3.27):

$$w(x,t) = u(t)\,v(x) \tag{3.27}$$

El espectro del campo muestreado resulta (Foti Ecs. 3.28–3.29):

$$Z(k,\omega) = W(k,\omega) * S(k,\omega) \tag{3.28}$$

donde $W(k,\omega)$ es la transformada 2D de la ventana. Para ventana boxcar 2D y una onda plana (Foti Ec. 3.25–3.26):

$$Z(k,\omega) = |D||T|\,\text{sinc}\!\left[\frac{D}{2}(k - k_0)\right]\text{sinc}\!\left[\frac{T}{2}(\omega - \omega_0)\right] \tag{3.26}$$

El resultado es un **producto de dos sinc**: la resolución en número de onda es $\Delta k_{Rayleigh} = 2\pi/D$ y la resolución en frecuencia es $\Delta f \approx 1/T$. La Figura 3.17 (p. 146) muestra la superficie espectral 3D: el pico ideal se convierte en un lóbulo principal 2D con lóbulos laterales en ambas dimensiones. La resolución y el *leakage* presentados en las secciones anteriores se aplican directamente al dominio 2D en ambas dimensiones simultáneamente.

#### Consecuencias para la resolución multimodal (Figura 3.18)

La limitación más crítica en la práctica ocurre con **múltiples modos** con diferentes $k_1$ y $k_2$. La Figura 3.18 (p. 147) ilustra cuatro casos para dos modos de Rayleigh de igual amplitud:

- **Fig. 3.18a**: diferencia $|k_1 - k_2|$ suficientemente grande → lóbulos principales no se superponen → **ambos modos resueltos correctamente**.
- **Fig. 3.18b**: diferencia menor → lóbulos se aproximan pero los picos individuales aún se distinguen.
- **Fig. 3.18c**: diferencia aún menor → lóbulos se superponen → el espectro muestra un único pico "aparente" entre los dos modos verdaderos → la curva de dispersión extraída es una **curva aparente** que no corresponde a ningún modo real.
- **Fig. 3.18d**: misma separación modal que (c) pero **apertura doble** → resolución mejorada → ambos modos correctamente resueltos.

La conclusión es inequívoca (Foti p. 148): *"to accurately measure multiple surface wave modes, the spatial sampling aperture has to provide sufficient wavenumber resolution to distinguish between modes."*

> **Implicación para la tesis**: en sitios con inversión de velocidad o modos superiores relevantes, una apertura insuficiente produce una curva de dispersión aparente que mezcla modos y genera perfiles $V_S(z)$ erróneos. Este análisis justifica cuantitativamente el criterio de diseño en ensayos [[MASW Method|MASW]]: la longitud del arreglo no es solo un parámetro logístico, sino el factor determinante de la resolución modal. La condición exacta es $D > 2\pi / |k_1 - k_2|$.

*(Fuente: Foti Ch. 3, Sec. 3.3.7, p. 141–148, Ecs. 3.17–3.29, Figs. 3.15–3.18)*

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

- **[[Body Waves|Ondas de cuerpo]]** (P y S): llegan antes o simultáneamente con las ondas superficiales. En aplicaciones de pequeña escala suelen tener menor amplitud. Pueden identificarse en tiempo-offset y eliminarse o ignorarse.
- **Modos superiores** de propagación: en sitios inversamente dispersivos pueden dominar la respuesta. Si el modelo solo considera el modo fundamental, los modos superiores son ruido coherente. La solución correcta es incluirlos en el modelo (inversión multimodal).
- **[[Near-field Effect|Efecto de campo cercano]]** (*near-field effect*): las [[Rayleigh Waves|Rayleigh waves]] solo se comportan como ondas planas más allá de cierta distancia de la fuente. Dentro de esa zona, el campo está dominado por contribuciones de ondas de cuerpo y la velocidad aparente no corresponde a la del modo fundamental.
- **Air blast**: la onda de presión acústica en el aire (velocidad ~331–360 m/s) puede ser detectada por los geófonos. Aparece en el dominio f-k como un evento lineal de velocidad constante.
- **Variaciones laterales**: heterogeneidades subsuperficiales hacen que las ondas superficiales no sigan el modelo de propagación plana 1D, generando difracción y distorsión de la velocidad aparente.

*(Fuente: Foti Ch. 3, Sec. 3.4.1.3–3.4.1.6, p. 158–160)*

---

### 3.4.1.7 Variaciones laterales

El procesamiento asume un modelo 1D: la propagación es lateralmente homogénea. Las variaciones laterales del subsuelo producen efectos que no pueden modelarse correctamente y deben considerarse ruido coherente.

Implicaciones prácticas:
- Evitar ubicar el arreglo en zonas con discontinuidades litológicas conocidas o capas buzantes.
- Arrays más cortos reducen el riesgo de variaciones laterales pero también la resolución espectral (trade-off apertura vs. homogeneidad lateral).
- Las variaciones laterales pueden identificarse comparando curvas de dispersión extraídas de diferentes segmentos del arreglo.

*(Fuente: Foti Ch. 3, Sec. 3.4.1.7, p. 162)*

### 3.4.1.8 Modos superiores

La propagación de ondas superficiales es inherentemente multimodal. En sitios inversamente dispersivos, los [[Surface Wave Modes|modos superiores]] pueden dominar la respuesta sobre el modo fundamental. Los modos superiores deben considerarse **información útil**, no ruido, a menos que el sistema de adquisición o inversión no pueda manejarlos.

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

La [[Dispersion Relation|curva de dispersión]] experimental es siempre una **curva aparente** que depende de los parámetros de adquisición, no solo de las propiedades del subsuelo.

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

El método [[SASW Method|SASW]] (*Spectral Analysis of Surface Waves*) es un caso especial con solo dos receptores. Su ventaja es la simplicidad logística; su limitación es la mayor vulnerabilidad al aliasing espacial y a la superposición de modos.

Para cubrir un rango amplio de frecuencias, se repite la medición con diferentes espaciados (short → alta frecuencia; long → baja frecuencia), usando el esquema de punto medio común (*common midpoint*) para mejorar la representatividad.

*(Fuente: Foti Ch. 3, Sec. 3.4.3.2, p. 178–179)*

#### 3.4.3.3 Métodos pasivos

##### El ruido sísmico ambiental como fuente

El ruido sísmico ambiental (*microtremors*) es un campo de ondas de fondo generado por una multitud de fuentes naturales y antropogénicas que actúan en los alrededores del sitio (Bonnefoy-Claudet et al. 2006). Dependiendo del rango de frecuencias:

- **Baja frecuencia (< 1 Hz)**: las fuentes son de origen natural, principalmente relacionadas con eventos geofísicos globales y, en particular, con las olas oceánicas que generan ondas sísmicas de largo período.
- **Alta frecuencia (> 1 Hz)**: las fuentes son predominantemente de origen humano — tráfico vehicular, actividad industrial, maquinaria. Incluso en áreas remotas y silenciosas, los elementos atmosféricos pueden dominar el campo de fondo a estas frecuencias.

Para aplicaciones superficiales, el componente de interés es el **microtremor de período corto** ($T < 1\,\text{s}$, $f > 1\,\text{Hz}$). El campo de microtremores está dominado por **componentes de ondas superficiales** ([[Rayleigh Waves|Rayleigh]] y [[Love Waves|Love]]), con contribuciones limitadas de ondas de cuerpo — esta característica es precisamente lo que hace que el ruido ambiental sea útil para sísmica de ondas superficiales.

##### Por qué usar métodos pasivos

En sitios urbanos o industriales, el ruido sísmico de fondo que degrada los datos activos puede verse, paradójicamente, como **señal** para el método pasivo. Las ventajas específicas son:

1. **Bajas frecuencias accesibles**: a baja frecuencia, el ruido ambiental puede generar ondas superficiales de mayor amplitud que las que producen fuentes impulsivas ligeras (sledgehammer). Esto permite investigar mayores profundidades sin necesidad de fuentes energéticas pesadas.
2. **Sitios con alta vibración ambiental**: en zonas urbanas con mucho tráfico, el ruido es tan intenso que las fuentes activas quedan oscurecidas — pero el método pasivo explota ese mismo ruido.
3. **Combinación activa + pasiva**: la estrategia más eficaz es combinar datos activos (alta frecuencia → resolución superficial) con datos pasivos (baja frecuencia → profundidad mayor), extendiendo así el rango de la curva de dispersión. Ejemplos concretos se muestran en el Capítulo 7.

##### Diferencias fundamentales respecto a la adquisición activa

La posición de la fuente en métodos pasivos es **desconocida y variable durante la adquisición**, lo que impide aplicar directamente las técnicas de análisis diseñadas para fuentes activas. La diferencia clave es que la fuente genera un **vector número de onda** $\mathbf{k}$ con componentes $(k_x, k_y)$. Un arreglo lineal solo detecta la proyección de $\mathbf{k}$ a lo largo del eje del arreglo, obteniendo una **velocidad aparente** que no es en general la velocidad de fase real de la onda. Para estimar correctamente la velocidad de fase se necesita conocer la dirección de propagación, lo que requiere un **arreglo 2D**.

##### Diseño del arreglo para datos pasivos

Se prefieren arreglos bidimensionales que permitan estimar el vector $\mathbf{k}$ completo. Parámetros de diseño:

- **Apertura total** (diámetro del array): controla la máxima longitud de onda detectada → máxima profundidad. Se recomienda una apertura de 1/3 a 1 vez la máxima longitud de onda de interés (Tokimatsu 1995; Asten y Henstridge 1984).
- **Espaciado entre receptores**: debe ser menor que la mitad de la mínima longitud de onda (criterio antialiasing), igual que en datos activos.

Configuraciones de array típicas en la práctica (**Fig. 3.44**, p. 181): L, T, cruz, cuadrado, círculo, triángulo equilátero simple y anidado, cuadrícula hexagonal y rectangular. La elección depende del método de procesamiento:
- Para métodos de [[SPAC Method|SPAC]]/ESAC: el **triángulo con triángulos equiláteros anidados** da buenos resultados con un número limitado de geófonos.
- Para métodos tipo beamformer o f-k 2D: las distribuciones irregulares pero con buena cobertura azimutal son preferidas.

##### Adquisición: registro de ruido ambiental

El proceso de adquisición es fundamentalmente diferente del activo: no hay un momento de disparo. Se registra el campo de ondas de fondo durante un tiempo suficientemente largo para obtener múltiples segmentos de datos estadísticamente estacionarios. En la práctica se requieren múltiples ventanas de 30 s o 1 minuto. Los parámetros de adquisición (frecuencia de muestreo, longitud del registro) se determinan en función de la frecuencia máxima de interés y de la resolución frecuencial deseada.

##### El caso especial de arrays lineales: ReMi

Por razones logísticas, hay interés en usar arreglos lineales también para mediciones pasivas, ya que permiten usar el mismo tendido del ensayo MASW activo. El método [[ReMi Method|ReMi]] (*Refraction Microtremor*) adopta esta estrategia. Bajo la hipótesis de que el campo de ruido es uniforme e isótropo (fuentes distribuidas en todas las direcciones con igual probabilidad), puede demostrarse que el array lineal sí detecta el número de onda real de las ondas superficiales (Sec. 4.6.3).

Sin embargo, las **limitaciones del array lineal para datos pasivos son severas**: solo puede identificar la proyección del número de onda a lo largo del eje del array. Si el campo no es isótropo (lo que ocurre frecuentemente en zonas urbanas con fuentes direccionales dominantes), los resultados pueden ser erróneos. El método ReMi tiene ventajas logísticas importantes pero debe aplicarse con cautela y verificar la hipótesis de isotropía.

*(Fuente: Foti Ch. 3, Sec. 3.4.3.3, pp. 179–181, Fig. 3.44)*

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
- Geófonos verticales: capturan la componente vertical del movimiento → sensibles a [[Rayleigh Waves|Rayleigh waves]].
- Geófonos horizontales transversales: sensibles a [[Love Waves|Love waves]].

La sensibilidad de fase del geófono introduce incertidumbre en la velocidad estimada. En mediciones de dos estaciones (SASW), este efecto puede ser crítico. En arrays multicanal el efecto es mitigado si todos los receptores son idénticos.

*(Fuente: Foti Ch. 3, Sec. 3.5.2.1, p. 193–197)*

#### Acelerómetros y MEMS

Los acelerómetros son útiles en aplicaciones de alta frecuencia (ensayos de pavimentos, NDT). Los sensores MEMS permiten alta frecuencia, bajo ruido y grabación hasta DC (aceleración estática). Están siendo adoptados progresivamente para aplicaciones de baja frecuencia.

*(Fuente: Foti Ch. 3, Sec. 3.5.2.2, p. 197–198)*

#### Acoplamiento y receptores de dos componentes

El acoplamiento receptor–suelo es fundamental. Los receptores se plantan con espiga de acero o se entierran para maximizar el contacto. Los land streamers ofrecen ventajas logísticas pero menor calidad de acoplamiento.

Los receptores de dos componentes (vertical + horizontal radial) permiten medir la polarización elíptica de las [[Rayleigh Waves|Rayleigh waves]] y separar [[Surface Wave Modes|modos]]. Son útiles para inversión conjunta o aplicaciones de caracterización avanzada.

*(Fuente: Foti Ch. 3, Sec. 3.5.2.3–3.5.2.4, p. 198–199)*

---

## Síntesis del capítulo

El flujo de trabajo completo de adquisición de ondas superficiales involucra:

1. **Diseño del arreglo**: espaciado $\Delta X$ (controla $k_{max}$), apertura $D$ (controla resolución modal), offset de fuente (controla campo cercano), duración de registro (controla resolución en frecuencia).

2. **Fuente**: generar suficiente energía a baja frecuencia para la profundidad objetivo. Sledgehammer para aplicaciones de ingeniería (<100 m); fuentes más energéticas para mayor profundidad.

3. **Receptores**: geófonos verticales de baja frecuencia natural (1–4.5 Hz) para capturar [[Rayleigh Waves|Rayleigh waves]] sobre un rango amplio de frecuencias.

4. **Control de ruido**: maximizar SNR (stacking, adquisición nocturna), identificar y mitigar ruido coherente (campo cercano, modos superiores, variaciones laterales).

La limitación fundamental es que la **[[Dispersion Relation|curva de dispersión]] experimental es siempre una curva aparente**: depende de los parámetros de adquisición, no solo del subsuelo. El proceso de [[Inversión|inversión]] debe tener esto en cuenta. Este capítulo es la base del flujo de trabajo del método [[MASW Method|MASW]] y sus variantes.

---

## Fuentes

- PDF: Sebastiano Foti Chapter 3 (book pages 121–200, secciones 3.1–3.5.2.5)
- Capítulo completado en esta iteración.
