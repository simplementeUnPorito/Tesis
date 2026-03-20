---
name: Procesamiento de Señales
description: Transformación de registros sísmicos tiempo-espacio en la curva de dispersión experimental; etapa central del flujo MASW entre adquisición e inversión
type: reference
---

# Procesamiento de Señales Sísmicas

> **Contexto:** El procesamiento de señales es la etapa intermedia del flujo de trabajo de los métodos de ondas superficiales: transforma los **registros sísmicos crudos** (sismogramas en el dominio tiempo–espacio) en la **curva de dispersión experimental** $c_p(f)$ que se usará en la [[Inversión|inversión]] para obtener el perfil $V_S(z)$. La calidad de la curva de dispersión extraída — su rango de frecuencias, su resolución y su incertidumbre — depende directamente de la calidad del procesamiento.
> **Fuente:** Foti et al. (2014), Cap. 4, pp. 193–260.

## El observable: curva de dispersión experimental

El producto del procesamiento es la curva de dispersión experimental: para cada frecuencia $f$ dentro del rango accesible del experimento, se estima la [[Phase Velocity|velocidad de fase]] $c_p(f)$ del modo dominante (generalmente el modo fundamental de Rayleigh). Esta curva es la huella dactilar del perfil de rigidez del subsuelo: cada perfil $V_S(z)$ produce una curva de dispersión característica.

El procesamiento determina:
- El **rango de frecuencias** accesible: de $f_{\min}$ (controlado por la longitud del arreglo) a $f_{\max}$ (controlado por el espaciado de geófonos y la fuente).
- La **resolución en velocidad**: capacidad de separar modos próximos en velocidad.
- La **incertidumbre** de cada punto de la curva: propagada a la inversión.

## Análisis frecuencia–número de onda (f-k)

El método estándar en [[MASW Method|MASW]] aplica la **transformada de Fourier 2D** al sismograma (array $u(x_j, t_n)$):

$$U(\omega, k) = \sum_{j=1}^{N_x} \sum_{n=1}^{N_t} u(x_j, t_n)\, e^{-i(\omega t_n - k x_j)}$$

El espectrograma f-k $|U(\omega, k)|$ presenta **crestas** donde la energía se concentra. Cada cresta corresponde a un modo de propagación; su posición $(f, k_{\text{cresta}})$ da la velocidad de fase:

$$c_p(f) = \frac{2\pi f}{k_{\text{cresta}}(f)}$$

La ventaja del análisis f-k es que separa modos en función de sus velocidades: diferentes modos de Rayleigh aparecen como crestas a diferentes $k$ para la misma $f$. Los modos de mayor orden y las ondas de cuerpo (de mayor velocidad, menor $k$) se distinguen visualmente en el espectrograma.

## Análisis tau-p (intercept time–slowness)

Una alternativa al análisis f-k es la transformada $\tau$-$p$ (slant-stack), que acumula la energía del sismograma a lo largo de rectas de pendiente $p = 1/c_p$ (slowness). Para cada frecuencia:

$$S(\tau, p) = \sum_j u(x_j, \tau + p\,x_j)$$

El máximo de $|S|$ a cada $f$ da la slowness $p^* = 1/c_p$ del modo dominante. Esta representación es numéricamente equivalente al análisis f-k (ambos son transformadas de Fourier 2D), pero con diferentes propiedades de resolución y sensibilidad al ruido.

## Método SASW: función de transferencia entre dos receptores

En el [[SASW Method|método SASW]], con solo dos receptores separados por $\Delta x$, la velocidad de fase se estima a partir del **desfase espectral** entre las señales:

$$\hat{\phi}_{12}(f) = \angle\left[\frac{U_2(f)}{U_1(f)}\right]$$

$$c_p(f) = \frac{2\pi f \Delta x}{\hat{\phi}_{12}(f)}$$

Este método es más susceptible a aliasing espacial (ambigüedad de $2\pi$ en la fase) y a la contaminación por [[Surface Wave Modes|modos superiores]], pero requiere solo dos sensores y es útil para validación rápida.

## Identificación de modos y selección de la curva

En el espectrograma f-k aparecen múltiples crestas correspondientes a diferentes modos. La identificación del **modo fundamental** (el más lento a frecuencias donde solo existen pocos modos, tipicamente a bajas frecuencias) requiere experiencia e inspección visual. Errores en la identificación modal (tomar un modo superior por el fundamental o viceversa) son la fuente principal de artefactos en el perfil $V_S$ invertido.

La práctica recomendada es verificar que la cresta seleccionada sea consistente con la [[Skin Depth|profundidad de investigación]] esperada para cada frecuencia.

## Incertidumbre de la curva de dispersión experimental

La incertidumbre de $c_p(f)$ se propaga desde:
- **Variabilidad entre disparos**: si se suman múltiples registros, la dispersión de los picos modales entre disparos da una estimación empírica de la incertidumbre.
- **Anchura del pico en el espectrograma**: cuanto más angosta la cresta en $k$, más precisa es la estimación de $k_{\text{cresta}}$ y menor la incertidumbre en $c_p$.
- **Presencia de ruido y modos contaminantes**: cerca de las transiciones modales o con fuentes de ruido cercanas, la cresta puede estar desplazada.

La incertidumbre se cuantifica como una banda de velocidad $c_p \pm \delta c$ para cada frecuencia y se usa en la inversión como pesos o como función de misfit.

## Referencias

- Foti et al. (2014), Cap. 4.1, pp. 193–215 — análisis f-k y tau-p; extracción de la curva de dispersión.
- Foti et al. (2014), Cap. 4.2, pp. 216–240 — métodos de dos estaciones (SASW) y estimación de incertidumbre.
