# Chapter 8 — Advanced Surface Wave Methods

> **Fuente:** Sebastiano Foti Chapter 8.pdf · pp. 393–440
> **Fase:** primera (completada)

## Introducción

El capítulo 8 extiende el marco estándar de los métodos de ondas superficiales —centrado en ondas de Rayleigh verticales adquiridas con fuentes activas en tierra— hacia aplicaciones y enfoques más avanzados. Los temas cubiertos son:

- **8.1** — Ondas Love: propagación, adquisición con fuentes horizontales e inversión conjunta con ondas Rayleigh.
- **8.2** — Ensayos marinos y costeros: ondas de Scholte en el fondo marino y ondas guiadas de tipo P.
- **8.3** — Inversión conjunta con otros métodos geofísicos (en particular con refracción de ondas P).
- **8.4** — Interferometría sísmica pasiva: método de correlación de ruido ambiental.
- **8.5** — Análisis multicomponente, polarización de ondas superficiales, y relación espectral H/V (HVSR): elipticidad de Rayleigh, identificación de modos, H/V pasivo, adquisición/procesamiento e interpretación.

El objetivo del capítulo no es una revisión exhaustiva sino dar perspectiva sobre las extensiones del método estándar, sus ventajas y sus diferencias con respecto al flujo de trabajo habitual.

---

## 8.1 Ondas Love

### 8.1.1 Naturaleza de las ondas Love

Las [[Love Waves|ondas Love]] consisten en movimiento de corte puramente horizontal (SH), perpendicular a la dirección de propagación y paralelo a la superficie libre. A diferencia de las [[Rayleigh Waves|ondas de Rayleigh]], **no pueden existir en un semiespacio homogéneo**: requieren al menos una capa de baja velocidad sobre un semiespacio más rígido para que la energía quede atrapada por reflexión total interna en la interfaz.

El mecanismo físico es análogo a una guía de onda: la energía SH se refleja repetidamente entre la superficie libre y la interfaz sólido-sólido, formando interferencia constructiva a ciertas frecuencias. Este modo de propagación fue descrito por Love (1911).

Las ondas Love son **modales y dispersivas**. La Figura 8.2 (p. 395) muestra las funciones de eigendesplazamiento de los cinco primeros modos a 80 Hz para un modelo con una capa de 4 m (Vs = 100 m/s) sobre un semiespacio (Vs = 300 m/s). La Figura 8.3 (p. 396) compara las curvas modales de Love (a) y Rayleigh (b) para el mismo modelo:

- Las curvas de Love son más regulares: los modos no se cruzan ni presentan puntos de osculación.
- Las curvas de Rayleigh presentan puntos de osculación (la curva del modo fundamental y la del primer modo superior se tocan en el recuadro discontinuo), lo que puede introducir ambigüedades en la identificación de modos experimentales.

Las **resonancias SH** en capas superficiales poco profundas producen señales de banda angosta en los registros de ondas Love. La frecuencia de resonancia puede estimarse con la regla de cuarto de longitud de onda:

$$f_{res} \approx \frac{V_{S,\text{top}}}{4H}$$

donde H es el espesor de la capa superficial. Aunque el espectro de amplitud de una traza individual pueda parecer de banda angosta, la curva de dispersión experimental puede recuperarse en un rango amplio de frecuencias mediante el análisis multicanal (Figura 8.6, p. 400).

En lo que respecta a la **polarización**: en materiales anisótropos, las ondas Love están asociadas a las velocidades de corte SH y las ondas Rayleigh a las velocidades SV. En medios isotrópicos, ambas ondas sensorizan el mismo parámetro Vs, lo que permite la inversión conjunta asumiendo isotropía.

### 8.1.2 Configuraciones experimentales

La adquisición de ondas de Rayleigh es directa con equipamiento sísmico estándar (fuente vertical sobre placa metálica + geófonos verticales), ya que el movimiento de partícula de Rayleigh tiene una componente vertical dominante en superficie.

En cambio, la adquisición de ondas Love requiere:

1. **Fuente horizontal:** una fuerza horizontal genera movimiento SH y, por tanto, ondas Love. La fuente más común en campo es golpear horizontalmente una viga o durmiente de madera cargado (el peso de personas paradas sobre el durmiente aumenta la fricción con el suelo). Esta fuerza también genera componentes de presión (ondas P y Rayleigh) que contaminan el registro.

2. **Receptores horizontales:** se requieren geófonos o acelerómetros con orientación horizontal perpendicular a la línea de adquisición (componente SH). Los receptores verticales son insensibles al movimiento SH puro.

**Técnica de inversión de polaridad:** dado que la fuerza horizontal genera tanto componentes SH (→ Love + SH refracciones) como componentes de compresión (→ Rayleigh + P refracciones), es posible separar las primeras invirtiendo la polaridad de la fuente (golpear en sentido opuesto). La componente SH cambia de signo al invertir la polaridad; la componente de compresión no. La **resta** de los dos registros cancela la componente de compresión y deja la componente SH. Una alternativa operacionalmente más eficiente es el uso de receptores acoplados que realizan esta resta eléctricamente de forma sincrónica (Sambuelli et al. 2001), aumentando la precisión y reduciendo el tiempo de adquisición.

**Covariables:** incluso con fuente horizontal, los registros contienen refracciones de ondas P y Rayleigh que se superponen. Su separación en el procesamiento (p.ej., mediante análisis f-k) puede ser difícil y requiere juicio del operador. La presencia de modos superiores bien definidos en Love puede facilitar la separación respecto a Rayleigh.

### 8.1.3 Ejemplo real — Isla Terceira (Azores)

**Sitio:** Localidad de São Sebastião, isla Terceira (Archipiélago de las Azores, Portugal). El pueblo sufrió daños graves por un terremoto en 1980 atribuido a efectos de amplificación local. El sitio se encuentra en una caldera volcánica con substrato de roca basáltica y presencia de conos piroclásticos laterales.

