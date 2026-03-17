# Linear Wave Propagation in Vertically Inhomogeneous Continua

## Introducción

Este capítulo desarrolla la teoría de propagación de ondas superficiales en medios:

- elásticos lineales
- viscoelásticos lineales

con el objetivo de establecer la base física para el **modelado directo (forward modeling)** utilizado en métodos de caracterización del subsuelo mediante ondas superficiales.

Aunque el desarrollo teórico incluye tanto [[Love Waves]] como [[Rayleigh Waves]], el capítulo se enfoca principalmente en **Rayleigh waves**, debido a su mayor relevancia en aplicaciones prácticas de:

- exploración geofísica
- ingeniería geotécnica
- caracterización sísmica de sitio

Las Rayleigh waves son particularmente importantes porque dominan el campo de ondas registrado por geófonos en mediciones de superficie y contienen información directa sobre el perfil de velocidades de [[S-Waves]].

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

---

## Fuente

- PDF: Sebastiano Foti Chapter 2
- sección: 2.1.3 Body waves in unbounded homogeneous elastic media

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

### Relación con el coeficiente de Poisson

El cociente entre velocidades puede expresarse en función del coeficiente de Poisson $\nu$:

# $$  
\frac{V_P}{V_S}

\sqrt{\frac{2(1-\nu)}{1-2\nu}}  
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

La velocidad de Rayleigh $c_R$ depende únicamente de $V_S$ y del coeficiente de Poisson $\nu$ (que determina $V_P/V_S$).

Para $\nu = 0.25$ (valor típico para muchas rocas):

$$
c_R \approx 0.9194 \, V_S
$$

En general, $c_R$ varía entre aproximadamente $0.87\,V_S$ y $0.96\,V_S$ para el rango de $\nu$ físicamente admisible ($0 \leq \nu < 0.5$).

> **Implicación crítica para la tesis**: $c_R \approx 0.92\,V_S$ en condiciones típicas. Los geófonos miden la velocidad de Rayleigh. La conversión a $V_S$ requiere conocer $\nu$ o asumirlo, lo que introduce incertidumbre en el perfil final.

---

### 2.2.3 Movimiento de partícula

El campo de desplazamientos asociado a las [[Rayleigh Waves]] en superficie presenta las siguientes características:

- **Trayectoria elíptica** en el plano vertical de propagación (plano $x$–$z$)
- En superficie: órbita **retrógrada** (sentido antihorario para propagación en $+x$)
- A una profundidad crítica de aproximadamente $0.2\lambda$: el movimiento cambia a **progrado** (sentido horario)
- El eje vertical de la elipse es mayor que el horizontal en superficie

Esta polarización elíptica en el plano vertical explica por qué los **geófonos verticales** son los sensores preferidos para capturar [[Rayleigh Waves]]: detectan directamente la componente dominante del movimiento.

> **Nota**: Los geófonos horizontales detectan la componente horizontal de la elipse, que es de menor amplitud en superficie. Para [[Love Waves]], en cambio, se requieren geófonos horizontales orientados transversalmente.

---

### 2.2.4 No-dispersividad en el half-space homogéneo

Un resultado central del capítulo es que en un [[Elastic Half Space]] homogéneo:

- $c_R$ **no depende de la frecuencia** ni del número de onda
- la ecuación secular de Rayleigh no contiene $\omega$ ni $k$ de forma independiente, sino únicamente a través del cociente $c_R = \omega/k$
- por tanto, las ondas de Rayleigh en este medio son **no dispersivas**

Esto establece la referencia fundamental: **la dispersión que observamos experimentalmente es evidencia directa de la heterogeneidad del subsuelo**.

---

## 2.3 Love Waves in Layered Media

### 2.3.1 Condición de existencia

Las [[Love Waves]] **no pueden existir en un semiespacio homogéneo**. Requieren al menos una estructura del tipo:
```text
capa superficial (V_S1 < V_S2)
────────────────────────────────
semiespacio inferior (V_S2)
```

