# Chapter 7 — Case Histories

> **Fuente:** Sebastiano Foti Chapter 7.pdf · pp. 351–end
> **Fase:** primera (en progreso)

## Introducción

El capítulo 7 presenta aplicaciones reales del método de ondas superficiales para la caracterización de sitios. A diferencia de los capítulos anteriores —que desarrollan el marco teórico de adquisición, procesamiento e inversión—, este capítulo integra todo el flujo de trabajo sobre datos experimentales reales. El objetivo es mostrar cómo las decisiones metodológicas afectan el resultado final en condiciones de campo reales.

El capítulo está organizado en cinco secciones:

- **7.1** — Comparación de técnicas de procesamiento con datos de fuente activa (sitio Saluggia, Italia)
- **7.2** — Comparación de estrategias de inversión con dataset combinado activo+pasivo (sitio La Salle, Alpes italianos)
- **7.3** — Determinación conjunta de perfiles Vs y Ds (sitios Memphis y Pisa)
- **7.4** — Casos con presencia de modos superiores
- **7.5** — Extracción de ground-roll de registros sísmicos de reflexión

Un mensaje clave del capítulo es que el análisis de ondas superficiales requiere *juicio de ingeniería*: la presencia de ruido, modos superiores, nivel freático incorrecto o errores de phase unwrapping puede llevar a resultados erróneos incluso con técnicas bien implementadas.

---

## 7.1 Comparación de técnicas de procesamiento — datos de fuente activa

**Sitio:** Saluggia, norte de Italia (llanura del río Dora Baltea).
**Litología:** gravas y arenas gravosas con lentes de arena fina y limo arcilloso. Nivel freático entre 2 y 3 m de profundidad.
**Instrumentación:** 24 geófonos verticales (4.5 Hz), dos configuraciones con separaciones receptor de 1 m y 3 m. Fuentes: maza de 6 kg (sledgehammer) y sistema de caída de peso de 130 kg desde 3 m de altura. El maza genera principalmente altas frecuencias (~50 Hz) y la caída de peso bajas frecuencias (~25 Hz). Véase Figura 7.1 (p. 352).

El diseño de dos configuraciones tiene como propósito cubrir rangos de frecuencia complementarios: el arreglo corto (1 m) para altas frecuencias con mayor SNR; el largo (3 m) para bajas frecuencias y mayor penetración. Esto ilustra el **trade-off entre resolución superficial y profundidad de investigación**, ya que la longitud del arreglo determina la longitud de onda máxima accesible.

### 7.1.1 Análisis de dos estaciones (SASW)

El método de [[SASW Method|SASW]] (Spectral Analysis of Surface Waves) trabaja con pares de receptores. Para cada par, se evalúan las siguientes cantidades espectrales (Figura 7.2, p. 354):

- **Fase del espectro cruzado (cross-power spectrum):** usada para estimar el retardo temporal dependiente de la frecuencia entre los dos receptores y, dado que la distancia es conocida, calcular la [[Phase Velocity|velocidad de fase]].
- **Función de coherencia:** indica la frecuencia de confianza del análisis. Un valor de coherencia cercano a 1 señala alta relación señal/ruido (SNR). Solo se seleccionan los rangos de frecuencia donde la coherencia es alta (~10–35 Hz para el par de 18 m analizado).
- **Autoespectro de potencia de cada receptor:** permite identificar la distribución de energía en frecuencia y verificar que ambos receptores registran el mismo modo.

Un aspecto crítico en el análisis SASW es el **phase unwrapping**: la fase medida es periódica (−180° a +180°), y los errores en la identificación de los saltos de fase se propagan directamente como errores en la [[Dispersion Relation|curva de dispersión]]. Un SNR bajo (como ocurre por debajo de 10 Hz) dificulta la identificación correcta de dichos saltos. Las curvas de dispersión experimentales para distintas separaciones de receptores se muestran en la Figura 7.3 (p. 355).

La estrategia práctica recomendada es procesar primero los pares con receptores cercanos (altas frecuencias, SNR alto) y luego verificar la consistencia con los pares más distantes. La superposición de ramas entre pares distintos permite detectar errores de unwrapping. Siempre se requiere juicio del operador.

### 7.1.2 Análisis frecuencia–número de onda (f-k)

El análisis multiestación se realiza transformando los datos del dominio tiempo–espacio (x-t) al dominio frecuencia–número de onda (f-k). La curva de dispersión experimental se extrae como la localización de los máximos espectrales (Figura 7.4, p. 356).

