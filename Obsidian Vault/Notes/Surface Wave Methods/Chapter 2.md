# Linear Wave Propagation in Vertically Inhomogeneous Continua

## Introducción

Este capítulo desarrolla la teoría de propagación de ondas superficiales en medios:

- elásticos lineales
- viscoelásticos lineales

con el objetivo de establecer la base física para el **modelado directo (forward modeling)** utilizado en métodos de caracterización del subsuelo mediante ondas superficiales.

Aunque el desarrollo teórico incluye tanto [[Love Waves]] como [[Rayleigh Waves]], el capítulo se enfoca principalmente en **Rayleigh waves**, debido a su mayor relevancia en aplicaciones prácticas de exploración geofísica, ingeniería geotécnica y caracterización sísmica de sitio.

Las [[Rayleigh Waves]] son particularmente importantes porque dominan el campo de ondas registrado por geófonos en mediciones de superficie y contienen información directa sobre el perfil de velocidades de [[S-Waves]]. En campo, a distancias de una o dos longitudes de onda desde la fuente, las ondas superficiales representan ~67% de la energía total generada por una fuente puntual vertical, con decaimiento geométrico $\propto r^{-0.5}$ frente a $r^{-2}$ de las ondas de cuerpo. Esta diferencia explica por qué el campo de ondas queda dominado por las componentes de Rayleigh a medida que se aleja de la fuente.

El contenido del capítulo progresa desde los fundamentos de la mecánica ondulatoria (Sec. 2.1) hasta la derivación rigurosa de las eigenfunciones de Rayleigh en semiespacios homogéneos (Sec. 2.2), la teoría de Love waves (Sec. 2.3), la generalización a medios verticalmente heterogéneos con múltiples modos de propagación (Sec. 2.4), y finalmente la extensión al caso viscoelástico que fundamenta la medición de atenuación en campo (Sec. 2.5). Este arco argumental es la columna vertebral teórica de todos los métodos de adquisición, procesamiento e inversión discutidos en los capítulos siguientes.

---

## Estructura del capítulo

El capítulo se divide en cinco secciones principales.

### 2.1 Basic notions of wave propagation

Esta sección introduce los fundamentos de propagación de ondas en medios continuos.

Primero se distinguen dos clases fundamentales de movimiento ondulatorio:

- **[[Hyperbolic Waves]]**
- **[[Wave Dispersion]]**

Luego se introducen las ecuaciones de movimiento en sólidos elásticos y la propagación de ondas de cuerpo en medios:

- homogéneos
- isotrópicos
- elásticos lineales

Esto permite introducir parámetros fundamentales como:

- [[Wavenumber]]
- [[Angular Frequency]]
- [[Phase Velocity]]
- [[Group Velocity]]

En este contexto aparecen las ondas de cuerpo:

- [[P-waves]]
- [[S-Waves]]

También se introducen ondas armónicas de la forma:

$$
\phi(x,t) = A e^{i(kx-\omega t)}
$$

La relación funcional entre frecuencia y número de onda constituye la [[Dispersion Relation]], que es central para describir ondas dispersivas.

### 2.2 Rayleigh waves in homogeneous elastic continua

En esta sección se demuestra la existencia de [[Rayleigh Waves]] propagándose en un medio elástico homogéneo semi-infinito.

El desarrollo teórico se realiza utilizando el método de [[Elastic Wave Potentials]].

El resultado principal es la obtención de la ecuación de dispersión de Rayleigh, que relaciona:

- propiedades elásticas del medio
- velocidad de propagación de la onda

Este resultado constituye la base teórica de los métodos modernos de caracterización de sitio mediante ondas superficiales.

### 2.3 Love waves in layered media

Esta sección analiza las condiciones necesarias para la existencia de [[Love Waves]].

Las Love waves aparecen cuando existe la siguiente estructura del subsuelo:

```text
capa elástica
sobre
semi-espacio elástico
```

Se estudian:

- condiciones de guiado de ondas
- [[Dispersion Relation]]
- comparación con [[Rayleigh Waves]]

Una diferencia fundamental es que las Love waves presentan comportamiento dispersivo cuando el medio es estratificado, fenómeno asociado a la [[Geometric Dispersion]].

### 2.4 Surface waves in vertically inhomogeneous media

Esta sección extiende el análisis a medios donde las propiedades mecánicas varían con la profundidad.

Se analizan:

- propagación de [[Rayleigh Waves]]
- propagación de [[Love Waves]]
- medios estratificados

Se introducen conceptos clave como:

- [[Mode Superposition]]
- velocidad de fase efectiva ([[Phase Velocity]])

También se revisita el [[Lamb’s Problem]], que describe la generación de ondas superficiales por una fuente puntual aplicada sobre la superficie libre del medio.

Este problema corresponde a la resolución de un problema de contorno no homogéneo asociado a la generación de ondas.

### 2.5 Wave propagation in dissipative media

La última sección introduce la propagación de ondas en medios disipativos.

Se discuten:

- modelos constitutivos de [[Viscoelastic Media]]
- mecanismos de [[Attenuation]]

Utilizando el principio de correspondencia elastic-viscoelastic, se obtienen las propiedades de propagación de ondas de cuerpo en medios viscoelásticos.

Posteriormente se analiza la propagación de ondas superficiales en medios:

- viscoelásticos
- verticalmente heterogéneos