La condición física necesaria es:

$$
V_{S1} < c_L < V_{S2}
$$

donde $c_L$ es la velocidad de fase de las Love waves.

Cuando esta condición se cumple, las ondas SH quedan **atrapadas** en la capa superior por reflexión total interna en la interfaz — es decir, la capa actúa como una **guía de ondas**.

### 2.3.2 Relación de dispersión de Love

La condición de frontera en la superficie libre ($z = 0$) y en la interfaz ($z = H$) conduce a la relación de dispersión de Love:

$$
\tan\left(\beta_1 H\right) = \frac{\mu_2 \beta_2}{\mu_1 \beta_1}
$$

donde:

$$
\beta_1 = \sqrt{\frac{\omega^2}{V_{S1}^2} - k^2}, \qquad \beta_2 = \sqrt{k^2 - \frac{\omega^2}{V_{S2}^2}}
$$

y $\mu_1$, $\mu_2$ son los módulos de corte de la capa y del semiespacio respectivamente.

A diferencia de la ecuación secular de Rayleigh en el half-space homogéneo, esta relación **sí contiene $\omega$ y $k$ de forma separada**, lo que confirma que las Love waves son intrínsecamente **dispersivas** en medios estratificados.

### 2.3.3 Modos de Love

La relación de dispersión de Love admite múltiples soluciones:

- **Modo fundamental** (modo 0): existe para todas las frecuencias
- **Modos superiores** (modo 1, 2, ...): cada uno tiene una frecuencia de corte mínima

A bajas frecuencias, la velocidad de fase del modo fundamental se aproxima a $V_{S2}$ (el semiespacio rígido domina). A altas frecuencias, se aproxima a $V_{S1}$ (la capa superficial domina).

Esta dependencia frecuencial es la base de la [[Geometric Dispersion]] para Love waves.

---

## 2.4 Surface Waves in Vertically Inhomogeneous Media

### 2.4.1 Extensión al caso general

Cuando las propiedades mecánicas varían continuamente o en capas múltiples con la profundidad, la ecuación secular de Rayleigh ya no tiene una solución analítica cerrada.

El problema debe resolverse **numéricamente**, lo que constituye el **problema directo (forward problem)** de los métodos de ondas superficiales.

Los algoritmos más utilizados son:

- **Método de la matriz de transferencia** (Thomson-Haskell): propaga condiciones de frontera capa por capa
- **Método de la matriz de rigidez global**: más estable numéricamente para medios con alta impedancia

### 2.4.2 Modos de propagación

En medios estratificados, tanto [[Rayleigh Waves]] como [[Love Waves]] presentan **múltiples modos de propagación**:

- modo fundamental: mayor amplitud, más fácil de identificar experimentalmente
- modos superiores: pueden contribuir significativamente cuando hay fuertes contrastes de velocidad

El campo de ondas registrado por un arreglo de geófonos es en general una **superposición de modos** — concepto central en [[Mode Superposition]].

> **Implicación para el diseño experimental**: si solo se extrae e invierte el modo fundamental asumiendo que domina el campo medido, pero modos superiores tienen contribución significativa, el perfil $V_S$ resultante puede ser erróneo. Esto es una fuente de error no siempre controlada.

### 2.4.3 Lamb's Problem revisitado