**Adquisición:** sismógrafo de 24 canales activos. Para ondas Love: durmiente de madera golpeado horizontalmente con maza + geófonos swyphone horizontales. Para ondas de Rayleigh: maza sobre placa de acero + geófonos verticales 4.5 Hz. Mismo arreglo espacial para ambas adquisiciones.

**Procesamiento:**

- **Rayleigh (Figura 8.7, p. 401):** el sismograma y su espectro f-k muestran dos ramas de dispersión. El modo fundamental sufre una atenuación fuerte (>1.3 dB/m), lo que lo debilita en el espectro. El modo superior, con mayor número de onda (mayor frecuencia), está menos atenuado por su menor profundidad de penetración y es claramente visible.
- **Love (Figura 8.8, p. 402):** el sismograma muestra un tren de ondas dominante de modo fundamental con baja velocidad (inicio ≈ 130 m/s, extremo ≈ 80 m/s en alta frecuencia) y buena coherencia espacial. El modo fundamental está mejor definido que el de Rayleigh.

**Resolución de ambigüedades:** la rama de velocidades de fase Love es consistente con la rama de menor velocidad del espectro de Rayleigh (modo fundamental). Esto permite confirmar qué rama del espectro f-k de Rayleigh corresponde al modo fundamental, resolviendo la ambigüedad generada por la presencia y visibilidad del modo superior. En síntesis, la **inversión conjunta Love + Rayleigh** proporciona mayor constraño del perfil Vs y mayor robustez en la identificación de modos.

> Figuras clave: 8.1 (p. 394), 8.2 (p. 395), 8.3 (p. 396), 8.4 (p. 398), 8.5 (p. 399), 8.6 (p. 400), 8.7 (p. 401), 8.8 (p. 402).

---

---

## 8.2 Ensayos marinos y costeros

La caracterización geofísica de sedimentos bajo agua es de gran interés para el diseño de estructuras portuarias, plataformas offshore, tendido de tuberías submarinas y estudios de riesgo sísmico marino. Los parámetros sísmicos (velocidad y atenuación) son necesarios para evaluar la respuesta dinámica del sitio.

Una dificultad fundamental en el contexto marino es que la **velocidad de onda P en sedimentos saturados es dominada por la compresibilidad del agua poral** (~1500 m/s) y varía poco entre tipos de sedimento. La **velocidad de onda S, en cambio, está controlada por el esqueleto sólido** y tiene una correlación directa con los parámetros geotécnicos. Además, Vs puede ser muchísimo menor que Vp en sedimentos blandos (razón Vp/Vs > 10), lo que implica que la variación de Vs en los primeros metros es un orden de magnitud mayor que la variación de Vp. El análisis de [[Scholte Waves|ondas de Scholte]] (análogo marino de las ondas de Rayleigh) permite estimar el perfil Vs del subfondo de manera no invasiva.

### 8.2.1 Ondas de Scholte

Las [[Scholte Waves|ondas de Scholte]] se propagan en la interfaz sólido-líquido (fondo marino), de forma análoga a las [[Rayleigh Waves|ondas de Rayleigh]] en la interfaz sólido-aire. Fueron descritas por Scholte (1947) como los **modos normales reales** del sistema de capas para el caso *soft bottom*, en el que la velocidad de corte del sólido es menor que la velocidad compresional del agua (condición casi universalmente cumplida en sedimentos no consolidados, donde Vs < 200 m/s << Vp_agua ≈ 1500 m/s).

**Características físicas:**
- **Movimiento de partícula:** elíptico retrógrado, similar a Rayleigh. La energía se concentra en la interfaz. Para dos semiespacios en contacto, la penetración es ≈ una longitud de onda en el sólido y ≈ media longitud de onda en el líquido.
- **Dispersión:** modales y dispersivas. El modo fundamental **no tiene frecuencia de corte** (existe para cualquier frecuencia), a diferencia de los modos superiores.
- **Velocidad:** siempre menor que la velocidad de Rayleigh para el mismo sólido. A frecuencia → 0, la velocidad de Scholte tiende a la velocidad de Rayleigh del semiespacio sólido. A frecuencia → ∞, tiende a la velocidad de onda de Stoneley en la interfaz sólido-líquido.

**Efecto de la capa de agua:** incluso una capa de agua muy delgada (0.5–3 m) modifica la curva de dispersión de Scholte respecto a la de Rayleigh (sin agua). La Figura 8.10b (p. 406) muestra que para Hw = 0.5 m ya existe una diferencia apreciable, y que la diferencia aumenta con Hw. En consecuencia, **analizar datos de Scholte con un modelo directo de ondas de Rayleigh** (ignorando la capa de agua) lleva a una **subestimación sistemática de Vs** en los sedimentos. Es imprescindible incluir el espesor y la velocidad del agua como parámetros en el modelo de inversión.

La Figura 8.12 (p. 407) muestra la diferencia relativa de velocidad entre Scholte y Rayleigh para el mismo sólido y distintos espesores de agua: para Hw = 3 m, la diferencia puede alcanzar hasta ~18% en el rango de 10–20 Hz.

**Generación y registro:**
- Fuentes: impacto o vibrador en el fondo marino, o **fuente de presión en la columna de agua** (air-gun, sparker). Un air-gun puede excitar ondas de Scholte con alta eficiencia en 100 m de agua; el filtro high-cut de la capa de agua actúa como limitación hacia las bajas frecuencias.
- Receptores: hidrófonos acoplados al fondo, geófonos enterrados en el sedimento (OBS — ocean bottom seismometer), o hidrófonos en líneas de tendido.

### 8.2.2 Ondas guiadas de tipo P