La atención se centra en la resolución del [[Rayleigh Eigenproblem]] en medios débilmente disipativos.

Este resultado constituye la base teórica de muchos procedimientos utilizados en geofísica para modelar la propagación de ondas superficiales en medios reales, donde la disipación de energía no puede despreciarse.

---

## 2.1 Basic notions of wave propagation

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

La solución general es la [[d’Alembert Solution]]:

$$
\phi(x,t)=f(x-c_0t)+g(x+c_0t)
$$

Esto representa la [[Wave Superposition]] de dos ondas:

- $f(x-c_0t)$ → propagándose hacia la derecha
- $g(x+c_0t)$ → propagándose hacia la izquierda

ambas con velocidad $c_0$.

![[Pasted image 20260311151531.png]]

La propiedad clave de las ondas hiperbólicas es que **no se distorsionan durante la propagación**, porque la velocidad de propagación no depende de la frecuencia y todos los números de onda viajan con la misma [[Phase Velocity]]:

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

Si $\omega(k)$ depende de $k$, la velocidad de fase no es constante.

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

Las categorías no son mutuamente excluyentes. Existen ondas que son soluciones de [[Hyperbolic Partial Differential Equations]] y, sin embargo, pueden presentar [[Wave Dispersion]] dependiendo del medio.

Ejemplos relevantes:

- [[Body Waves]] en medios elásticos homogéneos → no dispersivas
- [[Body Waves]] en medios disipativos o porosos → dispersivas

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

Un resultado importante discutido posteriormente en el capítulo es que:

- las [[Rayleigh Waves]] en un [[Elastic Half Space]] homogéneo son no dispersivas
- se vuelven dispersivas cuando el medio es [[Layered Media]]

### 2.1.2 Group Velocity

La **velocidad de grupo** describe la velocidad a la que se propaga la envolvente de un paquete de ondas en un medio dispersivo.

$$
c_g = \frac{d\omega}{dk}
$$

Si la velocidad de fase es:

$$
c_0 = \frac{\omega}{k}
$$

entonces también puede escribirse como:

$$
c_g = c_0 + k\frac{dc_0}{dk}
$$

![[Pasted image 20260311155937.png]]

Si se superponen dos ondas de frecuencias y números de onda muy cercanos, aparece una oscilación rápida interna y una envolvente lenta:

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

- una portadora senoidal de número de onda medio $k_m$ y frecuencia media $\omega_m$
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

A partir de las ecuaciones de la elastodinámica lineal se demuestra la existencia de dos tipos fundamentales de ondas de cuerpo:

- [[P-waves]]
- [[S-Waves]]

Estas ondas constituyen los modos básicos de propagación en sólidos elásticos y sirven como base física para la formación de [[Surface Waves]].

#### Marco físico

El modelo considera un medio continuo con las siguientes hipótesis:

- medio elástico lineal
- medio isotrópico
- deformaciones pequeñas
- medio homogéneo
- dominio no acotado

#### Campo de desplazamiento

La variable fundamental es el campo de desplazamiento:

$$
u(x,t)
$$

Este campo describe el desplazamiento de cada punto material del continuo respecto a su posición de equilibrio.

#### Tensor de deformación

Las deformaciones se describen mediante el [[Strain Tensor]]. Para deformaciones pequeñas:

$$
\varepsilon =
\frac{1}{2}
(\nabla u + (\nabla u)^T)
$$

#### Tensor de esfuerzos

Las fuerzas internas del medio se describen mediante el [[Stress Tensor]].

#### Fuerzas internas y ecuación de movimiento

Las fuerzas internas que actúan sobre un volumen diferencial se obtienen mediante la divergencia del tensor de esfuerzos:

$$
\nabla \cdot \sigma
$$

Aplicando el balance dinámico al continuo se obtiene:

$$
\nabla \cdot \sigma =
\rho \frac{\partial^2 u}{\partial t^2}
$$

#### Relación constitutiva

Para un material elástico isotrópico:

$$
\sigma =
\lambda\,tr(\varepsilon)\,I
+
2\mu\,\varepsilon
$$

con:

- $\lambda, \mu$ → constantes de Lamé
- $I$ → tensor identidad
- $tr(\varepsilon)$ → traza del tensor de deformación

Esta separación distingue entre deformación volumétrica y deformación de corte.

#### Ecuaciones de Navier

Sustituyendo la ley de Hooke en la ecuación de movimiento se obtiene:

$$
\mu \nabla^2 u +
(\lambda + \mu)\nabla(\nabla \cdot u)
=
\rho \frac{\partial^2 u}{\partial t^2}
$$

Estas ecuaciones constituyen un sistema de [[Hyperbolic Partial Differential Equations]].

#### Descomposición del campo de desplazamiento

Mediante la descomposición de Helmholtz, el campo admite:

- una componente irrotacional
- una componente rotacional

Como consecuencia, el sistema admite dos tipos independientes de ondas:

- [[P-waves]] → asociadas a $\nabla \cdot u$
- [[S-Waves]] → asociadas a $\nabla \times u$

#### Velocidades de propagación

Para [[P-waves]]:

$$
V_P =
\sqrt{
\frac{\lambda + 2\mu}{\rho}
}
$$

Para [[S-Waves]]:

$$
V_S =
\sqrt{
\frac{\mu}{\rho}
}
$$

Siempre se cumple:

