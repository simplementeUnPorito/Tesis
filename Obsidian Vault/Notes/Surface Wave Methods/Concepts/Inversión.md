
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

### Problemas Críticos

La inversión de curvas de dispersión presenta dificultades inherentes.

- **No Unicidad (Equivalencia)**  
  Diferentes perfiles de suelo pueden producir **curvas de dispersión casi idénticas** [6].

- **Ill-posedness**  
  El problema está **mal condicionado matemáticamente**, lo que implica que pequeñas variaciones en los datos pueden generar grandes cambios en el modelo resultante [6, 11].

- **Mitigación**  
  Para reducir la incertidumbre es importante incorporar **información a priori**, como registros de **sondeos (boreholes)** u otras pruebas geofísicas [6].