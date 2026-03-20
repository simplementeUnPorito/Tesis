# Chapter 6 — Inversion

**Fuente:** Sebastiano Foti, *Surface Wave Methods for Near-Surface Site Characterization*, Chapter 6, pp. 273–350 (aprox.)
**PDF prioritario:** Sebastiano Foti Chapter 6.pdf

---

## Síntesis del capítulo

La [[Inversión|inversión]] es el paso final de la interpretación de datos en el ensayo de ondas superficiales. Su objetivo es determinar el **perfil de velocidad de onda de corte Vs** —y eventualmente la [[Shear Damping Ratio|razón de amortiguamiento Ds]]— a partir de las [[Dispersion Relation|curvas de dispersión]] y/o atenuación medidas experimentalmente. Para ello se formula un **problema inverso**: encontrar los parámetros del modelo de subsuelo que reproducen los datos medidos.

El capítulo aborda este problema desde los fundamentos conceptuales hasta los algoritmos específicos:
- **6.1** Aspectos conceptuales: problemas directos e inversos, ill-posedness, estrategias de búsqueda
- **6.2** Modelización directa (*forward modeling*)
- **6.3** Métodos empíricos de inversión (SSRM, inversión manual)
- **6.4** Métodos analíticos de inversión (mínimos cuadrados, [[Tikhonov Regularization|regularización Tikhonov]], algoritmo de Occam, búsqueda global)
- **6.5** Incertidumbre en la inversión y enfoque bayesiano

---

## 6.1 Aspectos conceptuales

### 6.1.1 Problema directo e inverso en geofísica

El punto de partida es distinguir dos direcciones de análisis:

- **Problema directo (forward problem):** dado un modelo del subsuelo (parámetros mecánicos, espesor de capas, etc.), calcular la respuesta esperada —curva de dispersión o atenuación. Es un proceso de causa a efecto.
- **Problema inverso (backward/inverse problem):** dada la respuesta medida en campo, determinar los parámetros del modelo que la generan. Es el proceso de inferir causas desde efectos.

En la notación formal de Foti, si **G** es el operador matemático que representa el modelo físico, **m** los parámetros del modelo y **d** los datos observados, entonces:

$$G(m) = d \quad \text{(problema directo)}$$

El problema inverso busca determinar **m** conociendo **G** y **d**. En el caso de ondas superficiales, esto es un *problema de identificación de modelo* (categoría 2), que equivale a determinar los coeficientes de las ecuaciones diferenciales que gobiernan la propagación de ondas a partir del conocimiento de sus autovalores (velocidades de fase a distintas frecuencias).

> **Figura 6.1** (p. 276): Diagrama que ilustra la relación entre el problema directo (estimulación o convolución: G, m → d) y los dos tipos de problema inverso. Categoría 1: deconvolución (determinar m dado G y d). Categoría 2: identificación del modelo (determinar G dado m y d). El problema de ondas superficiales pertenece a la categoría 2.

> **Figura 6.2** (p. 276): Esquema conceptual del problema inverso geofísico. El subsuelo (geometría y propiedades mecánicas desconocidas) debe inferirse a partir de mediciones en superficie. Ilustra la irreductible incertidumbre del problema.

### 6.1.2 Ill-posedness: el problema del mal condicionamiento

Según Hadamard (1923), un problema matemático está **bien puesto** (*well-posed*) si cumple tres condiciones:
1. Existe solución (*existence*).
2. La solución es única (*uniqueness*).
3. La solución depende continuamente de los datos (*stability*).

Si alguna de estas condiciones falla, el problema es **ill-posed** (mal condicionado). Los problemas inversos violan habitualmente las condiciones de **unicidad** y **estabilidad**:

- **[[Non-uniqueness|No unicidad]]:** distintos perfiles de Vs pueden producir curvas de dispersión prácticamente idénticas. Matemáticamente, la información disponible no es suficiente para determinar unívocamente la solución. Ejemplo físico directo: distintas distribuciones de masa en el interior de la Tierra pueden producir el mismo campo gravitatorio en superficie.
- **Inestabilidad:** pequeñas variaciones en los datos de entrada (debidas a ruido o errores de medición) pueden traducirse en grandes cambios en el perfil resultante. Esto es particularmente grave en problemas no lineales, como la inversión de la curva de dispersión de Rayleigh.

En el caso de ondas superficiales, la no unicidad implica que **una misma curva de dispersión experimental puede corresponder a más de un perfil de Vs**. Esto no es una limitación del algoritmo de inversión, sino una propiedad intrínseca del problema físico.

**Estrategias de mitigación:**
- **Información a priori:** incorporar datos externos como perfiles de pozo (boreholes), ensayos SPT, mediciones de densidad, para restringir el espacio de soluciones admisibles.
- **Restricciones de suavidad o acotamiento:** forzar que los parámetros varíen dentro de rangos físicamente plausibles (por ejemplo, que la razón de amortiguamiento sea no negativa).
- **Métodos de regularización:** aproximar el problema ill-posed mediante una familia de problemas mejor condicionados. Los métodos de **regularización de Tikhonov** son los más utilizados y se desarrollan en la sección 6.4.

*Trazabilidad: Foti Cap. 6, §6.1.2, pp. 277–280*

### 6.1.3 Estrategias de inversión: local vs global

El problema de identificación de parámetros asociado con ondas superficiales se convierte en un problema de **optimización**: encontrar el vector de parámetros del modelo que minimiza una función de error entre la curva teórica y la experimental.

Los algoritmos de inversión se dividen en dos grandes familias:

**Métodos de búsqueda local (LS — Local Search):**
- Parten de un modelo inicial tentativo.
- En cada iteración, modifican los parámetros en la dirección que reduce el error de ajuste (típicamente calculando derivadas o el Jacobiano del operador G).
- Son **rápidos** y computacionalmente eficientes.
- **Limitación principal:** pueden converger a un mínimo local si el modelo inicial no está suficientemente cerca de la solución real. No hay forma simple de saber si la solución encontrada es un mínimo local o global.

