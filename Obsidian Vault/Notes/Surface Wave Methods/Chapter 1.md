# Overview of Surface Wave Methods

## 1.0 Introducción

> Fuente: Foti et al. (2014), Introducción al Capítulo 1, pp. 1–2.

Desde que Lord Rayleigh predijo su existencia en 1885, las ondas superficiales han atraído el interés de disciplinas tan diversas como la sismología, la geofísica, la ingeniería geotécnica, el ensayo no destructivo y la física del estado sólido. A pesar de las diferencias de escala — desde aplicaciones ultrasónicas en milímetros hasta la caracterización del manto terrestre a cientos de kilómetros — la idea fundamental es la misma: **explotar la dispersión geométrica de las ondas superficiales** para inferir las propiedades del interior de un medio a partir de mediciones en su frontera.

En ingeniería geotécnica, los métodos de ondas superficiales se han consolidado como herramientas **no invasivas** de caracterización de sitio. Su objetivo práctico es estimar el **perfil de velocidad de onda de corte** $V_S(z)$, que está directamente vinculado al módulo de corte a pequeñas deformaciones $G_{\max}$ y es la propiedad dinámica del suelo relevante para análisis de respuesta sísmica de sitio, diseño de cimentaciones y predicción de vibraciones. En algunos casos también se estima el perfil de amortiguamiento material $D_S(z)$.

La metodología estándar sigue tres pasos interconectados (Figura 1.4, p. 9): **adquisición** del movimiento superficial del suelo → **procesamiento** para extraer la curva de dispersión experimental → **inversión** para obtener el perfil $V_S(z)$. Este capítulo introduce los fundamentos y la perspectiva histórica del método, y establece las limitaciones y desafíos que determinan la práctica correcta.

---

## 1.1 Comportamiento del Suelo

> Fuente: Foti et al. (2014), Sección 1.1, pp. 2–3.

Los suelos son materiales particulados, multifásicos y discontinuos cuyo comportamiento mecánico es inherentemente no lineal e irreversible. Sin embargo, la **elasticidad lineal** proporciona un marco consistente para interpretar las pruebas sísmicas porque los niveles de deformación que producen las ondas sísmicas son extremadamente pequeños.

**¿Por qué es válida la hipótesis elástica?** El nivel de deformación de corte asociado a ensayos sísmicos es típicamente $\gamma < 10^{-5}$ (Burland 1989; Atkinson 2000), muy por debajo del umbral no lineal de los suelos ($\gamma \approx 10^{-4}$ a $10^{-3}$). A estas deformaciones, la curva esfuerzo–deformación del suelo es esencialmente lineal y el módulo de corte alcanza su valor máximo $G_{\max}$. Por tanto, la velocidad de onda de corte medida con métodos sísmicos corresponde a $G_{\max}$, la rigidez de referencia en reposo del suelo.

La respuesta elástica lineal de un sólido isótropo se describe completamente con **dos constantes elásticas** — por ejemplo, las constantes de Lamé $\lambda$ y $\mu$ (siendo $\mu = G$ el módulo de corte). Las velocidades sísmicas se expresan como (Ec. 1.1, p. 3):

$$V_P = \sqrt{\frac{\lambda + 2G}{\rho}}, \qquad V_S = \sqrt{\frac{G}{\rho}}$$

donde $\rho$ es la densidad. Esta relación directa entre velocidad y módulo elástico es la base física de toda la sismología aplicada.

**Limitación de $V_P$ en suelos saturados**: la compresibilidad del fluido intersticial domina la respuesta volumétrica del suelo saturado, haciendo que $V_P \to 1500$ m/s (velocidad del sonido en agua) sin relación con la rigidez del esqueleto. $V_S$, en cambio, refleja solo la rigidez de corte del esqueleto sólido, siendo insensible al contenido de agua. Por esto, $V_S$ es el parámetro objetivo de los métodos sísmicos de caracterización geotécnica (véase [[P-waves]] y [[S-Waves]]).

**Viscoelasticidad lineal**: la elasticidad pura no puede representar la disipación de energía observada en suelos incluso a deformaciones muy pequeñas (ciclos de carga–descarga muestran histéresis). El modelo viscoelástico lineal amplía el marco elástico incorporando amortiguamiento a través del [[Shear Damping Ratio|material damping ratio]] $D_S$. La propagación de ondas en medios viscoelásticos puede modelarse mediante el teorema de correspondencia elástico–viscoelástico (véase Sección 2.5 del libro): se reemplaza el módulo real $G$ por el módulo complejo $G^* = G(1 + 2iD_S)$, lo que introduce un número de onda complejo $k^* = k + i\alpha$ (véase [[Attenuation]]) con una parte real que controla la velocidad de fase y una parte imaginaria que controla el decaimiento espacial de amplitud.

---

## 1.1.1 Pruebas Sísmicas para Caracterización de Sitio
El vínculo entre la velocidad de propagación de ondas y las constantes elásticas del medio permite utilizar pruebas sísmicas para evaluar la variación de $V_s$ con la profundidad [1]. Entre sus ventajas *in situ* destacan la evaluación del geomaterial en su **estado no perturbado** y el **gran volumen de material** involucrado en la medición [1, 2].

Las pruebas se agrupan en dos categorías [3]:

1. **[[Métodos Sísmicos Invasivos]]**: requieren perforaciones (boreholes) o inserción de sondas.
2. **[[Métodos Sísmicos No Invasivos]]**: realizados desde superficie; presentan mayor incertidumbre, pero son más rentables y exploran volúmenes más representativos [3].

### Comparativa: Invasivos vs. No Invasivos

| Característica    | Métodos Invasivos (Borehole)                     | Métodos No Invasivos                      |
| :---------------- | :----------------------------------------------- | :---------------------------------------- |
| **Ejemplos**      | Cross-hole (CHT), Down-hole, P-S logging [2, 24] | SASW, MASW, Reflexión, Refracción [2, 25] |
| **Costo**         | Elevado (requiere perforación) [2, 24]           | Más costo-efectivo [2]                    |
| **Volumen**       | Puntual y localizado [2, 24]                     | Grandes volúmenes representativos [2, 26] |
| **Incertidumbre** | Baja (medición más directa) [2, 24]              | Mayor grado de incertidumbre [2]          |