La transformada empleada es la **doble transformada de Fourier**, cuya aplicación se limita a arreglos con espaciado uniforme entre receptores. La resolución en el dominio f es función de la duración de la ventana temporal; la resolución en el dominio k está limitada por el número de receptores y la longitud del arreglo. Para mejorar la resolución en k, se aplica **zero padding en espacio** (por ejemplo, 1024 puntos, añadiendo señales de amplitud cero al dataset experimental). Con el arreglo de 3 m (70.5 m de longitud), se obtiene la curva de dispersión de forma consistente entre 8 y 43 Hz.

La limitación en la frecuencia alta está determinada por la separación entre receptores (aliasing espacial) y por la atenuación de componentes de alta frecuencia en los geófonos distantes. La limitación en la frecuencia baja está determinada por la longitud total del arreglo.

Se muestra que las curvas de dispersión obtenidas con el análisis f-k son consistentes con las del análisis SASW para el rango de frecuencias donde ambas se solapan (Figura 7.5 y 7.8, pp. 357–360), confirmando que los dos métodos recuperan el mismo modo fundamental.

También se aplicaron transformadas **τ-p** (slant-stack) y **MASW** (Multichannel Analysis of Surface Waves, véase Figura 7.6 y 7.7). En el dominio de frecuencia–lentitud (f-slowness), la curva de dispersión se recupera como localización de máximos, con la ventaja de que la velocidad de fase se visualiza directamente (ya que es el inverso de la lentitud). Para este dataset, las curvas obtenidas con f-k y τ-p son prácticamente indistinguibles (Figura 7.8, p. 360).

### 7.1.3 Efecto del nivel freático en la inversión

La inversión de la curva de dispersión requiere parámetros a priori sobre la densidad y el [[Poisson Ratio|ratio de Poisson]] de cada capa, ya que estos tienen influencia limitada pero no nula sobre la curva de dispersión. La elección incorrecta puede introducir errores sistemáticos en el perfil Vs obtenido.

El efecto del nivel freático es especialmente importante: en suelos secos, el ratio de Poisson típico es 0.1–0.3. Sin embargo, para un medio poroso saturado, el ratio de Poisson aparente puede ser cercano a 0.5 (comportamiento no drenado en términos de propagación de onda). Por tanto, **ignorar el nivel freático equivale a asumir densidades y ratios de Poisson incorrectos para las capas saturadas**, con consecuencias significativas sobre el perfil Vs invertido.

En el sitio Saluggia, el nivel freático fue identificado a 3 m de profundidad mediante un estudio de refracción de ondas P (que detecta la interfaz saturado/no saturado como un salto abrupto en la velocidad de onda P). Se realizaron tres inversiones con diferente hipótesis sobre el nivel freático (Figura 7.9, p. 362):

- **Inversión 1** (nivel freático correcto, 3 m): perfil Vs con incremento gradual consistente con la estratigrafía y validado por ensayo cross-hole.
- **Inversión 2** (sin nivel freático): perfil Vs fuertemente incorrecto; las diferencias son atribuidas erróneamente a variaciones de Vs.
- **Inversión 3** (nivel freático incorrecto a 7 m): sobreestimación sistemática de Vs a profundidad.

La moraleja es clara: **toda la información geotécnica disponible (incluyendo nivel freático y litología) debe integrarse en la selección de los parámetros a priori** del problema inverso. La sinergia entre el método de refracción P y las ondas superficiales es particularmente poderosa en contextos sedimentarios someros (ver sección 6.4.4 del libro).

> Figuras clave: 7.1 (p. 352), 7.2 (p. 354), 7.3 (p. 355), 7.4 (p. 356), 7.5 (p. 357), 7.6 (p. 358), 7.7 (p. 359), 7.8 (p. 360), 7.9 (p. 362), 7.10 (p. 363).

---

---

## 7.2 Comparación de estrategias de inversión — dataset activo + pasivo

**Sitio:** La Salle, Alpes italianos (abanico aluvial de material heterogéneo "caótico").
**Motivación:** En abanicos aluviales la variación de rigidez con la profundidad es gradual; las fuentes activas pesadas (Vibroseís) no siempre están disponibles. La combinación de datos activos y pasivos permite extender el rango de frecuencias y alcanzar profundidades mayores sin equipamiento costoso.

