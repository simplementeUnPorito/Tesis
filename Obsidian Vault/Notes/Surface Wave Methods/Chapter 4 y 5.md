# Chapter 4 y 5 — Dispersion and Attenuation Analysis

## Capítulo 4: Análisis de dispersión

El objetivo central del análisis de dispersión es extraer la **[[Dispersion Relation|curva de dispersión]] experimental** a partir del campo de ondas registrado en superficie. Esta curva relaciona la [[Phase Velocity|velocidad de fase]] de las [[Rayleigh Waves|ondas de Rayleigh]] con la frecuencia y constituye el dato de entrada para la inversión (Capítulo 6).

### 4.1 Velocidad de fase y velocidad de grupo

#### Definición física

En un medio no dispersivo, las ondas se propagan con una sola velocidad y la forma de onda no cambia al propagarse. Cuando existe dispersión —como en las [[Surface Waves|ondas superficiales]] en medios heterogéneos— la velocidad depende de la frecuencia y la forma de onda cambia con la distancia (Rayleigh 1877). En este caso coexisten dos conceptos de velocidad (Foti Ec. 4.1):

$$V_{ph} = \frac{\omega}{k}, \qquad V_{g} = \frac{\partial \omega}{\partial k} \tag{4.1}$$

- **Velocidad de fase** ($V_{ph}$): velocidad a la que se propaga una fase particular de la onda (por ejemplo, una cresta o un nodo). Es la velocidad de un punto de fase constante.
- **Velocidad de grupo** ($V_g$): velocidad a la que viaja la energía de un paquete de ondas. Es la velocidad del *envelope* o envolvente del grupo. La Figura 4.2 (p. 207) ilustra visualmente la diferencia: las crestas individuales del tren de ondas viajan a $V_{ph}$, mientras que el grupo completo (la "caja" que contiene la energía) se desplaza a $V_g$.

#### Relación entre las dos velocidades

La relación entre $V_g$ y $V_{ph}$ se obtiene derivando (Foti Ec. 4.2):

$$V_g = V_{ph} + k\frac{dV_{ph}}{dk} = V_{ph}\left(1 - k\frac{dV_{ph}}{d\omega}\right)^{-1} \tag{4.2}$$

En un medio **no dispersivo**, las derivadas de $V_{ph}$ son nulas y $V_g = V_{ph}$. En medios **normalmente dispersivos** (velocidad de fase decrece con la frecuencia, como en la mayoría de los sitios de ingeniería), $dV_{ph}/dk < 0$ y por tanto $V_g < V_{ph}$: el paquete de ondas llega después que cualquier componente individual. Esto es visible en el shot gather: la envolvente del tren de ondas superficiales se desplaza más lentamente que las crestas dentro del tren.

#### Representación en el dominio f-k

La Figura 4.4 (p. 209) ilustra cuatro modos de propagación en el dominio f-k. Para un punto en la curva de dispersión:
- La **velocidad de fase** corresponde a la pendiente de la línea que une el origen con ese punto: $V_{ph} = f/k = \omega/k$.
- La **velocidad de grupo** corresponde a la **pendiente tangente** a la curva en ese punto: $V_g = d\omega/dk$.

Las líneas de velocidad de fase constante son rectas radiales desde el origen; las velocidades de grupo varían con la frecuencia y no son rectas.

#### Caso multimodal

En propagación multimodal, cada modo $n$ tiene sus propias curvas de dispersión de fase y de grupo (Figura 4.3, p. 208). Las curvas de grupo pueden cruzarse o acercarse entre modos incluso cuando las curvas de fase están bien separadas, lo que complica la identificación modal en el dominio del tiempo.

#### Por qué se usa la velocidad de fase en inversión

Los métodos de ondas superficiales para caracterización de sitios explotan principalmente la **velocidad de fase**, por dos razones fundamentales:
1. La velocidad de fase tiene una relación más directa y sensible con la estratigrafía $V_S(z)$ a través de la [[Dispersion Relation|curva de dispersión]].
2. La velocidad de fase se puede medir con mayor precisión a distancias de arreglo típicas en ingeniería: es la razón $\omega/k$ directamente observable en el espacio f-k, mientras que la velocidad de grupo requiere resolución temporal suficiente para separar la envolvente del tren de ondas.

Como se indica al comienzo del capítulo (Foti p. 205): *"group velocities are rarely used for near-surface applications."*