### Métodos principales
- **Cross-hole (CHT)**: medición directa entre pozos a la misma profundidad; alta precisión pero costo elevado por perforaciones [4].
- **Down-hole**: fuente en superficie y receptores en pozo; variantes con sondas CPT o DMT pueden evitar un pozo dedicado [4].
- **P-S Suspension Logging**: instrumento suspendido en pozo lleno de fluido (acople mecánico); útil para pozos profundos [5].
- **Reflexión y refracción**: técnicas no invasivas; la refracción se limita con capas ocultas o inversiones de velocidad [6, 7].
- **Métodos de ondas superficiales**: basados en inversión de ondas Rayleigh para estimar el perfil de $V_s$ [7].

---

## 1.2 Tipos de Ondas de Cuerpo

> Fuente: Foti et al. (2014), Sección 1.1, pp. 2–3.

En un sólido elástico, lineal, homogéneo e infinito se propagan dos tipos de ondas de cuerpo (véase [[Body Waves]]):

- **[[P-waves|Ondas P]]** (primarias o de compresión): el movimiento de partículas es paralelo a la dirección de propagación; producen compresión y dilatación alternante del volumen. Se propagan en sólidos y fluidos. Velocidad: $V_P = \sqrt{(\lambda + 2G)/\rho}$.

- **[[S-Waves|Ondas S]]** (secundarias o de corte): el movimiento de partículas es perpendicular a la dirección de propagación; producen distorsión pura sin cambio de volumen. Se propagan solo en sólidos. Velocidad: $V_S = \sqrt{G/\rho}$.

Las ondas S se subdividen en **[[SV-wave|SV]]** (polarización en el plano vertical de propagación, que se acopla con P) y **[[SH-wave|SH]]** (polarización horizontal transversal, matemáticamente desacoplada de P). El acoplamiento P–SV en la superficie libre es el mecanismo que da origen a las [[Rayleigh Waves|ondas de Rayleigh]]; las ondas SH guiadas en una capa blanda dan origen a las [[Love Waves|ondas de Love]].

Dado que $V_S$ depende solo del módulo de corte $G$ y no de la compresibilidad volumétrica, **es el parámetro de mayor relevancia geotécnica**: en suelos saturados, $V_P$ es dominado por la compresibilidad del agua (1500 m/s), mientras que $V_S$ refleja exclusivamente la rigidez del esqueleto sólido.

---

## 1.3 Ondas Superficiales

> Fuente: Foti et al. (2014), Sección 1.2, pp. 5–6.

Las ondas superficiales se originan a partir de la condición de **esfuerzo nulo en la frontera** del dominio — la superficie terrestre. Su patrón de radiación es esencialmente **bidimensional (2D)**: desde una fuente puntual vertical, las ondas de Rayleigh se propagan radialmente en el plano horizontal (Figura 1.1), pero no transfieren energía hacia el interior del semiespacio.

[INSERTE LA FIGURA 1.1 de la página 5]
*(Patrón de radiación 2D de ondas Rayleigh generadas por una fuente puntual vertical. Se aprecia la zona de campo cercano y la órbita de partícula elíptica característica de las ondas de Rayleigh.)*

Esta geometría bidimensional confiere a las ondas superficiales propiedades de propagación cualitativamente distintas a las de las ondas de cuerpo:

- **Atenuación geométrica reducida**: las ondas de cuerpo se expanden en tres dimensiones y su amplitud decae $\propto 1/r^2$. Las ondas de Rayleigh se expanden solo en dos dimensiones: desde una **fuente puntual**, la amplitud decae $\propto 1/\sqrt{r}$; desde una **fuente lineal** en un semiespacio homogéneo, no presentan ninguna atenuación geométrica (Ewing et al. 1957). La comparación resulta decisiva a campo lejano.

- **Dominancia energética en campo lejano**: a distancias del orden de 1 a 2 longitudes de onda desde la fuente, las ondas de cuerpo han decaído suficientemente y el campo de ondas queda dominado por las [[Surface Waves|ondas superficiales]]. Lamb (1904) fue uno de los primeros en reconocer esta propiedad y sus implicaciones para la transmisión de energía sísmica a grandes distancias.

- **Confinamiento en profundidad**: en la dirección perpendicular a la propagación (hacia el interior del semiespacio), el desplazamiento de partícula decae exponencialmente porque no se transporta energía hacia el interior. La mayor parte de la energía de deformación queda confinada dentro de ~1 longitud de onda $\lambda$ desde la superficie libre (Achenbach 1984). Esta propiedad establece la **relación frecuencia–profundidad** que hace posible la caracterización del subsuelo:
  - altas frecuencias → $\lambda$ corta → movimiento confinado a capas superficiales
  - bajas frecuencias → $\lambda$ larga → movimiento extendiéndose a mayor profundidad

### Tipos de ondas superficiales

Los tres tipos de ondas superficiales relevantes para caracterización de sitio son (Foti et al. 2014):

1. **[[Rayleigh Waves|Ondas de Rayleigh]]**: surgen del acoplamiento P–SV en la superficie libre. El movimiento de partícula es elíptico y retrógrado cerca de la superficie. Son fácilmente generadas por fuentes verticales y detectadas con geófonos verticales, lo que las convierte en el tipo más utilizado en aplicaciones geotécnicas.

2. **[[Love Waves|Ondas de Love]]**: generadas por la guía de ondas SH en una capa blanda suprayacente a un semiespacio más rígido. Requieren heterogeneidad estructural para existir. El movimiento de partícula es horizontal y transversal a la dirección de propagación. Sus aplicaciones de caracterización se discuten en el Capítulo 8.

3. **[[Scholte Waves|Ondas de Scholte]]**: ondas de interfaz entre un fluido (agua) y un sólido (sedimentos marinos). Son el equivalente submarino de las ondas de Rayleigh. Su velocidad de fase es dispersiva y controlada por la capa de agua y el perfil $V_S$ del fondo marino (véase Sección 8.2).