Además de las ondas de Scholte, el sistema agua-sedimentos permite la propagación de **[[P-guided Waves|ondas guiadas de tipo P]]** (*P-guided waves*), que corresponden a los **modos fugaces** (*leaky modes*) de la ecuación de dispersión: raíces complejas cuya parte real de la velocidad de fase supera la velocidad compresional del agua.

Físicamente son ondas P multireflejadas en la capa de agua (entre la superficie libre y el fondo marino), con energía parcialmente atrapada. Sus propiedades dependen principalmente de la **velocidad de onda P del agua y del subfondo**, no de Vs. Por eso son complementarias a las ondas de Scholte: juntas permiten estimar tanto Vs como Vp del subfondo.

En oceanografía acústica se denominan ondas ULF (*ultra-low frequency*), típicamente en el rango 1–100 Hz en plataformas continentales. En aguas muy someras, el rango de frecuencias se desplaza hacia valores más altos. La **aproximación acústica** (medio líquido homogéneo, Vs_sólido = 0, alto ratio de Poisson) es válida cuando el ratio de Poisson es alto, como es habitual en sedimentos saturados blandos.

**Información a priori necesaria:** la velocidad del agua (medible con un sensor de temperatura/salinidad o asumida ≈ 1500 m/s) y la velocidad compresional del subfondo (a priori o estimada del tiempo de llegada del primer arribo).

### 8.2.3 Ejemplo de adquisición marina

Un arreglo de **12 hidrófonos espaciados 2 m en el fondo marino** fue utilizado con una fuente tipo speargun (pistola de arpón, fuente de impacto en agua) para adquirir datos marinos (Figura 8.15, p. 411). El shot gather muestra:

- **Dominado por ondas guiadas de tipo P** (alta frecuencia, >1500 m/s): llegan primero, bien separadas.
- **Ondas de Scholte débiles:** visibles tras aplicar un **filtro paso-bajo** a las primeras trazas (Figura 8.16, p. 411). La velocidad del tren de Scholte es muy baja (<50 m/s), propio de sedimentos muy blandos.

La Figura 8.17 (p. 412) presenta un caso de **adquisición en la orilla** (shoreline): las primeras 12 trazas corresponden a geófonos en tierra y el resto a hidrófonos en el fondo. La fuente (maza) está sobre la orilla. En el mismo registro se identifican ondas de Rayleigh en la parte terrestre y ondas de Scholte en la parte submarina. Esto ilustra la posibilidad de **inversión conjunta** de datos terrestres y marinos para una caracterización continua a lo largo de la línea costera.

Si se adquieren simultáneamente ondas de Scholte (sensibles a Vs) y ondas guiadas de tipo P (sensibles a Vp), la **inversión conjunta** permite estimar ambos perfiles acoplando los modelos geométricos (espesores compartidos).

> Figuras clave: 8.9 (p. 404), 8.10 (p. 406), 8.11 (p. 407), 8.12 (p. 407), 8.13 (p. 409), 8.14 (p. 409), 8.15 (p. 411), 8.16 (p. 411), 8.17 (p. 412).

---

## 8.3 Inversión conjunta con otros datos geofísicos

El análisis estándar de ondas superficiales estima el perfil Vs(z) —y, en la variante de atenuación, el perfil Ds(z)— a partir de la curva de dispersión de ondas de Rayleigh o Love. Sin embargo, el problema inverso tiene sensibilidad limitada a ciertos parámetros: la velocidad de onda P (Vp), el ratio de Poisson (ν) y la densidad influyen de forma débil sobre la curva de dispersión de Rayleigh, lo que genera ambigüedad en la solución cuando estos parámetros no se conocen con precisión. Además, la no-unicidad del perfil Vs obtenido puede ser severa en presencia de inversiones de velocidad o cuando el rango de frecuencias es estrecho.

La incorporación de otros datos geofísicos independientes —sísmicos o no sísmicos— permite constrañar estos parámetros y reducir la no-unicidad del modelo. El principio físico subyacente es que cada método geofísico es sensible a propiedades distintas del mismo medio. Cuando varios datasets con complementariedad de información se invierten en conjunto, la solución está mejor constrañida que cualquiera de los datasets individualmente. Esta sección presenta el marco conceptual de la inversión conjunta (8.3.1) y ejemplos de aplicación con datos eléctricos, con diferentes tipos de ondas sísmicas, y con la combinación de ondas superficiales y refracción de ondas P (8.3.2).

### 8.3.1 Inversión conjunta

La integración de múltiples datasets mejora la resolución del subsuelo y mitiga la [[Non-uniqueness|no-unicidad]] inherente a cada método por separado. El término **inversión conjunta** designa el proceso de estimar los parámetros del modelo a partir de múltiples conjuntos de datos geofísicos, construyendo una única función objetivo que honra simultáneamente todos los datasets.

Se distinguen dos clases según el dominio de los parámetros:

- **Single-domain joint inversion:** múltiples datasets se usan para estimar un único dominio físico. Ejemplo: estimar el perfil Vs a partir de las curvas de dispersión de [[Rayleigh Waves|ondas de Rayleigh]] y [[Love Waves|ondas de Love]] simultáneamente, usando el mismo modelo de capas.
- **Multiple-domain joint inversion:** los datasets estiman múltiples propiedades físicas. Ejemplo: estimar Vp y Vs a partir de [[Refraction Seismics|refracción de ondas P]] y ondas superficiales, obteniendo un modelo conjunto con ambos parámetros.

Dentro de la inversión conjunta simultánea, el vínculo entre dominios puede ser de dos naturalezas:

- **Geométrico:** impone similitud en la distribución espacial de los parámetros, sin asumir una relación petrophysica entre ellos.
- **Petrofísico:** asume una relación local intrínseca entre los parámetros de los distintos dominios.

