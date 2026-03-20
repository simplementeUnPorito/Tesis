
La **inversión** es el paso final del procesamiento y se formula como un problema de **identificación de parámetros** [3, 8, 22].

El objetivo es encontrar las propiedades del medio —principalmente el perfil de velocidad de onda de corte \(V_s\)— que mejor expliquen los datos observados, representados por la **curva de dispersión experimental**.

---

### Problema Directo e Inverso

El proceso de inversión se basa en la comparación entre curvas teóricas y experimentales.

- **Problema Directo**:  
  Consiste en calcular una **curva de dispersión teórica** a partir de un perfil de suelo asumido [23, 24].

- **Problema Inverso**:  
  Busca determinar los parámetros del modelo (por ejemplo, \(V_s\) de cada capa) que permiten que la curva teórica reproduzca la curva experimental.

---

### El Proceso Matemático

La inversión se realiza mediante un proceso iterativo de ajuste del modelo.

1. **Modelo de Referencia**  
   Se asume inicialmente un modelo del subsuelo, normalmente **un modelo 1D estratificado** compuesto por capas **elásticas lineales y homogéneas** [9].

2. **Minimización del Error**  
   Los parámetros del modelo se ajustan hasta minimizar la diferencia entre la **curva de dispersión teórica** y la **experimental**, utilizando métricas como el **Root Mean Square (RMS)** [3, 24].

---

### Estrategias de Búsqueda

Existen diferentes enfoques para explorar el espacio de soluciones posibles.

- **Métodos de Búsqueda Local (LSM)**  
  Parten de un perfil inicial tentativo y buscan soluciones en su vecindad.  
  Son **rápidos**, pero pueden quedar atrapados en **mínimos locales** [4, 5].

- **Métodos de Búsqueda Global (GSM)**  
  Exploran un rango más amplio del espacio de soluciones (por ejemplo, **algoritmos genéticos** o **Monte Carlo**).  
  Son más **robustos**, aunque requieren mayor **esfuerzo computacional** [5, 10].

---

### Problemas Críticos: Ill-posedness

La inversión de curvas de dispersión presenta dificultades inherentes conocidas como **ill-posedness** (mal condicionamiento).

Según Hadamard (1923), un problema matemático está **bien puesto** (*well-posed*) si satisface tres condiciones:
1. **Existencia:** para todos los datos admisibles, existe al menos una solución.
2. **Unicidad:** para todos los datos admisibles, la solución es única.
3. **Estabilidad:** la solución depende continuamente de los datos (pequeñas variaciones en los datos producen solo pequeñas variaciones en la solución).

Si alguna de estas condiciones falla, el problema es **ill-posed**. Los problemas inversos violan habitualmente las condiciones de **unicidad** y **estabilidad**:

- **No unicidad (equivalencia):**
  Diferentes perfiles de suelo pueden producir **curvas de dispersión casi idénticas**. Una misma curva de dispersión experimental puede corresponder a más de un perfil de Vs. Esto no es un defecto del algoritmo: es una propiedad intrínseca del problema físico. Desde el punto de vista matemático, la información disponible (la curva de dispersión) no es suficiente para determinar unívocamente los parámetros del modelo.

- **Inestabilidad:**
  Pequeñas variaciones en los datos (causadas por ruido de medición) pueden generar grandes cambios en el modelo resultante. Para problemas lineales, esto se cuantifica mediante el **análisis de valores singulares** (SVD): el valor singular más pequeño controla la amplificación de los errores de perturbación. La tasa de decaimiento de los valores singulares mide el grado de inestabilidad del problema.

**Estrategias de mitigación:**

- **Información a priori:** incorporar datos externos como perfiles de pozo (boreholes), ensayos geotécnicos (SPT, CPT), mediciones de densidad o niveles freáticos, para restringir el espacio de soluciones admisibles.
- **Restricciones de suavidad y acotamiento:** forzar que la solución satisfaga condiciones como suavidad del perfil o que los parámetros se mantengan dentro de rangos físicamente plausibles (por ejemplo, razón de amortiguamiento no negativa).
- **Regularización de Tikhonov:** método matemático formal que convierte el problema ill-posed en una familia de problemas mejor condicionados, añadiendo un término de penalización que controla la complejidad de la solución. Los métodos de orden cero, primero y segundo controlan respectivamente la amplitud, la suavidad del primer gradiente o la curvatura del perfil. El **algoritmo de Occam** es un caso especial que busca el modelo más suave (mínima norma del gradiente) compatible con los datos.

*Trazabilidad: Foti Cap. 6, §6.1.2, pp. 277–280; §6.4.2, pp. 292 ss.*