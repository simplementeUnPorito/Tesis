# Chapter 4 y 5 — Dispersion and Attenuation Analysis

## Capítulo 4: Análisis de dispersión

El objetivo central del análisis de dispersión es extraer la **curva de dispersión experimental** a partir del campo de ondas registrado en superficie. Esta curva relaciona la velocidad de fase de las ondas de Rayleigh con la frecuencia y constituye el dato de entrada para la inversión (Capítulo 6).

### 4.1 Velocidad de fase y velocidad de grupo

Dos conceptos de velocidad coexisten en un medio dispersivo:

- **Velocidad de fase** ($V_{ph}$): velocidad a la que viaja una cresta de onda a frecuencia dada.
  $$V_{ph} = \frac{\omega}{k}$$
- **Velocidad de grupo** ($V_g$): velocidad a la que viaja la energía de un paquete de ondas.
  $$V_g = \frac{\partial \omega}{\partial k} = V_{ph}\left(1 - \frac{k}{V_{ph}}\frac{\partial V_{ph}}{\partial k}\right)^{-1}$$

En un medio no dispersivo $V_g = V_{ph}$. En medios estratificados reales, la dispersión geométrica hace que $V_g \neq V_{ph}$. Los métodos de ondas superficiales explotan principalmente la **velocidad de fase**, que tiene una relación más directa con la estratigrafía.

→ Ver concepto: [[Dispersion in Layered Media]]

*Fuente: Foti Ch. 4, Sec. 4.1, pp. 205–208*

---

### 4.2 Método estacionario de Rayleigh (SSRM)

El *Steady-State Rayleigh Method* (SSRM) es el más antiguo y conceptualmente más simple. Una fuente vibratoria genera ondas monocromáticas; un receptor se desplaza lateralmente hasta encontrar la posición donde la señal queda en fase con la fuente. Esa distancia es la longitud de onda $\lambda$ a esa frecuencia, y la velocidad se obtiene como:
$$V_R = f \cdot \lambda$$

**Limitaciones:** el proceso es lento (una frecuencia a la vez), requiere una fuente controlada y produce solo la curva del modo fundamental aparente. En la práctica fue reemplazado por métodos multicanal.

*Fuente: Foti Ch. 4, Sec. 4.2, pp. 208–211*

---

### 4.3 SASW — Análisis espectral de ondas superficiales

El método SASW usa **dos receptores** y una fuente impulsiva. La curva de dispersión se extrae del **espectro de potencia cruzado** entre las señales de los dos receptores:

$$S_{12}(\omega) = \hat{u}_1(\omega) \cdot \overline{\hat{u}_2(\omega)}$$

La fase del espectro cruzado $\theta_{12}(\omega) = \arg(S_{12})$ representa el desfase acumulado entre los dos receptores a cada frecuencia. La velocidad de fase se calcula como:

$$V_R(\omega) = \frac{\omega (x_2 - x_1)}{\theta_{12}(\omega)}$$

Dado que $\theta_{12}$ solo se mide entre $-\pi$ y $\pi$, es necesario un proceso de **phase unwrapping** (desenvoltura de fase) para recuperar la fase absoluta.

La **función de coherencia** $\gamma^2_{12}(\omega)$ actúa como indicador de calidad: valores próximos a 1 indican que la señal es coherente entre receptores y el resultado es confiable.

**Criterio de filtrado** (Nazarian y Stokoe 1984): para cada separación $D$ entre receptores, solo se conservan longitudes de onda en el rango:
$$D/3 < \lambda < 2D \quad \text{(Ec. 4.11)}$$
Esto evita tanto el campo cercano (longitudes de onda muy grandes) como la pérdida de resolución espacial (longitudes de onda muy pequeñas). Para cubrir un amplio rango de frecuencias es necesario repetir el ensayo con múltiples separaciones $D$.

→ Ver concepto: [[SASW Method]]

*Fuente: Foti Ch. 4, Sec. 4.3, pp. 211–220*

---

### 4.4 MOPA — Análisis de fase multi-offset

MOPA (*Multi-Offset Phase Analysis*) es la extensión multicanal de SASW. En lugar de dos receptores, se usa un array completo. Bajo la hipótesis de un **único modo de propagación**, la fase en el receptor $i$ a posición $x_i$ es:

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

→ Ver concepto: [[MOPA Method]]

*Fuente: Foti Ch. 4, Sec. 4.4, pp. 220–230*

---

### 4.5 Autocorrelación espacial (SPAC / ESAC)

El método SPAC (*Spatial Autocorrelation*), desarrollado por Aki (1957, 1965) para microtremores, se basa en la propiedad de que la **función de autocorrelación espacial** del campo de ondas contiene información sobre el número de onda.

Para un campo de ondas isótropo (ruido ambiental con fuentes distribuidas uniformemente en todas las direcciones), la función de autocorrelación normalizada es:

$$\rho(r) = J_0(k_0 r)$$

donde $J_0$ es la función de Bessel de orden cero y $r$ es la separación entre receptores. Estimando $\rho(r,\omega)$ experimentalmente a través de los espectros de potencia cruzados normalizados, se puede extraer $k_0$ para cada frecuencia y así la curva de dispersión.

La versión extendida **ESAC** (Ohori et al. 2002) no impone restricciones geométricas al array, lo que la hace más práctica.

**Limitaciones:**
- Solo proporciona una velocidad aparente (sin separación de modos).
- El efecto de campo cercano puede sesgar el coeficiente de autocorrelación del receptor de referencia.
- Para datos de fuente activa: no requiere distribución isótropa (la dirección es conocida). Para pasivos: la hipótesis de isotropía debe verificarse por la simetría del espectro.

*Fuente: Foti Ch. 4, Sec. 4.5, pp. 231–235*

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

→ Ver concepto: [[f-k Transform]]

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

La atenuación de las ondas superficiales tiene dos componentes: (a) la **disipación geométrica** (spreading cilíndrico: amplitud ∝ r⁻⁰·⁵) y (b) la **absorción intrínseca** del material, asociada a la viscoelasticidad del suelo. El Capítulo 5 se enfoca en extraer la componente intrínseca para estimar el perfil de **razón de amortiguamiento a pequeñas deformaciones** $D_s(z)$.

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

#### 5.5.1 Ancho de banda a mitad de potencia

Derivado del espectro f–k: la anchura del pico espectral a la frecuencia $f_0$ y número de onda $k_0$ puede relacionarse con el coeficiente de atenuación mediante el criterio de **media potencia** (amplitud = máximo / √2). Es análogo al método de resonancia de columna en laboratorio.

**Limitación:** la resolución espacial finita del array genera un ensanchamiento artificial del pico. Badsar et al. (2010) propusieron una corrección por ventaneo espacial.

#### 5.5.2 Decaimiento espacial de la intensidad de Arias

Método propuesto por Badsar et al. (2011): en lugar de estimar la curva de atenuación intermedia, se invierte directamente el decaimiento de la **intensidad de Arias** con el offset. Requiere un modelo elástico preciso ($V_s$ y $\nu$) como modelo de partida.

*Fuente: Foti Ch. 5, Sec. 5.5, pp. 268–270*

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