Antes de este marco riguroso, se utilizaba la **inversión conjunta cooperativa** (Lines et al. 1988): itera inversiones monodominio alternadamente, usando el resultado de una inversión como modelo inicial para la otra. El proceso se repite hasta la convergencia. Este enfoque es subjetivo y menos robusto que la inversión simultánea.

La representación esquemática de la Figura 8.18 (p. 414) ilustra el contraste: en (a) se invierten dos datasets de forma independiente y luego se compatibilizan los modelos; en (b) los dos datasets y el vínculo entre dominios entran juntos en un único proceso de inversión conjunta que produce un modelo único m(1,2).

#### 8.3.1.1 Inversión conjunta geométrica

El vínculo más simple entre dominios es la similitud geométrica de los modelos. Aunque los parámetros geofísicos de dos dominios sean aparentemente no correlacionados en valores, pueden compartir la misma estructura espacial porque ambos están controlados por los mismos rasgos geológicos.

El vínculo geométrico se incluye en la inversión conjunta mediante la **función cross-gradient** (Gallardo y Meju 2003), definida como el producto vectorial de los gradientes de los campos m₁ y m₂ en los dos dominios:

$$\bar{\tau} = \nabla m_1(x,y,z) \times \nabla m_1(x,y,z) \tag{8.1}$$

La función cross-gradient mide la similitud entre dos imágenes. Su valor es mínimo cuando los gradientes de ambos campos son colineales (los campos tienen la misma estructura espacial) y máximo donde los dos campos muestran distribuciones geométricas distintas. La Figura 8.19 (p. 415) muestra dos campos m₁ y m₂ con sus gradients y el cross-gradient resultante: en la zona donde la estructura geológica es similar (parte inferior), el cross-gradient es bajo, aunque los valores absolutos de los parámetros no estén correlacionados positivamente.

La función objetivo del ajuste geométrico incorpora los residuales de ambos datasets más el campo de cross-gradients (Tryggvason y Linde 2006). En un modelo 1D estratificado, la inversión conjunta geométrica implica espesores de capa similares entre los dos dominios, independientemente de si los valores de los parámetros están relacionados.

#### 8.3.1.2 Inversión conjunta petrofísica

Cuando los parámetros de los diferentes dominios tienen una relación petrofísica intrínseca, el vínculo se puede establecer mediante una **relación local entre parámetros**. Estas relaciones pueden ser leyes físicas analíticas o relaciones empíricas entre parámetros geofísicos; por ejemplo: la ley de Archie (1942) relaciona resistividad eléctrica y porosidad, la ecuación de Wyllie et al. (1956) relaciona velocidad sísmica con porosidad, y las relaciones de Gardner et al. (1974) vinculan velocidad P y densidad.

La función objetivo del ajuste petrofísico tiene tres elementos que se combinan con distintos pesos: los residuales de los datos de cada dominio, las regularizaciones monodominio, y los vínculos entre dominios. El vínculo petrofísico puede imponerse como restricción de igualdad (forzando exactamente la relación a priori) o como minimización del residual local entre la relación a priori y la relación obtenida del modelo (en este caso los parámetros de la relación petrofísica se convierten en incógnitas adicionales de la inversión; Jegen et al. 2009, De Stefano et al. 2011).

---

### 8.3.2 Inversión conjunta de ondas superficiales

Los métodos de ondas superficiales estiman mediante inversión los parámetros incógnitos del subsuelo (velocidad de onda S y razón de amortiguamiento). La inversión acoplada de velocidad y atenuación descrita en el [[Inversión|Capítulo 6]] ya puede considerarse una forma de inversión conjunta single-domain. En esta sección se discute la inversión conjunta de datos de ondas superficiales con otras mediciones geofísicas, sísmicas y no sísmicas.

El objetivo es doble: (1) mejorar la estimación de propiedades del suelo a las que la onda superficial tiene sensibilidad limitada —en particular Vp y el ratio de Poisson, que condicionan la presencia del nivel freático y la compresibilidad del medio—, y (2) mitigar la no-unicidad del problema inverso incorporando información estructural complementaria. El argumento central es que las fronteras litológicas del subsuelo afectan simultáneamente las propiedades mecánicas, eléctricas y compresionales del medio: al imponer que los modelos de diferentes dominios compartan la misma geometría, se reduce el espacio de soluciones aceptables.

La sección se organiza en tres bloques de aplicación: (1) inversión conjunta con datos **eléctricos y electromagnéticos** (VES, TDEM), aprovechando vínculos geométricos entre Vs y resistividad compartidos por las mismas fronteras litológicas; (2) inversión conjunta entre diferentes tipos de **ondas sísmicas** (Love + Rayleigh, Rayleigh + ondas guiadas); y (3) inversión conjunta de ondas superficiales con **refracción de ondas P**, la combinación más habitual en ingeniería geotécnica ya que ambos datasets suelen adquirirse simultáneamente con el mismo equipo sísmico sin coste operacional adicional significativo.

#### 8.3.2.1 Inversión conjunta con mediciones eléctricas y electromagnéticas

La inversión conjunta de la [[Dispersion Relation|curva de dispersión]] de ondas superficiales con datos eléctricos y electromagnéticos 1D puede explotar vínculos geométricos para imponer fronteras litológicas comunes. Los límites litológicos en el subsuelo somero afectan tanto la velocidad de onda S como la resistividad de las capas; por tanto, una inversión geométricamente acoplada es posible (Hering et al. 1995).

Los datos de sondeo eléctrico vertical (VES) y electromagnético en el dominio del tiempo (TDEM) proporcionan curvas de resistividad aparente en función de la geometría del arreglo de electrodos, que son análogas a las curvas de dispersión: ambas proporcionan información integral sobre los parámetros físicos correspondientes. Además, ambos modelos directos se basan en una **matriz de transferencia global** construida a partir de las matrices de cada capa para la solución 1D.