---

## 1.3.1 Dispersión Geométrica

> Fuente: Foti et al. (2014), Sección 1.2.1, pp. 6–8.

**Intuición física**: en un [[Elastic Half Space|semiespacio homogéneo]], la velocidad de las ondas de Rayleigh depende exclusivamente de las propiedades mecánicas del medio ($V_R \approx 0.92\,V_S$ para $\nu = 0.25$), **no de la frecuencia** — el semiespacio homogéneo es no dispersivo. Sin embargo, cuando el medio es verticalmente heterogéneo, ondas de diferente frecuencia “sienten” capas de distinta profundidad. Como cada capa puede tener propiedades distintas, la velocidad de fase pasa a depender de la frecuencia: el medio se vuelve **dispersivo geométricamente**. Este fenómeno es el fundamento físico de toda la metodología de ondas superficiales.

La Figura 1.2 (p. 7) ilustra el mecanismo en un medio de tres capas:

[INSERTE LA FIGURA 1.2 de la página 7]
*(Dispersión geométrica de ondas Rayleigh: perfil de movimiento de partícula vertical para una onda de alta frecuencia (λ corta, movimiento confinado a Capa 1) y una de baja frecuencia (λ larga, movimiento extendiéndose hasta Capa 3). La velocidad de la onda de alta frecuencia es controlada por las propiedades de la Capa 1; la de baja frecuencia, por una combinación de las tres capas.)*

- **Alta frecuencia** (λ corta): el movimiento de partícula queda confinado en la primera capa. La velocidad de la onda está controlada casi exclusivamente por las propiedades de esa capa superficial.
- **Baja frecuencia** (λ larga): el movimiento se extiende a mayor profundidad, involucrando las propiedades de múltiples capas. La velocidad resulta de una combinación ponderada, aproximadamente en proporción a cuánto movimiento ocurre en cada capa.

Al medir la velocidad de fase a diferentes frecuencias en el campo se obtiene la **curva de dispersión experimental** $V_R(f)$. Un gráfico de velocidad vs. longitud de onda muestra una tendencia creciente para un perfil normalmente dispersivo (Figura 1.3d, p. 8); representado en función de la frecuencia constituye la **curva de dispersión** en su forma convencional (Figura 1.3e, p. 8).

[INSERTE LA FIGURA 1.3 de la página 8]
*(Identificación de parámetros a partir de dispersión geométrica: (a) perfil de velocidad en capas, (b–c) movimiento de partícula a alta y baja frecuencia, (d) curva de dispersión en dominio longitud de onda–velocidad, (e) curva de dispersión en dominio frecuencia–velocidad. El problema inverso conecta (e) con (a).)*

**Problema directo y problema inverso**: el vínculo entre el perfil $V_S(z)$ y la [[Dispersion Relation|curva de dispersión]] define dos problemas complementarios:

- **Problema directo**: dado un modelo $V_S(z)$, calcular la curva de dispersión teórica. Se detalla en el Capítulo 2.
- **Problema inverso**: dada la curva de dispersión experimental, identificar el perfil $V_S(z)$. Se trata en el Capítulo 6.

Matematicamente, se formula como un problema de identificación de parámetros (Engl 1993). La solución y sus propiedades dependen fuertemente del modelo constitutivo adoptado para describir la respuesta del medio y las condiciones de sus fronteras.

---

## 1.4 Metodología de la Prueba

> Fuente: Foti et al. (2014), Sección 1.3, pp. 8–15.

La mayoría de las pruebas de ondas superficiales tienen como objetivo estimar el **perfil de velocidad de onda de corte** $V_S(z)$, estrechamente vinculado a la variación vertical del módulo de corte a pequeñas deformaciones. Esta tarea se realiza en dos etapas: primero se obtiene la **curva de dispersión experimental** a partir de los datos de campo; luego se resuelve el **problema de identificación de parámetros** para encontrar el perfil $V_S(z)$ que explica la dispersión observada. La interpretación se apoya en un modelo de referencia — usualmente un modelo 1D compuesto por una pila de capas elásticas lineales y homogéneas (Foti et al. 2014, p. 8).

Existe una gran variedad de ensayos de ondas superficiales, identificados con distintos acrónimos (SASW, MASW, ReMi, SPAC, HVSR…). Pueden diferir en el tipo de fuente, el número de receptores, las técnicas de procesamiento de señales y las estrategias de inversión, pero el principio general es esencialmente el mismo: explotar la [[Dispersion Relation|dispersión geométrica]] de las [[Surface Waves|ondas superficiales]] para inferir el perfil $V_S$.

**Flujo de trabajo estándar** (Figura 1.4, p. 9): el procedimiento se subdivide en tres pasos fuertemente interrelacionados que deben considerarse como un todo durante la interpretación:

1. **[[Adquisición de Datos|Adquisición]]**: observación y registro del movimiento superficial del suelo.
2. **[[Procesamiento de Señales|Procesamiento]]**: extracción de la curva de dispersión experimental (velocidad de fase vs. frecuencia).
3. **[[Inversión]]**: estimación del perfil $V_S(z)$ a partir de la curva de dispersión.

[INSERTE LA FIGURA 1.4 de la página 9]
*(Diagrama de flujo de las pruebas de ondas superficiales: adquisición del movimiento del suelo → procesamiento para obtener espectro f–k y curva de dispersión → inversión para obtener perfil $V_S(z)$ en capas.)*

La mayoría de los ensayos se realizan con **ondas de Rayleigh** porque son fáciles de generar con fuentes verticales y de detectar con geófonos verticales en la superficie. Las aplicaciones con ondas de Love son posibles pero presentan restricciones relacionadas con la estratigrafía y la dificultad de generar ondas SH. Las aplicaciones en el fondo marino emplean [[Scholte Waves|ondas de Scholte]] (véase Sección 1.6.4 y Capítulo 8).

### 1.4.1 Adquisición

> Fuente: Foti et al. (2014), Sección 1.3.1, pp. 10–11.

Los datos de ondas superficiales se recolectan con un número variable de **receptores en la superficie del terreno**, desplegados en configuraciones geométricas específicas según el ensayo.