*(Fuente: Foti Ch. 4, Sec. 4.1, pp. 205–208, Ecs. 4.1–4.2, Figs. 4.2–4.4)*

---

### 4.2 Método estacionario de Rayleigh (SSRM)

#### Contexto histórico

El *Steady-State Rayleigh Method* (SSRM) es el **primer método de caracterización de sitio mediante ondas superficiales** desarrollado para aplicaciones de ingeniería. Fue propuesto por Jones (1958, 1962) y posteriormente adoptado en el *Waterways Experiment Station* de Estados Unidos por Ballard (1964). Aunque fue ampliamente reemplazado por métodos más eficientes, estableció los conceptos fundamentales del workflow: generación de ondas, medición de la longitud de onda, y estimación de la velocidad como función de la frecuencia.

#### Principio físico y procedimiento

El SSRM genera ondas superficiales monocromáticas mediante un **vibrador electromecánico** que opera a una frecuencia fija. Cuando el vibrador actúa en dirección perpendicular a la superficie libre, genera predominantemente [[Rayleigh Waves|ondas de Rayleigh]]; orientado horizontalmente en dirección transversal a la línea de medición, genera [[Love Waves|ondas Love]]. La fuente y un receptor único son monitoreados en tiempo real mediante un osciloscopio.

El procedimiento de medición es el siguiente (Fig. 4.5, p. 210):

1. El vibrador opera a una frecuencia $f$ fija y constante.
2. El receptor se desplaza lateralmente alejándose del vibrador hasta encontrar la posición donde las señales del vibrador y del receptor están **en fase**.
3. Esa posición corresponde a un número entero de longitudes de onda de separación — la distancia entre dos posiciones sucesivas en fase es la longitud de onda $\lambda_R$ a esa frecuencia.
4. La velocidad de fase se calcula directamente como:

$$V_R = f \cdot \lambda_R$$

5. El proceso se repite para diferentes frecuencias de operación del vibrador, reconstruyendo la **[[Dispersion Relation|curva de dispersión]] experimental** $V_R(f)$.

#### Determinación robusta de la longitud de onda

Para evitar errores por posición única, se identifican **múltiples posiciones** donde la señal está en fase (separadas por múltiplos enteros de $\lambda_R$). En el plano offset–número de ciclos, estas posiciones se alinean en una recta; la pendiente inversa de esa recta da $\lambda_R$ (Fig. 4.6, p. 211). Este enfoque promedia el efecto del ruido y da una estimación más robusta.

Ejemplo numérico del libro (Fig. 4.6): para $f = 10\,\text{Hz}$ se obtiene $\lambda_R = 34\,\text{m}$ → $V_R = 340\,\text{m/s}$; para $f = 25\,\text{Hz}$ se obtiene $\lambda_R = 10\,\text{m}$ → $V_R = 250\,\text{m/s}$; para $f = 50\,\text{Hz}$ se obtiene $\lambda_R = 4\,\text{m}$ → $V_R = 200\,\text{m/s}$.

#### Variante multicanal: el método CSW

Una extensión con múltiples receptores en posiciones fijas es el *Continuous Surface Wave* (**CSW**) method (Matthews et al. 1996; Menzies y Matthews 1996). En este caso la velocidad de fase se calcula a partir de la pendiente del diagrama de ángulos de fase en función del offset fuente–receptor. Es conceptualmente análogo al MOPA (Sec. 4.4), pero con fuente vibratoria monocromática en lugar de impulsiva.

#### Limitaciones

- **Velocidad de adquisición**: una frecuencia a la vez → curva de dispersión lenta de construir, especialmente si se necesita un rango amplio de frecuencias.
- **Fuente activa controlada**: requiere un vibrador electromecánico, más costoso y menos portable que un sledgehammer.
- **No separa modos**: la velocidad observada es la velocidad de fase aparente del campo total, no la del modo fundamental.
- **Superado por métodos multicanal**: métodos como [[SASW Method|SASW]] (Sec. 4.3) y los métodos de transformada (Sec. 4.6) entregan la curva de dispersión completa en un solo disparo o registro.

A pesar de sus limitaciones, el SSRM demostró la viabilidad del concepto y sentó las bases para el desarrollo de todos los métodos posteriores de ondas superficiales en ingeniería.

*(Fuente: Foti Ch. 4, Sec. 4.2, pp. 208–211, Figs. 4.5–4.6)*

---

### 4.3 SASW — Análisis espectral de ondas superficiales

