# Linear Wave Propagation in Vertically Inhomogeneous Continua

## Introducción

Este capítulo desarrolla la teoría de propagación de [[Surface Waves|ondas superficiales]] en medios:

- [[Elasticity|elásticos lineales]]
- [[Viscoelastic Media|viscoelásticos lineales]]

con el objetivo de establecer la base física para el **modelado directo (forward modeling)** utilizado en métodos de caracterización del subsuelo mediante [[Surface Waves|ondas superficiales]].

Aunque el desarrollo teórico incluye tanto [[Love Waves]] como [[Rayleigh Waves]], el capítulo se enfoca principalmente en **Rayleigh waves**, debido a su mayor relevancia en aplicaciones prácticas de exploración geofísica, ingeniería geotécnica y caracterización sísmica de sitio.

Las [[Rayleigh Waves]] son particularmente importantes porque dominan el campo de ondas registrado por geófonos en mediciones de superficie y contienen información directa sobre el perfil de velocidades de [[S-Waves]]. En campo, a distancias de una o dos [[Wavelength|longitudes de onda]] desde la fuente, las [[Surface Waves|ondas superficiales]] representan ~67% de la energía total generada por una fuente puntual vertical, con decaimiento geométrico $\propto r^{-0.5}$ frente a $r^{-2}$ de las [[Body Waves|ondas de cuerpo]]. Esta diferencia explica por qué el campo de ondas queda dominado por las componentes de Rayleigh a medida que se aleja de la fuente.

El contenido del capítulo progresa desde los fundamentos de la mecánica ondulatoria (Sec. 2.1) hasta la derivación rigurosa de las eigenfunciones de Rayleigh en semiespacios homogéneos (Sec. 2.2), la teoría de Love waves (Sec. 2.3), la generalización a medios verticalmente heterogéneos con múltiples modos de propagación (Sec. 2.4), y finalmente la extensión al caso viscoelástico que fundamenta la medición de [[Attenuation|atenuación]] en campo (Sec. 2.5). Este arco argumental es la columna vertebral teórica de todos los métodos de [[Adquisición de Datos|adquisición]], [[Procesamiento de Señales|procesamiento]] e [[Inversión|inversión]] discutidos en los capítulos siguientes.

---

## Estructura del capítulo

El capítulo se divide en cinco secciones principales.

### 2.1 Basic notions of wave propagation

Esta sección introduce los fundamentos de propagación de ondas en medios continuos.

Primero se distinguen dos clases fundamentales de movimiento ondulatorio:

- **[[Hyperbolic Waves]]**
- **[[Wave Dispersion]]**

Luego se introducen las ecuaciones de movimiento en sólidos elásticos y la propagación de [[Body Waves|ondas de cuerpo]] en medios:

- homogéneos
- isotrópicos
- elásticos lineales

Esto permite introducir parámetros fundamentales como:

- [[Wavenumber]]
- [[Angular Frequency]]
- [[Phase Velocity]]
- [[Group Velocity]]

En este contexto aparecen las [[Body Waves|ondas de cuerpo]]:

- [[P-waves]]
- [[S-Waves]]

También se introducen ondas armónicas de la forma:

$$
\phi(x,t) = A e^{i(kx-\omega t)}
$$

La relación funcional entre frecuencia y [[Wavenumber|número de onda]] constituye la [[Dispersion Relation]], que es central para describir ondas dispersivas.

### 2.2 Rayleigh waves in homogeneous elastic continua

Esta sección demuestra la existencia de [[Rayleigh Waves|ondas de Rayleigh]] en un **[[Elastic Half Space|semiespacio elástico homogéneo]]** y establece sus propiedades fundamentales: [[Phase Velocity|velocidad de fase]], [[Attenuation|decaimiento en profundidad]], polarización elíptica y no-dispersividad. El desarrollo formal utiliza el método de [[Elastic Wave Potentials|potenciales de onda elástica]] (§2.2.2), que descompone el campo de desplazamiento en componentes irrotacional ([[P-waves|P]]) y solenoidal ([[SV-wave|SV]]) mediante la [[Helmholtz Decomposition|descomposición de Helmholtz]], y aplica las condiciones de esfuerzo nulo en la superficie libre.

El resultado principal — la **ecuación secular de Rayleigh** — es un polinomio implícito de tercer grado en la razón $V_R^2/V_S^2$ que determina la velocidad de la onda en función de $V_S$ y $V_P$ (o equivalentemente del [[Poisson Ratio|coeficiente de Poisson]]). Para $\nu = 0.25$, $V_R \approx 0.9194\,V_S$. La velocidad $V_R$ es **siempre ligeramente menor que $V_S$**, lo que asegura que la energía de Rayleigh quede atrapada en la superficie.

Este resultado es **la base teórica** de todos los métodos modernos de [[MASW Method|MASW]], [[SASW Method|SASW]] y métodos pasivos de ondas superficiales: la [[Inversión|inversión]] recupera $V_S(z)$ a partir de la variación de $V_R$ con la frecuencia en medios estratificados (Sec. 2.4).

### 2.3 Love waves in layered media

Esta sección establece las condiciones necesarias para la existencia de [[Love Waves|ondas de Love]] y deriva su relación de dispersión en el sistema más simple posible: una **capa elástica sobre un semiespacio elástico**. A diferencia de las [[Rayleigh Waves|ondas de Rayleigh]], que existen en cualquier semiespacio elástico (incluso homogéneo), las ondas de Love **requieren estratificación** para existir: son ondas SH guiadas por el contraste de impedancia entre la capa (velocidad $V_{S1}$) y el semiespacio ($V_{S2} > V_{S1}$). Sin contraste de velocidad, no hay onda de Love.

```text
capa elástica (VS1, ρ1, espesor h)
sobre
semi-espacio elástico (VS2 > VS1, ρ2)
```

La sección estudia:

- **condiciones de guiado**: cuándo el ángulo de incidencia de las ondas SH produce reflexión total interna y da lugar a una onda guiada atrapada en la capa
- **[[Dispersion Relation|relación de dispersión]]**: la ecuación trascendente que relaciona la [[Phase Velocity|velocidad de fase]] con la frecuencia y los parámetros del medio
- **comparación con [[Rayleigh Waves|ondas de Rayleigh]]**: las ondas de Love son puramente SH (no hay componente vertical), lo que las hace independientes de $V_P$ y más sensibles al contraste de [[Shear Modulus|módulo de corte]].

Una diferencia fundamental operativa es que las ondas de Love presentan **dispersión geométrica pura** ([[Geometric Dispersion]]) sin la complicación del acoplamiento P–SV. Sus [[Dispersion Curve|curvas de dispersión]] son más simples de interpretar y menos susceptibles a la [[Mode Superposition|superposición modal]] ambigua. En campo se requieren [[Geophone|geófonos]] horizontales transversales para registrarlas, a diferencia de los geófonos verticales estándar usados en [[MASW Method|MASW]] para [[Rayleigh Waves|Rayleigh]].

### 2.4 Surface waves in vertically inhomogeneous media

Esta sección extiende el análisis a medios donde las propiedades mecánicas varían con la profundidad.

Se analizan:

- propagación de [[Rayleigh Waves]]
- propagación de [[Love Waves]]
- [[Layered Media|medios estratificados]]

Se introducen conceptos clave como:

- [[Mode Superposition]]
- [[Phase Velocity|velocidad de fase]] efectiva ([[Phase Velocity]])