$$
V_S < V_P
$$

Estas velocidades corresponden a la [[Phase Velocity]] de las ondas de cuerpo. En medios homogéneos, además:

[[Group Velocity]] = [[Phase Velocity]]

#### Polarización de ondas S

Las [[S-Waves]] poseen dos posibles polarizaciones:

- SV → polarización vertical
- SH → polarización horizontal

Esto es fundamental para la clasificación de las [[Surface Waves]]:

- [[Rayleigh Waves]] → acoplamiento P + SV
- [[Love Waves]] → ondas SH guiadas

#### Conversión de modos

Cuando una onda incide sobre una interfaz entre medios elásticos ocurre [[Mode Conversion]].

- onda P incidente → ondas reflejadas y transmitidas P y SV
- onda SV incidente → ondas reflejadas y transmitidas P y SV
- onda SH incidente → solo ondas SH

Este fenómeno es esencial para comprender la propagación en [[Layered Media]] y [[Vertically Inhomogeneous Media]].

#### Ondas armónicas

Una solución monocromática del campo de desplazamientos puede escribirse como:

$$
u(x,t)=A_1 e^{i(\omega t-kx)} + A_2 e^{i(\omega t+kx)}
$$

donde:

- $\omega$ → [[Angular Frequency]]
- $k$ → [[Wavenumber]]

La velocidad de fase es:

$$
c=\frac{\omega}{k}
$$

Soluciones más generales pueden construirse mediante:

- [[Fourier Integral]]
- [[Wave Superposition]]

#### Importancia para métodos de ondas superficiales

Aunque esta sección describe ondas de cuerpo, su análisis es esencial para comprender los métodos de caracterización basados en [[Surface Waves]].

Las ondas superficiales pueden interpretarse como combinaciones de ondas de cuerpo que satisfacen condiciones de frontera en la superficie libre.

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

Las velocidades de propagación de ondas de cuerpo dependen de las propiedades elásticas del medio:

$$  
V_P=\sqrt{\frac{\lambda+2\mu}{\rho}},  
\qquad  
V_S=\sqrt{\frac{\mu}{\rho}}  
$$

De estas expresiones se deduce que:

$$  
V_P > V_S  
$$

porque las ondas P dependen de la rigidez volumétrica y de corte, mientras que las ondas S dependen únicamente de la rigidez de corte.

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

En suelos y depósitos saturados:

- $V_P$ no representa bien la rigidez del esqueleto del suelo
- $V_S$ es mucho más útil para caracterización geotécnica
- los métodos de ondas superficiales se centran principalmente en recuperar perfiles de $V_S$

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
- $k_\chi$ es el vector número de onda
- $\chi = P, S$ indica si se trata de onda longitudinal o transversal

Esta expresión representa una onda armónica propagándose en direcciones opuestas.
![[Pasted image 20260316140712.png]]
### Geometría de fase

El vector número de onda es normal a los planos de fase constante, definidos por:

$$  
k_\chi \cdot x = \text{constante}  
$$

La velocidad de fase de la onda monocromática es:

$$  
c = \frac{\omega}{|k|}  
$$

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

Cuando una onda incide sobre una interfaz entre medios elásticos:

- una onda P incidente genera ondas P y SV reflejadas y transmitidas
- una onda SV incidente genera ondas P y SV reflejadas y transmitidas
- una onda SH incidente genera únicamente ondas SH reflejadas y transmitidas
    
![[Pasted image 20260316141217.png]]
Este fenómeno de [[Mode Conversion]] es central para entender:

- propagación en [[Layered Media]]
- formación de [[Rayleigh Waves]]
- existencia de [[Love Waves]]

### Caso unidimensional

Para propagación 1D, la solución armónica se simplifica a:

$$  
u(x,t)=A_1 e^{i(\omega t-kx)} + A_2 e^{i(\omega t+kx)}  
$$

y el número de onda queda definido por:

$$  
k = \frac{\omega}{V}  
$$

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

#### Longitud de onda

La longitud de onda es la distancia entre dos puntos con la misma fase:

$$  
\lambda = \frac{2\pi}{k}  
$$

Combinando con la definición de velocidad de fase:

$$  
\lambda = \frac{V}{f}  
$$
![[Pasted image 20260316141321.png]]
Esta relación conecta directamente:

- velocidad de propagación
- frecuencia
- longitud de onda

### Importancia para métodos de ondas superficiales

Estas relaciones son fundamentales porque permiten conectar el comportamiento de ondas armónicas con la interpretación experimental.

En particular:

- la frecuencia controla la longitud de onda    
- la longitud de onda controla la profundidad efectiva de investigación
- la dependencia entre velocidad y frecuencia es la base de las curvas de dispersión

Por eso, estos parámetros serán esenciales en las secciones posteriores sobre:

- [[Rayleigh Waves]]
- [[Love Waves]]
- [[Dispersion Relation]]
- análisis de adquisición e inversión

## 2.2 Rayleigh Waves in Homogeneous Elastic Half-Spaces

### 2.2.1 Overview

Los continuos elásticos **homogéneos, isotrópicos y no acotados** solo permiten la propagación de ondas de cuerpo:

- [[P-waves]]
- [[S-Waves]]

Sin embargo, **la introducción de una frontera en el medio** permite la existencia de otro tipo de ondas llamadas **[[Surface Waves]]**, que se propagan **a lo largo de la superficie del medio** en lugar de propagarse a través de su interior.