**Sensores**: los receptores más comunes en aplicaciones de ingeniería y exploración ambiental son los **geófonos** (transductores electriodinámicos de velocidad), preferidos por su alta sensibilidad, robustez y bajo costo. Los geófonos de baja frecuencia (<2 Hz) tienden a ser más grandes, frágiles y costosos. Para aplicaciones de pequeña escala donde se requieren altas frecuencias y altas amplitudes (p. ej. caracterización de pavimentos), los **acelerómetros MEMS** son más apropiados.

**Dispositivos de almacenamiento**: cualquier hardware con un conversor A/D y capacidad de almacenamiento digital puede utilizarse — desde sismógrafos comerciales hasta tarjetas de adquisición conectadas a computadores. Los sismógrafos comerciales son la primera opción por su robustez, impermeabilidad y resistencia al polvo; los modernos incorporan computadores de campo para procesamiento preliminar en sitio.

**Fuentes de energía**: para generar ondas de Rayleigh superficiales se pueden usar diversas fuentes, siempre que aporten energía suficiente en el rango de frecuencias de interés:
- **Fuentes impulsivas (activas)**: martillos de mano o de caída libre para frecuencias altas; masas de mayor tamaño para componentes de baja frecuencia. Preferidas por ser económicas y portátiles.
- **Fuentes continuas (activas)**: shakers electromagnéticos pequeños hasta Vibroseis montados en camión (Vibroseis™). Generan ondas harmónicas controladas. Costosos y con tiempos de adquisición en campo más largos.
- **Microtremores (pasivos)**: ruido ambiental generado por actividades humanas (tráfico, maquinaria, construcción) y eventos naturales. Evitan la necesidad de fuentes activas. Su ventaja clave es que son ricos en componentes de **baja frecuencia**, lo que permite caracterizaciones profundas (decenas o cientos de metros). Su limitación es el escaso contenido de alta frecuencia, que reduce la resolución superficial.

**Estrategia óptima**: combinar mediciones activas y pasivas (Figura 1.5, p. 11) permite cubrir un rango de frecuencias más amplio que cualquiera de las dos por separado, mejorando simultáneamente la resolución superficial y la profundidad de investigación (véase también Capítulo 3).

[INSERTE LA FIGURA 1.5 de la página 11]
*(Combinación de fuentes activas y pasivas: el ensayo activo (arreglo lineal con fuente) cubre el rango de alta frecuencia; el ensayo pasivo (arreglo 2D registrando microtremores) cubre el de baja frecuencia. El procesamiento conjunto produce una curva de dispersión de mayor rango. La inversión produce un perfil $V_S$ más profundo y mejor resuelto.)*

### 1.4.2 [[Procesamiento de Señales|Procesamiento]]

> Fuente: Foti et al. (2014), Sección 1.3.2, pp. 12–13.

Los datos de campo se procesan para estimar los **parámetros de propagación de las ondas superficiales**, siendo el resultado principal la **curva de dispersión experimental** — la variación de la velocidad de fase de Rayleigh con la frecuencia.

El procesamiento se basa en la **Transformada de Fourier** para descomponer la historia temporal del movimiento de partícula en sus componentes de frecuencia. Distintos procedimientos de procesamiento están disponibles, pero todos explotan la relación entre la velocidad de fase y el desfase espacial de las señales entre receptores. Un ejemplo típico es el análisis en el dominio **frecuencia–número de onda (f–k)**: los datos de campo se transforman al dominio f–k y la curva de dispersión se obtiene seleccionando las amplitudes espectrales máximas (Figura 1.6, p. 12).

[INSERTE LA FIGURA 1.6 de la página 12]
*(Ejemplo de procesamiento con análisis f–k: (a) datos de campo — sismograma con 48 trazas y 70 m de apertura; (b) espectro f–k con crestas correspondientes al modo fundamental de Rayleigh; (c) curva de dispersión experimental resultante — velocidad de fase vs. frecuencia, de ~200 m/s a 45 Hz hasta ~900 m/s a 10 Hz.)*

El procesamiento puede realizarse directamente en campo con sistemas basados en PC. La inspección visual de la curva de dispersión antes de la inversión es importante para validar cualitativamente la calidad de los datos.

Además de la dispersión, los datos de campo pueden usarse para extraer la **curva de atenuación experimental** — el coeficiente de atenuación de las ondas superficiales como función de la frecuencia. Usando un procedimiento análogo al de la Figura 1.4 pero orientado a la amplitud en lugar de la fase, es posible invertir este dato para estimar el perfil del **material damping ratio** $D_S(z)$. La inversión conjunta de dispersión y atenuación determina simultáneamente $V_S(z)$ y $D_S(z)$ (véase Capítulos 5 y 6).

### 1.4.3 [[Inversión]]

> Fuente: Foti et al. (2014), Sección 1.3.3, pp. 13–15.

La inversión es el paso final de la interpretación de los ensayos de ondas superficiales. Su objetivo es **identificar los parámetros del modelo** (perfil $V_S(z)$) que producen una curva de dispersión teórica lo más cercana posible a la curva experimental.

**Mecánica del proceso**: la solución del **problema directo** (Capítulo 2) — calcular la curva de dispersión teórica para un modelo dado — forma la base de cualquier estrategia de inversión. La inversión minimiza una **función objetivo** que mide la distancia entre la curva experimental y la teórica, expresada habitualmente como la raíz del error cuadrático medio (RMS) de las diferencias entre los puntos de datos. El conjunto de parámetros del modelo que minimiza esta función es la solución del problema inverso (Figura 1.7, p. 14).

[INSERTE LA FIGURA 1.7 de la página 14]
*(Ejemplo de proceso de inversión: (a) perfil $V_S(z)$ resultante con capas de 200 a 1200 m/s; (b) comparación de curvas de dispersión teórica y experimental en dominio longitud de onda–velocidad; (c) misma comparación en dominio frecuencia–velocidad. El ajuste entre curva teórica (línea continua) y datos experimentales (puntos) es bueno en todo el rango.)*