El método [[SASW Method|SASW]] usa **dos receptores** y una fuente impulsiva. La [[Dispersion Relation|curva de dispersión]] se extrae del **espectro de potencia cruzado** entre las señales de los dos receptores:

$$S_{12}(\omega) = \hat{u}_1(\omega) \cdot \overline{\hat{u}_2(\omega)}$$

La fase del espectro cruzado $\theta_{12}(\omega) = \arg(S_{12})$ representa el desfase acumulado entre los dos receptores a cada frecuencia. La velocidad de fase se calcula como:

$$V_R(\omega) = \frac{\omega (x_2 - x_1)}{\theta_{12}(\omega)}$$

Dado que $\theta_{12}$ solo se mide entre $-\pi$ y $\pi$, es necesario un proceso de **phase unwrapping** (desenvoltura de fase) para recuperar la fase absoluta.

La **función de coherencia** $\gamma^2_{12}(\omega)$ actúa como indicador de calidad: valores próximos a 1 indican que la señal es coherente entre receptores y el resultado es confiable.

**Criterio de filtrado** (Nazarian y Stokoe 1984): para cada separación $D$ entre receptores, solo se conservan longitudes de onda en el rango:
$$D/3 < \lambda < 2D \quad \text{(Ec. 4.11)}$$
Esto evita tanto el campo cercano (longitudes de onda muy grandes) como la pérdida de resolución espacial (longitudes de onda muy pequeñas). Para cubrir un amplio rango de frecuencias es necesario repetir el ensayo con múltiples separaciones $D$.

*Fuente: Foti Ch. 4, Sec. 4.3, pp. 211–220*

---

### 4.4 MOPA — Análisis de fase multi-offset

[[MOPA|MOPA]] (*Multi-Offset Phase Analysis*) es la extensión multicanal de SASW. En lugar de dos receptores, se usa un array completo. Bajo la hipótesis de un **único modo de propagación**, la fase en el receptor $i$ a posición $x_i$ es:

$$\varphi_i(\omega) = -k(\omega) \cdot x_i + \varphi_0(\omega)$$

donde $k(\omega)$ es el número de onda y $\varphi_0(\omega)$ es la fase en el origen. Esto define un sistema lineal matricial:

$$\mathbf{\Phi} = \mathbf{G} \cdot \mathbf{M}$$

donde $\mathbf{\Phi} = [\varphi_1, \ldots, \varphi_N]^T$, $\mathbf{M} = [k, \varphi_0]^T$, y $\mathbf{G}$ contiene las posiciones. La solución en mínimos cuadrados (ponderada por las incertidumbres de fase) entrega:

$$V = \frac{2\pi f}{k}, \quad \sigma_V = \frac{2\pi f}{k^2} \sigma_k$$

**Ventajas respecto a SASW:**
- Utiliza toda la información del array → menor incertidumbre estadística.
- Permite detección de **efectos de campo cercano**: las fases de los primeros receptores se desvían de la tendencia lineal.
- Permite detectar **variaciones laterales**: un cambio de pendiente en la distribución fase-offset a una posición fija del array indica una discontinuidad lateral.
- Ofrece un **test estadístico de linealidad** (test chi-cuadrado, Ec. 4.26–4.27) para evaluar automáticamente si la hipótesis de modo único y campo lejano se cumple.

La no linealidad detectada en las fases puede deberse a:
1. Receptores en campo cercano (eliminar receptores afectados).
2. Variaciones laterales de impedancia (el método de Vignoli y Cassiani 2009 segmenta el array en zonas donde la hipótesis se verifica).

*Fuente: Foti Ch. 4, Sec. 4.4, pp. 220–230*

---

### 4.5 Autocorrelación espacial (SPAC / ESAC)

#### Principio matemático

El método SPAC (*Spatial Autocorrelation*), desarrollado por Aki (1957, 1965) para microtremores, extrae la velocidad de fase a partir de la **función de autocorrelación espacial** del campo de ondas. La autocorrelación espacial se define como (Foti Ec. 4.28):

$$R(\chi) = E\!\left[s(\mathbf{x},t)\,s(\mathbf{x}+\chi,t)\right] = \frac{1}{2\pi}\int_{-\infty}^{\infty} S(\mathbf{k})\,e^{-i\mathbf{k}\cdot\chi}\,d\mathbf{k}$$