**Métodos de búsqueda global (GS — Global Search):**
- Exploran el espacio de soluciones de forma más amplia (mediante cuadrícula sistemática, [[Monte Carlo Methods|Monte Carlo]], algoritmos genéticos, simulated annealing).
- Son **más robustos** frente a mínimos locales.
- Requieren mayor esfuerzo computacional.
- Ejemplos: Neighbourhood Algorithm, [[Monte Carlo Methods|Monte Carlo]], algoritmos evolutivos.

En la práctica, la mayoría de las inversiones de ondas superficiales utilizan métodos LS, usando la curva de dispersión modal o aparente como función de respuesta. Sin embargo, en perfiles inversamente dispersivos (con capas blandas o rígidas intercaladas), los métodos GS son más apropiados porque el espacio de soluciones puede tener múltiples mínimos.

> **Figura 6.3** (p. 282): Árbol taxonómico de los algoritmos para la solución del problema de identificación de parámetros con ondas superficiales. Clasifica los métodos por: tipo de inversión (global/local), tipo de análisis de atenuación (acoplado/desacoplado), tipo de movimiento H/V (acoplado/desacoplado), y tipo de función de respuesta (dominio frecuencia/tiempo, funciones modales/aparentes).

*Trazabilidad: Foti Cap. 6, §6.1.3, pp. 280–282*

---

## 6.2 Modelización directa (Forward Modeling)

La capacidad de resolver el problema inverso depende directamente de poder resolver eficientemente el **problema directo**: dado un modelo del subsuelo, calcular las curvas de dispersión y atenuación esperadas.

El modelo matemático del subsuelo debe especificar tres aspectos:

### 6.2.1 Modelo geométrico

Define cómo se idealiza la variabilidad espacial del subsuelo. Las opciones son:
- **Modelo 1D (unidimensional):** las propiedades mecánicas solo varían con la profundidad (modelo lateralmente homogéneo). Es el estándar en la práctica habitual de ensayos de ondas superficiales.
- **Modelos 2D/3D:** permiten variabilidad lateral. Son más realistas en sitios con complejidad geológica, pero mucho más costosos computacionalmente. Están disponibles en aplicaciones avanzadas.

La elección incorrecta del modelo geométrico puede introducir errores sistemáticos graves. Si el sitio tiene variabilidad lateral significativa y se usa un modelo 1D, los resultados serán sesgados.

### 6.2.2 Modelo numérico (discretización)

Determina cómo se representa matemáticamente el modelo geométrico:

- **Modelo discontinuo por capas (layered model):** el subsuelo se representa como un conjunto de capas horizontales homogéneas sobre un semiespacio. Dentro de cada capa, las propiedades son constantes. Es el esquema más utilizado en la práctica (Figura 6.4a).
- **Modelo continuo:** las propiedades varían continuamente con la profundidad. Es más apropiado para suelos homogéneos donde la velocidad aumenta gradualmente por el aumento de la presión de confinamiento con la profundidad (Figura 6.4b).

> **Figura 6.4** (p. 283): Comparación visual entre (a) modelo numérico discontinuo estratificado — el perfil Vs vs profundidad tiene forma de escalera — y (b) modelo numérico continuo — el perfil Vs varía de forma suave y continua. La elección entre ambos depende de las características geológicas del sitio.

### 6.2.3 Modelo constitutivo

Describe el comportamiento mecánico de los geomateriales bajo excitaciones dinámicas de baja amplitud:

- **Elasticidad lineal:** adecuada cuando la atenuación es despreciable o no interesa.
- **Viscoelasticidad lineal:** permite describir simultáneamente la dispersión y la atenuación. Es el modelo más común cuando se quiere invertir también la curva de atenuación.
- **Poroelasticidad (Biot):** reconoce la naturaleza multicomponente de los suelos saturados. Rara vez se usa en inversión de ondas superficiales porque el problema directo es considerablemente más complejo. Importante excepción: en sitios con nivel freático superficial, el coeficiente de Poisson debe reflejar correctamente las condiciones de saturación, ya que es muy diferente en materiales saturados respecto a materiales secos bajo carga dinámica no drenada.

### 6.2.4 Formulación del problema directo para inversión

Para un medio multicapa, el problema directo se escribe de forma vectorial:

**Dispersión (no lineal):**
$$G(V_s) = V_{R/L}$$

donde $V_s = [(V_s)_1, \ldots, (V_s)_{nl}]$ es el vector de velocidades de corte por capa y $V_{R/L}$ la curva de dispersión de Rayleigh (o Love). Este operador **G** es no lineal.

**Atenuación (lineal bajo disipación débil):**
$$G \cdot D_s = \alpha_{R/L}$$

donde $D_s$ es el vector de razones de amortiguamiento por capa y $\alpha_{R/L}$ la curva de atenuación. Este problema es **lineal**, lo que lo hace matemáticamente más tratable.

En resumen, existen tres tipos de problema directo en ondas superficiales: (I) predecir la dispersión desde $V_s$, (II) predecir la atenuación desde $D_s$, y (III) predecir la función de dispersión compleja desde el perfil de velocidad complejo $V_s^*$. Los problemas I y III son no lineales; el problema II es lineal.

*Trazabilidad: Foti Cap. 6, §6.2, pp. 282–286*

---

## 6.3 Inversión empírica — SSRM y métodos manuales

### 6.3.1 Método SSRM (Steady-State Rayleigh Method)

El método más antiguo y simple de inversión empírica es el **SSRM**, precursor de los modernos métodos espectrales (SASW, MASW).