**Estrategias de búsqueda** (Foti et al. 2014, pp. 14–15):
- **Métodos de búsqueda local (LSM)**: parten de un perfil tentativo y exploran su vecindad mediante gradiente o métodos análogos. Son rápidos porque requieren pocas evaluaciones del problema directo. Su limitación es el riesgo de convergencia a **mínimos locales** de la función objetivo, que pueden ser muy diferentes del mínimo global.
- **Métodos de búsqueda global (GSM)**: exploran el espacio completo de posibles soluciones (Monte Carlo, algoritmos genéticos, Neighbourhood Algorithm). Son más robustos que los LSM pero computacionalmente más costosos, dado que requieren un gran número de evaluaciones del problema directo.

**Ill-posedness y no unicidad**: el problema inverso es inherentemente **mal condicionado** (ill-posed) y no tiene solución única. Una consecuencia directa es el **problema de equivalencia**: múltiples perfiles $V_S(z)$ diferentes pueden producir curvas de dispersión teóricas igualmente cercanas a la experimental (véase [[Non-uniqueness]]). Una evaluación significativa de los perfiles equivalentes debe tener en cuenta las incertidumbres en los datos experimentales. Los datos a priori de perforaciones u otras pruebas geofísicas son elementos útiles para acotar el espacio de soluciones y mitigar el problema de equivalencia.

El **juicio de ingeniería** juega un papel importante en todo el procedimiento: los resultados de métodos de inversión automatizados deben examinarse con atención, con especial énfasis en los resultados intermedios de cada paso.

---

---

## 1.5 Perspectiva Histórica del Desarrollo Técnico

> Fuente: Foti et al. (2014), Sección 1.4, pp. 15–22.

El desarrollo de los métodos de ondas superficiales está estrechamente ligado a los avances en electrónica y computación. La mayoría de las herramientas actuales — transformadas en dominios frecuencia–número de onda, inversión de Rayleigh — tienen su origen en la sismología global y la geofísica de exploración, y fueron sucesivamente adaptadas a la escala ingenieril.

### 1.5.1 Sismología Global

Desde la década de 1920 los sismólogos estudiaron ondas superficiales para caracterizar el interior de la Tierra, aunque su uso sistemático se consolidó en los años 1950–1960 con el desarrollo de redes sísmicas de banda ancha (Ben-Menhaem 1995; Aki y Richards 2002). Las ondas de Rayleigh son fácilmente identificables en la componente vertical del sismograma; las ondas de Love en la componente transversal solo pudieron separarse con la llegada del registro digital. El flujo de trabajo en sismología global sigue el mismo esquema que en MASW: estimación de la [[Dispersion Curve|curva de dispersión]] (velocidad de grupo o de fase) seguida de inversión para obtener el perfil de rigidez.

Un desafío central fue la influencia de los [[Surface Wave Modes|modos superiores]]: la presencia de múltiples modos obliga a técnicas sofisticadas de filtrado modal. La inversión multimodal es ventajosa porque los modos superiores penetran a mayor profundidad que el fundamental (véase Capítulo 2), y este principio migró a los métodos de caracterización de sitio.

### 1.5.2 Geofísica de Exploración

En la exploración sísmica de hidrocarburos, el ground-roll — el tren de ondas Rayleigh que contamina los sismogramas de reflexión — es tratado como ruido coherente y filtrado mediante técnicas f-k o tau-p. La Figura 1.8 (p. 17) ilustra un sismograma de reflexión donde los primeros 1500 m de offset están dominados por ondas superficiales con múltiples modos. Las mismas herramientas desarrolladas para suprimir el ground-roll (Nolet y Pansa 1976; McMechan y Yedlin 1981) son las que se usan hoy para extraer la curva de dispersión en MASW.

La toma de conciencia de que el ground-roll contiene información de caracterización — en lugar de ser solo ruido — abrió el camino al uso de estos métodos en aplicaciones de superficie.

### 1.5.3 Aplicaciones de Ingeniería: de SASW a MASW

Las primeras aplicaciones ingenieriles de ondas superficiales se propusieron en los años 1950 con el método de estado estacionario de Rayleigh (Jones 1958, 1962; Ballard 1964), en el que un vibrador monocromático y un receptor se usaban para medir la longitud de onda de la onda de Rayleigh a cada frecuencia.

El salto cualitativo llegó con el **método SASW** (Spectral Analysis of Surface Waves), introducido en la Universidad de Texas en Austin a finales de los 1970s (Nazarian y Stokoe 1984; Stokoe et al. 1994). El SASW usa dos receptores y estima el [[Phase Velocity|desfase espectral]] entre ellos para obtener la velocidad de fase de Rayleigh. Aunque representó un avance teórico significativo, sus limitaciones prácticas — aliasing espacial, sensibilidad a modos superiores, baja tasa de producción en campo — abrieron el camino a los métodos multireceptor.

Los **métodos multiestación** (conocidos generalmente como **[[MASW Method|MASW]]** — Multistation Analysis of Surface Waves, introducido por Park et al. 1999 en el Kansas Geological Survey) emplean arreglos lineales con múltiples geófonos. Los datos se transforman al dominio f-k, donde los máximos espectrales identifican las velocidades de fase modales. Son más rápidos, más robustos y menos subjetivos que el SASW.

Los **estudios pasivos de microtremores** evitan la necesidad de fuentes activas: registran el ruido ambiental con arreglos 2D y extraen la dispersión mediante beamforming (Lacoss et al. 1969) o autocorrelación espacial [[SPAC Method|SPAC]] (Aki 1957). Son especialmente valiosos para frecuencias bajas (caracterización profunda a decenas o cientos de metros). El método [[ReMi Method|ReMi]] (Louie 2001) es una variante que usa un arreglo lineal y la transformada slant-stack sobre ruido ambiental. El cociente espectral [[HVSR|H/V]] (Nakamura 1989; Fäh et al. 2003) permite estimar la frecuencia fundamental del sitio con un único sensor triaxial.

---

## 1.6 Desafíos de los Métodos de Ondas Superficiales

> Fuente: Foti et al. (2014), Sección 1.5, pp. 21–29.