donde $\chi$ es el lag espacial y $E[\cdot]$ es el valor esperado. Esta expresión es la **transformada inversa de Fourier del espectro de número de onda**: la autocorrelación espacial codifica directamente el contenido espectral del campo de ondas.

#### Caso de fuente única (ondas unidireccionales)

Para una onda plana de amplitud unitaria con número de onda $\mathbf{k}_0$, la función de autocorrelación normalizada resulta (Foti Ec. 4.32–4.33):

$$\rho(\chi) = \cos(\mathbf{k}_0 \cdot \chi) \tag{4.33}$$

La estimación experimental se realiza mediante los espectros de potencia cruzados normalizados entre pares de receptores (Foti Ec. 4.34):

$$\rho(\chi,\omega) = \frac{\mathfrak{Re}\!\left(\hat{S}_{ij}(\omega)\right)}{\sqrt{\hat{S}_{ii}(\omega)\,\hat{S}_{jj}(\omega)}} \tag{4.34}$$

donde $\hat{S}_{ij}$ es el espectro cruzado promediado y $\hat{S}_{ii}$, $\hat{S}_{jj}$ son los espectros de potencia individuales. El número de onda $k_0(f)$ se obtiene minimizando el error de mínimos cuadrados entre Ec. 4.33 y los coeficientes de autocorrelación experimentales. La Figura 4.24 (p. 233) muestra ejemplos de ajuste a cuatro frecuencias; la curva de dispersión resultante se muestra en la Figura 4.25 (p. 233).

#### Caso de campo isótropo (microtremores pasivos)

Para un **campo de ondas isótropo** —fuentes distribuidas con igual probabilidad en todas las direcciones— el problema tiene simetría radial. En coordenadas polares, la autocorrelación normalizada resulta (Foti Ec. 4.39–4.40):

$$\rho(r) = J_0(k_0 r) \tag{4.40}$$

donde $J_0$ es la función de Bessel de orden cero de primera especie y $r$ es la separación entre receptores. Esta es la expresión original de Aki (1957). La estimación experimental usa un receptor de referencia en el origen del array con la expresión (Foti Ec. 4.41):

$$\rho(r,\omega) = \frac{\mathfrak{Re}\!\left(\hat{S}_{0j}(\omega)\right)}{\sqrt{\hat{S}_{00}(\omega)\,\hat{S}_{jj}(\omega)}} \tag{4.41}$$

donde el subíndice 0 denota el receptor de referencia. En la implementación original de Aki se requería un **array circular** para realizar el promedio azimutal de la autocorrelación a radio constante $r$.

#### ESAC y aplicabilidad a arrays lineales

La versión extendida **ESAC** (*Extended Spatial Autocorrelation*, Ohori et al. 2002) no impone restricciones geométricas: ajusta simultáneamente Ec. 4.33 o 4.40 a todos los pares de receptores disponibles con cualquier separación $r$. Esto la hace aplicable a arreglos lineales y geometrías arbitrarias en campo.

Tanto Ec. 4.33 (unidireccional) como Ec. 4.40 (isótropa) pueden usarse con ESAC. Para datos de **fuente activa** aplica la Ec. 4.33, ya que la dirección de propagación es conocida y la onda es unidireccional. Para datos **pasivos** aplica Ec. 4.40, bajo la hipótesis de isotropía del campo de ruido.

#### Limitaciones

- **No separa modos**: ambas expresiones entregan una velocidad de fase aparente (influencia ponderada de todos los modos). No es posible resolver modos individuales, independientemente de la resolución del arreglo.
- **Efecto de campo cercano**: puede sesgar el coeficiente de autocorrelación del receptor de referencia en datos activos.
- **Hipótesis de isotropía**: para datos pasivos debe verificarse (por ejemplo, por la simetría del espectro f-k).

*(Fuente: Foti Ch. 4, Sec. 4.5, pp. 231–235, Ecs. 4.28–4.41, Figs. 4.24–4.25)*

---

### 4.6 Métodos basados en transformadas

Los métodos de transformada convierten el campo de ondas del dominio espacio–tiempo al dominio **frecuencia–número de onda** (f–k) o **frecuencia–lentitud** (f–p), donde la curva de dispersión aparece como un lugar de máximos de energía.

#### 4.6.1 Dominio f–k (frecuencia–número de onda)

La transformada de Fourier 2D del sismograma $u(x,t)$ produce el espectro $U(k,\omega)$. Los máximos de $|U|^2$ a cada frecuencia corresponden a los números de onda modales, de donde se extrae la velocidad de fase:

$$V_{ph}(\omega) = \frac{\omega}{k_{max}(\omega)}$$

**Ventaja:** permite identificar varios modos de Rayleigh simultáneamente.
**Limitación:** requiere receptores equiespaciados. Para arrays no equiespaciados se emplea *frequency-domain beamforming*:

$$Z(\mathbf{k},\omega) = \mathbf{e}^H \mathbf{W} \mathbf{R} \mathbf{W}^H \mathbf{e}$$

donde $\mathbf{R}$ es la matriz de correlación espaciospectral y $\mathbf{e}$ es el vector de dirección (*steering vector*).

El método MASW (Park et al. 1999) es equivalente a beamforming con peso $w_m = 1/|S(x_m,\omega)|$ (normalización de amplitud). El peso óptimo para corrección de spreading geométrico es $w_m = \sqrt{x_m}$ (Zywicki 1999).

*Nota práctica:* se requiere zero-padding en el dominio espacial para mejorar la resolución del número de onda, y ventaneo (Hanning) para suprimir lóbulos laterales.

#### 4.6.2 Análisis frecuencia–lentitud (τ–p / MASW)

La transformada τ–p (*slant stack* o transformada de Radon lineal) acumula amplitudes a lo largo de líneas de pendiente $p$ (lentitud = $1/V$) en el plano tiempo–offset:

$$\bar{u}(\tau, p) = \int_{-\infty}^{\infty} u(\tau + px, x)\, dx$$

En el dominio frecuencia–lentitud, los modos de propagación aparecen como picos a las lentitudes modales. La conversión a curva de dispersión es directa: $V_{ph} = 1/p_{max}$.

La transformada τ–p puede calcularse a través del espectro f–k evaluando $U(f, k)$ a lo largo de la línea recta $k = fp$, lo que la convierte en una forma de la misma información bajo diferente parametrización.

**Comparación con f–k:** la imagen en frecuencia–lentitud tiende a ser más nítida e intuitiva. MASW (McMechan y Yedlin 1981) usa formalmente la transformada τ–p como base.

#### 4.6.3 ReMi (Refraction Microtremor)

ReMi (Louie 2001) adapta la metodología f–k al caso de **mediciones pasivas con arrays lineales**. Al usar ruido ambiental, la dirección de propagación de las fuentes es desconocida. Para una onda plana con ángulo $\vartheta$ respecto al array:

$$k_x = k \cdot \cos\vartheta$$

La velocidad aparente medida siempre sobrestima la verdadera ($V_{app} \geq V_{true}$). Sin embargo, si el campo de ondas es **isótropo**, el espectro ReMi tiene simetría y sus máximos se aproximan al número de onda verdadero.

El procedimiento de Strobbia y Cassiani (2011) permite la inversión automática del espectro ReMi sin picking manual, verificando además la hipótesis de isotropía por la simetría positiva/negativa del espectro.

*Fuente: Foti Ch. 4, Sec. 4.6, pp. 235–251*

---

### 4.7 Análisis de velocidad de grupo

La velocidad de grupo puede estimarse mediante el **método de filtros múltiples** (Dziewonski et al. 1969): se aplican filtros de banda estrecha centrados en diferentes frecuencias; el pico de la envolvente de cada señal filtrada indica el tiempo de arribo del grupo de ondas y, por tanto, la velocidad de grupo.

**Utilidad limitada en aplicaciones de ingeniería:** la resolución es generalmente insuficiente para separar modos a corta distancia. Su uso principal es en geofísica sismológica (cuenca sedimentaria, corteza). Puede complementar el análisis de velocidad de fase para la separación modal previa a la extracción de la curva de dispersión (Al-Hunaidi 1994; Karray y Lefebre 2009).

*Fuente: Foti Ch. 4, Sec. 4.7, pp. 251–253*

---

### 4.8 Errores e incertidumbres en el análisis de dispersión

Las incertidumbres en la curva de dispersión experimental provienen de:

1. **Ruido no correlado** (ruido ambiental externo): puede cuantificarse estadísticamente si se realizan repeticiones del ensayo.
2. **Ruido coherente** (efectos de campo cercano): introduce sesgo sistemático — no se promedia.
3. **Errores geométricos** (inclinación de geófonos, posicionamiento): efecto menor según O'Neill (2003).
4. **Errores de procesamiento** (propagación de errores a través de las transformadas): difícil de cuantificar formalmente para métodos de transformada.