En la inversión conjunta VES + ondas superficiales, los parámetros del modelo son el espesor, la velocidad de corte y la resistividad de cada capa. El Jacobiano combinado es una **única matriz** con las derivadas parciales de ambos conjuntos de datos respecto a todos los parámetros: las filas corresponden a los p valores de resistividad aparente ρ_app más los m valores de velocidad de fase v_r; las columnas contienen las derivadas respecto a los n−1 espesores h y los n valores Vs (más los n valores de resistividad ρ). La ausencia de un vínculo petrofísico se refleja en que las derivadas cruzadas entre dominios son cero.

La Figura 8.20 (p. 418) muestra un ejemplo de inversión conjunta de ondas superficiales y resistividad eléctrica (Comina et al. 2004): la estratigrafía del sitio consiste en capas alternadas de arenas y arcillas. La capa arcillosa (baja resistividad) es identificada en la inversión conjunta entre 8 y 13 m, y su espesor es relevante para evaluar el riesgo de filtraciones bajo un terraplén fluvial. La solución conjunta es más robusta y confiable que las inversiones individuales porque honra simultáneamente los dos datasets.

El mismo enfoque es aplicable a datos TDEM y a datos magnetotelúricos en combinación con ondas superficiales de largo período.

#### 8.3.2.2 Inversión conjunta con otros datos sísmicos

**Love + Rayleigh:** la inversión conjunta de ondas de Love y Rayleigh es una single-domain joint inversion. El mismo modelo de capas está constrañido por dos datasets distintos; las incógnitas son los espesores de capa y Vs, bajo la hipótesis de comportamiento isótropo.

**Rayleigh + ondas guiadas:** puede construirse una función de desajuste global que utiliza simultáneamente las curvas de dispersión de [[Rayleigh Waves|ondas de Rayleigh]] y de ondas guiadas. Una alternativa es usar la distancia entre las curvas modeladas independientemente a partir del mismo conjunto de capas (Roth et al. 1998).

**Ondas superficiales + refracción de ondas P:** esta combinación es especialmente interesante porque los dos datasets frecuentemente están disponibles juntos (son adquiribles en el mismo ensayo sísmico con coste operacional mínimo adicional), y los métodos se complementan en muchos aspectos (Foti et al. 2003):

- Los métodos de ondas superficiales superan algunas limitaciones inherentes de la refracción: son insensibles al **problema de capa oculta**, a inversiones de velocidad y a variaciones graduales de velocidad. Además, la sensibilidad a Vs es especialmente importante en sedimentos saturados donde Vp está controlada principalmente por la compresibilidad del fluido.
- La refracción aporta información a priori muy útil para la interpretación de ondas superficiales: la posición del substrato rocoso, la profundidad de la tabla de agua (que permite estimar el ratio de Poisson para el modelado de ondas superficiales), y una advertencia en caso de variaciones laterales de velocidad (topografía de los refractores).
- Cuando los dos métodos producen resultados independientemente confiables, la combinación Vp + Vs permite estimar propiedades mecánicas y porosidad del depósito. La relación entre los parámetros elásticos puede usarse como vínculo petrofísico (ratio de Poisson) o la similitud entre distribuciones espaciales puede usarse como vínculo geométrico.

#### 8.3.2.3 Inversión conjunta de refracción y ondas superficiales — Ejemplo del problema de capa oculta

El **problema de la capa oculta** es una de las posibles ambigüedades de la refracción sísmica: una capa intermedia puede no ser identificada porque sus primeros arrivals refractados llegan a la superficie después de los arrivals refractados críticamente desde una capa más rápida y profunda. En la práctica, la equivalencia se debe a que múltiples perfiles de velocidad pueden generar exactamente las mismas curvas de tiempo-distancia. La Figura 8.23 (p. 423) muestra cómo dos perfiles de velocidad muy diferentes producen curvas de tiempos de llegada idénticas.

**Ejemplo (Piatti et al. 2013):** sitio con suelo blando sobre capa de grava densa y substrato de arenisca dura a menos de 10 m de profundidad.

- **Datos de ondas superficiales (Figura 8.21, p. 421):** el sismograma y su [[Dispersion Relation|curva de dispersión]] de banda ancha fueron invertidos para un modelo estratificado que confirma la presencia de tres capas geológicas principales, con velocidades entre ~200 y ~800 m/s en el rango 20–80 Hz.
- **Datos de refracción (Figura 8.22, p. 422):** los tiempos de llegada de los shots de ida y vuelta muestran dos velocidades (V1 ≈ 330 m/s, V2 ≈ 2580 m/s) con una gran diferencia (contraste ~8x) y evidencia de un substrato ligeramente inclinado. La interpretación con un modelo de dos capas ubica el substrato entre 3.2 y 4 m de profundidad, pero el alto contraste de velocidad hace posible la existencia de una capa oculta de espesor significativo.
- **Inversión conjunta:** los tiempos de llegada del primer arribo (refracción) y la curva de dispersión (ondas superficiales) se invierten juntos imponiendo espesores de capa comunes para los modelos Vp y Vs. Se incluye un pequeño buzamiento como parámetro adicional. La inversión se realiza mediante optimización [[Monte Carlo Methods|Monte Carlo]], definiendo una función de desajuste conjunta como la media ponderada de los dos mínimos cuadráticos. Los resultados (Figura 8.24, p. 424) confirman el gran contraste de Vs y un buzamiento pequeño aceptable para la hipótesis 1D; los 20 mejores modelos se muestran en la Figura 8.24c.
- **Resultado (Figura 8.25, p. 424–425):** la inversión conjunta identifica la presencia de una capa de limo y arcilla a ~20 m de profundidad, embebida entre las gravas superiores y el substrato (flysch), lo que no era detectable con la refracción sola. Este resultado fue confirmado por información estratigráfica obtenida de sondeos mecánicos.