El [[Lamb's Problem]] describe la respuesta de un semiespacio elástico a una carga puntual en la superficie. Su solución muestra que:

- a distancias suficientemente grandes de la fuente, el campo está **dominado por ondas de Rayleigh**
- las ondas de cuerpo decaen más rápido y quedan en segundo plano
- la energía superficial se distribuye como un paquete de ondas con dispersión observable

Este resultado justifica por qué en arreglos de geófonos con fuente activa, si los receptores están ubicados a distancia mínima adecuada de la fuente, el campo medido es mayormente de Rayleigh.

---

## 2.5 Wave Propagation in Dissipative Media

### 2.5.1 Motivación

Los suelos y rocas reales **no son elásticos perfectos**: parte de la energía sísmica se convierte en calor durante la propagación. Ignorar este fenómeno conduce a modelos que sobreestiman las amplitudes a distancia y no permiten caracterizar el amortiguamiento del material.

### 2.5.2 Modelos viscoelásticos

La disipación se modela mediante el concepto de [[Viscoelastic Media]]. Los modelos más utilizados en geofísica son:

- **Modelo de Kelvin-Voigt**: esfuerzo proporcional a deformación más velocidad de deformación
- **Modelo de Maxwell**: elemento elástico en serie con elemento viscoso
- **Modelo de sólido estándar lineal**: combinación que reproduce mejor el comportamiento de geomateriales

En todos ellos, las constantes de Lamé $\lambda$ y $\mu$ se reemplazan por módulos **complejos** que dependen de la frecuencia:

$$
\tilde{\mu}(\omega) = \mu_R(\omega) + i\,\mu_I(\omega)
$$

### 2.5.3 Principio de correspondencia elástico-viscoelástico

El resultado fundamental que permite extender la teoría elástica a medios disipativos es el **principio de correspondencia**:

> Las soluciones del problema viscoelástico se obtienen reemplazando las constantes elásticas reales por sus equivalentes complejos dependientes de la frecuencia en las expresiones del caso elástico.

Esto implica que todas las fórmulas derivadas para medios elásticos (incluyendo la ecuación secular de Rayleigh) son válidas en medios viscoelásticos, simplemente haciendo $\lambda, \mu \in \mathbb{C}(\omega)$.

### 2.5.4 Número de onda complejo y atenuación

En un medio disipativo, el número de onda se vuelve complejo:

$$
\tilde{k} = k_R + i\,k_I
$$

La solución armónica toma la forma:

$$
u \propto e^{-k_I x} \, e^{i(k_R x - \omega t)}
$$

donde:

- $k_R$ → controla la fase (velocidad de fase: $c = \omega/k_R$)
- $k_I$ → controla la atenuación espacial de la amplitud

El **factor de calidad** $Q$ (o su inverso, el **material damping ratio** $D = 1/(2Q)$) cuantifica la disipación:

$$
D = \frac{k_I}{2k_R} = \frac{1}{2Q}
$$

### 2.5.5 Rayleigh Eigenproblem en medios disipativos

La extensión de las [[Rayleigh Waves]] a medios viscoelásticos verticalmente heterogéneos se formula como el [[Rayleigh Eigenproblem]] con coeficientes complejos.

Para el caso de **amortiguamiento débil** ($D \ll 1$, típico en suelos: $D \sim 1\text{–}10\%$), se aplica una perturbación de primer orden alrededor de la solución elástica.

El resultado es que:

- la velocidad de fase se ve levemente afectada por el amortiguamiento (corrección de segundo orden en $D$)
- la atenuación espacial es directamente proporcional a $D$

Esto justifica el enfoque estándar en geofísica: **primero caracterizar el perfil de velocidades $V_S$ desde la curva de dispersión, luego caracterizar el perfil de $D$ desde la curva de atenuación**.

> **Implicación para la tesis**: si el objetivo es solo el perfil $V_S$, ignorar la disipación introduce errores menores en la velocidad de fase (segundo orden en $D$). Si el objetivo es también el perfil de amortiguamiento, se requiere medir amplitudes con cuidado — lo que es significativamente más exigente instrumentalmente.

---

## Fuentes

- PDF: Sebastiano Foti Chapter 2
- Secciones: 2.2, 2.3, 2.4, 2.5
- Conceptos relacionados: [[Elastic Wave Potentials]], [[Rayleigh Eigenproblem]], [[Love Waves]], [[Layered Media]], [[Viscoelastic Media]], [[Mode Superposition]], [[Lamb's Problem]], [[Attenuation]]