Las **[[Rayleigh Waves]]** fueron predichas por primera vez por **Lord Rayleigh en 1885**.

Estas ondas aparecen como consecuencia de la **condición de esfuerzo nulo en la superficie libre** de un sólido elástico.

---

### Propagación superficial

A diferencia de las [[Body Waves]], las [[Rayleigh Waves]] presentan un patrón de radiación esencialmente **bidimensional (2D)**.
![[Pasted image 20260316143212.png]]
Esto implica que la energía se propaga principalmente:

- a lo largo de la superficie
- con muy poca propagación hacia el interior del medio.

Como consecuencia, las ondas superficiales presentan una **atenuación geométrica mucho menor** que las ondas de cuerpo.

---

### Atenuación geométrica

El decaimiento espacial de la amplitud depende del tipo de fuente.

Para un **medio elástico homogéneo semi-infinito**:

**Fuente lineal vertical**

- las [[Rayleigh Waves]] no presentan atenuación geométrica.

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

Esto implica que a distancias del orden de **una o dos longitudes de onda desde la fuente**, la contribución de las ondas de cuerpo se vuelve **despreciable** y el campo de ondas queda dominado por **[[Rayleigh Waves]]**.

Este fenómeno fue reconocido tempranamente en el contexto de [[Lamb’s Problem]], que estudia la generación de ondas por una carga aplicada en la superficie de un medio elástico.

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

Esta relación entre **longitud de onda y profundidad de penetración** es la base física de los métodos de caracterización del subsuelo mediante [[Surface Waves]].

En particular:

- frecuencias **bajas** (longitudes de onda grandes) investigan **mayores profundidades**
- frecuencias **altas** investigan **capas superficiales**

Este principio permite reconstruir perfiles de velocidad de corte del subsuelo mediante el análisis de la **[[Dispersion Relation]]** de [[Rayleigh Waves]].

### 2.2.2 Derivación mediante potenciales de onda elástica

La existencia de las [[Rayleigh Waves]] se demuestra formalmente mediante la descomposición de Helmholtz del campo de desplazamientos, aplicando condiciones de frontera en la superficie libre.

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

Cada potencial satisface su propia ecuación de onda:

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

La condición $\text{Re}(\alpha) > 0$ y $\text{Re}(\beta) > 0$ garantiza que las amplitudes **decaigan con la profundidad** — condición necesaria para que sean ondas superficiales y no ondas de cuerpo.

#### Condiciones de frontera en superficie libre

En $z = 0$ los esfuerzos normales y de corte deben ser nulos (superficie libre sin carga aplicada):

$$
\sigma_{zz}\big|_{z=0} = 0, \qquad \sigma_{xz}\big|_{z=0} = 0
$$

Aplicando estas dos condiciones al campo de desplazamientos derivado de los potenciales se obtiene un sistema lineal homogéneo en $A$ y $B$.

#### Ecuación secular de Rayleigh

Para que el sistema tenga solución no trivial, el determinante de la matriz de coeficientes debe ser cero. Esto conduce a la **ecuación secular de Rayleigh**:

$$
\left(2 - \frac{c_R^2}{V_S^2}\right)^2 = 4\sqrt{1 - \frac{c_R^2}{V_P^2}}\sqrt{1 - \frac{c_R^2}{V_S^2}}
$$

donde $c_R$ es la velocidad de fase de las ondas de Rayleigh.

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

- $c_R$ **no depende de la frecuencia** ni del número de onda
- la ecuación secular de Rayleigh no contiene $\omega$ ni $k$ de forma independiente, sino únicamente a través del cociente $c_R = \omega/k$
- por tanto, las ondas de Rayleigh en este medio son **no dispersivas**

La razón física de esta no-dispersividad es que el medio es homogéneo: no existe longitud de escala característica que introduzca un efecto de tamaño relativo. La onda de Rayleigh de cualquier frecuencia "ve" exactamente el mismo medio independientemente de su longitud de onda. En contraste, en un medio estratificado sí existe una longitud de escala natural (el espesor de las capas), y las ondas de diferente longitud de onda penetran profundidades diferentes y por tanto sienten medios distintos — esto es exactamente la dispersión geométrica.

Esta referencia tiene consecuencias directas para la caracterización del subsuelo: **la dispersión que observamos experimentalmente es evidencia directa de la heterogeneidad vertical del subsuelo**. Si un sitio tiene propiedades uniformes con la profundidad, la curva de dispersión es plana; si hay gradiente o capas con velocidades distintas, la curva tiene pendiente. Esto es lo que permite extraer información del perfil $V_S(z)$ a partir de la curva de dispersión medida con geófonos: la variación de velocidad de fase con la frecuencia mapea la variación de rigidez con la profundidad.

La no-dispersividad del semiespacio homogéneo sirve también como límite asintótico a alta y baja frecuencia en medios estratificados: cuando $\lambda \to 0$ (alta frecuencia), la onda "ve" solo la capa más superficial, y $c_R \to 0.92\,V_{S,\text{top}}$; cuando $\lambda \to \infty$ (baja frecuencia), la onda penetra todo el perfil y su velocidad tiende a $0.92\,V_{S,\text{semiespacio}}$.

---

## 2.3 Existence of Love Waves