**Fundamento físico:** en un semiespacio elástico homogéneo, la onda de Rayleigh tiene una velocidad de fase $V_R$ próxima a la velocidad de corte del medio: $V_R \approx 0.92 \cdot V_s$. Inversamente, $V_s \approx 1.1 \cdot V_R$. Además, el movimiento de onda superficial está confinado principalmente en la zona de la *skin depth* (~1 longitud de onda de profundidad), y la mayor parte de la energía se concentra dentro de los primeros $\lambda/3$ de profundidad.

**Procedimiento (Figura 6.5, p. 287):**
Para cada frecuencia del ensayo:
1. Medir la velocidad de fase $V_R^*$ y la longitud de onda $\lambda_R^*$.
2. Estimar $V_s \approx 1.1 \cdot V_R^*$.
3. Asignar ese valor de $V_s$ a la profundidad $z \approx \lambda_R^*/3$.
4. Repetir para todas las frecuencias disponibles → construir el perfil $V_s(z)$.

> **Figura 6.5** (p. 287): Esquema del procedimiento empírico SSRM. El diagrama muestra el mapeo desde el dominio $\{V_R, \lambda_R\}$ (izquierda) al dominio $\{V_s, \text{profundidad}\}$ (derecha).

**Limitaciones (Figura 6.6, p. 288):**
El método solo funciona bien para **perfiles normalmente dispersivos** (velocidad Vs aumenta monotónicamente con la profundidad — caso A en Fig. 6.6). En perfiles inversamente dispersivos (capa blanda intermedia = caso B; capa rígida superficial = caso C), el método falla en capturar la estructura real. Sin embargo, el perfil obtenido puede usarse como **modelo de referencia inicial** para algoritmos de inversión iterativos más rigurosos.

> **Figura 6.6** (p. 288): Resultados de la inversión empírica SSRM para tres perfiles sintéticos (A, B, C). Muestra el perfil real (línea negra continua) vs las estimaciones con distintos valores de λ/3, λ/2.5, λ/2. El caso A (normalmente dispersivo) tiene un ajuste aceptable; los casos B y C (inversamente dispersivos) presentan desviaciones significativas.

### 6.3.2 Inversión manual

Los métodos empíricos también incluyen los procedimientos **trial-and-error** (ensayo y error), en los que el operador ajusta manualmente los parámetros del modelo hasta obtener una curva teórica que visualmente reproduzca la experimental.

Requieren disponibilidad de un algoritmo de problema directo (forward solver). Son subjetivos y operador-dependientes, pero tienen la ventaja de que un operador experimentado puede converger a una solución razonable incluso en casos donde los algoritmos automáticos fallan (por ejemplo, curvas de dispersión "patológicas" donde el cálculo del Jacobiano es inestable).

*Trazabilidad: Foti Cap. 6, §6.3, pp. 286–289*

---

## 6.4 Inversión analítica

### 6.4.1 Medidas de bondad de ajuste

Antes de desarrollar algoritmos de inversión, es necesario definir qué significa "ajustar bien" los datos. El problema de ajustar una curva teórica a los datos experimentales es un **problema de regresión**, y la calidad del ajuste depende de la norma usada para medir el error.

El **error de predicción** entre los datos medidos **d** y los datos predichos **Gm** se escribe genéricamente como:

$$Er = \sum_{i=1}^{N} \left[ d_i - \sum_{j=1}^{M} (G_{ij} m_j) \right]^2$$

Este es el error en norma L₂. La solución que minimiza este error para un modelo lineal es la **solución de mínimos cuadrados**:

$$\mathbf{m} = (\mathbf{G}^T \mathbf{G})^{-1} \mathbf{G}^T \mathbf{d} \qquad (6.6)$$

**Normas alternativas (Lp):** la norma L₂ asigna mayor peso a errores grandes, haciéndola sensible a *outliers*. La norma L₁ es más robusta porque da igual peso a todos los errores. En general, la norma Lp de orden p > 2 amplifica aún más los errores grandes. La norma óptima depende de la distribución estadística de los errores: si los errores son gaussianos, L₂ es el estimador de máxima verosimilitud; si son de distribución exponencial doble, lo es L₁.

> **Figura 6.7** (p. 291): Ejemplo de regresión lineal con normas L₂, L₁ y Lp ante la presencia de un *outlier*. La L₂ es desviada por el outlier; la L₁ es más robusta. La Lp con p grande sigue la tendencia principal pero ignora el outlier.

**Implicación práctica:** en la inversión de curvas de dispersión, se suele usar L₂ por su tratabilidad matemática. Sin embargo, si los datos contienen mediciones atípicas (por ejemplo, por contaminación de modos superiores en ciertas frecuencias), considerar normas alternativas puede mejorar la robustez de la inversión.

*Trazabilidad: Foti Cap. 6, §6.4.1, pp. 289–292*

---

### 6.4.2 Problema inverso lineal

#### 6.4.2.1 SVD y la inversa generalizada de Moore-Penrose

El problema de inversión lineal se formula como **G·m = d**, donde **G** es una matriz N×M. Cuando el sistema no es cuadrado (N ≠ M) o no es de rango completo, la solución clásica (Ec. 6.6) puede no existir o no ser única. La solución general se obtiene mediante la **descomposición en valores singulares (SVD)**.

**Intuición física de la SVD:** cualquier matriz G puede descomponerse en tres factores que tienen interpretación geométrica clara: dos rotaciones (Q₁ y Q₂) y un escalado (Σ). Los valores singulares de Σ miden qué tan bien cada dirección del espacio de datos está conectada con el espacio de parámetros del modelo. Valores singulares grandes → buena conexión, estable. Valores singulares pequeños → conexión débil, inestable.

**Formulación (Ec. 6.9):**
$$\mathbf{G} = \mathbf{Q}_1 \mathbf{\Sigma} \mathbf{Q}_2^T$$

donde Q₁ es N×N ortogonal (espacio de datos), Q₂ es M×M ortogonal (espacio de parámetros), y Σ es N×M diagonal con los **valores singulares** s_i ≥ 0.