**Mejor práctica:** realizar múltiples disparos independientes y estimar la distribución estadística de la curva de dispersión. MOPA proporciona estimación directa de incertidumbre (σ_V). Para métodos de transformada, la repetición de shots es el camino más robusto.

El **coeficiente de variación** de la velocidad de fase tiende a ser bajo en alta frecuencia y más elevado en baja frecuencia (longitudes de onda largas), en acuerdo con múltiples estudios (Tuomi y Hiltunen 1996; Lai et al. 2005).

*Fuente: Foti Ch. 4, Sec. 4.8, pp. 253–254*

---

## Capítulo 5: Análisis de atenuación

La [[Attenuation|atenuación]] de las ondas superficiales tiene dos componentes: (a) la **disipación geométrica** (spreading cilíndrico: amplitud ∝ r⁻⁰·⁵) y (b) la **absorción intrínseca** del material, asociada a la viscoelasticidad del suelo. El Capítulo 5 se enfoca en extraer la componente intrínseca para estimar el perfil de **razón de amortiguamiento a pequeñas deformaciones** $D_s(z)$.

La medición de atenuación es más difícil y sensible que la de dispersión, porque las amplitudes son perturbadas por variaciones de acoplamiento, calibración de sensores y superposición modal.

### 5.1 Atenuación de ondas superficiales

En un medio viscoelástico, el número de onda es complejo:

$$k_n^* = k_n - i\alpha_n = \frac{\omega}{V_n} - i\alpha_n$$

donde $V_n$ es la velocidad de fase del modo $n$ y $\alpha_n$ es el coeficiente de atenuación exponencial. La amplitud del modo $n$ decae en campo lejano como:

$$A_n(\omega, r) = A_{n,0}(\omega) \cdot \frac{1}{\sqrt{r}} \cdot e^{-\alpha_n(\omega) \cdot r}$$

La **razón de amortiguamiento de fase de Rayleigh** se define como:

$$D(\omega) = \frac{\mathrm{Im}(k^{*2})}{2 \cdot \mathrm{Re}(k^{*2})}$$

Esta cantidad es análoga a la razón de amortiguamiento en ondas de cuerpo y varía con la frecuencia por la dispersión geométrica (tal como varía la velocidad de fase). El perfil $D_s(z)$ se obtiene por inversión de la curva de amortiguamiento de fase.

*Fuente: Foti Ch. 5, Sec. 5.1, pp. 255–258*

---

### 5.2 Regresión univariante amplitud vs offset

El método más directo: se mide la amplitud espectral $|U_2(r,\omega)|$ (desplazamiento de partícula vertical) en cada receptor y se ajusta la ecuación:

$$|U_2(r,\omega)| = F \cdot Y(r,\omega) \cdot e^{-\alpha_R(\omega) \cdot r}$$

donde $Y(r,\omega)$ es la función de spreading geométrico (calculada a partir del perfil de $V_s$ conocido o estimado), y $F$ es la magnitud de la fuerza fuente.

**Simplificación práctica:** si se asume propagación dominada por el modo fundamental en un medio homogéneo, $Y(r,\omega) \propto r^{-0.5}$, lo que reduce el problema a:

$$|U_2(r,\omega)| = F \cdot \frac{e^{-\alpha_R r}}{\sqrt{r}}$$

Esta simplificación introduce errores cuando los modos superiores son relevantes (oscilaciones en la función de spreading teórica). La fuente $F$ puede tratarse como incógnita adicional para independizar el análisis de su calibración.

*Fuente: Foti Ch. 5, Sec. 5.2, pp. 258–261*

---

### 5.3 Función de transferencia y número de onda complejo

Dispersión y atenuación son dos aspectos del mismo fenómeno propagativo: el número de onda complejo $k^*(\omega) = k_R(\omega) - i\alpha_R(\omega)$ contiene ambos. Es posible estimarlos **simultáneamente** a partir de la función de transferencia de desplazamiento:

$$T(r,\omega) = \frac{u_2(r,\omega)}{F \cdot e^{i\omega t}} = Y(r,\omega) \cdot e^{-ik^*(\omega) \cdot r}$$

En la práctica, $T(r,\omega)$ se estima por **deconvolución** de las trazas respecto al receptor más cercano:

$$\tilde{F}(r,\omega) = \frac{F_i(\omega)}{F_1(\omega)}$$