Los métodos de ondas superficiales son métodos inversos indirectos: estiman propiedades del subsuelo a partir de observaciones en la superficie, asumiendo un modelo y ajustando parámetros. Esta cadena —adquisición → procesamiento → inversión— introduce desafíos que deben comprenderse para interpretar correctamente los resultados.

### 1.6.1 Superposición Modal y Velocidad Aparente

En un [[Layered Media|medio estratificado]], las ondas de Rayleigh se propagan en múltiples modos con curvas de dispersión independientes (véase [[Surface Wave Modes]]). Con un número limitado de receptores, no es posible separar perfectamente todos los modos: el procesamiento extrae una única curva de dispersión *aparente* que resulta de la superposición energética de los modos presentes en el campo de ondas.

Cuando el perfil de $V_S$ crece monotónicamente con la profundidad (**medio normalmente dispersivo**), el modo fundamental concentra la mayor parte de la energía y la curva aparente coincide razonablemente con él. Sin embargo, cuando hay una inversión de velocidades (capa blanda subsuperficial) o una costra superficial rígida (**medio inversamente dispersivo**), los modos superiores pueden ser energéticamente dominantes en ciertas bandas de frecuencia. La Figura 1.9 (p. 22) ilustra cómo la curva aparente de un sitio inversamente dispersivo no corresponde a ningún modo individual, sino a una mezcla que produce una rampa ascendente en velocidad. Invertir esta curva asumiendo que es el modo fundamental conduce a un perfil $V_S$ erróneo.

La solución correcta es incluir la superposición modal en el problema directo (véase Sección 2.4 del libro): comparar la curva experimental con la curva teórica resultante de la superposición de todos los modos excitados, no solo del fundamental.

### 1.6.2 Efectos de Campo Cercano

El procesamiento estándar asume que el campo de ondas en el arreglo está compuesto exclusivamente por **ondas planas** de Rayleigh. Esta hipótesis solo es válida en el **campo lejano** ($r \gg \lambda_R$). En la zona próxima a la fuente (campo cercano), dos efectos contaminan la medición:

1. **Interferencia de ondas de cuerpo**: cerca de la fuente, las ondas P y SV no han decaído suficientemente ($\propto 1/r$) respecto a las superficiales ($\propto 1/\sqrt{r}$) y su superposición sesga la velocidad de fase aparente hacia valores más altos.
2. **Frente de onda cilíndrico**: los métodos f-k y tau-p asumen frentes planos; en el campo cercano el frente real es cilíndrico, introduciendo error sistemático en la extracción de la curva de dispersión (Zywicki y Rix 2005).

La **distancia crítica** a partir de la cual los efectos de campo cercano son despreciables varía entre 0.5 y 2 longitudes de onda, dependiendo del perfil del sitio (Sánchez-Salinero 1987; Tokimatsu 1995). La estrategia práctica es alejar el primer geófono del arreglo de la fuente (**offset mínimo** $x_{\min} \approx \lambda_{\max}/2$), aunque esto reduce la amplitud de señal a frecuencias altas (mayor atenuación material a offset grande) y compromete la resolución superficial. El diseño del arreglo requiere equilibrar ambos efectos.

### 1.6.3 Errores de Modelo

El modelo de referencia estándar para la inversión es una **pila 1D de capas elásticas lineales horizontales** (Figura 1.10, p. 24): cada capa $j$ se describe por $\{V_{Sj}, V_{Pj}, \rho_j, h_j\}$. Sus ventajas son la eficiencia computacional (método de la [[Layered Media|matriz de transferencia de Thomson-Haskell]]) y el número limitado de incógnitas. Con frecuencia se fijan $\rho$ y el [[Poisson Ratio|coeficiente de Poisson]] $\nu$ de cada capa, reduciendo las incógnitas a $2n-1$ (velocidades $V_S$ y espesores, excepto el semiespacio inferior).

La selección de $\nu$ es crítica en suelos saturados. Por encima de la tabla de agua, $\nu \approx 0.2$–$0.3$ y $V_P$ refleja la rigidez del esqueleto. Por debajo, el agua intersticial domina la compresibilidad volumétrica: $V_P \to 1500$ m/s y $\nu \to 0.5$. Usar $\nu$ incorrecto introduce un error sistemático en el perfil $V_S$ invertido (véase Sección 7.1.2 del libro).

El modelo 1D asume heterogeneidad solo vertical. Si existe variación lateral marcada (capas inclinadas, depósitos de relleno con geometría irregular, cuña de sedimentos), los resultados son sesgados. Una verificación útil es repetir el ensayo en líneas perpendiculares o aplicar la técnica de **ventana deslizante** (moving window) para generar pseudo-secciones 2D de $V_S$ (Socco et al. 2009).

### 1.6.4 Resolución y Profundidad de Investigación

La resolución de los métodos de ondas superficiales **decrece con la profundidad**. La Figura 1.11 (p. 27) muestra los kernels de sensibilidad: la misma perturbación del 10% en $V_S$ produce un cambio mayor en la curva de dispersión si está en la capa superficial que si está a mayor profundidad. La capa superficial afecta toda la curva de dispersión; las capas profundas solo afectan las frecuencias bajas, donde los datos son escasos.

La **profundidad máxima investigable** se estima a partir de la longitud de onda máxima del experimento: $z_{\max} \approx \lambda_{\max}/2$. Esto depende directamente de la frecuencia mínima accesible, que está controlada por la longitud del arreglo y la calidad de la fuente. Los métodos pasivos de microtremores extienden la investigación en profundidad al proporcionar energía a frecuencias muy bajas.

La Figura 1.12 (p. 28) ilustra otro problema: si la curva de dispersión experimental está igualmente espaciada en frecuencia, la representación en el dominio longitud de onda–velocidad muestra una concentración de puntos a longitudes de onda cortas y muy pocos puntos a longitudes de onda largas. Esto hace que la inversión esté sobre-condicionada por la parte superficial del perfil. Estrategias de remuestreo con distribución exponencial de frecuencias, o el ajuste de la curva en el dominio de longitud de onda, permiten mejorar la distribución de la información y la calidad del perfil invertido a profundidad.

---