**Inversa generalizada de Moore-Penrose (Ec. 6.11–6.12):**
$$\mathbf{G}^{-g} = (\mathbf{Q}_2)_q \mathbf{\Sigma}_q^{-1} (\mathbf{Q}_1^T)_q$$
$$\mathbf{m} = \mathbf{G}^{-g} \mathbf{d} = (\mathbf{Q}_2)_q \mathbf{\Sigma}_q^{-1} (\mathbf{Q}_1^T)_q \mathbf{d}$$

donde q es el rango de **G**. Esta inversa generalizada funciona para cualquier combinación de N y M:
- **Sobredeterminado (N > M):** proporciona la solución de mínimos cuadrados (idéntica a Ec. 6.6).
- **Subdeterminado (N < M):** proporciona la solución de mínima norma L₂ (mínima longitud). Esta solución no siempre es físicamente razonable para ondas superficiales.
- **Mixto-determinado:** combinación de los anteriores. Ocurre frecuentemente en geofísica cuando las capas superficiales están bien iluminadas (sobredeterminadas) y las capas profundas mal iluminadas (subdeterminadas).

> **Figura 6.8** (p. 295): Ilustración del problema mixto-determinado en geofísica. Las capas superficiales son recorridas por múltiples rayos sísmicos (sobredeterminadas), mientras que las capas profundas no son alcanzadas por ningún rayo (subdeterminadas, zona "dark"). El modelo correcto debe respetar la profundidad de investigación máxima.

**Implicación práctica:** al diseñar un experimento MASW o SASW, conviene asegurarse de que el rango de frecuencias muestreado corresponda a profundidades de investigación realistas, de modo que el problema resulte sobredeterminado y la solución de mínimos cuadrados sea única y estable.

#### 6.4.2.2 Número de condición e inestabilidad

La solución SVD se puede reescribir como:
$$\mathbf{m} = \sum_{i=1}^{q} \frac{[(\mathbf{Q}_1^T)_i \cdot \mathbf{d}]}{s_i} [(\mathbf{Q}_2)_i] \qquad (6.13)$$

Los coeficientes de la expansión son proporcionales a **1/sᵢ**: los valores singulares pequeños amplifican el ruido de los datos. Esto es la raíz matemática de la inestabilidad.

El **número de condición** cuantifica el grado de inestabilidad:
$$cond(\mathbf{G}) = \frac{s_1}{s_k} \qquad (6.14)$$

donde s₁ es el mayor valor singular y s_k es el menor. Un número de condición grande indica un problema muy mal condicionado: pequeñas perturbaciones en **d** producen grandes cambios en **m**.

Importante: la ill-posedness es una propiedad intrínseca de la matriz **G** (es decir, del diseño del experimento y la geometría del problema), no del algoritmo utilizado. No se puede resolver con un mejor algoritmo; solo se puede mitigar con regularización o información a priori.

*Trazabilidad: Foti Cap. 6, §6.4.2.1–6.4.2.2, pp. 293–298*

#### 6.4.2.3 Regularización de Tikhonov

La **[[Tikhonov Regularization|regularización de Tikhonov]]** es la técnica más sistemática para mitigar la ill-posedness. La idea central es modificar el problema de minimización añadiendo un término de penalización que controla la complejidad de la solución:

**Regularización de orden cero (Ec. 6.15):**
$$\min \left\{ \|\mathbf{Gm} - \mathbf{d}\|_2^2 + \mu^2 \|\mathbf{m}\|_2^2 \right\}$$

El parámetro μ (multiplicador de Lagrange) controla el trade-off entre:
- minimizar el error de ajuste a los datos (primer término)
- mantener la solución simple / pequeña (segundo término)

Con μ = 0, se recupera el problema de mínimos cuadrados original (sin regularización). Con μ grande, la solución es forzada hacia valores pequeños, reduciendo la inestabilidad pero aumentando el error de ajuste.

**Solución (Ec. 6.16–6.17) — mínimos cuadrados amortiguados:**
$$\mathbf{m} = (\mathbf{G}^T\mathbf{G} + \mu^2 \mathbf{I})^{-1} \mathbf{G}^T \mathbf{d}$$

En términos SVD, los coeficientes de la expansión se multiplican por **factores de filtro** $s_i^2/(s_i^2 + \mu^2)$: los valores singulares grandes (estables) se preservan casi sin cambios, mientras que los pequeños (inestables) son fuertemente amortiguados.

**Regularización de orden superior (Ec. 6.18–6.20):**
En lugar de penalizar la norma de **m**, se penaliza la derivada del perfil:
$$\min \left\{ \|\mathbf{Gm} - \mathbf{d}\|_2^2 + \mu^2 \|\mathbf{L}^n \mathbf{m}\|_2^2 \right\}$$

donde **L** es la **matriz de rugosidad** (diferencias finitas centradas, Ec. 6.19):
- **n = 1**: penaliza el gradiente del perfil (favorece perfiles suaves con variación lenta con la profundidad)
- **n = 2**: penaliza la curvatura (favorece perfiles aún más suaves)
- **n = 0**: regularización de orden cero (penaliza la amplitud)

La regularización de orden superior es especialmente apropiada en geofísica porque es físicamente razonable esperar que las propiedades del suelo varíen de forma gradual con la profundidad.

**Implicación práctica:** la elección del orden de regularización y del valor de μ afecta directamente el perfil de Vs resultante. Un μ demasiado pequeño produce perfiles con oscilaciones espurias; uno demasiado grande produce perfiles excesivamente suaves que pierden detalles reales de la estratigrafía. La determinación del μ óptimo requiere criterios como la curva L (*L-curve*) o el principio de discrepancia.

#### 6.4.2.4 Otros métodos de regularización