Esta eliminación de la firma de la fuente hace el método robusto frente a incertidumbres en la fuerza aplicada. La regresión no lineal sobre $k^*(\omega)$ entrega simultáneamente $V_R(\omega)$ y $\alpha_R(\omega)$.

**Iteración necesaria:** $Y(r,\omega)$ requiere conocer el perfil $V_s(z)$, que se obtiene de la inversión de la curva de dispersión. Por tanto, el procedimiento es iterativo: primero se invierte la dispersión, luego se calcula $Y$, luego se estima la atenuación, y se repite hasta convergencia (ver Sec. 6.4.3 para la inversión acoplada).

*Fuente: Foti Ch. 5, Sec. 5.3, pp. 261–265*

---

### 5.4 Estimación multicanal multimodal del número de onda complejo

La superposición modal produce oscilaciones en la amplitud vs offset que contaminan la estimación de $\alpha_R$. Misbah y Strobbia (2014) propusieron un método basado en la extensión del algoritmo **MUSIC** (*Multiple Signal Classification*, Schmidt 1986) al caso del número de onda complejo, capaz de:

- Separar las contribuciones de amplitud de múltiples modos.
- Estimar las curvas de atenuación modales (no solo la aparente).
- Operar sobre arrays no equiespaciados.

El procedimiento incluye: corrección del spreading cilíndrico → transformada al dominio frecuencia → cálculo de la matriz de autocovarianza → extracción de eigenvectores → pseudoespectro cuyo máximo da $k^*_n$ por cada modo $n$.

*Fuente: Foti Ch. 5, Sec. 5.4, pp. 265–269*

---

### 5.5 Enfoques simplificados

#### 5.5.1 Método del ancho de banda a mitad de potencia

El método del **ancho de banda a mitad de potencia** (Badsar et al. 2010) extrae las curvas de atenuación directamente a partir de los **espectros f-k** utilizados en el análisis de dispersión, sin requerir un análisis separado de amplitudes en el dominio espacio-offset.

##### Principio físico

El concepto se basa en la analogía con el análisis de resonancia de estructuras (Clough y Penzien 1993): para un sistema con amortiguamiento, el ancho del pico de respuesta en frecuencia medido a la amplitud $1/\sqrt{2}$ del máximo (criterio de "media potencia") está relacionado con la razón de amortiguamiento. En un espectro f-k, el pico de energía de un modo de propagación tiene un ancho que depende tanto de la resolución espectral del array (efecto de ventana) como del amortiguamiento intrínseco del suelo.

El mismo concepto se aplica al espectro frecuencia–número de onda: la anchura del pico espectral a la amplitud $1/\sqrt{2}$ del máximo en la dirección del número de onda, para una frecuencia fija, se relaciona con el coeficiente de atenuación espacial $\alpha_R(\omega)$ (Badsar et al. 2010).

##### El problema del ventaneo espacial

El principal obstáculo del método es el efecto del **muestreo espacial finito**: la limitación de la ventana espacial (apertura finita del array) produce un ensanchamiento artificial del pico espectral en el dominio del número de onda — exactamente el *spectral leakage* discutido en la Sec. 3.3.5. Este ensanchamiento artificial **sobreestima** el amortiguamiento: el ancho observado del pico es mayor que el atribuible únicamente a la atenuación intrínseca.

Badsar et al. (2010) resolvieron este problema evaluando la **atenuación artificial** introducida por el ventaneo espacial mediante el estudio de la función de respuesta del array (función de ventana espacial). La atenuación espacial verdadera se obtiene substrayendo la contribución artificial de la estimada:

$$\alpha_{R,\text{real}} = \alpha_{R,\text{estimado}} - \alpha_{R,\text{artificial}}$$

Este procedimiento de corrección hace el método aplicable a arrays de apertura moderada, que son los más comunes en ingeniería.

##### Capacidad multimodal

Una ventaja del método es que puede identificar los coeficientes de atenuación de **diferentes modos de propagación**, siempre que sus contribuciones espectrales puedan separarse en el plano f-k. La Fig. 5.10 (p. 269) muestra los resultados para los datos de la Fig. 5.7 (24 geófonos, $\Delta x = 2\,\text{m}$, sledgehammer): se identificaron tres modos de propagación, y la razón de amortiguamiento del modo fundamental varía entre 1% y 4% en el rango 5–40 Hz.

