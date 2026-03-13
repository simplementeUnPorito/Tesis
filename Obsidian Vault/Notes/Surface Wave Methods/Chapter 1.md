# Overview of Surface Wave Methods

## 1.0 Introducción
El objetivo principal de los métodos de ondas superficiales es utilizar la **dispersión** de las ondas superficiales para inferir propiedades mecánicas del subsuelo [1, 5]. En la práctica, se presentan como una herramienta **no invasiva** para estimar perfiles de rigidez mediante la velocidad de onda de corte ($V_s$) y, en ciertos casos, perfiles de amortiguamiento [6, 7].

---

## 1.1 Comportamiento del Suelo
Los suelos presentan una respuesta mecánica compleja debido a su naturaleza particulada y multifásica.

- **Naturaleza compleja**: materiales particulados, multifásicos y discontinuos [8].
- **Aproximación de deformación pequeña (small-strain)**: en los niveles de deformación típicos de pruebas geofísicas se adopta la **elasticidad lineal** [1, 9].
- **Viscoelasticidad**: se emplea para representar disipación de energía y amortiguamiento que la elasticidad pura no captura [10, 11].

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
En un sólido elástico, lineal, homogéneo e infinito se propagan dos tipos de ondas [12]:

- [[P-waves]]: ondas primarias o de compresión (longitudinales).
- [[S-Waves]]: ondas secundarias o de corte (transversales).

---

## 1.3 Ondas Superficiales
Las ondas superficiales son particularmente útiles para la caracterización de geomateriales porque se originan a partir de la condición de **esfuerzo nulo** en un límite de dominio (p. ej. la superficie terrestre) [2, 4]. Su patrón de radiación es esencialmente bidimensional (2D), lo que les confiere propiedades de propagación distintas a las ondas de cuerpo [2, 5].

![[ch1_2D_radiation_pattern_Rayleigh_surface.png]]
*(Ref: Figura 1.1 - Patrón de radiación 2D de ondas Rayleigh generadas por una fuente puntual vertical [5])*

### Propiedades clave
- **Baja atenuación geométrica**: mientras las ondas de cuerpo se expanden en 3D (atenuación $\propto r^{-2}$), las ondas Rayleigh desde fuente puntual decaen aproximadamente como $r^{-0.5}$ [3, 6]. Para una fuente lineal, no presentan atenuación geométrica en un semiespacio elástico homogéneo [3, 5].
- **Dominancia en campo lejano**: debido a su menor tasa de decaimiento, a distancias del orden de una a dos longitudes de onda desde la fuente, las ondas de cuerpo se vuelven despreciables y el campo queda dominado por [[Rayleigh Waves]] [3, 5, 7].
- **Confinamiento de energía**: la mayor parte de la energía de deformación asociada al movimiento de ondas superficiales se concentra a profundidades del orden de una longitud de onda $\lambda$ desde la superficie libre [8, 9]. (La amplitud decae rápidamente con la profundidad, por lo que la contribución del movimiento se vuelve pequeña al incrementar $z$) [9].

![[ch1 Geometric Dispersion of rayleigh waves.png]]
*(Ref: Figura 1.2 - Movimiento de partículas a diferentes frecuencias en medios estratificados [10])*

- **Relación frecuencia–profundidad**:
  - altas frecuencias (λ corta) → profundidades someras [8, 11]
  - bajas frecuencias (λ larga) → capas más profundas [8, 12]

### Variantes de ondas superficiales
1. [[Rayleigh Waves]]: combinación de potenciales P y SV; fáciles de generar y detectar verticalmente en superficie [13-15].
2. [[Love Waves]]: ondas transversales SH polarizadas horizontalmente; requieren heterogeneidad (p. ej. capa blanda sobre rígida) para existir [15-17].
3. [[Scholte Waves]]: ondas de interfaz entre fluido (agua) y sólido (sedimentos marinos) [18-20].

---

## 1.3.1 [[Geometric Dispersion]]
La dispersión geométrica es el fenómeno central que hace posible caracterizar el subsuelo desde mediciones superficiales [13, 14]. En un semiespacio elástico lineal, homogéneo e isótropo, las ondas de Rayleigh **no son dispersivas** (su velocidad no depende de la frecuencia) [11, 21, 22]. En medios verticalmente heterogéneos, la velocidad de fase se vuelve dependiente de la frecuencia, permitiendo inferir propiedades del medio mediante un proceso de **inversión** [11, 12, 23].

- **Alta frecuencia**: longitudes de onda cortas que “ven” principalmente capas superficiales [14, 16].
- **Baja frecuencia**: longitudes de onda largas que involucran propiedades de capas profundas [14, 17].

---