- **Constraints de bounds:** se impone que los parámetros permanezcan en rangos físicamente admisibles (por ejemplo, Ds ≥ 0). Se resuelven con multiplicadores de Lagrange o mínimos cuadrados con restricciones.
- **Variación total (*total variation*):** usa la norma L₁ en lugar de L₂ para la penalización del gradiente. A diferencia de Tikhonov, no penaliza las discontinuidades abruptas, lo que lo hace adecuado para sitios con interfaces geológicas bien definidas entre capas de propiedades muy diferentes.

#### 6.4.2.5 Resolución y matrices de resolución

Una vez obtenida la solución, cabe preguntarse: ¿qué tan bien están determinados los parámetros del modelo?

**Matriz de resolución del modelo (Ec. 6.21–6.23):**
$$\mathbf{R}_m = \mathbf{G}^{-g} \mathbf{G}$$

Si Rm = I (identidad), los parámetros están perfectamente resueltos. En la práctica, Rm difiere de I: los elementos diagonales menores que 1 indican que el parámetro correspondiente está "promediado" con sus vecinos. Cuanto más próximos a 1 los elementos diagonales, mejor resuelta está esa capa.

**Matriz de resolución de los datos (Ec. 6.22):**
$$\mathbf{R}_d = \mathbf{G} \mathbf{G}^{-g}$$

Rd describe qué tan bien los datos predichos reproducen los datos observados.

**Función de spread de Dirichlet (Ec. 6.24):**
$$\text{spread}(\mathbf{R}_m) = \|\mathbf{R}_m - \mathbf{I}\|_2^2$$

Cuanto menor el spread, más cerca está Rm de la identidad y mejor resueltos los parámetros.

*Trazabilidad: Foti Cap. 6, §6.4.2.3–6.4.2.5, pp. 298–303*

---

### 6.4.3 Problema inverso no lineal

La inversión de la curva de [[Dispersion Relation|dispersión]] de Rayleigh (Ec. 6.2) es intrínsecamente **no lineal**: la relación entre el perfil de Vs y la curva de dispersión no puede escribirse como una multiplicación matricial simple. Esto complica enormemente el problema.

#### 6.4.3.1 Linealización por transformación de variables

Algunos problemas no lineales pueden convertirse en lineales mediante una transformación de variables. El ejemplo más directo en ondas superficiales es la medición de la **curva de atenuación**:

La ecuación de regresión para la atenuación (Ec. 6.25) es no lineal:
$$|T(r,0,\omega)| = |T(r,\omega)| \cdot \frac{C}{\sqrt{r}} \cdot e^{-\alpha_R(\omega) \cdot r}$$

Aplicando logaritmo a ambos lados (Ec. 6.26), el problema se convierte en una regresión lineal:
$$\log\left(\sqrt{r} \cdot |T(r,\omega)|\right) = \log C - \alpha_R(\omega) \cdot r$$

**Advertencia importante:** la linearización por transformación de variables introduce un sesgo sistemático en la solución, porque la transformación altera la distribución estadística de los errores (que ya no serán gaussianos) y la estructura de varianza de los datos. En la Figura 6.9, los coeficientes de atenuación obtenidos con la regresión no lineal y la linealizada difieren en ~30%.

> **Figura 6.9** (p. 304): Comparación entre (a) regresión no lineal y (b) regresión lineal (linearizada) para la medición de la curva de atenuación a 69.5 Hz. Ambas tienen R² = 0.98 pero producen valores distintos de αR.

#### 6.4.3.2 Métodos LS iterativos y técnicas GS

Cuando la linearización no es posible o introduce sesgos inaceptables, se recurre a métodos iterativos. La expansión en serie de Taylor de G(m) alrededor de un modelo inicial m₀ da:

$$\mathbf{G}(\mathbf{m}) \approx \mathbf{G}(\mathbf{m}_0) + \mathbf{J}(\mathbf{m})_{\mathbf{m}_0} \cdot (\mathbf{m} - \mathbf{m}_0) \qquad (6.29)$$

donde **J** es la **matriz Jacobiana** (gradiente del operador G respecto a los parámetros del modelo). Truncando a primer orden, el problema no lineal se convierte localmente en lineal y puede resolverse con los métodos de la sección 6.4.2. Iterando este proceso:

$$\mathbf{m}_{k+1} = (\mathbf{J}_k^T \mathbf{J}_k)^{-1} \mathbf{J}_k^T \cdot \left\{ \mathbf{J}_k \cdot \mathbf{m}_k + [\mathbf{d} - \mathbf{G}(\mathbf{m}_k)] \right\} \qquad (6.32)$$

Esta es la base del método de **Gauss-Newton** y sus variantes (Levenberg-Marquardt, gradiente descendente conjugado). El método de **Levenberg-Marquardt** es el más usado en inversiones no lineales de tamaño pequeño a mediano.

**El problema de los mínimos locales:** en problemas no lineales, la función de error E(m) puede tener múltiples mínimos locales. Dependiendo del modelo inicial, el algoritmo puede converger a un mínimo local en lugar del global.

> **Figura 6.10** (p. 307): Comparación del error de predicción E(m) como función del parámetro del modelo para (a) problema no lineal (superficie con múltiples mínimos) y (b) problema lineal (paraboloide con mínimo único). El problema no lineal requiere encontrar el mínimo global entre múltiples mínimos locales.

> **Figura 6.11** (p. 308): Cuatro casos típicos de complejidad creciente del espacio de soluciones en inversión no lineal: (a) mínimo único bien definido, (b) dos mínimos globales igualmente válidos, (c) múltiples mínimos periódicos (no unicidad severa), (d) "fondo plano" — rango continuo de soluciones (ill-conditioning extremo).

**Métodos de búsqueda global (GS):** diseñados para evitar los mínimos locales explorando el espacio completo de soluciones. Incluyen:
- **Estrategia multistart:** lanzar múltiples búsquedas LS desde modelos iniciales aleatorios y quedarse con la mejor solución.
- **Algoritmos genéticos:** mimetizan procesos evolutivos (selección, cruzamiento, mutación) para explorar simultáneamente el espacio de soluciones.
- **Simulated annealing:** permite aceptar soluciones peores temporalmente (con cierta probabilidad) para escapar de mínimos locales.
- **Monte Carlo:** exploración estadística exhaustiva del espacio de parámetros.