También se revisita el [[Lamb's Problem]], que describe la generación de [[Surface Waves|ondas superficiales]] por una fuente puntual aplicada sobre la superficie libre del medio.

Este problema corresponde a la resolución de un problema de contorno no homogéneo asociado a la generación de ondas.

### 2.5 Wave propagation in dissipative media

La última sección introduce la propagación de ondas en medios disipativos.

Se discuten:

- modelos constitutivos de [[Viscoelastic Media]]
- mecanismos de [[Attenuation]]

Utilizando el [[Correspondence Principle|principio de correspondencia elástico–viscoelástico]], se obtienen las propiedades de propagación de [[Body Waves|ondas de cuerpo]] en [[Viscoelastic Media|medios viscoelásticos]].

Posteriormente se analiza la propagación de ondas superficiales en medios:

- viscoelásticos
- verticalmente heterogéneos

La atención se centra en la resolución del [[Rayleigh Eigenproblem]] en medios débilmente disipativos.

Este resultado constituye la base teórica de muchos procedimientos utilizados en geofísica para modelar la propagación de ondas superficiales en medios reales, donde la disipación de energía no puede despreciarse.

---

## 2.1 Basic notions of wave propagation

> Fuente: Foti et al. (2014), Sección 2.1, pp. 35–65.

Esta sección establece el vocabulario y las herramientas matemáticas comunes a toda la propagación de ondas en medios continuos: tipos de ondas, parámetros cinemáticos (frecuencia, [[Wavenumber|número de onda]], [[Phase Velocity|velocidad de fase]], [[Group Velocity|velocidad de grupo]]), y la descripción del movimiento de partícula ([[Body Waves|ondas de cuerpo]] P y S, polarización). Estos conceptos son el vocabulario técnico que atraviesa todos los capítulos del libro.

### 2.1.1 Two Categories of Wave Motion

Una [[Wave]] puede definirse como cualquier perturbación reconocible que se transfiere de una parte de un medio a otra con una velocidad de propagación identificable. Durante su propagación la perturbación puede:

- deformarse
- atenuarse
- cambiar su velocidad

mientras la señal siga siendo identificable.

Un criterio fundamental de clasificación distingue entre:

- **[[Hyperbolic Waves]]**
- **[[Wave Dispersion]]**

Esta clasificación sigue siendo útil incluso al restringirse al caso de [[Linear Waves]].

#### [[Hyperbolic Waves]]

Las [[Hyperbolic Waves]] están descritas por [[Hyperbolic Partial Differential Equations]] y representan el caso más simple de propagación ondulatoria.

Un ejemplo clásico es la [[1D Wave Equation]]:

$$
\frac{\partial^2 \phi}{\partial x^2} = \frac{1}{c_0^2}\frac{\partial^2 \phi}{\partial t^2}
$$

- $\phi(x,t)$: campo de la onda
- $x$: coordenada espacial
- $t$: tiempo
- $c_0$: [[Phase Velocity]]

La solución general es la [[d'Alembert Solution]]:

$$
\phi(x,t)=f(x-c_0t)+g(x+c_0t)
$$

Esto representa la [[Wave Superposition]] de dos ondas:

- $f(x-c_0t)$ → propagándose hacia la derecha
- $g(x+c_0t)$ → propagándose hacia la izquierda

ambas con velocidad $c_0$.

![[Pasted image 20260311151531.png]]

La propiedad clave de las ondas hiperbólicas es que **no se distorsionan durante la propagación**, porque la velocidad de propagación no depende de la frecuencia y todos los [[Wavenumber|números de onda]] viajan con la misma [[Phase Velocity]]:

$$
c = c_0
$$

#### [[Wave Dispersion]]

Las [[Wave Dispersion]] presentan un comportamiento distinto. Se caracterizan porque la [[Angular Frequency]] depende del [[Wavenumber]]:

$$
\phi(x,t)=A e^{i[kx-\omega(k)t]}
$$

- $A$: amplitud
- $k$: [[Wavenumber]]
- $\omega(k)$: [[Angular Frequency]] dependiente de $k$

La [[Phase Velocity]] corresponde a la velocidad de propagación de un punto de fase constante:

$$
kx-\omega(k)t=\text{const}
$$

por lo que:

$$
c=\frac{\omega(k)}{k}
$$

Si $\omega(k)$ depende de $k$, la [[Phase Velocity|velocidad de fase]] no es constante.

Cuando distintas componentes espectrales viajan con diferentes velocidades:

- cada frecuencia se propaga a una velocidad distinta
- las señales con múltiples frecuencias cambian de forma

este fenómeno se denomina [[Wave Dispersion]].

![[Pasted image 20260311152029.png]]

La solución general de una ecuación de onda dispersiva puede expresarse mediante una [[Fourier Integral]]:

$$
\phi(x,t)=\frac{1}{2\pi}\int_{-\infty}^{\infty}A(k)e^{i[kx-\omega(k)t]}dk
$$

Esto representa una [[Wave Superposition]] de ondas monocromáticas, donde cada componente tiene su propio [[Wavenumber]] y su propia [[Phase Velocity]].

#### Ejemplo físico: [[Water Waves]]

Un ejemplo clásico de dispersión ocurre en [[Surface Water Waves]], donde la [[Dispersion Relation]] depende de la profundidad del agua.

| Régimen | Relación de dispersión |
| --- | --- |
| Agua profunda | $\omega=\sqrt{gk}$ |
| Agua somera | $\omega=k\sqrt{gh}$ |
| Profundidad intermedia | $\omega=\sqrt{gk\tanh(kh)}$ |

![[Pasted image 20260311154523.png]]

#### Intersección entre ondas hiperbólicas y dispersivas

Las categorías no son mutuamente excluyentes. Existen ondas que son soluciones de [[Hyperbolic Partial Differential Equations|ecuaciones hiperbólicas]] y, sin embargo, pueden presentar [[Wave Dispersion|dispersión]] dependiendo del medio de propagación.

En medios **homogéneos elásticos lineales**, las [[Body Waves|ondas de cuerpo]] son hiperbólicas y **no dispersivas**: la velocidad de fase no depende de la frecuencia. En cambio, en medios **heterogéneos** (estratificados), **porosos** o **disipativos**, las mismas ecuaciones producen dispersión:

- [[Body Waves|Ondas de cuerpo]] en medios elásticos homogéneos → no dispersivas (velocidad constante)
- [[Body Waves|Ondas de cuerpo]] en medios disipativos ([[Viscoelastic Media|viscoelásticos]]) → dispersivas por [[Material Dispersion|dispersión material]]
- [[Surface Waves|Ondas superficiales]] en medios estratificados → dispersivas por [[Geometric Dispersion|dispersión geométrica]]

La distinción es fundamental para los métodos de ondas superficiales: la [[Geometric Dispersion|dispersión geométrica]] es el fenómeno explotado para recuperar perfiles de velocidad del subsuelo, mientras que la [[Material Dispersion|dispersión material]] (Sec. 2.5) permite estimar el amortiguamiento intrínseco.

#### Tipos de dispersión

Es importante distinguir entre:

##### [[Material Dispersion]]

Originada por las propiedades constitutivas del medio.

Ejemplos:

- [[Viscoelastic Media]]
- [[Porous Media]]

##### [[Geometric Dispersion]]

Aparece cuando el medio es [[Vertically Inhomogeneous Media]] o estratificado.

Consecuencias:

- la [[Phase Velocity]] depende de la frecuencia
- aparecen múltiples [[Surface Wave Modes]]

#### Implicación para [[Surface Waves]]

Un resultado importante que se deriva del análisis de la [[Dispersion Relation|relación de dispersión]] es que:

- las [[Rayleigh Waves|ondas de Rayleigh]] en un [[Elastic Half Space|semiespacios elástico homogéneo]] son **no dispersivas** — la velocidad de fase es constante, independiente de la frecuencia, y el perfil de profundidad de la onda es siempre el mismo.
- se vuelven **dispersivas** en [[Layered Media|medios estratificados]] — distintas frecuencias penetran a distintas profundidades y experimentan propiedades elásticas diferentes, generando una relación $V_{ph}(f)$ que contiene la información sobre el perfil $V_S(z)$.

Esta propiedad de dispersión geométrica es el fundamento físico de todos los métodos de inversión de ondas superficiales: la variación de la [[Phase Velocity|velocidad de fase]] con la frecuencia se usa como dato observacional para recuperar el perfil de velocidades del subsuelo.

### 2.1.2 Group Velocity

La **[[Group Velocity|velocidad de grupo]]** describe la velocidad a la que se propaga la envolvente de un paquete de ondas en un medio dispersivo.

$$
c_g = \frac{d\omega}{dk}
$$

Si la [[Phase Velocity|velocidad de fase]] es:

$$
c_0 = \frac{\omega}{k}
$$

entonces también puede escribirse como:

$$
c_g = c_0 + k\frac{dc_0}{dk}
$$

![[Pasted image 20260311155937.png]]

Si se superponen dos ondas de frecuencias y [[Wavenumber|números de onda]] muy cercanos, aparece una oscilación rápida interna y una envolvente lenta:

- la onda portadora se mueve con [[Phase Velocity]]
- la envolvente se mueve con [[Group Velocity]]

En un medio dispersivo, ambas velocidades no coinciden en general.

Si se consideran dos ondas monocromáticas de amplitud igual:

$$
\phi(x,t)=A\sin(k_1x-\omega_1t)+A\sin(k_2x-\omega_2t)
$$

con

$$
k_m = \frac{k_1+k_2}{2}, \qquad \Delta k = \frac{k_1-k_2}{2}
$$

$$
\omega_m = \frac{\omega_1+\omega_2}{2}, \qquad \Delta \omega = \frac{\omega_1-\omega_2}{2}
$$

la señal puede reescribirse como:

$$
\phi(x,t)=2A\cos(\Delta k x-\Delta \omega t)\sin(k_m x-\omega_m t)
$$

Esta expresión muestra:

- una portadora senoidal de [[Wavenumber|número de onda]] medio $k_m$ y frecuencia media $\omega_m$
- una envolvente moduladora que se desplaza con velocidad $\Delta\omega/\Delta k$

Al tomar el límite para $\Delta k \to 0$ se obtiene:

$$
c_g = \lim_{\Delta k \to 0}\frac{\Delta \omega}{\Delta k}=\frac{d\omega}{dk}
$$

La velocidad de grupo puede interpretarse como la velocidad de propagación de la modulación de un paquete de ondas y, en medios dispersivos, se asocia con la propagación de energía de la perturbación.

Esto implica que:

- si $c_0 > c_g$, la portadora parece avanzar desde la parte trasera del grupo hacia el frente
- si $c_0 < c_g$, la portadora parece desplazarse desde el frente hacia atrás

![[Pasted image 20260311155917.png]]

#### Aplicación a geófonos

En arreglos de geófonos no se registra una onda monocromática ideal, sino paquetes de ondas con contenido espectral finito. Por eso, la velocidad de grupo tiene impacto directo en cómo llega la energía al arreglo.

Impacto práctico:

- controla el avance de la envolvente observable en el registro
- afecta la localización temporal de máximos de energía
- influye en la interpretación de señales dispersivas de [[Surface Waves]], [[Rayleigh Waves]] y [[Love Waves]]
- ayuda a distinguir entre propagación de fase y propagación efectiva del paquete registrado

#### Implicaciones para el diseño experimental

- El espaciamiento entre geófonos debe permitir resolver el desplazamiento de la envolvente.
- El largo total del arreglo debe ser suficiente para observar la dispersión del paquete.
- El ancho de banda de adquisición condiciona qué tan bien puede estimarse $d\omega/dk$.
- Confundir [[Phase Velocity]] con velocidad de transporte de energía lleva a interpretaciones físicas erróneas.

### 2.1.3 Body Waves in Unbounded Homogeneous Elastic Media

Esta sección introduce el modelo fundamental de propagación de ondas en medios elásticos continuos.

A partir de las ecuaciones de la elastodinámica lineal se demuestra la existencia de dos tipos fundamentales de [[Body Waves|ondas de cuerpo]]:

- [[P-waves]]
- [[S-Waves]]

Estas ondas constituyen los modos básicos de propagación en sólidos elásticos y sirven como base física para la formación de [[Surface Waves]].

#### Marco físico

El modelo considera un medio continuo con las siguientes hipótesis, cada una con implicaciones físicas concretas:

- **medio elástico lineal** — la respuesta deformacional es proporcional al esfuerzo aplicado y completamente reversible; no hay histéresis ni disipación de energía (extensión viscoelástica en §2.5).
- **medio isotrópico** — las propiedades mecánicas son independientes de la dirección; el medio queda caracterizado por únicamente dos parámetros escalares ([[Lamé Constants|constantes de Lamé]] $\lambda, \mu$).
- **deformaciones pequeñas** — se aplica la teoría lineal de deformaciones ($|\nabla u| \ll 1$), que permite ignorar los términos cuadráticos en el [[Strain Tensor|tensor de deformación]] y superponer soluciones.
- **medio homogéneo** — las propiedades son constantes en el espacio; no hay variación espacial de $\lambda$, $\mu$ o $\rho$. Esta hipótesis se relaja en la Sec. 2.4 para medios estratificados.
- **dominio no acotado** — sin reflexiones desde bordes laterales o inferior; condición de campo lejano. En la práctica, esta condición se aplica mediante condiciones de [[Radiation Condition|condición de radiación de Sommerfeld]].

#### Campo de desplazamiento

La variable fundamental es el **campo vectorial de desplazamiento** $\mathbf{u}(\mathbf{x}, t)$, que asigna a cada punto material $\mathbf{x}$ del continuo su desplazamiento respecto a la posición de equilibrio en el instante $t$.

En el caso unidimensional simplificado se escribe $u(x,t)$, pero en el problema general tridimensional $\mathbf{u} = (u_1, u_2, u_3)$ tiene tres componentes independientes. Las mediciones geofísicas de campo registran típicamente la componente vertical $u_3$ (geófonos verticales) y/o las componentes horizontales $u_1, u_2$ (geófonos de tres componentes), en función del tipo de onda de interés: la componente vertical registra las [[Rayleigh Waves|ondas de Rayleigh]], mientras que la componente horizontal transversal registra las [[Love Waves|ondas de Love]].

#### Tensor de deformación

Las deformaciones se describen mediante el [[Strain Tensor|tensor de deformaciones infinitesimal]] $\boldsymbol{\varepsilon}$, que cuantifica el cambio relativo de longitudes y ángulos. Para deformaciones pequeñas ($|\nabla \mathbf{u}| \ll 1$), la parte simétrica del gradiente de desplazamiento es suficiente:

$$
\boldsymbol{\varepsilon} =
\frac{1}{2}
(\nabla \mathbf{u} + (\nabla \mathbf{u})^T)
$$

La componente diagonal $\varepsilon_{ii}$ representa la deformación longitudinal en la dirección $i$ (extensión/compresión), mientras que las componentes fuera de diagonal $\varepsilon_{ij}$ ($i \neq j$) representan deformaciones angulares (cizallamiento). La traza $\text{tr}(\boldsymbol{\varepsilon}) = \nabla \cdot \mathbf{u}$ mide el cambio volumétrico, directamente ligado a las [[P-waves|ondas P]].

#### Tensor de esfuerzos

Las fuerzas internas del medio se describen mediante el [[Stress Tensor|tensor de esfuerzos]] $\boldsymbol{\sigma}$, una matriz simétrica de 3×3 = 9 componentes (6 independientes por simetría). El componente $\sigma_{ij}$ representa la fuerza por unidad de área que actúa en la dirección $j$ sobre la cara cuya normal apunta en la dirección $i$.

La **diagonal** ($\sigma_{11}, \sigma_{22}, \sigma_{33}$) contiene los esfuerzos normales (compresión/tracción perpendicular a la cara). Los elementos **fuera de la diagonal** ($\sigma_{12}, \sigma_{13}, \sigma_{23}$) son los esfuerzos cortantes (tangenciales). La traza del tensor, $\text{tr}(\boldsymbol{\sigma}) = \sigma_{11} + \sigma_{22} + \sigma_{33}$, es proporcional a la presión hidrostática. La simetría $\sigma_{ij} = \sigma_{ji}$ se desprende del balance de momentos angulares.

*(Fuente: Foti Ch. 2, Sec. 2.1.2, p. 38–40)*

#### Fuerzas internas y ecuación de movimiento

Las fuerzas internas que actúan sobre un volumen diferencial se obtienen mediante la divergencia del [[Stress Tensor|tensor de esfuerzos]]. La fuerza resultante por unidad de volumen en la dirección $i$ es $\sum_j \partial \sigma_{ij}/\partial x_j$, o en notación vectorial:

$$
\mathbf{f}_{int} = \nabla \cdot \boldsymbol{\sigma}
$$

Aplicando la **segunda ley de Newton** al volumen diferencial (balance dinámico, ignorando fuerzas de cuerpo externas) se obtiene la ecuación de movimiento del continuo:

$$
\nabla \cdot \boldsymbol{\sigma} =
\rho \frac{\partial^2 \mathbf{u}}{\partial t^2}
$$

Esta ecuación relaciona la distribución interna de esfuerzos con la aceleración del campo de desplazamiento. Es válida para cualquier material continuo, independientemente de la relación constitutiva. La especificidad del comportamiento elástico lineal aparece al sustituir la relación constitutiva ([[Hooke's Law|ley de Hooke]]) en esta ecuación, dando lugar a las [[Navier Equations|ecuaciones de Navier]] (sección siguiente).

#### Relación constitutiva

La [[Hooke's Law|ley de Hooke generalizada]] para un material elástico lineal isotrópico relaciona el [[Stress Tensor|tensor de esfuerzos]] $\boldsymbol{\sigma}$ con el [[Strain Tensor|tensor de deformaciones]] $\boldsymbol{\varepsilon}$:

$$
\boldsymbol{\sigma} =
\lambda\,\text{tr}(\boldsymbol{\varepsilon})\,\mathbf{I}
+
2\mu\,\boldsymbol{\varepsilon}
$$

con:

- $\lambda, \mu$ → [[Lamé Constants|constantes de Lamé]] (los dos parámetros independientes del medio isotrópico)
- $\mathbf{I}$ → tensor identidad
- $\text{tr}(\boldsymbol{\varepsilon}) = \nabla \cdot \mathbf{u}$ → traza del tensor de deformación (deformación volumétrica)

El término $\lambda\,\text{tr}(\boldsymbol{\varepsilon})\,\mathbf{I}$ representa la respuesta esférica (cambio de volumen, asociado a [[P-waves|ondas P]]), mientras que $2\mu\,\boldsymbol{\varepsilon}$ representa la respuesta de corte (cambio de forma, asociado a [[S-Waves|ondas S]]). La separación de estas contribuciones permite tratar P y S como ondas independientes en medios homogéneos. El parámetro $\mu$ (módulo de corte) es equivalente al [[Shear Modulus|módulo de corte dinámico]] $G_{\max} = \mu = \rho V_S^2$, el parámetro geotécnico de mayor interés práctico.

#### Ecuaciones de Navier

Sustituyendo la [[Hooke's Law|ley de Hooke]] (relación constitutiva elástica isotrópica) en la ecuación de movimiento se obtienen las **ecuaciones de Navier**, la formulación vectorial de la elastodinámica lineal:

$$
\mu \nabla^2 \mathbf{u} +
(\lambda + \mu)\nabla(\nabla \cdot \mathbf{u})
=
\rho \frac{\partial^2 \mathbf{u}}{\partial t^2}
$$

Estas ecuaciones constituyen un sistema de [[Hyperbolic Partial Differential Equations|ecuaciones diferenciales parciales hiperbólicas]], cuya solución general describe propagación de perturbaciones a velocidades finitas. El primer término $\mu \nabla^2 \mathbf{u}$ controla la propagación de ondas de corte (velocidad $V_S = \sqrt{\mu/\rho}$); el segundo término $(\lambda + \mu)\nabla(\nabla \cdot \mathbf{u})$ controla la propagación de ondas compresionales (velocidad $V_P = \sqrt{(\lambda+2\mu)/\rho}$). La separación formal de estas contribuciones mediante la [[Helmholtz Decomposition|descomposición de Helmholtz]] (sección siguiente) permite tratar las ondas P y S como modos independientes.

#### Descomposición del campo de desplazamiento

Mediante la [[Helmholtz Decomposition|descomposición de Helmholtz]], cualquier campo vectorial se puede descomponer de forma única en una **parte irrotacional** (gradiente de un escalar) y una **parte solenoidal** (rotacional de un vector):

$$\mathbf{u} = \nabla \phi + \nabla \times \boldsymbol{\psi}$$

donde $\phi$ es el **potencial escalar** (irrotacional, $\nabla \times \nabla\phi = 0$) y $\boldsymbol{\psi}$ es el **potencial vectorial** (solenoidal, $\nabla \cdot \nabla\times\boldsymbol{\psi} = 0$). Sustituyendo esta descomposición en las [[Navier Equations|ecuaciones de Navier]], el sistema se separa en dos ecuaciones de onda independientes:

- $\phi$ satisface la ecuación de onda con velocidad $V_P = \sqrt{(\lambda+2\mu)/\rho}$ → **[[P-waves|onda P]]** (irrotacional, compresional)
- $\boldsymbol{\psi}$ satisface la ecuación de onda con velocidad $V_S = \sqrt{\mu/\rho}$ → **[[S-Waves|onda S]]** (solenoidal, de corte)

Esta separación es la base formal del **método de [[Elastic Wave Potentials|potenciales de onda elástica]]** utilizado en la derivación de las [[Rayleigh Waves|ondas de Rayleigh]] (§2.2.2) y las [[Love Waves|ondas de Love]] (§2.3).

#### Velocidades de propagación

Las dos velocidades de cuerpo del medio elástico isotrópico se expresan como:

Para [[P-waves|ondas P]] (compresionales):

$$
V_P = \sqrt{\frac{\lambda + 2\mu}{\rho}}
$$

Para [[S-Waves|ondas S]] (de corte):

$$
V_S = \sqrt{\frac{\mu}{\rho}}
$$

Siempre se cumple $V_S < V_P$ (ya que $\lambda + 2\mu > \mu$ para medios físicamente admisibles con $\lambda > 0$). En materiales geológicos típicos, la razón $V_P/V_S$ varía desde ~1.5–1.7 en rocas duras hasta ~5–20 en sedimentos saturados. El [[Shear Modulus|módulo de corte]] $G = \mu = \rho V_S^2$ es la propiedad mecánica directamente accesible mediante ondas de corte.

Estas velocidades corresponden a la [[Phase Velocity|velocidad de fase]] de las [[Body Waves|ondas de cuerpo]] monocromáticas en medios **homogéneos**. En medios homogéneos, además, [[Group Velocity|velocidad de grupo]] = [[Phase Velocity|velocidad de fase]] (no hay dispersión). La dispersión (diferencia entre velocidades de fase y grupo) aparece solo en medios **heterogéneos** (estratificados), donde distintas frecuencias penetran distintas profundidades — principio físico de los métodos de ondas superficiales.

#### Polarización de ondas S

Las [[S-Waves|ondas S]] poseen movimiento de partícula perpendicular a la dirección de propagación y admiten dos modos de polarización independientes, definidos respecto al plano vertical de propagación:

- **[[SV-wave|SV]]** (Shear-Vertical): polarización en el plano vertical que contiene la dirección de propagación. Las ondas SV se acoplan con las [[P-waves|ondas P]] en interfaces (conversión P–SV) y son el componente de corte vertical de las [[Rayleigh Waves|ondas de Rayleigh]].
- **[[SH-wave|SH]]** (Shear-Horizontal): polarización horizontal, perpendicular al plano de propagación. Las ondas SH no se acoplan con P ni SV en interfaces planas y constituyen el modo de las [[Love Waves|ondas de Love]].

Esta distinción de polarización es fundamental para la clasificación de las [[Surface Waves|ondas superficiales]]: las [[Rayleigh Waves]] resultan del acoplamiento P + SV con la condición de superficie libre, mientras que las [[Love Waves]] son ondas SH guiadas por contrastes de impedancia en [[Layered Media|medios estratificados]].

#### Conversión de modos

Cuando una onda incide sobre una interfaz entre medios elásticos, la discontinuidad de propiedades genera **[[Mode Conversion|conversión de modos]]**: la onda incidente se descompone en ondas reflejadas y transmitidas que pertenecen a tipos de onda diferentes.

Las reglas de conversión dependen de la polarización:
- **Onda P incidente** → ondas reflejadas y transmitidas P (compresión) y SV (cortante vertical), en la proporción determinada por los coeficientes de reflexión-transmisión de Zoeppritz.
- **Onda SV incidente** → ondas reflejadas y transmitidas P y SV (acoplamiento P-SV siempre activo).
- **Onda SH incidente** → **solo ondas SH**: las ondas de corte horizontal no se acoplan con P ni SV — esta desconexión es la base matemática de la existencia de las [[Love Waves|ondas Love]] como modos guiados puros.

**Implicación para [[Surface Waves|ondas superficiales]]**: en [[Layered Media|medios estratificados]], la conversión de modos en cada interfaz genera la interferencia constructiva que forma las ondas de Rayleigh y Love como soluciones modales del sistema de capas. Cada modo resulta de una condición de resonancia específica que involucra múltiples reflexiones y conversiones entre interfaces. El análisis completo de estas conversiones mediante la [[Thomson-Haskell Matrix|matriz de Thomson-Haskell]] (§2.4.1.1) constituye el [[Forward Problem|problema directo]] para la [[Inversión|inversión]] de ondas superficiales.

*(Fuente: Foti Ch. 2, Sec. 2.3, p. 57–59)*

#### Ondas armónicas

La solución **monocromática** (un único componente de frecuencia $\omega$) del campo de desplazamientos para propagación 1D puede escribirse como superposición de una onda progresiva y una regresiva:

$$
u(x,t)=A_1 e^{i(\omega t-kx)} + A_2 e^{i(\omega t+kx)}
$$

donde $A_1$ es la amplitud compleja de la onda en la dirección $+x$ y $A_2$ en la dirección $-x$. Los parámetros fundamentales son:

- $\omega$ → [[Angular Frequency|frecuencia angular]] ($\omega = 2\pi f$)
- $k$ → [[Wavenumber|número de onda]] ($k = 2\pi / \lambda$)

La [[Phase Velocity|velocidad de fase]] relaciona ambas variables a través de la [[Dispersion Relation|relación de dispersión]] del medio:

$$
c = V_{ph} = \frac{\omega}{k}
$$

Para ondas en medios no dispersivos (como cuerpo en medio homogéneo), $c$ es constante con $\omega$. En medios dispersivos (como ondas superficiales en medio estratificado), $c = c(\omega)$ es una función de la frecuencia — la [[Dispersion Curve|curva de dispersión]].

Soluciones más generales para campos de ondas multifrequencia (paquetes de onda, señales transitorias) se construyen mediante superposición:

- [[Fourier Integral|transformada de Fourier]] → suma continua de componentes monocromáticas
- [[Wave Superposition|superposición de modos]] → suma discreta de modos propios en medios estratificados

#### Importancia para métodos de ondas superficiales

Aunque esta sección describe [[Body Waves|ondas de cuerpo]], su análisis es esencial para comprender los métodos de caracterización basados en [[Surface Waves]].

Las ondas superficiales pueden interpretarse como combinaciones de [[Body Waves|ondas de cuerpo]] que satisfacen condiciones de frontera en la superficie libre.

En particular:

- [[Rayleigh Waves]] → acoplamiento P + SV
- [[Love Waves]] → ondas SH guiadas

Por lo tanto, las propiedades de las ondas superficiales dependen directamente de:

- $V_P$
- $V_S$

y de la estructura del medio descrita en [[Layered Media]].

Estos principios constituyen la base física de los métodos utilizados en [[Métodos Sísmicos No Invasivos]].

![[Pasted image 20260316135658.png]]

### Relación entre $V_P$ y $V_S$

Las velocidades de propagación de [[Body Waves|ondas de cuerpo]] dependen de las propiedades elásticas del medio:

$$  
V_P=\sqrt{\frac{\lambda+2\mu}{\rho}},  
\qquad  
V_S=\sqrt{\frac{\mu}{\rho}}  
$$

De estas expresiones se deduce que $V_P > V_S$ en cualquier material físicamente admisible, porque las [[P-waves|ondas P]] dependen de la **rigidez volumétrica** ($\lambda + 2\mu$, que incluye tanto la resistencia al cambio de volumen como la resistencia al cizallamiento), mientras que las [[S-Waves|ondas S]] dependen únicamente de la **rigidez de corte** ($\mu$). La razón $V_P/V_S$ es un indicador de la compresibilidad relativa del material: materiales duros e incompresibles (como granito) tienen $V_P/V_S \approx 1.7$; materiales blandos y compresibles (como arcillas saturadas) pueden tener $V_P/V_S > 10$. Esta razón equivale a $\sqrt{(2-2\nu)/(1-2\nu)}$ en función del [[Poisson Ratio|coeficiente de Poisson]] $\nu$ (sección siguiente).

### Relación con el [[Poisson Ratio|coeficiente de Poisson]]

El cociente entre velocidades puede expresarse en función del [[Poisson Ratio|coeficiente de Poisson]] $\nu$:

$$
\frac{V_P}{V_S} = \sqrt{\frac{2(1-\nu)}{1-2\nu}}
$$

Esto muestra que siempre se cumple:

$$  
V_S < V_P  
$$

Para un valor típico de varios materiales,

$$  
\nu = 0.25  
$$

se obtiene aproximadamente:

$$  
V_P = \sqrt{3},V_S  
$$

### Limitación en geomateriales saturados

Aunque esta relación permite estimar $V_S$ a partir de $V_P$ y $\nu$, este procedimiento no debe utilizarse en geomateriales, especialmente en suelos saturados.

Bajo condiciones no drenadas:

- la compresibilidad del agua domina la respuesta volumétrica
- el coeficiente de Poisson se aproxima a $0.5$
- la velocidad de onda P aumenta fuertemente

En ese límite:

$$  
\nu \to 0.5  
$$

lo que llevaría idealmente a:

$$  
V_P \to \infty  
$$

Esto no significa que el suelo sea infinitamente rígido, sino que la onda P queda controlada principalmente por la muy baja compresibilidad del agua.

### Implicación práctica para caracterización de suelos

En suelos y depósitos saturados, la práctica estándar de caracterización geotécnica se orienta hacia $V_S$ y no $V_P$ por las razones ya descritas:

- $V_P$ no representa bien la rigidez del esqueleto del suelo en condiciones saturadas — está controlada por la compresibilidad del fluido intersticial (agua), no por la rigidez del esqueleto sólido. En suelos bajo el nivel freático, $V_P \approx 1450$–$1600$ m/s independientemente de la compacidad del suelo.
- $V_S$ depende exclusivamente de la rigidez de corte del esqueleto sólido y es insensible al contenido de fluido. En suelos saturados y no saturados con la misma estructura de granos, los valores de $V_S$ son comparables; esto no ocurre con $V_P$.
- Los métodos de [[Surface Waves|ondas superficiales]] — que son métodos de onda de corte — se centran principalmente en recuperar perfiles de $V_S(z)$. El [[Shear Modulus|módulo de corte dinámico]] $G_{\max} = \rho \cdot V_S^2$ es directamente aplicable al análisis de respuesta sísmica de sitio, clasificación de suelo normativa ([[Vs30|$V_{S,30}$]]) y predicción de asentamientos dinámicos.

### Valores típicos de velocidades en geomateriales

Los valores de $V_P$ y $V_S$ pueden variar ampliamente según el material.
![[Pasted image 20260316140452.png]]
Ejemplos típicos cerca de superficie:
- rocas cristalinas: velocidades altas de $V_P$ y $V_S$
- arenas densas: valores intermedios
- arcillas muy blandas: valores bajos

En general:
- materiales más rígidos presentan mayores velocidades
- materiales blandos o poco consolidados presentan menores velocidades
- la saturación incrementa especialmente $V_P$

### Solución armónica general

Una solución monocromática del campo de desplazamientos puede escribirse como:

$$  
u(x,t)=A_1 e^{i(\omega t-k_\chi \cdot x)} + A_2 e^{i(\omega t+k_\chi \cdot x)}  
$$

donde:

- $A_1, A_2$ son amplitudes constantes
- $\omega$ es la frecuencia angular
- $k_\chi$ es el vector [[Wavenumber|número de onda]]
- $\chi = P, S$ indica si se trata de onda longitudinal o transversal

Esta expresión representa una onda armónica propagándose en direcciones opuestas.
![[Pasted image 20260316140712.png]]
### Geometría de fase

El vector [[Wavenumber|número de onda]] $\mathbf{k}$ es **normal a los planos de fase constante** (frentes de onda), definidos por:

$$  
\mathbf{k} \cdot \mathbf{x} = \text{constante}  
$$

Estos planos se propagan en la dirección de $\mathbf{k}$ con la [[Phase Velocity|velocidad de fase]]:

$$  
c = \frac{\omega}{|\mathbf{k}|}  
$$

La geometría de los frentes de onda determina si la propagación es plana (frentes paralelos, válida en campo lejano), cilíndrica (frentes circulares en 2D, relevante para [[Rayleigh Waves|ondas superficiales]] desde fuente puntual) o esférica (frentes esféricos en 3D, para [[Body Waves|ondas de cuerpo]]). En el análisis de [[MASW Method|MASW]], el procesamiento f-k asume frentes planos, lo que es válido en campo lejano ($r \gg \lambda$) pero introduce error en el [[Near-field Effect|campo cercano]].

### Polarización de ondas P y S

La dirección del movimiento de partículas depende del tipo de onda:

- en ondas P, la polarización es paralela a la dirección de propagación
- en ondas S, la polarización es perpendicular a la dirección de propagación

En una onda S, el movimiento puede descomponerse en dos componentes ortogonales.
Cuando la propagación es vertical, aparecen dos polarizaciones importantes:

- [[SV-wave]]: polarización vertical
- [[SH-wave]]: polarización horizontal

Esta distinción es fundamental porque:

- [[Rayleigh Waves]] involucran acoplamiento P-SV
- [[Love Waves]] corresponden a ondas SH guiadas

### Conversión de modos en interfaces

Cuando una onda incide sobre una interfaz entre medios elásticos con propiedades diferentes, se produce **conversión de modos**: parte de la energía se transmite en el mismo modo y parte se convierte al otro tipo de onda. Las reglas de conversión dependen de la polarización:

- Una **onda P incidente** genera ondas P y SV reflejadas y transmitidas (el acoplamiento P–SV es obligatorio en interfaz plana con contraste impedimético).
- Una **onda SV incidente** genera ondas P y SV reflejadas y transmitidas (mismo acoplamiento P–SV).
- Una **onda SH incidente** genera únicamente ondas SH reflejadas y transmitidas — el movimiento puramente horizontal transversal no se acopla con los modos P ni SV.
    
![[Pasted image 20260316141217.png]]

Este fenómeno de [[Mode Conversion|conversión de modos]] tiene consecuencias fundamentales para la geofísica de ondas superficiales:

- En [[Layered Media|medios estratificados]], cada interfaz P–SV genera ondas reflejadas y transmitidas en ambos modos. La superposición de todas estas contribuciones es lo que da lugar a los modos de propagación de las [[Rayleigh Waves|ondas de Rayleigh]] (solución propia del problema de capas con condición de frontera libre en superficie).
- El desacoplamiento de SH explica por qué las [[Love Waves|ondas de Love]] (modo SH guiado) tienen curvas de dispersión más simples y menos susceptibles a la [[Mode Superposition|superposición modal]] confusa: los modos Love no interaccionan con los modos P–SV.
- La conversión de modos en la superficie libre es el mecanismo que produce la polarización elíptica característica de las [[Rayleigh Waves|ondas de Rayleigh]].

### Caso unidimensional

Para propagación 1D a lo largo del eje $x$, la solución armónica se simplifica a una superposición de ondas progresiva (dirección $+x$) y regresiva (dirección $-x$):

$$  
u(x,t)=A_1 e^{i(\omega t-kx)} + A_2 e^{i(\omega t+kx)}  
$$

donde el [[Wavenumber|número de onda]] escalar queda directamente relacionado con la [[Phase Velocity|velocidad de fase]] $V$:

$$  
k = \frac{\omega}{V}  
$$

Esta relación es la base de la extracción de la [[Dispersion Curve|curva de dispersión]] en el análisis de ondas superficiales: en el dominio f-k, la pendiente de la línea que une el origen con el máximo espectral es exactamente $V_{ph}(f) = f/k$, y el conjunto de estas pendientes para todas las frecuencias forma la [[Dispersion Curve|curva de dispersión]] experimental.

### Parámetros fundamentales de una onda armónica

#### Frecuencia angular y frecuencia

$$  
\omega = 2\pi f  
$$

#### Periodo

El periodo es el intervalo temporal entre dos puntos con la misma fase:

$$  
T = \frac{2\pi}{\omega}  
$$

#### [[Wavelength|Longitud de onda]]

La [[Wavelength|longitud de onda]] es la distancia entre dos puntos con la misma fase:

$$  
\lambda = \frac{2\pi}{k}  
$$

Combinando con la definición de [[Phase Velocity|velocidad de fase]]:

$$  
\lambda = \frac{V}{f}  
$$
![[Pasted image 20260316141321.png]]
Esta relación conecta directamente:

- velocidad de propagación
- frecuencia
- [[Wavelength|longitud de onda]]

### Importancia para métodos de ondas superficiales

Estas relaciones son fundamentales porque permiten conectar el comportamiento de ondas armónicas con la interpretación experimental.

En particular:

- la frecuencia controla la [[Wavelength|longitud de onda]]
- la [[Wavelength|longitud de onda]] controla la profundidad efectiva de investigación
- la dependencia entre velocidad y frecuencia es la base de las [[Dispersion Relation|curvas de dispersión]]

Por eso, estos parámetros serán esenciales en las secciones posteriores sobre:

- [[Rayleigh Waves]]
- [[Love Waves]]
- [[Dispersion Relation]]
- análisis de [[Adquisición de Datos|adquisición]] e [[Inversión|inversión]]

## 2.2 Rayleigh Waves in Homogeneous Elastic Half-Spaces

> Fuente: Foti et al. (2014), Sección 2.2, pp. 65–80.

El caso del **[[Elastic Half Space|semiespacio elástico homogéneo]]** es el punto de partida canónico para entender las [[Rayleigh Waves|ondas de Rayleigh]]: es el único caso exactamente tratable de forma analítica y proporciona las relaciones fundamentales entre [[Phase Velocity|velocidad de fase]] $V_R$, [[Shear Modulus|módulo de corte]] $G$ y [[Poisson Ratio|razón de Poisson]] $\nu$. Su solución es **no dispersiva** ($V_R = \text{const}$), lo que sirve de referencia para apreciar cuánto modifica la heterogeneidad vertical la respuesta dispersiva del medio estratificado.

### 2.2.1 Overview

Los continuos elásticos **homogéneos, isotrópicos y no acotados** solo permiten la propagación de [[Body Waves|ondas de cuerpo]]:

- [[P-waves|ondas P]] (compresionales, velocidad $V_P$)
- [[S-Waves|ondas S]] (de corte, velocidad $V_S$)

Sin embargo, **la introducción de una frontera libre en el medio** — la condición de esfuerzo tangencial y normal nulos en la superficie — permite la existencia de un tercer tipo de ondas: las **[[Surface Waves|ondas superficiales]]**, que se propagan a lo largo de la superficie en lugar de propagarse hacia el interior.

Las **[[Rayleigh Waves|ondas de Rayleigh]]** fueron predichas teóricamente por **Lord Rayleigh en 1885** ("On waves propagated along the plane surface of an elastic solid", *Proc. London Math. Soc.*), antes de cualquier observación sismológica. Su existencia se estableció puramente por análisis matemático de las condiciones de borde en la superficie libre de un semiespacio elástico. La observación ulterior en registros sísmicos reales (terremotos, explosiones) confirmó la predicción: las ondas de Rayleigh son la fase dominante de amplitud en los sismogramas de campo lejano, especialmente en la componente vertical.

Estas ondas resultan del **acoplamiento resonante** entre las componentes P y SV en la superficie libre: ambas componentes se propagan horizontalmente (a lo largo de la superficie) con el mismo número de onda $k_R$, y la condición de borde libre selecciona la única velocidad $V_R < V_S < V_P$ para la que esta superposición satisface el decaimiento en profundidad.

---

### Propagación superficial

A diferencia de las [[Body Waves|ondas de cuerpo]], que propagan energía esféricamente en 3D, las [[Rayleigh Waves|ondas de Rayleigh]] presentan un patrón de radiación esencialmente **bidimensional (2D)** — sus frentes de onda son cilíndricos, propagándose horizontalmente a lo largo de la superficie con amplitudes que decaen exponencialmente en profundidad.

![[Pasted image 20260316143212.png]]

Esto implica que la energía se propaga principalmente:

- a lo largo de la superficie, con frentes cilíndricos de radio creciente
- con amplitud decreciente exponencialmente con la profundidad (ver §Decaimiento con profundidad)
- sin propagación hacia el interior del medio más allá de una o dos longitudes de onda.

Como consecuencia, las [[Rayleigh Waves|ondas de Rayleigh]] presentan una **[[Attenuation|atenuación]] geométrica mucho menor** que las [[Body Waves|ondas de cuerpo]]: la amplitud decrece como $r^{-0.5}$ (fuente puntual, propagación cilíndrica) frente a $r^{-2}$ para las ondas de cuerpo en la superficie. Esta diferencia de decaimiento explica por qué, a distancias del orden de una longitud de onda, el campo de ondas sísmicas en superficie queda dominado por las ondas superficiales — justificando la viabilidad de los métodos [[MASW Method|MASW]] a distancias moderadas de la fuente.

---

### Atenuación geométrica

El decaimiento espacial de la amplitud depende del tipo de fuente.

Para un **medio elástico homogéneo semi-infinito**:

**Fuente lineal vertical**

- las [[Rayleigh Waves]] no presentan [[Geometric Spreading|atenuación geométrica]].

**Fuente puntual vertical**

- la amplitud decae proporcionalmente a:

$$
\frac{1}{\sqrt{r}}
$$

donde $r$ es la distancia a la fuente.

En contraste, las [[Body Waves]] propagándose a lo largo de la superficie presentan una atenuación proporcional a:

$$
\frac{1}{r^2}
$$

Esto implica que a distancias del orden de **una o dos longitudes de onda desde la fuente**, la contribución de las [[Body Waves|ondas de cuerpo]] se vuelve **despreciable** y el campo de ondas queda dominado por **[[Rayleigh Waves]]**.

Este fenómeno fue reconocido tempranamente en el contexto de [[Lamb's Problem]], que estudia la generación de ondas por una carga aplicada en la superficie de un medio elástico.

---

### Decaimiento con profundidad

El campo de desplazamientos generado por una [[Rayleigh Waves]] presenta una propiedad característica:

la **amplitud decrece exponencialmente con la profundidad**.

Esto ocurre porque la energía de estas ondas **no se propaga hacia el interior del medio**, sino que permanece confinada cerca de la superficie.

De hecho, esta propiedad suele utilizarse como **definición operativa de una [[Surface Waves]]**.

---

### Profundidad efectiva de penetración

La mayor parte de la energía de deformación asociada al movimiento de una [[Rayleigh Waves]] está confinada aproximadamente dentro de una profundidad del orden de:

$$
\lambda
$$

donde $\lambda$ es la **[[Wavelength]]** de la onda.

Una forma de describir esta propiedad es mediante el concepto de **[[Skin Depth]]**, definido como la profundidad a la cual la amplitud disminuye por un factor:

$$
\frac{1}{e}
$$

Para las [[Rayleigh Waves]] en un medio homogéneo:

$$
\text{Skin depth} \approx 0.94 \lambda
$$

Esto implica que:

- **longitudes de onda grandes → mayor profundidad de penetración**
- **longitudes de onda pequeñas → menor profundidad de penetración**
![[Pasted image 20260316144212.png]]
---

### Implicación geofísica fundamental

Esta relación entre **[[Wavelength|longitud de onda]] y profundidad de penetración** es la base física de todos los métodos de caracterización del subsuelo mediante [[Surface Waves|ondas superficiales]]. La [[Dispersion Curve|curva de dispersión]] experimental — la variación de la [[Phase Velocity|velocidad de fase]] con la frecuencia — refleja directamente la variación de $V_S$ con la profundidad:

- frecuencias **bajas** (longitudes de onda grandes, $\lambda \approx V_S/f$) investigan **mayores profundidades** — la onda "siente" el promedio de las propiedades elásticas hasta $\sim\lambda$ de profundidad.
- frecuencias **altas** investigan **capas superficiales** — la onda es más energética a poca profundidad y su velocidad refleja las propiedades de las capas más someras.

Este principio permite reconstruir perfiles de velocidad de corte del subsuelo mediante el análisis de la [[Dispersion Relation|relación de dispersión]] de [[Rayleigh Waves|ondas de Rayleigh]]: la [[Inversión|inversión]] de la [[Dispersion Curve|curva de dispersión]] experimental $V_{ph}(f)$ determina el perfil $V_S(z)$ mediante un [[Forward Problem|problema directo]] iterativo (Capítulo 6). La profundidad máxima de investigación $z_{max} \approx \lambda_{max}/2$ queda determinada por la longitud de onda máxima accesible con el arreglo de adquisición.

### 2.2.2 Derivación mediante [[Elastic Wave Potentials|potenciales de onda elástica]]

La existencia de las [[Rayleigh Waves]] se demuestra formalmente mediante la [[Helmholtz Decomposition|descomposición de Helmholtz]] del campo de desplazamientos, separando las contribuciones irrotacional ([[P-waves|onda P]]) y solenoidal ([[S-Waves|onda SV]]), y aplicando las condiciones de frontera en la superficie libre del [[Elastic Half Space|semiespacios elástico]]. El resultado es la **ecuación de dispersión de Rayleigh**, un polinomio implícito en la razón $V_R/V_S$ que determina la velocidad de propagación de la [[Rayleigh Waves|onda de Rayleigh]] en función de las constantes elásticas del medio. Esta sección es el núcleo matemático del capítulo y la base de los algoritmos de [[Forward Problem|modelado directo]] (forward problem) empleados en la [[Inversión|inversión]].

#### Planteamiento del problema

Se considera un medio:

- elástico lineal
- homogéneo
- isotrópico
- semi-infinito: $z \geq 0$ (superficie libre en $z = 0$, medio se extiende hacia $z > 0$)

El campo de desplazamientos $\mathbf{u}$ se descompone mediante los [[Elastic Wave Potentials]]:

$$
\mathbf{u} = \nabla \phi + \nabla \times \mathbf{\psi}
$$

donde:

- $\phi$ → potencial escalar (asociado a [[P-waves]])
- $\mathbf{\psi}$ → potencial vectorial (asociado a [[S-Waves]])

Cada potencial satisface su propia [[1D Wave Equation|ecuación de onda]]:

$$
\nabla^2 \phi = \frac{1}{V_P^2}\frac{\partial^2 \phi}{\partial t^2}
$$

$$
\nabla^2 \mathbf{\psi} = \frac{1}{V_S^2}\frac{\partial^2 \mathbf{\psi}}{\partial t^2}
$$

#### Solución armónica en 2D

Para el problema plano (propagación en $x$, profundidad $z$), se proponen soluciones de la forma:

$$
\phi = A \, e^{-\alpha z} \, e^{i(kx - \omega t)}
$$

$$
\psi = B \, e^{-\beta z} \, e^{i(kx - \omega t)}
$$

donde:

$$
\alpha = \sqrt{k^2 - \frac{\omega^2}{V_P^2}}, \qquad \beta = \sqrt{k^2 - \frac{\omega^2}{V_S^2}}
$$

La condición $\text{Re}(\alpha) > 0$ y $\text{Re}(\beta) > 0$ garantiza que las amplitudes **decaigan con la profundidad** — condición necesaria para que sean ondas superficiales y no [[Body Waves|ondas de cuerpo]].

#### Condiciones de frontera en superficie libre

La superficie terrestre es un **semiespacio libre**: ninguna fuerza externa actúa desde el semispacio superior (aire), por lo que los esfuerzos en la interfaz $z = 0$ deben ser nulos. Las dos condiciones son:

$$
\sigma_{zz}\big|_{z=0} = 0, \qquad \sigma_{xz}\big|_{z=0} = 0
$$

La primera anula el esfuerzo normal (compresión/tracción perpendicular a la superficie); la segunda anula el esfuerzo cortante (fricción tangencial). En el contexto de la descomposición de Helmholtz, estas condiciones se traducen en relaciones entre las amplitudes $A$ (potencial escalar $\phi$ — onda P) y $B$ (potencial vectorial $\psi$ — onda SV):

$$
\left[\frac{\partial^2\phi}{\partial z^2} + \frac{\partial^2\phi}{\partial x^2}\right]\bigg|_{z=0} + \lambda/\mu \cdot \nabla^2\phi\big|_{z=0} + 2\frac{\partial^2\psi}{\partial x \partial z}\bigg|_{z=0} = 0
$$

Aplicando ambas condiciones al campo de desplazamientos derivado de los potenciales se obtiene un **sistema lineal homogéneo en $A$ y $B$**: $\mathbf{M}(c_R, V_P, V_S) \cdot [A, B]^T = \mathbf{0}$. Para que el sistema tenga solución no trivial (y por tanto ondas de superficie reales) el determinante de la matriz de coeficientes $\mathbf{M}$ debe ser cero — condición que define la ecuación secular.

*(Fuente: Foti Ch. 2, Sec. 2.2.1, p. 44–47)*

#### Ecuación secular de Rayleigh

Para que el sistema tenga solución no trivial, el determinante de la matriz de coeficientes debe ser cero. Esto conduce a la **ecuación secular de Rayleigh**:

$$
\left(2 - \frac{c_R^2}{V_S^2}\right)^2 = 4\sqrt{1 - \frac{c_R^2}{V_P^2}}\sqrt{1 - \frac{c_R^2}{V_S^2}}
$$

donde $c_R$ es la [[Phase Velocity|velocidad de fase]] de las [[Rayleigh Waves|ondas de Rayleigh]].

Esta ecuación puede reescribirse en términos de la razón $\xi = c_R / V_S$ como un polinomio:

$$
\xi^6 - 8\xi^4 + \left(24 - 16\frac{V_S^2}{V_P^2}\right)\xi^2 - 16\left(1 - \frac{V_S^2}{V_P^2}\right) = 0
$$

Este polinomio cúbico en $\xi^2$ tiene en general una única raíz real físicamente admisible (con $0 < c_R < V_S$).

#### Resultado fundamental

La velocidad de Rayleigh $c_R$ depende únicamente de $V_S$ y del [[Poisson Ratio|coeficiente de Poisson]] $\nu$ (que determina $V_P/V_S$).

Para $\nu = 0.25$ (valor típico para muchas rocas):

$$
c_R \approx 0.9194 \, V_S
$$

En general, $c_R$ varía entre $0.862\,V_S$ (para $\nu = 0$) y $0.955\,V_S$ (para $\nu \to 0.5$) para el rango de $\nu$ físicamente admisible ($0 \leq \nu < 0.5$), como ilustra la **Fig. 2.15** del texto.

> **Implicación crítica para la tesis**: $c_R \approx 0.92\,V_S$ en condiciones típicas. Los geófonos miden la velocidad de Rayleigh. La conversión a $V_S$ requiere conocer $\nu$ o asumirlo, lo que introduce incertidumbre en el perfil final.

#### Eigenfunciones de desplazamiento (Foti Ecs. 2.43–2.45)

Una vez conocida $c_R$, los desplazamientos horizontal $u_1$ y vertical $u_2$ asociados a la onda de Rayleigh en el semiespacio son (Foti Ec. 2.43):

$$
\begin{cases}
u_1 = \dfrac{ics\cdot B_4}{\omega(1-c^2/2V_S^2)}\left[\left(1 - \dfrac{c^2}{2V_S^2}\right)\cdot e^{-sx_2} - e^{-rx_2}\right]\cdot e^{i(kx_1-\omega t)}\\[10pt]
u_2 = \dfrac{c^2rs\cdot B_4}{\omega^2(1-c^2/2V_S^2)}\left[\left(1 - \dfrac{c^2}{2V_S^2}\right)^{-1}\cdot e^{-sx_2} - e^{-rx_2}\right]\cdot e^{i(kx_1-\omega t)}
\end{cases}
$$

donde $c = V_R$, $r = \sqrt{k^2 - \omega^2/V_P^2}$, $s = \sqrt{k^2 - \omega^2/V_S^2}$. Estas expresiones muestran que ambas componentes decaen exponencialmente con la profundidad $x_2$.

Las eigenfunciones de profundidad $r_1(x_2)$ y $r_2(x_2)$ (Foti Ec. 2.45) satisfacen la **ecuación de la elipse** (Foti Ec. 2.44):

$$
\frac{u_1^2}{r_1^2(x_2)} + \frac{u_2^2}{r_2^2(x_2)} = 1
$$

Es decir, en cada profundidad la partícula describe una trayectoria elíptica en el plano $x_1$–$x_2$. En superficie, el cociente de amplitudes vertical/horizontal es aproximadamente 1.5 (Foti p. 60).

*(Fuente: Foti Ch. 2, Sec. 2.2.3, pp. 58–60, Ecs. 2.43–2.45)*

---

### 2.2.3 Movimiento de partícula

El campo de desplazamientos asociado a las [[Rayleigh Waves]] en superficie presenta las siguientes características:

- **Trayectoria elíptica** en el plano vertical de propagación (plano $x_1$–$x_2$) — Foti Ec. 2.44, **Fig. 2.16**
- En superficie: órbita **retrógrada** (sentido antihorario para propagación en $+x_1$)
- A una profundidad crítica $x_2^c$ (profundidad donde la componente horizontal se anula): el movimiento cambia a **prógrado** (sentido horario)
- El eje vertical de la elipse es mayor que el horizontal en superficie (~1.5:1)

La profundidad crítica $x_2^c \approx 0.2\lambda$ se obtiene de (Foti Ec. 2.46):

$$
x_2^c = \frac{\ln\!\left(1 - \dfrac{V_R^2}{2V_S^2}\right)}{\omega\!\left(\sqrt{\dfrac{1}{V_R^2} - \dfrac{1}{V_S^2}} - \sqrt{\dfrac{1}{V_R^2} - \dfrac{1}{V_P^2}}\right)}
$$

donde ln(·) es el logaritmo natural. Corresponde a la profundidad a la que el desplazamiento horizontal se anula y el movimiento se vuelve puramente vertical.

*(Fuente: Foti Ch. 2, Sec. 2.2.3, p. 60, Ec. 2.46)*

Esta polarización elíptica en el plano vertical explica por qué los **geófonos verticales** son los sensores preferidos para capturar [[Rayleigh Waves]]: detectan directamente la componente dominante del movimiento.

> **Nota**: Los geófonos horizontales detectan la componente horizontal de la elipse, que es de menor amplitud en superficie. Para [[Love Waves]], en cambio, se requieren geófonos horizontales orientados transversalmente.

---

### 2.2.4 No-dispersividad en el half-space homogéneo

Un resultado central del capítulo es que en un [[Elastic Half Space]] homogéneo:

- $c_R$ **no depende de la frecuencia** ni del [[Wavenumber|número de onda]]
- la ecuación secular de Rayleigh no contiene $\omega$ ni $k$ de forma independiente, sino únicamente a través del cociente $c_R = \omega/k$
- por tanto, las [[Rayleigh Waves|ondas de Rayleigh]] en este medio son **no dispersivas**

La razón física de esta no-dispersividad es que el medio es homogéneo: no existe longitud de escala característica que introduzca un efecto de tamaño relativo. La onda de Rayleigh de cualquier frecuencia "ve" exactamente el mismo medio independientemente de su [[Wavelength|longitud de onda]]. En contraste, en un medio estratificado sí existe una longitud de escala natural (el espesor de las capas), y las ondas de diferente [[Wavelength|longitud de onda]] penetran profundidades diferentes y por tanto sienten medios distintos — esto es exactamente la dispersión geométrica.

Esta referencia tiene consecuencias directas para la caracterización del subsuelo: **la dispersión que observamos experimentalmente es evidencia directa de la heterogeneidad vertical del subsuelo**. Si un sitio tiene propiedades uniformes con la profundidad, la [[Dispersion Curve|curva de dispersión]] es plana; si hay gradiente o capas con velocidades distintas, la curva tiene pendiente. Esto es lo que permite extraer información del perfil $V_S(z)$ a partir de la [[Dispersion Curve|curva de dispersión]] medida con geófonos: la variación de [[Phase Velocity|velocidad de fase]] con la frecuencia mapea la variación de rigidez con la profundidad.

La no-dispersividad del semiespacio homogéneo sirve también como límite asintótico a alta y baja frecuencia en medios estratificados: cuando $\lambda \to 0$ (alta frecuencia), la onda "ve" solo la capa más superficial, y $c_R \to 0.92\,V_{S,\text{top}}$; cuando $\lambda \to \infty$ (baja frecuencia), la onda penetra todo el perfil y su velocidad tiende a $0.92\,V_{S,\text{semiespacio}}$.

---

## 2.3 Existence of Love Waves

Las [[Love Waves]] fueron predichas matemáticamente por A.E.H. Love en 1911. Son ondas transversales horizontalmente polarizadas ([[SH-wave|SH]]) que surgen de la interferencia constructiva de ondas SH en [[Layered Media|medios inhomogéneos estratificados]].

**Las Love waves no pueden existir en un semiespacio homogéneo.** Requieren al menos una capa superficial sobre un semiespacio más rígido:

```text
capa superficial   ρ₁, μ₁   V_S1   (0 ≤ x₂ ≤ h)
──────────────────────────────────────────────────
semiespacio        ρ₂, μ₂   V_S2   (x₂ > h)
```

La condición física necesaria para la existencia de Love waves es:

$$
V_{S1} < c_L < V_{S2}
$$

donde $c_L = \omega/k$ es la [[Phase Velocity|velocidad de fase]] de las Love waves. Cuando esta condición se cumple, las [[SH-wave|ondas SH]] quedan **atrapadas** en la capa superior por reflexión total interna en la interfaz — la capa actúa como una **[[Wave Guide|guía de ondas]]**. Si $V_{S2} \leq V_{S1}$, las Love waves no existen.

*(Fuente: Foti Ch. 2, Sec. 2.3, p. 60–61)*

---

### Relación de dispersión de Love (Foti Ec. 2.54)

La combinación de condiciones de frontera — esfuerzo nulo en $x_2 = 0$, continuidad de desplazamiento y esfuerzo en $x_2 = h$, y condición de radiación $u_3 \to 0$ para $x_2 \to \infty$ — conduce a la **ecuación de dispersión de Love** (Foti Ec. 2.54):

$$
\tan\!\left(\frac{\omega h}{V_{S1}}\sqrt{1 - \left(\frac{V_{S1}}{c}\right)^2}\right) - \frac{V_{S2}}{V_{S1}}\cdot\frac{\rho_2}{\rho_1}\cdot\frac{\sqrt{\left(\frac{V_{S2}}{V_{S1}}\right)^2 - \left(\frac{c}{V_{S1}}\right)^2}}{\sqrt{\left(\frac{c}{V_{S1}}\right)^2 - 1}} = 0
$$

donde $c = \omega/k = V_L$ es la [[Phase Velocity|velocidad de fase]] de la Love wave y $h$ es el espesor de la capa.

Esta ecuación es **trascendente y no tiene solución cerrada en general**. Sus propiedades clave:

- $c$ depende de $\omega$: las Love waves son **intrínsecamente dispersivas** en medios estratificados (contraste directo con Rayleigh en half-space homogéneo)
- En el límite de baja frecuencia: $c \to V_{S2}$ (domina el semiespacio)
- En el límite de alta frecuencia: $c \to V_{S1}$ (domina la capa superficial)
- La dispersión de Love es puramente geométrica: no requiere disipación

*(Fuente: Foti Ch. 2, Sec. 2.3, p. 63, Ec. 2.54)*

---

### Modos de Love y frecuencia de corte (Foti Ec. 2.55)

La relación de dispersión de Love admite múltiples soluciones (modos) a cada frecuencia. La estructura modal es asimétrica:

- **[[Surface Wave Modes|Modo fundamental]]** ($n = 1$): existe para **todas** las frecuencias — incluso para $\omega \to 0$, aunque su [[Phase Velocity|velocidad de fase]] tiende a $V_{S2}$ (velocidad del semiespacio) a baja frecuencia y a $V_{S1}$ (velocidad de la capa) a alta frecuencia.
- **[[Surface Wave Modes|Modos superiores]]** ($n = 2, 3, \ldots$): existen solo por encima de una **frecuencia de corte** $\omega_c^n$, por debajo de la cual la energía no puede quedar atrapada en la capa.

La [[Angular Frequency|frecuencia angular]] de corte del $n$-ésimo modo es (Foti Ec. 2.55):

$$
\frac{\omega_c^n \cdot h}{V_{S1}} = \frac{\pi(n-1)}{\sqrt{1 - \left(\frac{V_{S1}}{V_{S2}}\right)^2}}, \qquad n = 1, 2, \ldots
$$

**Implicación práctica:** la frecuencia de corte del primer modo superior ($n=2$) depende del espesor de la capa $h$ y del contraste de velocidad $V_{S1}/V_{S2}$. Para un sitio con $h = 20$ m y $V_{S1}/V_{S2} = 0.5$, $\omega_c^2 \approx \pi V_{S1}/(h\sqrt{1-(V_{S1}/V_{S2})^2}) \approx \pi \cdot V_{S1}/(h \cdot 0.866)$. Capas superficiales delgadas producen [[Surface Wave Modes|modos superiores]] a frecuencias altas, accesibles con arreglos de geófonos densos.

Esta dependencia frecuencial multimodal es la base de la [[Geometric Dispersion|dispersión geométrica]] para ondas de Love y justifica el uso del análisis multimodal en la [[Inversión|inversión]] de sitios con estratificación pronunciada.

*(Fuente: Foti Ch. 2, Sec. 2.3, p. 65, Ec. 2.55)*

![[Pasted image 20260317202522.png]]
---

## 2.4 Surface Waves in Vertically Inhomogeneous Media

> Fuente: Foti et al. (2014), Sección 2.4, pp. 80–96.

La heterogeneidad vertical del subsuelo transforma las [[Surface Waves|ondas superficiales]] en ondas **dispersivas**: su [[Phase Velocity|velocidad de fase]] deja de ser constante y pasa a depender de la frecuencia. Esta [[Geometric Dispersion|dispersión geométrica]] — que en el semiespacio homogéneo está ausente — es el fenómeno físico central que hace posible la caracterización del subsuelo. La sección desarrolla el marco matemático que describe este fenómeno: el **problema de autovalores diferencial** para [[Rayleigh Waves|ondas de Rayleigh]] y [[Love Waves|Love]] en [[Layered Media|medios estratificados]], cuya solución proporciona los modos de propagación $c_n(\omega)$ y las funciones de eigendesplazamiento que controlan la [[Sensitivity Kernel|sensibilidad]] del dato al perfil de $V_S$.

### 2.4.1 Problema de autovalores asociado a ondas superficiales libres (Foti Ecs. 2.65–2.74)

En un medio verticalmente inhomogéneo — donde $\lambda = \lambda(x_2)$, $\mu = \mu(x_2)$, $\rho = \rho(x_2)$ son funciones de la profundidad $x_2$ — las ecuaciones de Navier ya no admiten soluciones planas propagantes simples. La búsqueda de soluciones **modales** del tipo $e^{i(\omega t - kx_1)}$ con decaimiento en $x_2 \to \infty$ (condición de onda superficial) conduce a dos **[[Eigenvalue Problem|problemas de autovalores diferenciales]]** con operador $d/dx_2$ — uno para [[Love Waves|ondas de Love]] (modo SH) y otro para [[Rayleigh Waves|ondas de Rayleigh]] (modo P–SV). Para cada frecuencia $\omega$, los autovalores son los números de onda $k_j(\omega)$ que producen modos guiados con las condiciones de frontera correctas. Su existencia y multiplicidad determinan el espectro modal del medio estratificado.

#### Sistemas de EDOs de primer orden

Para **Love waves** (Foti Ec. 2.65):

$$
\frac{d}{dx_2}\begin{bmatrix}l_1\\l_2\end{bmatrix} = \begin{bmatrix}0 & \mu(x_2)^{-1}\\ k^2\mu(x_2)-\omega^2\rho(x_2) & 0\end{bmatrix}\begin{bmatrix}l_1\\l_2\end{bmatrix}
$$

Para **Rayleigh waves** (Foti Ec. 2.66), sistema de cuarto orden $d\mathbf{f}/dx_2 = A(x_2)\cdot\mathbf{f}(x_2)$ donde $\mathbf{f} = [r_1, r_2, r_3, r_4]^T$ contiene las funciones propias de desplazamiento ($r_1$, $r_2$) y esfuerzo ($r_3$, $r_4$).

#### Condiciones de contorno (Foti Ecs. 2.72–2.73)

Las condiciones de contorno imponen dos requerimientos físicos simultáneos: (1) **superficie libre** — los esfuerzos normales se anulan en $x_2 = 0$ (nadie ejerce fuerza sobre el semispacio desde arriba); (2) **radiación** — los desplazamientos decrecen con la profundidad (la energía queda confinada cerca de la superficie).

Para **[[Love Waves|Love waves]]**: $l_2 = 0$ en $x_2 = 0$ (esfuerzo cortante nulo en superficie), y $l_1 \to 0$ para $x_2 \to \infty$ (amplitud nula a profundidad infinita).

Para **[[Rayleigh Waves|Rayleigh waves]]**: $r_3 = r_4 = 0$ en $x_2 = 0$ (ambas componentes del vector de esfuerzo nulas en superficie), y $r_1, r_2 \to 0$ para $x_2 \to \infty$.

**Implicación física**: estas condiciones sobredeterminan el sistema de EDOs — solo ciertos valores discretos de $k$ (los autovalores) permiten satisfacerlas simultáneamente. Esto es lo que genera la estructura modal discreta: [[Surface Wave Modes|modo fundamental]], primer modo superior, etc. A cada frecuencia $\omega$ solo un conjunto finito de números de onda $k_j(\omega)$ son soluciones válidas.

*(Fuente: Foti Ch. 2, Sec. 2.4.1, p. 70–72, Ecs. 2.72–2.73)*

#### Ecuación de dispersión general (Foti Ec. 2.74)

Soluciones no triviales existen solo para autovalores $k_j = k_j(\omega)$, $j = 1, \ldots, M$. La relación implícita que los define es:

$$
\Phi_{L/R}[\lambda(x_2),\, \mu(x_2),\, \rho(x_2),\, k,\, \omega] = 0
$$

Esta es la **ecuación secular** (o ecuación de dispersión general): altamente no lineal y trascendente, sin solución cerrada. Sus raíces $k_j(\omega)$ dependen del perfil completo de propiedades elásticas $\lambda(x_2)$, $\mu(x_2)$ y $\rho(x_2)$ — es decir, del modelo de subsuelo completo. La [[Dispersion Curve|curva de dispersión]] $V_j(\omega) = \omega/k_j(\omega)$ codifica toda la información sobre la estructura del subsuelo que puede extraerse desde la superficie.

**Propiedades clave**:
- La función $\Phi_{L/R}$ se evalúa numéricamente para cada par $(k, \omega)$ mediante los algoritmos de la sección siguiente (Thomson–Haskell, matrices de rigidez).
- Para un medio homogéneo (sin estratificación), $\Phi_R = 0$ tiene una única raíz real: $V_R \approx 0.919 V_S$ — la velocidad de Rayleigh del semispacio homogéneo.
- En un [[Layered Media|medio estratificado]], $\Phi_{L/R} = 0$ tiene múltiples raíces a cada frecuencia: los modos de propagación. El número de modos crece con la frecuencia.

*(Fuente: Foti Ch. 2, Sec. 2.4.1, p. 72, Ec. 2.74)*

#### Algoritmos numéricos (Foti Sec. 2.4.1.1, p. 72–74)

Tres familias principales de algoritmos evalúan numéricamente $\Phi_{L/R}(k, \omega)$:

- **[[Thomson-Haskell Matrix|Thomson–Haskell]] (transfer matrix)**: construye la función $\Phi_{L/R}[\cdot]$ multiplicando matrices de capa 4×4 (Rayleigh) o 2×2 (Love). Las raíces de $\Phi = 0$ son los autovalores. Es el algoritmo más común por su implementación directa, pero sufre **inestabilidad numérica a alta frecuencia/profundidad**: el producto de matrices exponenciales produce overflow o cancelación catastrófica de dígitos significativos. En la práctica se normaliza $\Phi$ o se usa en combinación con técnicas de *root-bracketing*.

- **Matriz de rigidez dinámica (Kausel–Roesset 1981)**: reemplaza las matrices de transferencia por matrices de rigidez de capa ensambladas de forma similar a la mecánica estructural (método de elementos finitos). Es numéricamente más estable porque opera con matrices definidas positivas. Usada en la mayoría de códigos modernos (DISPACK, SurfSeis).

- **Coeficientes de reflexión–transmisión (Kennett 1974)**: algoritmo recursivo que modela explícitamente la interferencia constructiva entre modos mediante coeficientes globales de reflexión y transmisión. El más estable numéricamente de los tres, pero más complejo de implementar. Permite tratar capas fluidas y sólidas en el mismo medio.

*(Fuente: Foti Ch. 2, Sec. 2.4.1.1, p. 72–74)*

#### Ejemplo numérico (Foti Tabla 2.4 y Figs. 2.20–2.22)

La **Fig. 2.20** ilustra el comportamiento de $|\Phi_R[\cdot]|$ calculada con Thomson–Haskell en función del [[Wavenumber|número de onda]] a $f = 50\,\text{Hz}$, para el sistema estratificado de la **Tabla 2.4**:

| Capa | Espesor (m) | $V_P$ (m/s) | $V_S$ (m/s) | $\rho$ (Mg/m³) |
|------|-------------|-------------|-------------|-----------------|
| 1 | 10 | 200 | 100 | 1.9 |
| 2 | 10 | 400 | 200 | 1.9 |
| 3 | 10 | 600 | 300 | 1.9 |
| Semiespacio | ∞ | 1000 | 500 | 1.9 |

La función oscila rápidamente con el [[Wavenumber|número de onda]] (especialmente a alta frecuencia), lo que requiere técnicas robustas de *root-bracketing* con bisección para localizar confiablemente todas las raíces.

La **Fig. 2.21** muestra las [[Dispersion Curve|curvas de dispersión]] modales (24 modos identificados) para este sistema: [[Phase Velocity|velocidad de fase]] Rayleigh vs. frecuencia. Cada curva corresponde a un autovalor de la Ec. 2.71. Los [[Surface Wave Modes|modos superiores]] tienen mayor [[Phase Velocity|velocidad de fase]] y mayor profundidad de penetración. Al aumentar la frecuencia, aparecen nuevos modos y las curvas se empaquetan más densamente.

La **Fig. 2.22** muestra los perfiles de profundidad de las eigenfunciones de desplazamiento $r_1$ (horizontal) y $r_2$ (vertical) a $f = 16\,\text{Hz}$ para los primeros 4 modos. El resultado clave es que **los [[Surface Wave Modes|modos superiores]] penetran más profundamente**, lo que fundamenta la posibilidad de invertir [[Surface Wave Modes|modos superiores]] para resolver estructuras a mayor profundidad.

*(Fuente: Foti Ch. 2, Sec. 2.4.1, pp. 65–76, Ecs. 2.56–2.74, Tabla 2.4, Figs. 2.20–2.22)*

---

### 2.4.2 Modos de propagación y superposición modal

En medios estratificados, tanto [[Rayleigh Waves]] como [[Love Waves]] presentan **múltiples modos de propagación**:

- [[Surface Wave Modes|modo fundamental]]: mayor amplitud en superficie, más fácil de identificar experimentalmente
- [[Surface Wave Modes|modos superiores]]: mayor profundidad de penetración; pueden dominar cuando hay fuertes contrastes de velocidad

El campo de ondas registrado por un arreglo de geófonos es en general una **superposición de modos** — ver [[Mode Superposition]].

> **Implicación crítica para la tesis**: en medios inversamente dispersivos, los [[Surface Wave Modes|modos superiores]] contribuyen de manera importante incluso a frecuencias bajas. Invertir la [[Dispersion Curve|curva de dispersión]] aparente como si fuera del [[Surface Wave Modes|modo fundamental]] introduce errores sistemáticos en el perfil $V_S(z)$. Este es uno de los problemas más frecuentes en la práctica.

> [!EXAMPLE] Evidencia empírica: Paper 031 (Tokimatsu et al. 1992) — [[Surface Wave Modes|modos superiores]] dominan la dispersión aparente en perfiles con inversión de velocidad
> **Paper 031 (Tokimatsu, Tamura & Kojima 1992, *J. Geotech. Eng.* ASCE 118(10):1529–1543, 352 citas)** analiza teóricamente el efecto de los [[Surface Wave Modes|modos superiores]] de [[Rayleigh Waves|ondas de Rayleigh]] sobre la [[Dispersion Curve|curva de dispersión]] aparente medida en campo (contexto SASW). Usando cálculo multimodal por [[Thomson-Haskell Matrix|matriz de transferencia]] en perfiles sintéticos estratificados, el estudio demuestra que: (1) en perfiles con **inversión de velocidad** (capa rígida sobre capa blanda), los [[Surface Wave Modes|modos superiores]] pueden **dominar energéticamente** la curva aparente incluso a bajas frecuencias, desplazándola hasta 2× la velocidad del [[Surface Wave Modes|modo fundamental]]; (2) invertir la curva aparente asumiendo [[Surface Wave Modes|modo fundamental]] produce subestimaciones sistemáticas de $V_S$ en profundidad. Este resultado motiva directamente los métodos de [[Inversión|inversión]] multimodal (como los de Xia 2003, Paper 025) y las búsquedas globales estocásticas (Maraschini 2010, Paper 034) que no requieren asignación modal a priori.
> — Research Database, entrada 031; Tokimatsu et al. (1992), *J. Geotech. Eng.* ASCE 118(10):1529–1543. DOI: 10.1061/(ASCE)0733-9410(1992)118:10(1529).

---

### 2.4.3 El problema de la fuente: Lamb's Problem

#### Solución en el campo lejano (Foti Ec. 2.75)

El [[Lamb's Problem]] describe la respuesta de un [[Elastic Half Space|semiespacio elástico]] homogéneo a una carga puntual vertical armónica $F\,e^{i\omega t}$ en la superficie libre. El desplazamiento vertical de Rayleigh en **aproximación de campo lejano** es (Foti Ec. 2.75):

$$
u_2(r,\omega) = \frac{F\,e^{i\omega t}}{2i\mu}\cdot k_R\cdot\Psi(k_R)\cdot H_0^{(2)}(k_R r)
$$

donde $r = \sqrt{x_1^2 + x_3^2}$, $k_R = \omega/V_R$, y $H_0^{(2)}(\cdot)$ es la [[Hankel Function|función de Hankel]] de segundo tipo y orden cero. Para $|k_R r| \gg 1$, la expansión asintótica muestra que la amplitud decae como $r^{-0.5}$ (frentes de onda cilíndricos).

Las [[Body Waves|ondas de cuerpo]], en cambio, decaen como $r^{-2}$ en la superficie libre — mucho más rápido.

#### Umbral de campo cercano / campo lejano

El campo total se descompone en $\mathbf{u} = \mathbf{u}_B + \mathbf{u}_S$. En el **campo lejano**, la contribución de [[Body Waves|ondas de cuerpo]] es despreciable.

**Umbral cuantitativo** (Foti Sec. 2.4.2, p. 86): en medios *normalmente dispersivos*, los efectos de [[Near-field Effect|campo cercano]] son significativos hasta:

$$
r \lesssim \frac{\lambda_R}{2}
$$

En medios *inversamente dispersivos*, el campo cercano puede extenderse hasta $r \approx 2\lambda_R$.

> **Implicación para diseño experimental**: el primer geófono debe ubicarse al menos a $\lambda_R/2$ de la fuente — idealmente a $\lambda_R$. A baja frecuencia (longitudes de onda grandes), esta restricción obliga a usar arreglos con offset fuente-receptor largo.

*(Fuente: Foti Ch. 2, Sec. 2.4.2.1, p. 78–83, Ec. 2.75)*

---

### 2.4.4 Función de atenuación geométrica de Rayleigh (Foti Sec. 2.4.2.3)

En un semiespacio homogéneo, la amplitud de las Rayleigh waves decae como $r^{-0.5}$ (ley de distribución cilíndrica). En un semiespacio verticalmente inhomogéneo, la ley de decaimiento se **modifica** por la interferencia entre modos.

La función que describe este decaimiento generalizado es la **función de atenuación geométrica de Rayleigh** $Y_l(r, x_2, \omega)$, $l = r, 2$, obtenida de la superposición modal (Foti Ec. 2.90). El campo de desplazamiento se escribe como:

$$
u_l(r, x_2, \omega) = F \cdot Y_l(r, x_2, \omega) \cdot e^{i[\omega t - \psi_l(r, x_2, \omega)]}, \qquad l = r, 2
$$

En el caso homogéneo ($M=1$), $Y_l$ se reduce a $E_l/\sqrt{r}$, recuperando la ley $r^{-0.5}$. En medios estratificados, la forma de $Y_l$ depende de la frecuencia y del perfil de velocidades, y puede desviarse sustancialmente de $r^{-0.5}$ al aumentar la frecuencia.

*(Fuente: Foti Ch. 2, Sec. 2.4.2.3, p. 84–90, Ec. 2.90)*

---

### 2.4.5 [[Phase Velocity|Velocidad de fase]] aparente (efectiva) de Rayleigh (Foti Sec. 2.4.2.4) ★

**Este es el concepto más crítico de la tesis**: lo que los geófonos miden no es la [[Phase Velocity|velocidad de fase]] de ningún modo individual, sino la **[[Phase Velocity|velocidad de fase]] aparente** o efectiva resultante de la superposición de todos los modos activos.

#### Definición (Foti Ec. 2.93)

A partir de la condición de fase constante del campo resultante, la [[Phase Velocity|velocidad de fase]] aparente es:

$$
V_l^{app}(r, x_2, \omega) = \frac{\omega}{\partial\psi_l(r, x_2, \omega)/\partial r}, \qquad l = r, 2
$$

Es una cantidad **local**: su valor depende de la posición del receptor $r$. Al variar con $\omega$ y $r$ define una **superficie de dispersión** $V_l^{app}(r, 0, \omega)$ en el plano $(\omega, r)$.

#### Expresión explícita en términos de autofunciones (Foti Ec. 2.95)

$$
V_r^{app}(r,x_2,\omega) = 2\omega\cdot\frac{\displaystyle\sum_{i=1}^{M}\sum_{j=1}^{M}\frac{r_1(x_2,k_i)\,r_1(x_2,k_j)\,r_2(0,k_i)\,r_2(0,k_j)\,\cos[r(k_i-k_j)]}{\left[(V_R)_i(U_R)_i(I_R)_i\right]\left[(V_R)_j(U_R)_j(I_R)_j\right]\sqrt{k_i k_j}}}{\displaystyle\sum_{n=1}^{M}\sum_{m=1}^{M}\frac{r_1(x_2,k_n)\,r_1(x_2,k_m)\,r_2(0,k_n)\,r_2(0,k_m)\,(k_n+k_m)\,\cos[r(k_n-k_m)]}{\left[(V_R)_n(U_R)_n(I_R)_n\right]\left[(V_R)_m(U_R)_m(I_R)_m\right]\sqrt{k_n k_m}}}
$$

donde $(V_R)_j$, $(U_R)_j$ y $(I_R)_j$ son la [[Phase Velocity|velocidad de fase]], velocidad de grupo e integral de energía del $j$-ésimo modo.

#### Implicaciones para la [[Inversión|inversión]]
![[Pasted image 20260318140813.png]]
- En medios **normalmente dispersivos**: la curva aparente está cerca del [[Surface Wave Modes|modo fundamental]] a frecuencias intermedias; la aproximación monomodal suele ser aceptable
- En medios **inversamente dispersivos**: la curva aparente diverge significativamente del [[Surface Wave Modes|modo fundamental]] desde frecuencias bajas (~8 Hz en los ejemplos de Foti) — invertirla como [[Surface Wave Modes|modo fundamental]] introduce errores severos en $V_S(z)$
- Lo que los métodos experimentales ([[MASW Method|MASW]], f-k) extraen es $V^{app}$, no curvas modales; el proceso de [[Inversión|inversión]] debe tener esto en cuenta

*(Fuente: Foti Ch. 2, Sec. 2.4.2.4, p. 90–95, Ecs. 2.93–2.95)*

> [!EXAMPLE] Evidencia empírica: Paper 002 (Xia et al. 1999) — dispersión multimodal en medio estratificado
> **Paper 002 (Xia, Miller & Park 1999, *Geophysics* 64(3):691–700, 2000+ citas)** — el paper fundacional de la [[Inversión|inversión]] [[MASW Method|MASW]] — implementa el [[Forward Problem|problema directo]] para [[Rayleigh Waves|ondas de Rayleigh]] en medios estratificados usando la [[Thomson-Haskell Matrix|matriz de Thomson-Haskell]], cuya solución es exactamente el eigenproblem desarrollado en esta sección (§2.4.1). El sitio de Kansas (substrato de caliza, perfil normalmente dispersivo) mostró una [[Dispersion Curve|curva de dispersión]] aparente dominada por el [[Surface Wave Modes|modo fundamental]] en el rango 5–50 Hz, con [[Surface Wave Modes|modos superiores]] visibles pero energéticamente débiles en el espectro f-k. La [[Jacobian Matrix|Jacobiana]] analítica calculada a partir de las autofunciones de eigendesplazamiento (ecuaciones análogas a Ec. 2.66) permitió convergencia del esquema Gauss-Newton en <5 iteraciones. El perfil $V_S$ resultante concordó con sondeos de refracción dentro del 15% en los primeros 10 m, validando el eigenproblem de Rayleigh como herramienta de caracterización para el [[Forward Problem|problema directo]] en [[Inversión|inversión]] iterativa.
>
> — Research Database, entrada 002; Xia et al. (1999), *Geophysics* 64(3):691–700.

---

## 2.5 Surface Waves in Vertically Inhomogeneous, Inelastic Continua

> Fuente: Foti et al. (2014), Sección 2.5, pp. 96–117.

La extensión del marco elástico al caso **[[Viscoelastic Media|viscoelástico]]** permite modelar la disipación de energía intrínseca de los geomateriales reales. La consecuencia observable en la propagación de ondas superficiales es doble: (1) la [[Phase Velocity|velocidad de fase]] se vuelve compleja — la parte real gobierna la propagación y la parte imaginaria el decaimiento espacial de amplitud — y (2) la [[Dispersion Curve|curva de dispersión]] presenta una ligera dependencia adicional de la frecuencia debida a la [[Attenuation|atenuación]] (dispersión por relajación). El producto de esta sección — el operador del [[Forward Problem|problema directo]] para medios viscoelásticos — es la base teórica del análisis de atenuación desarrollado en el Capítulo 5.

### 2.5.1 Motivación y marco constitutivo

Los suelos y rocas reales **no son elásticos perfectos**: parte de la energía sísmica se disipa como calor por deformación viscosa interna (rozamiento entre partículas, movimiento de fluido poral). Este fenómeno es relevante para el diseño sísmico porque controla la amplificación del movimiento del suelo: mayor amortiguamiento → menor amplificación en la frecuencia de resonancia del depósito.

Cuantitativamente, el amortiguamiento material se expresa mediante la **[[Shear Damping Ratio|razón de amortiguamiento]]** $D_S$ (también escrita $D$ o $\xi$ en literatura de ingeniería sísmica), que representa la fracción de energía disipada por ciclo de deformación. Para suelos dentro del rango de deformación lineal cíclica (típicamente deformación de corte $\gamma < 10^{-5}$), los valores típicos son $D_S \approx 1\text{–}5\%$.

La **[[Viscoelastic Media|viscoelasticidad]] lineal** es el marco constitutivo más simple y físicamente consistente para describir este comportamiento. Se basa en cuatro hipótesis: (1) **pequeñas deformaciones** (linealización del tensor de deformación), (2) **invariancia temporal** (las propiedades del material no cambian con el tiempo), (3) **postulado de herencia** (el esfuerzo en el instante $t$ depende de toda la historia previa de deformación), y (4) **hipótesis de memoria débil** (la influencia del pasado remoto es despreciable, lo que garantiza la existencia de la integral de Boltzmann).

El marco viscoelástico lineal es fundamentalmente diferente de la plasticidad o la histéresis no lineal: solo describe la disipación en el régimen de deformaciones infinitesimales. Para niveles de deformación mayores, se requieren modelos más complejos (hiperbólico, Ramberg-Osgood, etc.) que están fuera del alcance de los métodos de ondas superficiales estándar.

*(Fuente: Foti Ch. 2, Sec. 2.5.1, p. 96–106)*

---

### 2.5.2 Modelo constitutivo: ecuación de Boltzmann (Foti Ec. 2.96)
![[Pasted image 20260318141045.png]]
Bajo esas hipótesis, la relación esfuerzo–historia de deformación es (Foti Ec. 2.96):

$$
\boldsymbol{\sigma}(t) = \int_{-\infty}^{t} \mathbf{G}(t-\tau):\frac{d\boldsymbol{\varepsilon}(\tau)}{d\tau}\,d\tau
$$

donde $\mathbf{G}(t)$ es el **tensor función de relajación** del material. Para un material isotrópico, solo dos funciones escalares son necesarias: $G_S(t)$ (corte) y $G_B(t)$ (volumétrica).

En el dominio frecuencial, para excitación armónica $\boldsymbol{\varepsilon}(t) = \boldsymbol{\varepsilon}_0 e^{i\omega t}$, la relación se convierte en (Foti Ec. 2.98):

$$
\boldsymbol{\sigma}(t) = \mathbf{G}^*(\omega):\boldsymbol{\varepsilon}_0\,e^{i\omega t}
$$

donde $\mathbf{G}^*(\omega) = \mathbf{G}_{(1)}(\omega) + i\,\mathbf{G}_{(2)}(\omega)$ es el **módulo complejo**. Las partes real e imaginaria son los módulos de *storage* y de *loss*.

*(Fuente: Foti Ch. 2, Sec. 2.5.1, p. 98–100, Ec. 2.96)*

---

### 2.5.3 Relaciones de Kramers–Krönig y causalidad (Foti Ec. 2.99)

Las partes real e imaginaria del módulo complejo **no son independientes**. Están ligadas por las **[[Kramers-Kronig Relations|relaciones de Kramers–Krönig]]** (Foti Ec. 2.99):

$$
G_{(1)}(\omega) = G_{(e)} + \frac{2}{\pi}\int_0^{\infty}\frac{G_{(2)}(\tau)\cdot\omega^2}{\tau\cdot(\omega^2-\tau^2)}\,d\tau
$$

donde $G_{(e)} = G(t \to \infty)$ es la respuesta de equilibrio.

Estas relaciones son consecuencia directa del **principio de causalidad física** — la respuesta no puede preceder a la excitación. En términos de parámetros físicos de propagación ($V_\chi(\omega)$ y $D_\chi(\omega)$), la restricción análoga es (Foti Ec. 2.130):

$$
V_\chi^2(\omega) + \omega^2\cdot\frac{4}{\pi}\int_0^{\infty}\frac{D_\chi(\tau)}{\tau\cdot(\tau^2-\omega^2)}\cdot V_\chi^2(\tau)\,d\tau = G_{(e)\chi}\cdot\frac{2(1+4D_\chi^2)}{1+\sqrt{1+4D_\chi^2}}
$$

**Implicación directa**: la [[Phase Velocity|velocidad de fase]] $V_\chi(\omega)$ y el amortiguamiento $D_\chi(\omega)$ de ondas en un suelo real **no pueden asignarse independientemente** — están restringidos por la Ec. 2.130. Esto implica que los materiales viscoelásticos son **inherentemente dispersivos**.

*(Fuente: Foti Ch. 2, Sec. 2.5.1–2.5.2, p. 100, 111, Ecs. 2.99, 2.130)*

---

### 2.5.4 Ondas viscoelásticas en medios homogéneos: principio de correspondencia

La analogía entre las ecuaciones de campo de la elasticidad y la [[Viscoelastic Media|viscoelasticidad]] en el dominio frecuencial constituye el **[[Correspondence Principle|principio de correspondencia elástico–viscoelástico]]** (Foti Sec. 2.5.2). Su enunciado es notablemente conciso:

> Las soluciones del problema [[Viscoelastic Media|viscoelástico]] en dominio frecuencial se obtienen reemplazando las constantes elásticas reales $\lambda$, $\mu$ por sus equivalentes complejos $G_S^*(\omega)$, $G_B^*(\omega)$ en las expresiones del caso elástico.

Esta sustitución es posible porque la [[Fourier Integral|transformada de Fourier]] de la integral de Boltzmann transforma la convolución temporal en una multiplicación por el módulo complejo en el dominio frecuencial. Las ecuaciones de movimiento transformadas son **formalmente idénticas** a las ecuaciones elásticas con módulos reales, excepto que los módulos son ahora funciones complejas de $\omega$.

El **poder del principio de correspondencia** reside en que **no es necesario re-derivar toda la teoría de ondas**: las [[Dispersion Relation|relaciones de dispersión]] para [[Rayleigh Waves|ondas de Rayleigh]] y [[Love Waves|Love]], las condiciones de borde, las expresiones de [[Phase Velocity|velocidad de fase]] — todas son válidas en medios viscoelásticos con la sustitución $\{V_S, V_P\} \to \{V_S^*, V_P^*\}$. En particular, la **ecuación secular de Rayleigh** (que en el caso elástico tiene coeficientes reales y raíces reales) pasa a tener coeficientes complejos y raíz compleja $V_R^* = V_R - i\,V_R\,D_R$, donde la parte imaginaria codifica la atenuación de la onda de Rayleigh.

#### Velocidades complejas de [[Body Waves|ondas de cuerpo]] (Foti Ec. 2.118)

$$
V_P^*(\omega) = \sqrt{\frac{G_B^*(\omega) + \frac{4}{3}G_S^*(\omega)}{\rho}}, \qquad V_S^*(\omega) = \sqrt{\frac{G_S^*(\omega)}{\rho}}
$$

El [[Wavenumber|número de onda]] complejo $k_\chi^* = \omega/V_\chi^* = k_\chi - i\alpha_\chi$ conduce a la solución armónica:

$$
u \propto e^{-\alpha_\chi x}\,e^{i(k_\chi x - \omega t)}
$$

donde $\alpha_\chi$ es el **coeficiente de atenuación espacial**.

#### Razón de amortiguamiento material (Foti Ec. 2.115)

La **razón de amortiguamiento material** $D_\chi$ cuantifica la fracción de energía elástica disipada por ciclo de deformación. Se define como la relación entre la parte imaginaria y real del módulo complejo:

$$
D_\chi(\omega) = \frac{G_{(2)\chi}}{2G_{(1)\chi}}, \qquad \chi = P, S
$$

donde $G_{(1)\chi}$ es el módulo de almacenamiento (energía recuperable — deformación elástica) y $G_{(2)\chi}$ es el módulo de pérdida (energía disipada — histéresis). El factor 2 en el denominador aparece de la definición energética: la energía disipada por ciclo dividida por $4\pi$ veces la energía máxima almacenada.

**Relación con el factor de calidad**: $Q_\chi(\omega) = 1/(2D_\chi(\omega))$. Un suelo con $D_S = 5\%$ tiene $Q_S = 10$ — absorbe el 10% de la energía por ciclo. Valores típicos para geomateriales dentro del umbral de deformación lineal: $D_S \approx 1\text{–}5\%$, $D_P \approx 0.5\text{–}2\%$ (las ondas P disipen menos por su mecanismo de deformación volumétrica vs. cortante).

**Importancia**: $D_S(z)$ es el segundo parámetro objetivo de la [[Inversión|inversión]] viscoelástica (después de $V_S(z)$). Controla la amplificación dinámica del suelo en la frecuencia de resonancia del depósito — relevante para la evaluación del efecto de sitio sísmico.

*(Fuente: Foti Ch. 2, Sec. 2.5.2, p. 106–108, Ec. 2.115)*

*(Fuente: Foti Ch. 2, Sec. 2.5.2, p. 106–112, Ecs. 2.115, 2.118)*

---

### 2.5.5 Aproximación de disipación débil (Foti Ec. 2.128)

Expandiendo la expresión exacta de $V_\chi^*$ en serie de MacLaurin en $D_\chi$ y reteniendo solo términos de **primer orden**:

$$
\boxed{V_\chi^*(\omega) \approx V_\chi(\omega)\,[1 + i\,D_\chi(\omega)]}
$$

Válida para:

$$
\sup[D_\chi(\omega)] \leq 0.05 \quad \text{(Foti Ec. 2.129)}
$$

Experimentalmente, los geomateriales dentro del umbral de deformación lineal cíclica satisfacen típicamente $D \sim 1\text{–}5\%$, por lo que esta aproximación es adecuada para la mayoría de aplicaciones geofísicas (Foti p. 110).

**Consecuencia crítica**: la [[Phase Velocity|velocidad de fase]] $V_\chi(\omega)$ se ve afectada por $D$ solo en **segundo orden** — la disipación no afecta significativamente la [[Dispersion Curve|curva de dispersión]]. Esto justifica el procedimiento estándar: [[Inversión|inversión]] de dispersión primero (para $V_S$), [[Inversión|inversión]] de atenuación después (para $D_S$), tratándolas como problemas desacoplados.

*(Fuente: Foti Ch. 2, Sec. 2.5.2, p. 110, Ec. 2.128)*

---

### 2.5.6 [[Rayleigh Eigenproblem]] en medios débilmente disipativos (Foti Ec. 2.133)

La combinación del [[Correspondence Principle|principio de correspondencia]] con la **hipótesis de disipación débil** ($D_S, D_P \leq 5\%$) y los [[Variational Principles|principios variacionales de Love–Rayleigh]] produce el resultado más importante de la sección: una expresión analítica cerrada para la [[Phase Velocity|velocidad de fase]] $V_R(\omega)$ y el [[Attenuation Coefficient|coeficiente de atenuación]] $\alpha_R(\omega)$ en función de los perfiles de velocidad y amortiguamiento. Este resultado — Foti Ec. 2.133 — es el **[[Forward Problem|operador del problema directo]] viscoelástico** que se invierte en los algoritmos de Capítulo 6 para recuperar $V_S(z)$ y $D_S(z)$ simultáneamente desde las curvas medidas.

Aplicando los principios variacionales bajo la hipótesis de disipación débil (Ecs. 2.128–2.129), se obtiene (Foti Ec. 2.133):

$$
\begin{cases}
V_R(\omega) = V_R^e + \displaystyle\int_0^\infty V_S\frac{\partial V_R}{\partial V_S}\bigg|_{\omega,V_P}\!\!\left[1-\frac{V_S^{e2}}{V_S^2}\right]dx_2 + \int_0^\infty V_P\frac{\partial V_R}{\partial V_P}\bigg|_{\omega,V_S}\!\!\left[1-\frac{V_P^{e2}}{V_P^2}\right]dx_2\\[12pt]
\alpha_R(\omega) = \dfrac{\omega}{[V_R(\omega)]^2}\left\{\displaystyle\int_0^\infty V_S D_S\frac{\partial V_R}{\partial V_S}\bigg|_{\omega,V_P}dx_2 + \int_0^\infty V_P D_P\frac{\partial V_R}{\partial V_P}\bigg|_{\omega,V_S}dx_2\right\}
\end{cases}
$$

donde $V_R^e$ es la velocidad de Rayleigh del medio elástico asociado ($D=0$), y las derivadas $\partial V_R/\partial V_S$, $\partial V_R/\partial V_P$ son las **[[Sensitivity Kernel|sensitividades]]** de la velocidad de Rayleigh respecto al perfil de velocidades.

#### Consecuencias fundamentales

1. **Desacopla** los dos problemas inversos:
   - Primero: invertir $V_R(\omega)$ para obtener $V_S(x_2)$ → problema **altamente no lineal**
   - Luego: invertir $\alpha_R(\omega)$ para obtener $D_S(x_2)$ dado $V_S$ → problema **lineal**

2. $V_R(\omega)$ y $\alpha_R(\omega)$ se calculan a partir de la solución del problema de autovalores **elástico** — no se requiere resolver el problema viscoelástico completo

3. Validez: solo para $D \leq 5\%$ — dentro del rango típico de geomateriales

> **Implicación para la tesis**: si el objetivo es el perfil $V_S$, la disipación es de segundo orden y puede ignorarse en la [[Dispersion Curve|curva de dispersión]]. Si el objetivo incluye el perfil $D_S$, se requiere medir amplitudes con calibración cuidadosa — exigencia instrumental significativamente mayor.

*(Fuente: Foti Ch. 2, Sec. 2.5.3, p. 113–119, Ec. 2.133)*

> [!EXAMPLE] Evidencia empírica: Paper 008 (Socco & Strobbia 2004) — tutorial completo: desacoplamiento $V_S$/$D_S$ y flujo de [[Inversión|inversión]] en campo
> **Paper 008 (Socco & Strobbia 2004, *Near Surface Geophysics* Vol.2(4):165–185, 306 citas)** presenta el flujo metodológico completo para caracterización sísmica superficial, validando en datos reales que el análisis del [[Attenuation Coefficient|coeficiente de atenuación]] puede desacoplarse del análisis de [[Phase Velocity|velocidad de fase]] bajo la hipótesis de disipación débil (Foti Ec. 2.133): la [[Inversión|inversión]] de [[Dispersion Curve|dispersión]] para $V_S(z)$ se realiza primero; la [[Inversión|inversión]] de atenuación para $D_S(z)$ se ejecuta después usando el perfil $V_S$ como entrada. El tutorial confirma que los geomateriales típicos satisfacen $D \leq 5\%$, validando la aplicabilidad práctica del [[Correspondence Principle|principio de correspondencia viscoelástico]]. Las guías de adquisición y procesamiento cubren efectos de [[Near-field Effect|campo cercano]], aliasing espacial, métodos de [[Inversión|inversión]] locales y globales. Un resultado clave: la estimación de $D_S$ requiere calibración de amplitudes —exigencia no requerida en la [[Inversión|inversión]] de dispersión— lo que eleva significativamente la complejidad instrumental al incluir la atenuación como objetivo de [[Inversión|inversión]].
> — Research Database, entrada 008; Socco & Strobbia (2004), *Near Surface Geophysics* Vol.2(4):165–185. DOI: 10.3997/1873-0604.2004015.

---

## Fuentes

- PDF: Sebastiano Foti Chapter 2 (book pages 37–120)
- Secciones cubiertas: 2.1–2.5