### 7.2.1 Dataset experimental

**Datos activos:** 48 geófonos verticales de 4.5 Hz con espaciado de 1.5 m (longitud total del arreglo: 70.5 m). Fuente: maza de 8 kg. Se apilaron 30 disparos para reducir ruido. El análisis en el dominio f-k (Figura 7.12, p. 365) permite obtener la curva de dispersión en el rango 10–40 Hz.

**Datos pasivos:** arreglo circular de 75 m de diámetro con geófonos verticales de 2 Hz. El procesamiento se realizó con el método de *frequency-domain beamformer* (Zywicki 1999): para cada frecuencia de interés, se construye el espectro de densidad espectral de potencia en función de número de onda en dos direcciones ortogonales (kx, ky). El pico del espectro identifica tanto la velocidad de propagación como la **dirección de llegada de la fuente dominante** (Figura 7.13, p. 365).

En este sitio, la fuente de microtremores (probablemente actividad de construcción a cientos de metros) llegaba desde una dirección preferencial. Esto invalida el uso de métodos que asumen campo difuso isotrópico (como [[SPAC Method|SPAC]]); el beamformer es apropiado porque no impone esa hipótesis. Se advierte que la identificación de fuentes también tiene aplicaciones en sismología urbana y estudios forenses.

**Curva de dispersión combinada:** la unión de datos activos (10–40 Hz) y pasivos (5–15 Hz) extiende la curva experimental hacia bajas frecuencias (Figura 7.14, p. 367). La incertidumbre de los datos activos es notablemente menor que la de los pasivos: el coeficiente de variación (CV = desviación estándar / media de VR) es <2% en datos activos y 3–6% en pasivos (Figura 7.15, p. 368).

**Estimación de profundidad de investigación y resolución:**

La longitud de onda máxima disponible determina la profundidad máxima investigable (aproximadamente λ/2):

$$\lambda_{\max} = \frac{V_R}{f} = \frac{780 \text{ m/s}}{5 \text{ Hz}} = 155 \text{ m} \quad \Rightarrow \quad z_{\max} \approx 80 \text{ m}$$

La longitud de onda mínima determina la resolución en capas superficiales:

$$\lambda_{\min} = \frac{250 \text{ m/s}}{41.5 \text{ Hz}} = 6 \text{ m} \quad \Rightarrow \quad \text{primera capa resoluble} \approx 3 \text{ m}$$

Estos criterios son guías prácticas derivadas de la relación entre [[Wavelength|longitud de onda]] de [[Rayleigh Waves|Rayleigh]] y profundidad de sensibilidad. Las capas más delgadas de 3 m o más profundas de 80 m no estarán bien constrenidas por este dataset.

> Figuras clave: 7.11 (p. 364), 7.12 (p. 365), 7.13 (p. 365), 7.14 (p. 367), 7.15 (p. 368).

### 7.2.2 Inversión empírica

Antes de resolver el problema inverso formalmente, puede obtenerse un perfil orientativo mediante la **mapeo directo de la curva de dispersión** (ver sección 6.3 del libro). Cada punto (f, VR) de la curva experimental se transforma en un punto del perfil pseudo-Vs usando:

$$V_s \approx 1.1 \cdot V_R(f) \quad \text{a profundidad} \quad z = \frac{\lambda}{2.5} = \frac{V_R / f}{2.5}$$

Esta relación se basa en el comportamiento de las [[Rayleigh Waves|ondas de Rayleigh]] en un [[Elastic Half Space|semiespacio elástico homogéneo]]: la [[Phase Velocity|velocidad de fase]] de Rayleigh es ligeramente inferior a Vs (≈ 0.92–0.95 × Vs), y la mayor parte de la energía penetra hasta λ/2–λ/3. El factor 1.1 y el denominador 2.5 son aproximaciones empíricas derivadas de ese contexto homogéneo.

El resultado es el **pseudo-perfil Vs** de la Figura 7.16a (p. 369): una curva continua (no en capas), directamente trazada desde la curva de dispersión. Este perfil **no puede sustituir una inversión formal** porque la relación Vs ≈ 1.1 VR solo es válida para medios normalmente dispersivos sin inversiones de velocidad. Sin embargo, es útil para:

- Obtener una primera estimación de la variación de rigidez con la profundidad.
- Construir el **modelo inicial** para procedimientos iterativos de inversión formal (Figura 7.16b, p. 369).