Las [[Love Waves]] fueron predichas matemáticamente por A.E.H. Love en 1911. Son ondas transversales horizontalmente polarizadas (SH) que surgen de la interferencia constructiva de ondas SH en medios inhomogéneos estratificados.

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

donde $c_L = \omega/k$ es la velocidad de fase de las Love waves. Cuando esta condición se cumple, las ondas SH quedan **atrapadas** en la capa superior por reflexión total interna en la interfaz — la capa actúa como una **guía de ondas**. Si $V_{S2} \leq V_{S1}$, las Love waves no existen.

*(Fuente: Foti Ch. 2, Sec. 2.3, p. 60–61)*

---

### Relación de dispersión de Love (Foti Ec. 2.54)

La combinación de condiciones de frontera — esfuerzo nulo en $x_2 = 0$, continuidad de desplazamiento y esfuerzo en $x_2 = h$, y condición de radiación $u_3 \to 0$ para $x_2 \to \infty$ — conduce a la **ecuación de dispersión de Love** (Foti Ec. 2.54):

$$
\tan\!\left(\frac{\omega h}{V_{S1}}\sqrt{1 - \left(\frac{V_{S1}}{c}\right)^2}\right) - \frac{V_{S2}}{V_{S1}}\cdot\frac{\rho_2}{\rho_1}\cdot\frac{\sqrt{\left(\frac{V_{S2}}{V_{S1}}\right)^2 - \left(\frac{c}{V_{S1}}\right)^2}}{\sqrt{\left(\frac{c}{V_{S1}}\right)^2 - 1}} = 0
$$

donde $c = \omega/k = V_L$ es la velocidad de fase de la Love wave y $h$ es el espesor de la capa.

Esta ecuación es **trascendente y no tiene solución cerrada en general**. Sus propiedades clave:

- $c$ depende de $\omega$: las Love waves son **intrínsecamente dispersivas** en medios estratificados (contraste directo con Rayleigh en half-space homogéneo)
- En el límite de baja frecuencia: $c \to V_{S2}$ (domina el semiespacio)
- En el límite de alta frecuencia: $c \to V_{S1}$ (domina la capa superficial)
- La dispersión de Love es puramente geométrica: no requiere disipación

*(Fuente: Foti Ch. 2, Sec. 2.3, p. 63, Ec. 2.54)*

---

### Modos de Love y frecuencia de corte (Foti Ec. 2.55)

La relación de dispersión admite múltiples ramas (modos):

- **Modo fundamental** ($n = 1$): existe para **todas** las frecuencias
- **Modos superiores** ($n = 2, 3, \ldots$): existen solo por encima de una **frecuencia de corte**

La frecuencia angular de corte del $n$-ésimo modo es (Foti Ec. 2.55):

$$
\frac{\omega_c^n \cdot h}{V_{S1}} = \frac{\pi(n-1)}{\sqrt{1 - \left(\frac{V_{S1}}{V_{S2}}\right)^2}}, \qquad n = 1, 2, \ldots
$$

Esta dependencia frecuencial multimodal es la base de la [[Geometric Dispersion]] para Love waves.

*(Fuente: Foti Ch. 2, Sec. 2.3, p. 65, Ec. 2.55)*

![[Pasted image 20260317202522.png]]
---

## 2.4 Surface Waves in Vertically Inhomogeneous Media

### 2.4.1 Problema de autovalores asociado a ondas superficiales libres (Foti Ecs. 2.65–2.74)

Cuando $\lambda = \lambda(x_2)$, $\mu = \mu(x_2)$, $\rho = \rho(x_2)$, las ecuaciones de Navier se generalizan (Foti Ec. 2.56). La búsqueda de soluciones del tipo ondas superficiales conduce a dos **problemas de autovalores diferenciales** con operador $d/dx_2$.

#### Sistemas de EDOs de primer orden

Para **Love waves** (Foti Ec. 2.65):

$$
\frac{d}{dx_2}\begin{bmatrix}l_1\\l_2\end{bmatrix} = \begin{bmatrix}0 & \mu(x_2)^{-1}\\ k^2\mu(x_2)-\omega^2\rho(x_2) & 0\end{bmatrix}\begin{bmatrix}l_1\\l_2\end{bmatrix}
$$

Para **Rayleigh waves** (Foti Ec. 2.66), sistema de cuarto orden $d\mathbf{f}/dx_2 = A(x_2)\cdot\mathbf{f}(x_2)$ donde $\mathbf{f} = [r_1, r_2, r_3, r_4]^T$ contiene las funciones propias de desplazamiento ($r_1$, $r_2$) y esfuerzo ($r_3$, $r_4$).

#### Condiciones de contorno (Foti Ecs. 2.72–2.73)

Para **Love waves**: $l_2 = 0$ en $x_2 = 0$, y $l_1 \to 0$ para $x_2 \to \infty$

Para **Rayleigh waves**: $r_3 = r_4 = 0$ en $x_2 = 0$, y $r_1, r_2 \to 0$ para $x_2 \to \infty$

#### Ecuación de dispersión general (Foti Ec. 2.74)

Soluciones no triviales existen solo para autovalores $k_j = k_j(\omega)$, $j = 1, \ldots, M$. La relación implícita que los define es:

$$
\Phi_{L/R}[\lambda(x_2),\, \mu(x_2),\, \rho(x_2),\, k,\, \omega] = 0
$$