## 1.7 Aplicaciones Típicas
El uso de métodos de ondas superficiales ha crecido significativamente para resolver problemas de ingeniería, geofísica y sismología [1].

### 1.7.1 Caracterización de sitio

> Fuente: Foti et al. (2014), Sección 1.6.1, pp. 29–30.

El uso primario de los métodos de ondas superficiales es la determinación del **perfil de velocidad de onda de corte** $V_S(z)$. La velocidad $V_S$ está directamente vinculada al módulo de corte a pequeñas deformaciones $G_{\max} = \rho V_S^2$, que es la propiedad dinámica del suelo relevante para:

- **Respuesta sísmica de sitio**: el perfil $V_S$ controla la amplificación y el contenido de frecuencias de las ondas sísmicas al propagarse desde la roca base hacia la superficie. Hay una afinidad directa entre los modelos usados en MASW (pila 1D de capas elásticas) y los modelos de análisis de respuesta sísmica de sitio (código SHAKE y sucesores). Los perfiles equivalentes en términos de dispersión de Rayleigh también tienden a ser equivalentes en términos de amplificación sísmica (Foti et al. 2009) — lo que implica que el impacto de la [[Non-uniqueness|no-unicidad]] en la respuesta sísmica es menor de lo que podría temerse.
- **Estimación de $V_{S,30}$**: los códigos sísmicos clasifican los suelos por el promedio ponderado de $V_S$ en los primeros 30 m ([[Vs30]]). Los métodos de ondas superficiales permiten estimarlo de manera económica y sin necesidad de perforaciones. La Figura 1.13 (p. 30) compara $V_{S,30}$ obtenido con pruebas invasivas y con ondas superficiales para sitios en Estados Unidos e Italia, mostrando buena correlación en un amplio rango de rigideces.
- **Vibraciones de cimentaciones y asentamientos**: $G_{\max}$ es la rigidez de entrada para análisis de interacción suelo–estructura y predicción de asentamientos bajo cargas dinámicas.
- **Amortiguamiento material**: la curva de atenuación experimental — obtenida midiendo el decaimiento espacial de la amplitud de Rayleigh a cada frecuencia (véase Capítulo 5) — permite invertir el perfil del **material damping ratio** $D_S$ in situ. La inversión conjunta de dispersión y atenuación (véase Capítulo 6) determina simultáneamente $V_S(z)$ y $D_S(z)$. Una ventaja sobre los métodos en pozo es que los receptores en superficie permiten verificar el acople suelo–receptor, evitando errores sistemáticos de amplitud que afectan a las mediciones en borehole.

![[ch1 Comparison of V_s30 determined with invasive test and surface wave tests.png]]
*(Ref: Figura 1.13, p. 30 — Comparación de $V_{S,30}$ obtenido con pruebas invasivas y de ondas superficiales en sitios de EE.UU. e Italia)*

### 1.7.2 Mejora de Suelos y Monitoreo

> Fuente: Foti et al. (2014), Sección 1.6.2, p. 31.

Las pruebas de ondas superficiales pueden usarse como herramienta de **monitoreo de la efectividad de técnicas de mejora de suelo**. Repitiendo el ensayo en diferentes momentos del proceso de mejora — por ejemplo, antes y después de vibro-compactación, inyección de lechada o instalación de columnas de grava — se obtiene la evolución temporal del perfil $V_S$. La curva de dispersión experimental cambia con la rigidez del suelo, y la inversión produce una estimación cuantitativa del efecto de la mejora a cada profundidad.

Aplicaciones documentadas incluyen el monitoreo de **mitigación de licuefacción en arenas** mediante compactación (Andrus et al. 1998), el monitoreo de preconsolidación en arcillas (Raptakis 2012) y el control de calidad de la compactación en terraplenes y rellenos (Kim et al. 2001). La ventaja clave es que el ensayo es no invasivo y puede repetirse sin alterar el suelo.

Una aplicación particular es el monitoreo de **permafrost**: la repetición estacional del ensayo en regiones frías permite detectar variaciones de rigidez causadas por ciclos de congelación–descongelación (Alkire 1992), relevante para aplicaciones geotécnicas en taludes y sistemas de cimentación en permafrost.

### 1.7.3 Ensayo No Destructivo de Pavimentos

> Fuente: Foti et al. (2014), Sección 1.6.3, pp. 31–32.

La caracterización de pavimentos fue una de las primeras aplicaciones de los métodos de ondas superficiales en ingeniería: las primeras aplicaciones del [[SASW Method|SASW]] estuvieron orientadas a pavimentos (Heisey et al. 1982; Nazarian 1984). Los pavimentos son medios típicamente horizontales y estratificados, lo que los hace ideales para el modelo de capas planas. Los objetivos son el control de calidad durante la construcción y el seguimiento del deterioro a lo largo del ciclo de vida.

Los desafíos específicos de pavimentos son:
- **Altas frecuencias necesarias**: el espesor de las capas es del orden de centímetros, requiriendo frecuencias de cientos de Hz. Los geófonos estándar son insuficientes; se usan acelerómetros MEMS.
- **Perfil inversamente dispersivo**: la capa asfáltica superficial es más rígida que la base granular y el subrasante. Esto hace que los [[Surface Wave Modes|modos superiores]] sean energéticamente importantes y deba considerarse la superposición modal en la inversión.
- **Ventaja informativa**: la geometría del sistema de pavimento es conocida a priori, lo que reduce el número de incógnitas y hace más robusto el proceso de inversión.

### 1.7.4 Caracterización Offshore y Near-Shore

> Fuente: Foti et al. (2014), Sección 1.6.4, p. 32.

Las aplicaciones submarinas de los métodos de ondas superficiales se basan en las **[[Scholte Waves|ondas de Scholte]]**, que son el equivalente de las ondas de Rayleigh en la interfaz sólido–fluido (fondo marino). Las ondas de Scholte se propagan a lo largo del fondo marino y su velocidad de fase es dispersiva: depende de la frecuencia y está controlada por la profundidad del agua y el perfil $V_S$ de los sedimentos marinos.