### 7.2.3 Inversión determinista (mínimos cuadrados)

La inversión determinista aplica el algoritmo de mínimos cuadrados con amortiguamiento de Herrmann (1994): un método de búsqueda local iterativo que minimiza la diferencia entre la curva de dispersión teórica y la experimental. El perfil obtenido de la inversión empírica sirve como modelo inicial (Figura 7.17, p. 370).

El perfil Vs resultante (Figura 7.18, p. 370) se compara con ensayos down-hole en dos sitios del mismo abanico aluvial (distancias ~1 km entre sitios). El acuerdo es significativo considerando la naturaleza del material y la heterogeneidad lateral esperada.

La **incertidumbre del perfil Vs** se estima propagando la incertidumbre de la curva de dispersión experimental a través de la linealización del problema inverso (método FOSM, sección 6.5.3 del libro). Las barras de error sobre el perfil Vs muestran que:

- En capas superficiales (donde dominan los datos activos con bajo CV), el CV de Vs es <1%.
- En capas profundas (donde dominan los datos pasivos con mayor CV), el CV de Vs sube hasta ~6%.

Crucialmente, **no hay amplificación del error**: el CV de salida no supera el de entrada. Esto indica que el proceso de inversión es bien condicionado para este dataset.

> Figuras clave: 7.16 (p. 369), 7.17 (p. 370), 7.18 (p. 370).

### 7.2.4 Inversión estocástica (Monte Carlo)

Los métodos de búsqueda local pueden quedar atrapados en mínimos locales de la función de desajuste (*misfit*). Para evaluar la [[Non-uniqueness|no-unicidad]] de la solución y obtener una caracterización probabilística del espacio de soluciones, se aplica el método de [[Monte Carlo Methods|Monte Carlo]] global de Socco & Boiero (2008).

El algoritmo genera una **población de 10⁵ modelos** de perfil Vs mediante muestreo aleatorio. Aprovecha las propiedades de escala de las curvas modales para guiar el muestreo de manera eficiente. Se aplica un **test de Fisher** para seleccionar el subconjunto de modelos aceptables: aquellos cuyo desajuste es estadísticamente compatible con la incertidumbre experimental. Los perfiles seleccionados se grafican en escala de grises según el misfit (más oscuro = menor misfit), como en la Figura 7.19 (p. 372).

Los resultados muestran que:
- Las capas superficiales son bien constrenidas: pequeño rango de variación en Vs.
- Las capas profundas presentan mayor incertidumbre: el rango de Vs aceptable es amplio (Figura 7.19).
- La curva de dispersión teórica de todos los modelos aceptables ajusta bien la curva experimental (Figura 7.20, p. 372), confirmando la equivalencia en términos de datos.

**Implicación en respuesta sísmica:** aunque los perfiles Vs difieren entre sí en profundidad, los espectros de respuesta 1D calculados con cada perfil son prácticamente idénticos (Figura 7.21, p. 373). Esto muestra que la **no-unicidad de la solución no necesariamente se traduce en incertidumbre práctica** para aplicaciones de ingeniería sísmica.

**Estimación de Vs,30:** el [[Vs30|parámetro Vs,30]] (velocidad de corte promedio en los primeros 30 m) calculado para cada perfil aceptable varía entre ~480 y 505 m/s (Figura 7.22, p. 374). La variación es estrecha, confirmando que Vs,30 es un parámetro robusto incluso ante la no-unicidad de la inversión.

> Figuras clave: 7.19 (p. 372), 7.20 (p. 372), 7.21 (p. 373), 7.22 (p. 374).

### 7.2.5 Inversión con medio verticalmente heterogéneo (continuo)

El modelo de capas horizontales es la representación estándar en la inversión de ondas superficiales. Sin embargo, en materiales de abanico aluvial la variación de rigidez con la profundidad es en realidad gradual (debida principalmente al incremento de presión de confinamiento). Representar este perfil continuo con escalones introduce una aproximación.

La inversión de la curva de dispersión de la Figura 7.14b utilizando un **modelo verticalmente heterogéneo continuo** (código de Rix & Lai 2013) produce un perfil Vs suave (Figura 7.23, p. 375). La comparación con el perfil por capas (Figura 7.18) muestra un buen acuerdo general, con la excepción de la capa más superficial: el perfil por capas exhibe un salto abrupto de Vs en los primeros metros, asociado a la capa de suelo vegetal, que el modelo continuo no reproduce bien. Para esa zona, la representación por capas es más apropiada.