Esta es la ecuación de dispersión general: altamente no lineal, trascendente, sin solución cerrada.

#### Algoritmos numéricos (Foti Sec. 2.4.1.1, p. 72–74)

- **Thomson–Haskell (transfer matrix)**: construye $\Phi_{L/R}[\cdot]$ multiplicando matrices de capa; las raíces son los autovalores. Más común por su simplicidad, pero numéricamente inestable a alta frecuencia
- **Matriz de rigidez dinámica (Kausel–Roesset 1981)**: reemplaza las matrices de transferencia por matrices de rigidez de capa; más estable
- **Coeficientes de reflexión–transmisión (Kennett)**: algoritmo recursivo; modela explícitamente la interferencia constructiva entre modos

#### Ejemplo numérico (Foti Tabla 2.4 y Figs. 2.20–2.22)

La **Fig. 2.20** ilustra el comportamiento de $|\Phi_R[\cdot]|$ calculada con Thomson–Haskell en función del número de onda a $f = 50\,\text{Hz}$, para el sistema estratificado de la **Tabla 2.4**:

| Capa | Espesor (m) | $V_P$ (m/s) | $V_S$ (m/s) | $\rho$ (Mg/m³) |
|------|-------------|-------------|-------------|-----------------|
| 1 | 10 | 200 | 100 | 1.9 |
| 2 | 10 | 400 | 200 | 1.9 |
| 3 | 10 | 600 | 300 | 1.9 |
| Semiespacio | ∞ | 1000 | 500 | 1.9 |

La función oscila rápidamente con el número de onda (especialmente a alta frecuencia), lo que requiere técnicas robustas de *root-bracketing* con bisección para localizar confiablemente todas las raíces.

La **Fig. 2.21** muestra las curvas de dispersión modales (24 modos identificados) para este sistema: velocidad de fase Rayleigh vs. frecuencia. Cada curva corresponde a un autovalor de la Ec. 2.71. Los modos superiores tienen mayor velocidad de fase y mayor profundidad de penetración. Al aumentar la frecuencia, aparecen nuevos modos y las curvas se empaquetan más densamente.

La **Fig. 2.22** muestra los perfiles de profundidad de las eigenfunciones de desplazamiento $r_1$ (horizontal) y $r_2$ (vertical) a $f = 16\,\text{Hz}$ para los primeros 4 modos. El resultado clave es que **los modos superiores penetran más profundamente**, lo que fundamenta la posibilidad de invertir modos superiores para resolver estructuras a mayor profundidad.

*(Fuente: Foti Ch. 2, Sec. 2.4.1, pp. 65–76, Ecs. 2.56–2.74, Tabla 2.4, Figs. 2.20–2.22)*

---

### 2.4.2 Modos de propagación y superposición modal

En medios estratificados, tanto [[Rayleigh Waves]] como [[Love Waves]] presentan **múltiples modos de propagación**:

- modo fundamental: mayor amplitud en superficie, más fácil de identificar experimentalmente
- modos superiores: mayor profundidad de penetración; pueden dominar cuando hay fuertes contrastes de velocidad

El campo de ondas registrado por un arreglo de geófonos es en general una **superposición de modos** — ver [[Mode Superposition]].

> **Implicación crítica para la tesis**: en medios inversamente dispersivos, los modos superiores contribuyen de manera importante incluso a frecuencias bajas. Invertir la curva de dispersión aparente como si fuera del modo fundamental introduce errores sistemáticos en el perfil $V_S(z)$. Este es uno de los problemas más frecuentes en la práctica.

---

### 2.4.3 El problema de la fuente: Lamb's Problem

#### Solución en el campo lejano (Foti Ec. 2.75)