Para aplicaciones a **gran escala** (líneas de exploración de varios km, geometrías 3D), los dos datasets tienen diferente densidad espacial y diferente resolución: las ondas superficiales resuelven con alta densidad el Vs de las porciones superficiales, mientras que la refracción resuelve con menor resolución (pero mayor profundidad) los principales refractores Vp. La Figura 8.26 (p. 425) ilustra esquemáticamente el muestreo diferenciado del modelo. La Figura 8.27 (p. 426) muestra un ejemplo 2D de 10 km en el Golfo de Suez (Strobbia et al. 2010) con una plataforma de inversión conjunta flexible que resuelve simultáneamente diferentes escalas: la distribución de Vp para los 400 m más superficiales correlaciona bien con la sección de reflexión apilada.

> Figuras clave: 8.18 (p. 414), 8.19 (p. 415), 8.20 (p. 418), 8.21 (p. 421), 8.22 (p. 422), 8.23 (p. 423), 8.24 (p. 424), 8.25 (p. 424–425), 8.26 (p. 425), 8.27 (p. 426).

---

## 8.4 Interferometría sísmica pasiva

La [[Seismic Interferometry|interferometría sísmica]] designa el principio de generar trazas sísmicas desde fuentes virtuales mediante la cross-correlación o la convolución de observaciones en diferentes receptores. Las dos aplicaciones principales son: (1) la estimación o aislamiento de una componente del campo de ondas, y (2) la estimación de las propiedades del medio de propagación. En esta sección se discuten aspectos de la interferometría sísmica pasiva como herramienta para analizar ondas superficiales en datos de ruido ambiental o microtremores.

Estudios teóricos recientes demostraron que el campo difuso de ruido ambiental puede transformarse, mediante cross-correlación, en una respuesta de impulso sísmica determinista, estimando la **función de Green** entre receptores (Weaver y Lobkis 2001, 2002; Snieder 2004; Wapenaar 2004; Wapenaar y Fokkema 2006). En sismología global, con ondas coda y registros largos de ruido, se demostró que la componente de onda superficial de la función de Green entre dos receptores puede recuperarse de la cross-correlación de las observaciones en esos receptores (Campillo y Paul 2003; Shapiro y Campillo 2004). El potencial de este enfoque en el rango de frecuencias altas, en la escala de la ingeniería sísmica, también ha sido demostrado.

**Principio de la interferometría sísmica pasiva** (siguiendo la revisión de Wapenaar et al. 2010a):

Considérense dos receptores R₁ y R₂ que observan señales de ondas superficiales provenientes de distintas fuentes S_j dispersas alrededor de ellos. Para cada fuente, las señales registradas T(s_j, r₁) y T(s_j, r₂) se cross-correlacionan, generando la traza T₁₂(s_j). La traza correlacionada depende de la posición de la fuente y de las propiedades del subsuelo entre los receptores (Figura 8.28, p. 427).

El proceso se repite para todas las fuentes disponibles, generando una multiplicidad de trazas correlacionadas —una por cada fuente— que se reúnen en un **correlogram gather** (Figura 8.29, p. 428), ordenadas según el azimut de la fuente. Este gather muestra la variación de la correlación según la posición de la fuente y es regular y suave a pesar de la diferente distancia de las fuentes, porque la correlación elimina los efectos de propagación desde la fuente hasta los receptores.

En la **suma** de las trazas correlacionadas, las contribuciones de fuentes en puntos opuestos se anulan entre sí. Solo las fuentes en los **puntos estacionarios** (aquellos casi alineados con los dos receptores) contribuyen constructivamente, produciendo una traza con la respuesta causal y anti-causal desde el primer receptor hasta el segundo. La traza resultante puede interpretarse como la respuesta de impulso de una fuente virtual colocada en R₁ medida en R₂.

Las señales extraídas pueden procesarse como datos activos virtuales. La principal aplicación es la recuperación de la velocidad de fase de ondas superficiales a partir del ruido ambiental (Shapiro y Campillo 2004). La mayoría de las aplicaciones se basan en el análisis de arrays 2D dispersos y conducen a una determinación tomográfica de la distribución de velocidades de ondas superficiales.

**Interferograma vs ReMi:**

En un campo de ondas no isotrópico, el uso de un array lineal no permite corregir la velocidad aparente y puede llevar a velocidades largamente sobreestimadas. Sin embargo, bajo la hipótesis de campo difuso de ruido ambiental, pueden usarse enfoques similares al método [[ReMi Method|ReMi]] (refraction microtremor), usando un receptor como fuente virtual: el sismograma resultante puede procesarse como un dataset activo con análisis f-k estándar. La ventaja sobre ReMi es que la validación de las hipótesis es más fácil y el espectro f-k correspondiente tiene rasgos más similares a los espectros usuales de datos activos.

Para comparar los dos enfoques (Figura 8.30–8.31, p. 429), se generaron sintéticos con 1000 fuentes alrededor de un array lineal de receptores en un medio estratificado. El interferograma tiene simetría alrededor de t = 0 (propiedad básica de la cross-correlación). Su espectro f-k muestra los máximos exactamente sobre el número de onda teórico verdadero; el proceso interferométrico cancela las contribuciones opuestas. En comparación, el espectro ReMi del mismo dataset sintético (Figura 8.31b) muestra los máximos sobre el número de onda aparente (no el verdadero), lo que puede conducir a sobreestimación si el campo no es perfectamente isotrópico.

El interferograma también ayuda a validar la hipótesis básica de ruido isotrópico: si existe una fuente dominante a distancia limitada, el interferograma muestra eventos no lineales que advierten sobre la invalidez de los resultados (Figura 8.32, p. 430).