Este ejemplo ilustra que la elección del modelo de referencia (capas vs. continuo) debe basarse en el conocimiento geológico del sitio: capas para estratigrafías diferenciadas, modelo continuo para depósitos granulares homogéneos con gradiente de compactación.

> Figura clave: 7.23 (p. 375).

---

---

## 7.3 Determinación conjunta de perfiles Vs y Ds

La cuantificación del [[Shear Damping Ratio|amortiguamiento material]] Ds es relevante para aplicaciones sísmicas porque la disipación de energía en ciclos histéreticos condiciona la amplificación del movimiento del suelo. Un suelo con mayor amortiguamiento disipa parte de la energía sísmica incidente, reduciendo la amplificación en la frecuencia de resonancia del depósito. Este parámetro no puede derivarse del perfil Vs ni está relacionado biunívocamente con ningún índice geotécnico estático; por tanto, debe estimarse de forma independiente mediante ensayos específicos.

Los ensayos de laboratorio (columna resonante, ensayos cíclicos triaxiales) pueden medir Ds sobre muestras, pero presentan dos limitaciones importantes: (1) representan volúmenes muy pequeños de suelo (~decenas de cm³), lo que dificulta la representatividad del volumen del depósito real, y (2) el valor de Ds depende del nivel de deformación impuesto, que en laboratorio puede diferir del nivel de campo bajo solicitación sísmica real.

Los ensayos in situ de ondas superficiales pueden estimar Ds en grandes volúmenes del depósito natural, bajo condiciones reales de presión de confinamiento y estructura del suelo. Sin embargo, para extraer Ds del coeficiente de atenuación experimental αR(ω), es necesario corregir la **atenuación geométrica** —disminución de amplitud por la expansión cilíndrica del frente de onda desde la fuente— y el efecto del [[Near-field Effect|campo cercano]] en los receptores más próximos. El incumplimiento de estas correcciones produce una sobreestimación sistemática de Ds (Capítulo 5).

La metodología de inversión simultánea de las curvas de dispersión y atenuación para obtener perfiles conjuntos Vs(z) y Ds(z) fue descrita en la Sección 6.4.3.4. Este capítulo presenta dos casos de aplicación en condiciones de campo reales: el sitio de **Memphis** (Tennessee, EE.UU.), con geología sedimentaria simple y nivel freático conocido, y la **Torre de Pisa** (Italia), con una estratigrafía compleja de relevancia histórico-geotécnica donde la comparación con ensayos cross-hole y columna resonante permite validar la metodología.

### 7.3.1 Memphis (Tennessee, EE.UU.)

**Sitio:** Mud Island, frente al centro de Memphis. Isla formada artificialmente por dragado del río Mississippi. Nivel freático a 8 m de profundidad. Perfil relativamente homogéneo.

**Adquisición:** La fuente de ondas fue un vibrador electrodinámico operado en modo *swept-sine* (frecuencia barrida) en el rango 3.75–100 Hz. Los receptores fueron acelerómetros verticales con respuesta plana en frecuencia (0.10–300 Hz), colocados a 15 distancias distintas desde la fuente: 2.44, 3.05, 3.66, 4.57, 5.49, 6.71, 8.54, 10.37, 12.80, 15.24, 18.29, 21.34, 24.39, 28.96 y 33.54 m. La aceleración de la armadura del vibrador también fue medida con un acelerómetro piezoeléctrico para estimar la fuerza de entrada y así calcular la función de transferencia.

**Procesamiento:** En cada receptor se calculó la función de transferencia experimental (cociente entre la señal registrada y la fuerza de entrada), promediada sobre 10 mediciones repetidas para reducir la varianza. Cada función de transferencia es compleja y contiene tanto información de fase (→ velocidad de fase, curva de dispersión) como de amplitud (→ coeficiente de atenuación). Se realizó una **regresión del número de onda complejo** contra la expresión analítica de la función de transferencia para un semiespacio viscoelástico (Ecuación 5.10 del libro), obteniéndose simultáneamente VR(f) y αR(f) a cada frecuencia. La Figura 7.24 (p. 376) muestra un ejemplo de la regresión para f = 33.78 Hz: la fase ajustada da VR = 163.11 m/s, y la amplitud ajustada da αR = 0.046 m⁻¹.