El [[Lamb's Problem]] describe la respuesta de un semiespacio elástico homogéneo a una carga puntual vertical armónica $F\,e^{i\omega t}$ en la superficie libre. El desplazamiento vertical de Rayleigh en **aproximación de campo lejano** es (Foti Ec. 2.75):

$$
u_2(r,\omega) = \frac{F\,e^{i\omega t}}{2i\mu}\cdot k_R\cdot\Psi(k_R)\cdot H_0^{(2)}(k_R r)
$$

donde $r = \sqrt{x_1^2 + x_3^2}$, $k_R = \omega/V_R$, y $H_0^{(2)}(\cdot)$ es la función de Hankel de segundo tipo y orden cero. Para $|k_R r| \gg 1$, la expansión asintótica muestra que la amplitud decae como $r^{-0.5}$ (frentes de onda cilíndricos).

Las ondas de cuerpo, en cambio, decaen como $r^{-2}$ en la superficie libre — mucho más rápido.

#### Umbral de campo cercano / campo lejano

El campo total se descompone en $\mathbf{u} = \mathbf{u}_B + \mathbf{u}_S$. En el **campo lejano**, la contribución de ondas de cuerpo es despreciable.

**Umbral cuantitativo** (Foti Sec. 2.4.2, p. 86): en medios *normalmente dispersivos*, los efectos de campo cercano son significativos hasta:

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

### 2.4.5 Velocidad de fase aparente (efectiva) de Rayleigh (Foti Sec. 2.4.2.4) ★

**Este es el concepto más crítico de la tesis**: lo que los geófonos miden no es la velocidad de fase de ningún modo individual, sino la **velocidad de fase aparente** o efectiva resultante de la superposición de todos los modos activos.

#### Definición (Foti Ec. 2.93)

A partir de la condición de fase constante del campo resultante, la velocidad de fase aparente es:

$$
V_l^{app}(r, x_2, \omega) = \frac{\omega}{\partial\psi_l(r, x_2, \omega)/\partial r}, \qquad l = r, 2
$$

Es una cantidad **local**: su valor depende de la posición del receptor $r$. Al variar con $\omega$ y $r$ define una **superficie de dispersión** $V_l^{app}(r, 0, \omega)$ en el plano $(\omega, r)$.

#### Expresión explícita en términos de autofunciones (Foti Ec. 2.95)

$$
V_r^{app}(r,x_2,\omega) = 2\omega\cdot\frac{\displaystyle\sum_{i=1}^{M}\sum_{j=1}^{M}\frac{r_1(x_2,k_i)\,r_1(x_2,k_j)\,r_2(0,k_i)\,r_2(0,k_j)\,\cos[r(k_i-k_j)]}{\left[(V_R)_i(U_R)_i(I_R)_i\right]\left[(V_R)_j(U_R)_j(I_R)_j\right]\sqrt{k_i k_j}}}{\displaystyle\sum_{n=1}^{M}\sum_{m=1}^{M}\frac{r_1(x_2,k_n)\,r_1(x_2,k_m)\,r_2(0,k_n)\,r_2(0,k_m)\,(k_n+k_m)\,\cos[r(k_n-k_m)]}{\left[(V_R)_n(U_R)_n(I_R)_n\right]\left[(V_R)_m(U_R)_m(I_R)_m\right]\sqrt{k_n k_m}}}
$$

donde $(V_R)_j$, $(U_R)_j$ y $(I_R)_j$ son la velocidad de fase, velocidad de grupo e integral de energía del $j$-ésimo modo.

#### Implicaciones para la inversión
![[Pasted image 20260318140813.png]]
- En medios **normalmente dispersivos**: la curva aparente está cerca del modo fundamental a frecuencias intermedias; la aproximación monomodal suele ser aceptable
- En medios **inversamente dispersivos**: la curva aparente diverge significativamente del modo fundamental desde frecuencias bajas (~8 Hz en los ejemplos de Foti) — invertirla como modo fundamental introduce errores severos en $V_S(z)$
- Lo que los métodos experimentales (MASW, f-k) extraen es $V^{app}$, no curvas modales; el proceso de inversión debe tener esto en cuenta

*(Fuente: Foti Ch. 2, Sec. 2.4.2.4, p. 90–95, Ecs. 2.93–2.95)*

---

## 2.5 Surface Waves in Vertically Inhomogeneous, Inelastic Continua

### 2.5.1 Motivación y marco constitutivo

Los suelos y rocas reales **no son elásticos perfectos**: parte de la energía sísmica se disipa como calor por deformación viscosa interna (rozamiento entre partículas, movimiento de fluido poral). Este fenómeno es relevante para el diseño sísmico porque controla la amplificación del movimiento del suelo: mayor amortiguamiento → menor amplificación en la frecuencia de resonancia del depósito.

Cuantitativamente, el amortiguamiento material se expresa mediante la **razón de amortiguamiento** $D_S$ (también escrita $D$ o $\xi$ en literatura de ingeniería sísmica), que representa la fracción de energía disipada por ciclo de deformación. Para suelos dentro del rango de deformación lineal cíclica (típicamente deformación de corte $\gamma < 10^{-5}$), los valores típicos son $D_S \approx 1\text{–}5\%$.

La **viscoelasticidad lineal** es el marco constitutivo más simple y físicamente consistente para describir este comportamiento. Se basa en cuatro hipótesis: (1) **pequeñas deformaciones** (linealización del tensor de deformación), (2) **invariancia temporal** (las propiedades del material no cambian con el tiempo), (3) **postulado de herencia** (el esfuerzo en el instante $t$ depende de toda la historia previa de deformación), y (4) **hipótesis de memoria débil** (la influencia del pasado remoto es despreciable, lo que garantiza la existencia de la integral de Boltzmann).

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

Las partes real e imaginaria del módulo complejo **no son independientes**. Están ligadas por las **relaciones de Kramers–Krönig** (Foti Ec. 2.99):

$$
G_{(1)}(\omega) = G_{(e)} + \frac{2}{\pi}\int_0^{\infty}\frac{G_{(2)}(\tau)\cdot\omega^2}{\tau\cdot(\omega^2-\tau^2)}\,d\tau
$$

donde $G_{(e)} = G(t \to \infty)$ es la respuesta de equilibrio.

Estas relaciones son consecuencia directa del **principio de causalidad física** — la respuesta no puede preceder a la excitación. En términos de parámetros físicos de propagación ($V_\chi(\omega)$ y $D_\chi(\omega)$), la restricción análoga es (Foti Ec. 2.130):

$$
V_\chi^2(\omega) + \omega^2\cdot\frac{4}{\pi}\int_0^{\infty}\frac{D_\chi(\tau)}{\tau\cdot(\tau^2-\omega^2)}\cdot V_\chi^2(\tau)\,d\tau = G_{(e)\chi}\cdot\frac{2(1+4D_\chi^2)}{1+\sqrt{1+4D_\chi^2}}
$$

**Implicación directa**: la velocidad de fase $V_\chi(\omega)$ y el amortiguamiento $D_\chi(\omega)$ de ondas en un suelo real **no pueden asignarse independientemente** — están restringidos por la Ec. 2.130. Esto implica que los materiales viscoelásticos son **inherentemente dispersivos**.

*(Fuente: Foti Ch. 2, Sec. 2.5.1–2.5.2, p. 100, 111, Ecs. 2.99, 2.130)*

---

### 2.5.4 Ondas viscoelásticas en medios homogéneos: principio de correspondencia

La analogía entre las ecuaciones de campo de la elasticidad y la viscoelasticidad en el dominio frecuencial constituye el **principio de correspondencia elástico–viscoelástico** (Foti Sec. 2.5.2):

> Las soluciones del problema viscoelástico en dominio frecuencial se obtienen reemplazando las constantes elásticas reales $\lambda$, $\mu$ por sus equivalentes complejos $G_S^*(\omega)$, $G_B^*(\omega)$ en las expresiones del caso elástico.

Esto hace que todas las fórmulas derivadas para medios elásticos (incluyendo la ecuación secular de Rayleigh) sean válidas en medios viscoelásticos, con $\lambda, \mu \in \mathbb{C}(\omega)$.

#### Velocidades complejas de ondas de cuerpo (Foti Ec. 2.118)

$$
V_P^*(\omega) = \sqrt{\frac{G_B^*(\omega) + \frac{4}{3}G_S^*(\omega)}{\rho}}, \qquad V_S^*(\omega) = \sqrt{\frac{G_S^*(\omega)}{\rho}}
$$

El número de onda complejo $k_\chi^* = \omega/V_\chi^* = k_\chi - i\alpha_\chi$ conduce a la solución armónica:

$$
u \propto e^{-\alpha_\chi x}\,e^{i(k_\chi x - \omega t)}
$$

donde $\alpha_\chi$ es el **coeficiente de atenuación espacial**.

#### Razón de amortiguamiento material (Foti Ec. 2.115)

$$
D_\chi(\omega) = \frac{G_{(2)\chi}}{2G_{(1)\chi}}, \qquad \chi = P, S
$$

Su relación con el factor de calidad: $Q_\chi(\omega) = 1/(2D_\chi(\omega))$.

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

**Consecuencia crítica**: la velocidad de fase $V_\chi(\omega)$ se ve afectada por $D$ solo en **segundo orden** — la disipación no afecta significativamente la curva de dispersión. Esto justifica el procedimiento estándar: inversión de dispersión primero (para $V_S$), inversión de atenuación después (para $D_S$), tratándolas como problemas desacoplados.

*(Fuente: Foti Ch. 2, Sec. 2.5.2, p. 110, Ec. 2.128)*

---

### 2.5.6 Rayleigh Eigenproblem en medios débilmente disipativos (Foti Ec. 2.133)

Aplicando principios variacionales de Love–Rayleigh bajo la hipótesis de disipación débil (Ecs. 2.128–2.129), se obtiene el resultado central de la sección (Foti Ec. 2.133):

$$
\begin{cases}
V_R(\omega) = V_R^e + \displaystyle\int_0^\infty V_S\frac{\partial V_R}{\partial V_S}\bigg|_{\omega,V_P}\!\!\left[1-\frac{V_S^{e2}}{V_S^2}\right]dx_2 + \int_0^\infty V_P\frac{\partial V_R}{\partial V_P}\bigg|_{\omega,V_S}\!\!\left[1-\frac{V_P^{e2}}{V_P^2}\right]dx_2\\[12pt]
\alpha_R(\omega) = \dfrac{\omega}{[V_R(\omega)]^2}\left\{\displaystyle\int_0^\infty V_S D_S\frac{\partial V_R}{\partial V_S}\bigg|_{\omega,V_P}dx_2 + \int_0^\infty V_P D_P\frac{\partial V_R}{\partial V_P}\bigg|_{\omega,V_S}dx_2\right\}
\end{cases}
$$

donde $V_R^e$ es la velocidad de Rayleigh del medio elástico asociado ($D=0$), y las derivadas $\partial V_R/\partial V_S$, $\partial V_R/\partial V_P$ son las **sensitividades** de la velocidad de Rayleigh respecto al perfil de velocidades.

#### Consecuencias fundamentales

1. **Desacopla** los dos problemas inversos:
   - Primero: invertir $V_R(\omega)$ para obtener $V_S(x_2)$ → problema **altamente no lineal**
   - Luego: invertir $\alpha_R(\omega)$ para obtener $D_S(x_2)$ dado $V_S$ → problema **lineal**

2. $V_R(\omega)$ y $\alpha_R(\omega)$ se calculan a partir de la solución del problema de autovalores **elástico** — no se requiere resolver el problema viscoelástico completo

3. Validez: solo para $D \leq 5\%$ — dentro del rango típico de geomateriales

> **Implicación para la tesis**: si el objetivo es el perfil $V_S$, la disipación es de segundo orden y puede ignorarse en la curva de dispersión. Si el objetivo incluye el perfil $D_S$, se requiere medir amplitudes con calibración cuidadosa — exigencia instrumental significativamente mayor.

*(Fuente: Foti Ch. 2, Sec. 2.5.3, p. 113–119, Ec. 2.133)*

---

## Fuentes

- PDF: Sebastiano Foti Chapter 2 (book pages 37–120)
- Secciones cubiertas: 2.1–2.5