Los métodos GS son más robustos que los LS pero computacionalmente mucho más costosos. Son especialmente importantes para perfiles inversamente dispersivos.

#### 6.4.3.3 Jacobiano analítico vs numérico

Todos los métodos LS iterativos requieren calcular el **Jacobiano** J(m) en cada iteración. Existen dos aproximaciones:

- **Jacobiano numérico:** se calcula perturbando cada parámetro y evaluando G(m + δm) – G(m). Es general pero computacionalmente costoso (requiere nl + 1 evaluaciones del problema directo por iteración) y numéricamente inestable.
- **Jacobiano analítico:** derivadas exactas de G(Vs) respecto a Vs calculadas mediante fórmulas explícitas. Para la velocidad de fase de Rayleigh VR, existen expresiones analíticas exactas (Ec. 6.33) derivadas de los principios variacionales de Love y Rayleigh.

La ventaja clave del Jacobiano analítico en ondas superficiales es que puede calcularse con los mismos eigenfunciones del problema directo (sin perturbaciones adicionales), lo que lo hace eficiente y estable.

**Observación importante sobre Vp:** la velocidad de fase de Rayleigh es relativamente insensible a cambios en Vp (o equivalentemente en la razón de Poisson). Esto produce un "fondo plano" en la función de error (Figura 6.11d) cuando se intenta invertir Vp. Por eso, en la práctica, Vp (o la razón de Poisson) se asume conocida a priori y solo se invierte Vs.

#### 6.4.3.4 Algoritmo de Occam — inversión conjunta de dispersión y atenuación

El **algoritmo de Occam** (Constable et al. 1987, adaptado por Lai 2005) es el método más completo presentado en el capítulo: realiza la **inversión conjunta** de la curva de dispersión y la curva de atenuación simultáneamente, usando la teoría de variables complejas para tratar ambas curvas como una sola función compleja.

**Motivación física:** en medios viscoelásticos, la [[Phase Velocity|velocidad de fase]] y la atenuación no son independientes — están relacionadas por la dispersión material (relaciones de Kramers-Krönig). Invertirlas por separado (inversión desacoplada) introduce errores sistemáticos porque:
1. Los parámetros Vs y Ds se obtienen de dos inversiones independientes, y la incertidumbre de la primera se propaga a la segunda.
2. La inversión acoplada usa una restricción interna (las ecuaciones de Cauchy-Riemann) que mejora el condicionamiento del problema.

**Formulación (Ec. 6.34–6.35):**
El problema directo se escribe en términos de la velocidad de onda de corte **compleja**:
$$\mathbf{G}^*(V_s^*) = V_R^* \qquad (6.34)$$

donde $V_s^* = V_s(1 + iD_s)$ encapsula simultáneamente la velocidad de corte real y la razón de amortiguamiento en un solo parámetro complejo.

**Procedimiento iterativo (Ec. 6.44):**
En cada iteración, el algoritmo busca el perfil $V_s^*$ más suave (mínima rugosidad R₁ o R₂) compatible con un error de ajuste aceptable $\tilde{Er}$:
$$V_s^* = \left\{ \mu(\mathbf{L}^T\mathbf{L}) + [\mathbf{W}^* \cdot (\mathbf{J}^*)_{V_{s0}}]^H \cdot [\mathbf{W}^* \cdot (\mathbf{J}^*)_{V_{s0}}] \right\}^{-1} \cdot [\ldots]$$

El parámetro μ es el multiplicador de Lagrange (parámetro de suavizado) ajustado iterativamente para que el error residual sea igual a $\tilde{Er}$. La restricción de que $V_s^*$ solo tenga partes imaginarias negativas garantiza que el amortiguamiento Ds sea siempre positivo.

Una vez convergido, se recuperan Vs y Ds de la parte real e imaginaria de $V_s^*$ (Ec. 6.45).

> **Figura 6.12** (p. 318): Ajuste entre curvas sintéticas de dispersión (superior) y atenuación (inferior) de Rayleigh y las curvas teóricas obtenidas con el algoritmo de Occam, convergiendo en 3 iteraciones.

> **Figura 6.13** (p. 319): Perfiles Vs y Ds obtenidos de la inversión conjunta con Occam para el medio de la Tabla 6.1 (4 capas + semiespacio). Los perfiles recuperados coinciden bien con los perfiles reales.

**Tabla 6.1** (p. 319): Parámetros del medio sintético usado para la validación del algoritmo de Occam: 4 capas (espesores 5, 10, 10 m + semiespacio), Vp entre 400–1000 m/s, Vs entre 200–500 m/s, Ds entre 0.020–0.035, ρ = 1.7–1.8 Mg/m³. El medio es **normalmente dispersivo**.

*Trazabilidad: Foti Cap. 6, §6.4.3, pp. 303–320*

---

### 6.4.4 Información a priori en la inversión

La información a priori es la herramienta más efectiva para mitigar la no unicidad del problema inverso de ondas superficiales. En la práctica, los ensayos de ondas superficiales suelen ejecutarse en conjunto con otras técnicas geotécnicas y geofísicas que proporcionan información complementaria.

#### Registros de pozo (boreholes)

Si se dispone de información estratigráfica de pozos cercanos, los **espesores de capa** pueden fijarse como parámetros conocidos en la inversión, reduciendo significativamente el número de incógnitas. Esto mejora el condicionamiento del problema y produce perfiles de Vs más confiables. Si no hay datos de pozo, una regla práctica es asumir espesores de capa que aumenten con la profundidad, para reflejar la disminución intrínseca de la resolución con la profundidad en los métodos no invasivos.

#### Refracción sísmica de ondas P