**Inversión:** Se aplicó mínimos cuadrados con amortiguamiento (Herrmann 1994) para invertir simultáneamente las curvas de dispersión y atenuación experimentales y obtener los perfiles de Vs(z) y Ds(z) (Sección 6.4.3.4 del libro). La Figura 7.25 (p. 377) compara las curvas experimentales y teóricas del mejor ajuste, tanto para dispersión como para atenuación.

**Resultados:** La Figura 7.26 (p. 378) muestra el perfil Vs comparado con un ensayo de cono de penetración sísmica (SCPT), y el perfil Ds en función de la profundidad. El acuerdo del perfil Vs con el SCPT es bueno. El perfil Ds es plausible físicamente, aunque la comparación con datos independientes de laboratorio no se reporta en este caso.

> Figuras clave: 7.24 (p. 376), 7.25 (p. 377), 7.26 (p. 378).

### 7.3.2 Pisa — Torre Inclinada

**Sitio:** La Torre de Pisa ha sido objeto de caracterización geotécnica exhaustiva para estudios de estabilidad. La estratigrafía es particularmente delicada:
- **0–10 m:** limo arenoso ligeramente arcilloso, con lentes de arena y arcilla.
- **10–50 m:** formación arcillosa (~30 m de espesor).
- **10–20 m:** zona de arcilla blanda muy uniforme — causa de los asentamientos diferenciales de la Torre.
- **Nivel freático:** 2–3 m de profundidad, con fluctuaciones estacionales marcadas.

**Adquisición:** Se usaron dos fuentes sísmicas para cubrir rangos de frecuencia complementarios: sistema de caída de peso de 130 kg desde 3 m (array largo, bajas frecuencias) y maza de 8 kg (array corto, altas frecuencias). Esto responde al trade-off entre longitud del arreglo y banda de frecuencia. Sismógrafo de 24 canales con geófonos de 4.5 Hz. El sitio de ensayo y la posición del ensayo cross-hole adyacente se muestran en la Figura 7.27 (p. 379).

**Procesamiento:** La función de transferencia experimental se obtiene mediante el procedimiento de deconvolución descrito en la Sección 5.3 del libro, que puede aplicarse cuando los receptores son equivalentes (misma respuesta en frecuencia). La regresión del número de onda complejo sobre el rango de frecuencias usable produce las curvas de dispersión y atenuación (Figura 7.28, p. 379).

**Inversión:** Mínimos cuadrados con amortiguamiento (Herrmann 1994), inversión simultánea para Vs y Ds. Los resultados se reportan en la Figura 7.29 (p. 380):

- **Perfil Vs vs. ensayo cross-hole (CHT):** el acuerdo es bueno, especialmente en capas más profundas. La homogeneidad lateral del depósito permite una comparación directa significativa.
- **Perfil Ds vs. dispositivo de columna resonante (RCT):** los valores obtenidos en laboratorio (muestras de alta calidad) y por el método SWM son consistentes para capas profundas. Sin embargo, en las capas más superficiales el SWM tiende a sobreestimar Ds.

**Por qué se sobreestima Ds en capas superficiales:** Las ondas superficiales de alta frecuencia (que sensorizan las capas someras) interactúan con heterogeneidades del medio. El *scattering* de energía en estas heterogeneidades introduce una atenuación aparente que no es material (no disipa calor) pero se comporta como tal en la señal registrada. Además, fenómenos de disipación distintos de la atenuación viscoelástica (como la fricción en la interfaz entre partículas) no están explícitamente modelados en el proceso de inversión. En consecuencia, el Ds estimado desde ondas superficiales puede considerarse como un **límite superior** del amortiguamiento material real en capas superficiales.

Este resultado es consistente con la dependencia en frecuencia del amortiguamiento en suelos: el ratio de amortiguamiento es más pronunciado en el rango de altas frecuencias, precisamente donde se obtiene la información de capas superficiales.

> Figuras clave: 7.27 (p. 379), 7.28 (p. 379), 7.29 (p. 380).

---

---

## 7.4 Tratamiento de modos superiores

En medios verticalmente heterogéneos, la curva de dispersión experimental puede ser en realidad una **curva de dispersión aparente**, resultante de la superposición de contribuciones de múltiples modos de propagación (véase Sección 2.4 del libro). Cuando la curva experimental no corresponde al modo fundamental sino a modos superiores —o alterna entre modos según el rango de frecuencias—, aplicar una inversión estándar que asume modo fundamental produce perfiles Vs erróneos.