## 1.4 Metodología de la Prueba
El objetivo fundamental de la mayoría de las pruebas de ondas superficiales es estimar el perfil de velocidad de onda de corte $V_s$, estrechamente vinculado a la variación vertical del módulo de corte a deformaciones pequeñas [1]. La interpretación se apoya en un modelo de referencia, usualmente un modelo 1D estratificado compuesto por capas elásticas lineales y homogéneas [1].

### Flujo de trabajo estándar
Según la Figura 1.4, el procedimiento se divide en tres pasos interrelacionados que deben considerarse como un todo durante la interpretación [2, 3]:

1. [[Adquisición de Datos]]: observación y registro del movimiento del suelo en la superficie.
2. [[Procesamiento de Señales]]: obtención de la curva de dispersión experimental (frecuencia vs. velocidad de fase).
3. [[Inversión]]: estimación de propiedades del sitio (perfil $V_s$) a partir de la curva.

![[ch1_flowchart_methodology.png]]
*(Ref: Figura 1.4 - Diagrama de flujo de las pruebas de ondas superficiales [4])*

### 1.4.1 Adquisición
Los datos se recolectan típicamente con receptores en superficie configurados en arreglos geométricos específicos [5].

- **Sensores**: se prefieren geófonos por sensibilidad y bajo costo; para baja frecuencia o pequeña escala (pavimentos) se emplean acelerómetros MEMS [5].
- **Fuentes de energía**:
  - **Activas**: impulsivas (martillo, caída de pesos) o vibratorias (shakers electromagnéticos o Vibroseis) [6, 7].
  - **Pasivas**: ruido ambiental o microtremores; ventaja: aportan bajas frecuencias para caracterizaciones profundas (decenas o cientos de metros) [6].
- **Estrategia óptima**: combinación de mediciones activas y pasivas para cubrir un rango más amplio de frecuencias y mejorar la resolución tanto superficial como profunda [6, 8].

![[ch1_active_passive_combination.png]]
*(Ref: Figura 1.5 - Combinación de fuentes activas y pasivas [9])*

### 1.4.2 [[Procesamiento de Señales|Procesamiento]]
Los datos de campo se procesan para estimar parámetros de propagación, siendo el resultado principal la **curva de dispersión experimental** [1].

- Se basa en la Transformada de Fourier para descomponer el movimiento en componentes de frecuencia [1].
- Permite estimar la velocidad de fase según la configuración del ensayo [1].
- También puede obtenerse la curva de atenuación experimental para caracterizar amortiguamiento del suelo [2].

![[ch1_Example of processing of experimental data using wavenumber analysis.png]]

### 1.4.3 [[Inversión]]
La inversión es el paso final de la interpretación [3].

- Se apoya en la solución del problema directo para comparar curvas teóricas con la experimental [3].
- El objetivo es minimizar una función objetivo (usualmente el error RMS) entre ambas curvas [3].
- **Estrategias**: métodos de búsqueda local (rápidos pero con riesgo de mínimos locales) y búsqueda global (más robustos pero costosos computacionalmente) [4, 5].
- **Desafío**: el problema es **ill-posed** y presenta **no unicidad**, pudiendo existir perfiles equivalentes para una misma curva [6].

![[ch1 Example of inversion procecss.png]]

---

## 1.6 Aplicaciones Típicas
El uso de métodos de ondas superficiales ha crecido significativamente para resolver problemas de ingeniería, geofísica y sismología [1].

### 1.6.1 Caracterización de sitio
Es el uso primario de estas pruebas en la actualidad: determinar el perfil $V_s$ [1].

- **Parámetros geotécnicos**: $V_s$ está directamente vinculada al módulo de corte a deformaciones pequeñas ($G_{max}$), relevante para respuesta sísmica de sitio, vibraciones de cimentaciones y transmisión de vibraciones en el suelo [1].
- **Predicciones**: se utiliza para predecir asentamientos y analizar interacción suelo–estructura [1].
- **Evaluación de $V_{s,30}$**: códigos sísmicos emplean el promedio ponderado de $V_s$ en los primeros 30 m para clasificación de suelos [2]. Los métodos de ondas superficiales lo estiman eficientemente al no requerir la precisión (ni costo) de métodos invasivos [2].
- **Amortiguamiento del suelo**: la atenuación de Rayleigh permite obtener el perfil del material damping ratio $D$ in situ [3].
  - **Ventaja sobre borehole**: receptores en superficie permiten verificar acople suelo–receptor y evitar errores de amplitud comunes en pozos [4].
  - **Frecuencias relevantes**: frecuencias de estas pruebas suelen estar más próximas a las de interés para respuesta sísmica que en pruebas cross-hole [4].

![[ch1 Comparison of V_s30 determined with invasive test and surface wave tests.png]]