Las configuraciones de adquisición MASW y las de refracción sísmica de ondas P son compatibles (misma geometría fuente-receptor), por lo que es fácil realizar ambas campañas simultáneamente. La refracción P proporciona:
- **Profundidad al lecho rocoso** (bedrock): puede usarse como cota fija en el modelo de inversión.
- **Posición del nivel freático**: afecta la [[Phase Velocity|velocidad de Vp]] y la razón de Poisson, que es muy diferente en suelos saturados y secos. Aunque la curva de dispersión de Rayleigh no es muy sensible a Vp, si la posición del nivel freático no se conoce y se asume incorrectamente, los resultados de la inversión pueden estar sesgados.

> **Figura 6.14** (p. 322): Inversión de datos de ondas superficiales con restricciones de la refracción P. (a) Curvas de dispersión teórica y experimental. (b) Perfiles Vs de ondas superficiales (SWM) y Vp de refracción, mostrando coherencia entre ambos métodos.

#### Inversión conjunta de datos geofísicos

Los métodos de sondeo eléctrico vertical (VES) y de ondas superficiales comparten estructuras de modelización muy similares (modelo 1D en capas), lo que permite una **inversión conjunta** que determina simultáneamente la resistividad eléctrica, Vs y los espesores de capa. La inversión conjunta produce un problema mejor condicionado que las dos inversiones independientes: con nl capas, la inversión conjunta determina 3nl incógnitas (Vs, resistividad, espesor), mientras que cada inversión individual determina solo 2nl – 1. La solución del problema conjunto es matemáticamente más bien-condicionado.

*Trazabilidad: Foti Cap. 6, §6.4.4, pp. 320–323*

---

## 6.5 Incertidumbre en la inversión

La incertidumbre es un aspecto fundamental de cualquier proceso de medición e inversión. En ondas superficiales, hay dos fuentes principales de incertidumbre que se propagan de forma acumulada:
1. **Incertidumbre de los datos:** errores en la medición de la curva de dispersión y atenuación.
2. **Incertidumbre del modelo:** cómo esos errores se proyectan en el perfil de Vs y Ds resultante.

### 6.5.1 Problemas lineales con errores gaussianos

Si el problema inverso es lineal y los errores de los datos son **gaussianos**, la propagación de la incertidumbre tiene solución exacta. Si los datos **d** son una variable aleatoria normal con media E(d) y covarianza Cov(d), entonces los parámetros del modelo **m = G⁻ᵍd** son también normalmente distribuidos con:

$$\begin{cases} E(\mathbf{m}) = \mathbf{G}^{-g} E(\mathbf{d}) \\ \text{Cov}(\mathbf{m}) = \mathbf{G}^{-g} \text{Cov}(\mathbf{d}) (\mathbf{G}^{-g})^T \end{cases} \qquad (6.47)$$

**Verificación de gaussianidad:** antes de aplicar estas fórmulas, debe verificarse que los datos siguen una distribución normal. El test estándar es el **test chi-cuadrado** (χ²), que compara la distribución de frecuencias observada con la esperada para una gaussiana.

> **Figura 6.15** (p. 326): Distribución de frecuencia relativa de velocidades de fase experimentales medidas en un sitio real en Italia a f = 11.5 Hz, comparada con la distribución gaussiana ajustada. El ajuste es razonablemente bueno.

> **Figura 6.16** (p. 327): Gráfica de χ² vs frecuencia para el conjunto de datos. Todos los puntos caen bajo el umbral χ²₀.₀₅, confirmando que la hipótesis de gaussianidad es válida en todo el rango de frecuencias de interés.

**Problemas no lineales:** si la inversión es no lineal, los errores gaussianos de los datos se mapean en distribuciones no gaussianas de los parámetros del modelo, complicando el análisis. La aproximación práctica más usada es el método **FOSM (First-Order Second-Moment)**, que usa el Jacobiano en el punto de convergencia para linealizar la relación datos-parámetros:

$$\text{Cov}[\mathbf{m}] \approx \left[ (\mathbf{J}^T \text{Cov}[\mathbf{d}]^{-1} \mathbf{J})^{-1} \mathbf{J}^T \text{Cov}[\mathbf{d}]^{-1} \right]_{\text{last}} \cdot \text{Cov}[\mathbf{d}] \cdot [\ldots]^T \qquad (6.51)$$

Esta aproximación es adecuada si la no linealidad no es severa en torno a la solución y si los datos no son excesivamente ruidosos.

*Trazabilidad: Foti Cap. 6, §6.5.1, pp. 324–329*

---

### 6.5.2 Incertidumbre en las mediciones de ondas superficiales

#### Curva de dispersión experimental (SASW — dos estaciones)

En el método de dos estaciones, la velocidad de fase se estima como:
$$V_R(\omega) = \frac{\omega(x_2 - x_1)}{\arg[S_{12}(\omega)]} \qquad (6.52)$$

donde $S_{12}(\omega)$ es el **espectro de potencia cruzado** de las señales de los dos receptores. La varianza de $V_R(\omega)$ puede calcularse propagando la varianza del argumento de $S_{12}$ usando FOSM (Ec. 6.54), y depende de la **coherencia ordinaria** $\gamma_{12}^2(\omega)$ entre las dos señales: mayor coherencia → menor incertidumbre.

#### Métodos multicanal (MASW)

Con arrays de múltiples receptores, la curva de dispersión se obtiene como una regresión lineal de las fases de desplazamiento sobre las posiciones de los receptores. La incertidumbre de $V_R(\omega)$ se obtiene de la covarianza de la estimación del número de onda $k_R(\omega)$ (Ec. 6.47 con G dada por Ec. 6.57), que depende del número de receptores y sus separaciones.

Para métodos basados en transformadas (f-k, τ-p), la propagación de incertidumbre es más difícil de calcular analíticamente, siendo preferible estimarla directamente a partir de la variabilidad estadística de los datos medidos mediante repeticiones del ensayo.