*(Fuente: Foti Ch. 5, Sec. 5.5.1, pp. 268–270, Figs. 5.9–5.10)*

---

#### 5.5.2 Decaimiento espacial de la intensidad de Arias

El método propuesto por Badsar et al. (2011) evita el paso intermedio de estimar la curva de atenuación $\alpha_R(\omega)$ de las ondas de Rayleigh. En cambio, invierte **directamente el decaimiento de la intensidad de Arias con el offset** para obtener el perfil de razón de amortiguamiento $D_s(z)$.

##### Concepto de la intensidad de Arias

La **intensidad de Arias** de una señal sísmica es proporcional a la integral del cuadrado de la aceleración en el tiempo:

$$I_A(x) = \frac{\pi}{2g}\int_0^{T_d} a^2(x,t)\,dt$$

Es una medida de la energía total contenida en el registro a cada offset $x$. En un medio viscoelástico, la intensidad de Arias decae con la distancia a la fuente de manera que depende tanto del spreading geométrico como de la absorción intrínseca del suelo.

##### Procedimiento

1. Se invierte la curva de dispersión (Sec. 4.6) para obtener un modelo elástico inicial $V_s(z)$ y se estima el perfil de Poisson $\nu(z)$ de forma independiente (por ejemplo, de $V_P$).
2. Se calcula el modelo directo viscoelástico: se ajusta iterativamente el perfil de razón de amortiguamiento $D_s(z)$ hasta que el decaimiento espacial simulado de la intensidad de Arias coincide con el observado experimentalmente.

##### Limitación fundamental

La principal exigencia del método es que requiere un **modelo elástico preciso en términos de velocidades de onda S y P y del coeficiente de Poisson**. Estos perfiles deben evaluarse de forma independiente y con alta exactitud antes de aplicar el método. Cualquier error en el modelo elástico se propagará directamente al perfil de amortiguamiento estimado.

Esta dependencia fuerte del modelo elástico hace que el método sea más adecuado como complemento de una inversión conjunta que como procedimiento independiente.

*(Fuente: Foti Ch. 5, Sec. 5.5.2, p. 270)*

---

### 5.6 Incertidumbre en la medición de atenuación

La incertidumbre en los coeficientes de atenuación es mayor que en la velocidad de fase porque:

1. **Scattering por heterogeneidades** (cracks, cavidades, discontinuidades topográficas) produce reflexión y difracción que reduce la amplitud aparente → sobreestimación de la atenuación intrínseca.
2. **Variaciones de acoplamiento y calibración** entre receptores → perturbaciones de amplitud no atribuibles al suelo.
3. **Superposición modal** → oscilaciones en la amplitud que no siguen el decaimiento exponencial simple.

Los coeficientes estimados son valores **aparentes**: combinan contribuciones de varios modos ponderadas por su excitación. Solo el método multimodal (Sec. 5.4) separa las contribuciones modales.

*Fuente: Foti Ch. 5, Sec. 5.6, pp. 270–271*

---

## Síntesis

El análisis de dispersión produce la curva de velocidad de fase aparente $V_R(f)$. La elección del método determina qué información se puede extraer:

| Método | Tipo de fuente | Receptores | Puede separar modos | Incertidumbre estadística |
|--------|---------------|------------|---------------------|--------------------------|
| SSRM | Activa (vibrador) | 1 | No | Baja resolución |
| SASW | Activa | 2 | No | Limitada |
| MOPA | Activa | Array lineal | No (asume modo único) | Estimación directa |
| f–k / MASW | Activa | Array lineal | Sí (teóricamente) | Por repetición de shots |
| SPAC / ESAC | Activa o pasiva | Array 2D o lineal | No | Por ensemble |
| ReMi | Pasiva | Array lineal | No | Requiere isotropía |

La curva de dispersión experimental es **siempre aparente**: refleja la influencia ponderada de varios modos. La distinción entre modos se vuelve crítica en el proceso de inversión (ver Capítulo 6).

El análisis de atenuación añade la curva $\alpha_R(f)$, que junto con la curva de dispersión constituye el conjunto de datos para la inversión acoplada (Sec. 6.4.3) que entrega perfiles de $V_s(z)$ y $D_s(z)$.

---

## Fuentes

- PDF: Sebastiano Foti Chapter 4 (pp. 205–254)
- PDF: Sebastiano Foti Chapter 5 (pp. 255–271)
- Secciones clave: 4.1–4.8, 5.1–5.6