Existen dos enfoques principales para manejar esta situación:

1. **Modelado de la curva aparente:** el modelo directo calcula la curva de dispersión aparente tomando en cuenta las contribuciones de todos los modos y la geometría de adquisición. El desajuste se define como la distancia entre la curva aparente experimental y la teórica. Es preciso pero computacionalmente costoso, y requiere evaluar derivadas parciales complejas para métodos de búsqueda local.

2. **Desajuste por determinante** (*determinant misfit*, Maraschini et al. 2010): el desajuste se define como el valor del **determinante de la matriz de transferencia de Haskell-Thomson** evaluado en los números de onda experimentales. En un [[Layered Media|medio estratificado]], las curvas de dispersión modales son exactamente los ceros de este determinante. Por tanto, si un punto experimental (k_exp, f) pertenece a cualquier modo de Rayleigh del modelo de referencia, el valor del determinante será cero. Para cualquier modelo que no coincida, el valor del determinante será distinto de cero. El desajuste se calcula como la suma de los valores del determinante evaluados en todos los puntos experimentales.

Las ventajas del *determinant misfit* son dobles: (1) **no es necesario asignar a priori los puntos experimentales a un modo específico** — el algoritmo acepta puntos de cualquier modo; (2) la evaluación del modelo directo es muy ligera computacionalmente porque no requiere buscar los ceros del determinante, solo evaluarlo en puntos conocidos. Esto lo hace especialmente adecuado para métodos globales de búsqueda con poblaciones de millones de modelos. La Figura 7.30 (p. 382) ilustra la superficie del determinante en el espacio (frecuencia, velocidad): los valles corresponden a las curvas modales.

**Ejemplo aplicado:** sitio de una pista no pavimentada, 24 geófonos verticales con espaciado 0.7 m, maza de 8 kg. La capa superficial es grava y guijarros compactados artificialmente (rígida). Por debajo hay un depósito aluvial-coluvial que yace sobre roca turbidítica débil (capa blanda intercalada). La estratigrafía implica una **inversión de velocidad** en el subsuelo: la capa superficial rígida, la roca blanda intermedia y el substrato rígido.

La curva de dispersión experimental muestra un incremento de velocidad con la frecuencia en el rango alto (Figura 7.31b, p. 383): la rama sigue modos superiores tanto en la banda alta de frecuencias (por la capa rígida superficial) como en la baja (por la roca dura). El modo fundamental queda "atrapado" en la capa blanda intermedia. La identificación de números de modo no es factible.

La inversión se realizó con Monte Carlo global sobre 10⁷ perfiles generados aleatoriamente, usando el *determinant misfit*. Los mejores perfiles (Figura 7.31a) recuperan la capa dura superficial coherente con la información geológica disponible, con una inversión de velocidad en la porción superficial del perfil. La Figura 7.31c muestra el valor del determinante de Haskell-Thomson del mejor modelo en escala de grises (más oscuro = más cercano a cero = mejor ajuste), con los puntos experimentales superpuestos como puntos blancos, confirmando que siguen las curvas modales sin pertenecer a un solo modo.

> Figuras clave: 7.30 (p. 382), 7.31a (p. 383), 7.31b (p. 383), 7.31c (p. 384).

---

## 7.5 Inversión de ondas superficiales en datos sísmicos de reflexión

Los datos de reflexión sísmica contienen con frecuencia ondas superficiales de alta energía, denominadas tradicionalmente **[[Ground Roll|ground-roll]]**. En el flujo de trabajo convencional de reflexión, el ground-roll se considera ruido coherente que se atenúa en campo (usando arreglos de receptores, fuentes de alta frecuencia) y se filtra en procesamiento. Sin embargo, desde la perspectiva del método de ondas superficiales, estas señales contienen información valiosa sobre el perfil de velocidad de corte de la zona superficial.

Si la geometría de adquisición no es demasiado agresiva contra las ondas superficiales, estas quedan bien preservadas en los registros de reflexión y pueden analizarse con las mismas técnicas descritas en capítulos anteriores. Las ventajas frente a un levantamiento dedicado de ondas superficiales son:
- **Fuentes potentes** (explosivos, vibroseis): alto SNR incluso a grandes offsets.
- **Gran rango de offsets:** mejora la resolución en número de onda y la separación modal.
- **Alta cobertura (fold) estadística:** la redundancia estadística permite curvas de dispersión más confiables.
- Cobertura espacial lateral densa → útil para construir modelos 2D y 3D de Vs.