La dispersión de las ondas de Scholte converge hacia la dispersión de Rayleigh a medida que la capa de fluido se hace más delgada. La interpretación requiere modelar explícitamente la capa de agua en el problema directo. Aplicaciones pioneras del SASW submarino se realizaron en la Universidad de Texas (Manesh 1991; Luke 1994), con fuente y receptor colocados directamente en el fondo marino. Para aguas profundas, se usan sismómetros de fondo oceánico (OBS) y fuentes de energía remolcadas desde embarcaciones, una tecnología habitual en la industria del petróleo y gas.

### 1.7.5 Caracterización Near-Surface en Exploración Sísmica

> Fuente: Foti et al. (2014), Sección 1.6.5, pp. 32–34.

En la sísmica de reflexión para exploración de hidrocarburos, las **perturbaciones del near-surface** son fuentes de distorsión de los datos. Las ondas P deben viajar dos veces a través de la capa superficial (al bajar y al subir), y su heterogeneidad introduce retardos de tiempo que distorsionan las imágenes sísmicas — estos se corrigen con las llamadas *static corrections*. Tradicionalmente estas correcciones se calculan con sísmica de refracción, pero los métodos de ondas superficiales ofrecen una alternativa: invertir el ground-roll para obtener un modelo $V_S$ del near-surface que luego se usa para estimar o refinar las correcciones estáticas.

El ground-roll — el mismo fenómeno que los sismólogos de exploración trataban como ruido coherente a eliminar — contiene la información de dispersión para esta inversión. Las mismas herramientas desarrolladas para suprimir el ground-roll (análisis f-k, filtros tau-p) se usan hoy para extraer la curva de dispersión y obtener modelos de velocidad 2D y 3D del near-surface. La Figura 1.14 (p. 34) muestra un "volumen de dispersión 3D": un mapa de velocidad de fase a longitud de onda constante sobre un área de ~22×22 km, mostrando variaciones laterales de rigidez superficial a escala regional.

### 1.7.6 Detección de Anomalías

> Fuente: Foti et al. (2014), Sección 1.6.6, p. 34.

Además de la determinación de perfiles 1D de rigidez, los métodos de ondas superficiales pueden usarse para **detectar anomalías locales**: oquedades, inclusiones rígidas, zonas de suelo suelto o rellenos irregulares. La presencia de una anomalía perturba el campo de ondas de forma reconocible — cambia la amplitud, la velocidad de fase aparente o introduce reflexiones anómalas del ground-roll. La identificación de la anomalía se basa en el análisis de estas perturbaciones más que en la inversión formal de la curva de dispersión.

A escala regional, la distribución espacial de la velocidad near-surface puede usarse para identificar **fallas geológicas y lineamentos estructurales** (en el sentido geológico), útil para el modelado geológico y para la seguridad de perforaciones en exploración de hidrocarburos.

---

## 1.8 Ventajas y Limitaciones de los Métodos de Ondas Superficiales

> Fuente: Foti et al. (2014), Sección 1.7, pp. 34–36.

### Ventajas principales

**No invasivos y económicos**: no requieren perforaciones. Pueden realizarse donde no es posible o conveniente penetrar el terreno (rellenos contaminados, residuos sólidos urbanos, suelos con infraestructura). Son rápidos — un ensayo MASW activo típico se completa en pocas horas — y el equipo es portátil.

**Robustos en entornos ruidosos**: a diferencia de otros métodos sísmicos basados en tiempos de llegada, los métodos de ondas superficiales son menos sensibles al ruido de fondo porque trabajan con señales de alta amplitud (ground-roll). En zonas urbanas o industriales con tráfico o maquinaria, el ruido ambiental puede incluso aprovecharse como fuente en métodos pasivos.

**Independientes de la estratigrafía de velocidades**: los métodos de refracción sísmica fallan ante inversiones de velocidad (capas blandas bajo capas duras). Los métodos de ondas superficiales no tienen esta limitación — funcionan para cualquier secuencia de capas, tanto normalmente como inversamente dispersivas, aunque con mayor complejidad en la inversión en el segundo caso.

**Representatividad volumétrica**: el arreglo de geófonos promedia las propiedades lateralmente. Para sitios con heterogeneidades horizontales moderadas, el resultado representa el comportamiento global del depósito — más representativo que un ensayo de pozo puntual.

**Bajo costo de adquisición de amortiguamiento**: obtener el perfil $D_S(z)$ con métodos invasivos (cross-hole) es técnicamente exigente y costoso. Con ondas superficiales, la curva de atenuación se obtiene del mismo experimento que la curva de dispersión, sin necesidad de instrumentación adicional.

### Limitaciones principales

**Hipótesis 1D**: el modelo de referencia estándar (pila de capas horizontales) asume que no hay variación lateral de propiedades dentro del área del ensayo. Si la variación lateral es marcada, el perfil invertido puede ser engañoso. La estrategia habitual es realizar ensayos en múltiples posiciones y orientaciones para evaluar la variabilidad lateral, o usar técnicas de ventana deslizante para generar pseudo-secciones 2D (véase Sección 1.6.3 del libro).

**No-unicidad de la inversión**: el problema inverso es mal condicionado. Múltiples perfiles $V_S(z)$ pueden producir curvas de dispersión teóricas igualmente cercanas a la experimental (véase [[Non-uniqueness]]). La evaluación correcta requiere cuantificar la incertidumbre — incluyendo la de los datos experimentales — y usar información a priori (niveles freáticos, borehole existentes, geología) para restringir el espacio de soluciones.

**Resolución decreciente con la profundidad**: las capas delgadas cerca de la superficie son bien resueltas; las perturbaciones de $V_S$ a gran profundidad tienen efecto pequeño sobre la curva de dispersión (véase [[Skin Depth]] y kernels de sensibilidad, Sección 1.5.4). Las capas profundas solo pueden caracterizarse en términos de comportamiento promedio, no como objetos individuales delgados.

**Juicio de ingeniería necesario**: los resultados de métodos automáticos de inversión deben revisarse críticamente. El conocimiento de la física de la propagación, la calidad de los datos y la geología del sitio son ingredientes esenciales para una interpretación confiable.