> Figuras clave: 8.28 (p. 427), 8.29 (p. 428), 8.30 (p. 429), 8.31 (p. 429), 8.32 (p. 430).

---

## 8.5 Análisis multicomponente, polarización y relación espectral H/V

La amplitud de las contribuciones modales de las ondas superficiales en función de la frecuencia depende de la ubicación y el espectro de la fuente, pero también está fuertemente afectada por la estructura de velocidades del subsuelo. En principio, es posible usar el espectro de amplitud medido como dato experimental para estimar las propiedades del sitio, pero controlar o medir el espectro de radiación de la fuente no es sencillo. Sin embargo, el ratio entre las componentes horizontal y vertical del desplazamiento de las ondas superficiales **solo depende de las propiedades del sitio** para una ubicación y dirección de fuente dadas. Por tanto, la **polarización como función de la frecuencia** puede usarse para estimar las propiedades del sitio.

En ensayos activos con ondas superficiales, la razón espectral o **elipticidad** de las [[Rayleigh Waves|ondas de Rayleigh]] puede estimarse analizando la polarización de datos activos multicomponente. En datos pasivos dominados por ondas de Rayleigh, el ratio promedio entre las componentes horizontal y vertical (razón H/V) puede estimarse sobre registros largos y usarse para evaluar las propiedades locales del sitio.

**Elipticidad en medio homogéneo:** el ratio V/H es constante y es función del ratio de Poisson.

**Elipticidad en medios estratificados:** es dependiente de la frecuencia. El efecto de la estratificación sobre la elipticidad se ilustra en la Figura 8.33 (p. 431) mediante un modelo simple: una capa de 25 m sobre un semiespacio (Vs_semiespacio = 500 m/s), con Vs_capa variando de 200 a 500 m/s. Las curvas modales de dispersión (Figura 8.33a) y las curvas de elipticidad V/H del modo fundamental (Figura 8.33b) muestran que:

- Para mayor **contraste de velocidad** entre capa y semiespacio, la elipticidad varía en un rango más amplio con la frecuencia.
- La polarización es más vertical en el rango de alta frecuencia (donde la energía está confinada en la capa superficial de baja velocidad, con mayor influencia del semiespacio rígido), y más horizontal en el rango de baja frecuencia.
- Para un contraste mayor a 2, la componente horizontal supera a la vertical en el rango de baja frecuencia.
- Cuando el contraste es grande, el espectro de amplitud de la componente vertical presenta un **máximo fuerte** y también un **cero**: una frecuencia a la que la componente vertical se anula y el movimiento es puramente horizontal. El sentido de la órbita elíptica cambia alrededor de este punto.

Estas características hacen que la curva de elipticidad sea informativa sobre las propiedades del subsuelo, en particular sobre el contraste de velocidad y el espesor de las capas superficiales.

La mayoría de las aplicaciones usan la **elipticidad horizontal** (ratio H/V). La Figura 8.34 (p. 432) muestra el ratio H/V del modo fundamental en escala logarítmica para un modelo de capa de baja velocidad de 25 m y 200 m/s sobre un semiespacio de 800 m/s (Vp = 1500 m/s, 2000 m/s). El comportamiento tiene cinco regímenes según la frecuencia:

- **A — muy baja frecuencia:** movimiento elíptico antihorario.
- **B — primera singularidad f_H:** el movimiento se vuelve puramente horizontal (la componente vertical se anula); el ratio H/V → ∞.
- **C — frecuencia intermedia:** movimiento horario, progresivamente más vertical.
- **D — segunda singularidad f_V:** el movimiento es puramente vertical; H/V → 0.
- **E — alta frecuencia:** polarización dominada por las propiedades de la capa superficial.

La **frecuencia natural del sitio** es la frecuencia de resonancia fundamental de corte, f_0 = Vs/(4H) (cuarto de longitud de onda). El pico del ratio H/V (f_H) es muy cercano a esta frecuencia natural cuando la capa tiene baja velocidad homogénea. En casos con gradiente o estratificación dentro de la capa de baja velocidad, el cero de la componente vertical puede estar a una frecuencia ligeramente superior a la frecuencia natural. El ratio de Poisson y la densidad tienen efectos de segundo orden. La Figura 8.35 (p. 434) muestra, para un solo modelo, la función de transferencia sísmica y la elipticidad horizontal; el cross-plot para una muestra Monte Carlo de 2000 casos confirma que f_H ≈ f_0.

### 8.5.1 Identificación de modos con alto contraste de velocidad

Una aplicación importante de los datos multicomponente es la **identificación de modos** en casos ambiguos. La **osculación de modos** es el fenómeno donde dos modos se acercan mucho en velocidad de fase y sus amplitudes también presentan una transición suave. Ocurre con grandes contrastes de impedancia. En la Figura 8.36 (p. 435), la transición entre el modo fundamental y el primer modo superior es continua tanto en velocidad como en amplitud.

En la práctica, la energía salta del modo fundamental al modo superior, creando una curva de dispersión aparentemente continua. Con resolución espacial limitada de los datos reales, la identificación de la superposición de modos puede ser imposible (ver también Sección 7.4). La Figura 8.37 (p. 436) muestra datos sintéticos donde la resolución espacial limitada lleva a una curva de dispersión aparente asociada al modo fundamental en alta frecuencia y al primer modo superior en baja frecuencia. Esta mala identificación puede evitarse si se registra la **componente horizontal** (in-line): permite identificar el modo fundamental por debajo de la frecuencia de osculación, como se muestra en la comparación de espectros f-k vertical vs. horizontal de la Figura 8.38 (p. 437).

### 8.5.2 H/V pasivo