### 7.5.1 Aplicación con datos de ingeniería en 2D

El caso presentado corresponde al mismo **sitio La Salle** (Alpes italianos) de la Sección 7.2, pero ahora usando dos líneas de reflexión sísmica previamente adquiridas (Socco et al. 2008, 2009). El mapa de la Figura 7.32 (p. 386) muestra las dos líneas de reflexión (L1 y L2), los pozos de down-hole y los puntos de ensayos activos/pasivos de ondas superficiales.

**Extracción de curvas de dispersión:** se aplica la técnica de **ventana deslizante** sobre los sismogramas de reflexión (Figura 7.33, p. 386): se extraen subventanas temporales solapadas a lo largo de la línea, y para cada posición de ventana se calcula el espectro f-k y se extrae la curva de dispersión experimental. Esto produce un conjunto de curvas de dispersión distribuidas espacialmente a lo largo de cada línea (Figura 7.34, p. 387), representando las propiedades de velocidad locales en cada posición.

**Inversión con restricción lateral:** los perfiles Vs obtenidos para cada ventana se invierten con un esquema de **inversión con restricciones laterales** (*laterally constrained inversion*): los perfiles 1D individuales están acoplados entre sí mediante penalizaciones que favorecen la suavidad lateral. Las Figuras 7.35 (p. 388) y 7.36 (p. 389) muestran los modelos Vs pseudo-2D para L1 y L2, superpuestos sobre las secciones de reflexión sísmica. Los resultados se comparan con ensayos down-hole (flechas largas) y ensayos activos/pasivos de ondas superficiales (flechas cortas), con buen acuerdo.

La limitación de profundidad es ~50 m, impuesta por el uso de geófonos de alta frecuencia en la reflexión (no adecuados para extraer bajas frecuencias de ondas superficiales). La extensión a mayor profundidad se logra combinando con los ensayos pasivos dedicados (Sección 7.2).

### 7.5.2 Aplicación con datos de exploración en 3D

En la industria de exploración, el uso de receptores individuales de punto (en lugar de arreglos geofónicos combinados) produce datos con mejor muestreo espacial de las ondas superficiales: sin aliasing, con longitudes de onda cortas accesibles y con heterogeneidades superficiales bien resueltas. La alta cobertura (miles de disparos para una sola posición receptora) ofrece una redundancia estadística extrema.

**Procesamiento:** a partir de 3D, se forman *supergathers* locales (trazas de todos los receptores dentro de una apertura definida alrededor de un punto). Para cada supergather se extrae la curva de dispersión mediante transformadas aptas para arreglos irregulares y bidimensionales. Las curvas de dispersión para todas las posiciones pueden organizarse en un **volumen de dispersión** (dispersion volume): velocidad de fase como función de las coordenadas geográficas (easting, northing) y longitud de onda. La Figura 7.37 (p. 390) muestra la pseudosección del modo fundamental para una línea receptora de 10 km.

**Cartografía geológica:** el volumen de dispersión puede ser "cortado" a una longitud de onda fija, produciendo un mapa de velocidades de fase que refleja variaciones laterales del subsuelo. La Figura 7.38 (p. 391) muestra una rebanada a λ = 130 m para un área de ~300 km² en Egipto (estudio de exploración, Strobbia et al. 2011): se identifican zonas de alta velocidad (lechos de wadis) y zonas de baja velocidad (fallas paralelas al sistema principal del Golfo de Suez), demostrando el potencial para **mapeo de estructuras geológicas superficiales** en proyectos de exploración en frontera.

La inversión puede ejecutarse de forma local (1D por posición) o con esquemas 2D/3D que añaden regularización lateral. El modelo Vs resultante (Figura 7.39, p. 392) tiene aplicaciones directas en: correcciones de estáticas para el procesamiento de reflexión, conversión Vs→Vp para modelado de velocidades, y descripción de la geología superficial para interpretación integrada.

> Figuras clave: 7.32–7.36 (pp. 386–389), 7.37 (p. 390), 7.38 (p. 391), 7.39 (p. 392).

---

> **Chapter 7 — estado:** completado (primera fase). Secciones 7.1–7.5 cubiertas.