#### Curva de atenuación y medición conjunta

La incertidumbre de la curva de atenuación $\alpha_R(\omega)$ se propaga desde la varianza de las amplitudes del espectro de desplazamiento usando FOSM. En la medición conjunta de dispersión y atenuación mediante la función de transferencia $H(r,\omega)$, la varianza del número de onda complejo $k_R^*(\omega)$ encapsula simultáneamente la incertidumbre de $V_R$ y de $\alpha_R$ (Ec. 6.70–6.72).

> **Implicación práctica para geófonos y MASW:** la incertidumbre de la curva de dispersión disminuye al aumentar el número de receptores, la longitud del array y la coherencia de las señales. Posicionamiento incorrecto de los receptores, acoplamiento deficiente con el suelo y ruido ambiental no coherente son las principales fuentes de incertidumbre experimental. Estudios experimentales (O'Neill 2003) muestran que coeficientes de variación de 5–10% para las velocidades de fase de Rayleigh son típicos incluso en presencia de ruido significativo.

*Trazabilidad: Foti Cap. 6, §6.5.2, pp. 329–338*

---

### 6.5.3 Estimación de la varianza de los parámetros del modelo

Una vez estimada la incertidumbre de los datos (curva de dispersión), el siguiente paso es proyectarla sobre los parámetros del modelo (perfil de Vs).

Para la **inversión de la curva de dispersión** (no lineal), usando el Jacobiano J_Vs evaluado en la última iteración:
$$\text{Cov}[\mathbf{V}_s] = [(\mathbf{J}_{V_s}^T \text{Cov}[\mathbf{V}_R]^{-1} \mathbf{J}_{V_s})^{-1} \mathbf{J}_{V_s}^T \text{Cov}[\mathbf{V}_R]^{-1}]_{\text{last}} \cdot \text{Cov}[\mathbf{V}_R] \cdot [\ldots]^T \qquad (6.75)$$

Si se usa el **algoritmo de Occam**, la incertidumbre de Vs incluye además el efecto del parámetro de suavizado μ (Ec. 6.76), que amortigua la proyección de los errores de los datos sobre los parámetros del modelo.

Para la **inversión de la curva de atenuación** (lineal), la propagación de la incertidumbre es directa mediante mínimos cuadrados estándar (Ec. 6.77).

> **Figura 6.17** (p. 341): Perfil de Vs con barras de error (desviación estándar) obtenido con el algoritmo de Occam aplicado a datos reales en Italia. Coeficientes de variación de 0.2–4%.

> **Figura 6.18** (p. 341): Curva de dispersión experimental con barras de error, y curva teórica final del algoritmo de Occam (iteración 9). La región de baja frecuencia (<11 Hz) tiene mayor incertidumbre (hasta 14%) que la región de alta frecuencia.

**Conclusión del capítulo sobre incertidumbre:** los métodos SASW y MASW son técnicas robustas con coeficientes de variación del orden del 5–10% incluso con ruido ambiental significativo, lo que los hace aplicables en entornos urbanos. La incertidumbre aumenta con la profundidad, lo que refleja la disminución de la resolución intrínseca del método.

*Trazabilidad: Foti Cap. 6, §6.5.3, pp. 339–343*

---

### 6.5.4 Trade-off entre resolución y varianza

Existe una tensión fundamental e inevitable entre la **resolución espacial** del modelo y la **incertidumbre** de sus parámetros:

- Un modelo con **más capas** tiene mayor resolución (puede detectar variaciones más finas con la profundidad), pero la incertidumbre de cada parámetro es mayor porque hay más incógnitas para la misma cantidad de datos.
- Un modelo con **menos capas** tiene parámetros bien determinados con baja incertidumbre, pero pierde detalles estratigráficos.

Esta relación se visualiza mediante la **curva de trade-off** (Figura 6.20): no existe un modelo ideal único — la elección correcta de la resolución del modelo debe hacerse en función de los objetivos de la investigación y de la redundancia de los datos disponibles.

> **Figura 6.20** (p. 346): Diagrama conceptual de la curva de trade-off entre la dispersión de la resolución del modelo (Rm) y la varianza de los parámetros (σm²). La región de pares posibles (Rm, σm) está acotada por la curva de trade-off.

> **Figura 6.21** (p. 347): Comparación de perfiles Vs con barras de incertidumbre obtenidos con modelos de (a) 5 capas y (b) 10 capas. El modelo de 10 capas tiene mayor incertidumbre, especialmente en capas superficiales.

**Consecuencia práctica:** al realizar inversiones MASW, es preferible usar el menor número de capas que sea consistente con la geología conocida del sitio. La regla práctica es usar espesores de capa que aumenten con la profundidad (siguiendo la disminución de la resolución con la profundidad), y validar los resultados comparando con boreholes o refracción sísmica cuando estén disponibles.

*Trazabilidad: Foti Cap. 6, §6.5.4, pp. 344–347*

---

## Estado de síntesis

| Sección | Estado |
|---------|--------|
| 6.1 Aspectos conceptuales | ✅ sintetizado |
| 6.2 Forward Modeling | ✅ sintetizado |
| 6.3 Métodos empíricos (SSRM) | ✅ sintetizado |
| 6.4.1 Medidas de bondad de ajuste | ✅ sintetizado |
| 6.4.2 Problema inverso lineal (SVD, Tikhonov) | ✅ sintetizado |
| 6.4.3 Problema inverso no lineal (LS/GS, Occam) | ✅ sintetizado |
| 6.4.4 Información a priori | ✅ sintetizado |
| 6.5 Incertidumbre (mediciones, proyección, trade-off) | ✅ sintetizado |

**Chapter 6: completado (primera fase)**

---

*Trazabilidad: Sebastiano Foti Chapter 6.pdf, pp. 273–347. Síntesis completa, 2026-03-19.*