Las técnicas monoestación pasivas basadas en la relación espectral H/V (**HVSR**) han sido extensamente debatidas e investigadas. La técnica fue introducida por Nogoshi e Igarashi (1971) y se popularizó con los trabajos de Nakamura (1989, 1996, 2000). La interpretación original de Nakamura atribuye la curva H/V directamente a la respuesta sísmica de ondas S en el sitio; el acuerdo general en la comunidad es, sin embargo, que las **ondas superficiales dominan la respuesta H/V** en la mayoría de los casos.

Un gran número de estudios experimentales y teóricos ha demostrado que, en la mayoría de las situaciones, el campo de ruido ambiental está dominado por ondas superficiales (Horike 1985; Arai y Tokimatsu 1998) y que el pico observado en la curva de razón espectral está relacionado con la elipticidad de las [[Rayleigh Waves|ondas de Rayleigh]].

Cuando los datos se adquieren y procesan correctamente, el ratio H/V depende de las propiedades del sitio. Las distintas situaciones son:

- **Fuentes de ruido dentro de la capa sedimentaria o en superficie cerca de la estación:** el pico está relacionado con la elipticidad horizontal del modo fundamental de las ondas de Rayleigh. Con grandes contrastes de velocidad y fuentes someras, el rol de las ondas superficiales es dominante.
- **Fuentes lejanas:** puede aparecer un segundo pico relacionado con la resonancia de ondas de corte de la onda head-wave.
- **Fuentes profundas (en el substrato):** los picos se deben a la resonancia de la onda head.

La importancia relativa de las [[Rayleigh Waves|ondas de Rayleigh]] y [[Love Waves|ondas de Love]] puede afectar la forma de la curva H/V y varía de sitio a sitio. Los métodos de vibración ambiental con estaciones multicomponente monoestación y el método H/V pueden contribuir eficazmente a la evaluación del efecto de sitio sísmico, especialmente en microzonación sísmica urbana y en países en desarrollo por su bajo costo.

### 8.5.3 Adquisición y procesamiento de H/V

La adquisición y el procesamiento de datos H/V están documentados extensamente en la documentación del proyecto SESAME (SESAME 2004). Las condiciones clave son:

- **Receptores multicomponente de baja frecuencia:** los sensores y el digitalizador deben garantizar sensibilidad en todo el rango de frecuencias de interés, bajo ruido electrónico y respuesta sincrónica para todos los componentes.
- **Condiciones del sitio:** evitar estructuras subterráneas, suelo blando o irregular (barro, hierba, hielo, grava), y fuentes de ruido como maquinaria y tráfico.
- **Duración de los registros:** desde pocos minutos para depósitos superficiales hasta media hora cuando el pico esperado está a menos de 1 Hz. La duración debe aumentarse si hay perturbaciones transitorias.

El procesamiento H/V comprende los pasos: selección de partes estacionarias del registro rechazando pulsos transitorios, cálculo de espectros de Fourier, suavizado de espectros, combinación de las componentes horizontales, cálculo del ratio H/V, promediado sobre diferentes ventanas temporales, y estimación de valores promedio con desviación estándar para identificar los picos confiables.

### 8.5.4 Interpretación de H/V

En la interpretación original de Nakamura (1989), la razón espectral está directamente relacionada con la respuesta de ondas S. El acuerdo de la comunidad sismológica e ingenieril es, sin embargo, que las ondas superficiales dominan la respuesta H/V. Con grandes contrastes de velocidad y fuentes someras cercanas a la estación, el rol de las ondas superficiales es dominante. En algunos casos (campo de ruido dominado por [[Rayleigh Waves|ondas de Rayleigh]] en modo fundamental), puede identificarse un máximo nítido y también un mínimo relacionado con el cero de la elipticidad H/V (Figura 8.39, p. 439).

Criterios de interpretación de la curva H/V:

1. **Curva con pico claro y no industrial:** indica la presencia de un gran contraste de impedancia en alguna profundidad; la frecuencia del pico es cercana a la frecuencia fundamental del sitio. Si el espesor es conocido, puede estimarse Vs. El valor del pico **no** está relacionado con el factor de amplificación del sitio.
2. **Curva plana (valores H/V entre 0.5 y 2):** probablemente el perfil de velocidades local no tiene contrastes de impedancia significativos.
3. **Ambigüedad y no-unicidad:** la posible no-unicidad de la curva computada no debe ignorarse. Usar una sola curva para la caracterización del sitio puede llevar a incertidumbres severas.

Las técnicas avanzadas de procesamiento e interpretación implican la **inversión de la curva H/V** para la identificación de parámetros del modelo, como en la inversión de dispersión de ondas superficiales (Fäh et al. 2001). Las curvas H/V se corrigen primero por la contaminación de ondas SH y Love, y luego se invierten. Arai y Tokimatsu (2000) mostraron que los ratios H/V pueden reproducirse mejor incluyendo la contribución de los modos superiores de [[Rayleigh Waves|ondas de Rayleigh]] y [[Love Waves|ondas de Love]]. Dada la fuerte no-linealidad de las curvas, la búsqueda global es preferible para la inversión; la cantidad limitada de información en las curvas de elipticidad requiere información a priori (p.ej., sobre la profundidad del substrato) o restricciones adicionales para una interpretación confiable.

La **inversión conjunta de curvas de dispersión y ratios espectrales H/V** ha sido aplicada para aumentar la fiabilidad respecto a cada inversión individual (Parolai et al. 2005). Las adquisiciones multicanal y multicomponente permiten la extracción simultánea de curvas de dispersión y ratios espectrales, con lo que tanto las [[Rayleigh Waves|ondas de Rayleigh]] como las [[Love Waves|ondas de Love]] pueden ser identificadas y procesadas, constrañendo mejor la inversión.

> Figuras clave: 8.33 (p. 431), 8.34 (p. 432), 8.35 (p. 434), 8.36 (p. 435), 8.37 (p. 436), 8.38 (p. 437), 8.39 (p. 439).
