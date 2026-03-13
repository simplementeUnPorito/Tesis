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

# Estructura del capítulo

El capítulo se divide en cinco secciones principales.

---

## 2.1 Basic notions of wave propagation

Esta sección introduce los fundamentos de propagación de ondas en medios continuos.

Primero se describen dos clases fundamentales de movimiento ondulatorio:

- **ondas hiperbólicas**
- **ondas dispersivas**

Posteriormente se revisan:

- las ecuaciones de movimiento en sólidos elásticos
- la propagación de ondas de cuerpo en medios:
  - homogéneos
  - isotrópicos
  - elásticos lineales

Esto permite introducir parámetros fundamentales asociados a las ondas, como:

- número de onda
- frecuencia
- [[Phase Velocity]]
- [[Group Velocity]]

En este contexto aparecen las ondas de cuerpo:

- [[P-waves]]
- [[S-Waves]]

También se introduce el concepto de **ondas armónicas**, que se describen mediante soluciones de la forma:

$$
\phi(x,t) = A e^{i(kx-\omega t)}
$$

La relación funcional entre frecuencia y número de onda constituye la [[Relación de Dispersión]], concepto fundamental para describir ondas dispersivas.

---

## 2.2 Rayleigh waves in homogeneous elastic continua

En esta sección se demuestra la existencia de [[Rayleigh Waves]] propagándose en un medio elástico homogéneo semi-infinito.

El desarrollo teórico se realiza utilizando el método de [[Elastic Wave Potentials]].

El resultado principal es la obtención de la **ecuación de dispersión de Rayleigh**, que relaciona:

- propiedades elásticas del medio
- velocidad de propagación de la onda

Este resultado constituye la base teórica de los métodos modernos de caracterización de sitio mediante ondas superficiales.

---

## 2.3 Love waves in layered media

Esta sección analiza las condiciones necesarias para la existencia de [[Love Waves]].

Las Love waves aparecen cuando existe la siguiente estructura del subsuelo:
```
capa elástica
sobre
semi-espacio elástico
```

Se estudian:

- las condiciones de guiado de ondas
- la [[Relación de Dispersión]]
- la comparación con [[Rayleigh Waves]]

Una diferencia fundamental es que las Love waves presentan propiedades **dispersivas** cuando el medio es estratificado, fenómeno asociado a la [[Dispersión Geométrica]].

---

## 2.4 Surface waves in vertically inhomogeneous media

Esta sección extiende el análisis a medios donde las propiedades mecánicas varían con la profundidad.

Se analizan:

- propagación de [[Rayleigh Waves]]
- propagación de [[Love Waves]]
- medios estratificados

Se introducen conceptos clave como:

- [[Mode Superposition]]
- velocidad de fase efectiva ([[Phase Velocity]])

También se revisita el [[Lamb’s Problem]], que describe la generación de ondas superficiales por una fuente puntual aplicada sobre la superficie libre del medio.

Este problema corresponde a la resolución de un **problema de contorno no homogéneo** asociado a la generación de ondas.

---

## 2.5 Wave propagation in dissipative media

La última sección introduce la propagación de ondas en **medios disipativos**.

Se discuten:

- modelos constitutivos de [[Viscoelastic Media]]
- mecanismos de [[Attenuation]] de ondas

Utilizando el **principio de correspondencia elastic-viscoelastic**, se obtienen las propiedades de propagación de ondas de cuerpo en medios viscoelásticos.

Posteriormente se analiza la propagación de ondas superficiales en medios:

- viscoelásticos
- verticalmente heterogéneos

La atención se centra en la resolución del [[Rayleigh Eigenproblem]] en medios débilmente disipativos.

Este resultado constituye la base teórica de muchos procedimientos utilizados en geofísica para modelar la propagación de ondas superficiales en medios reales, donde la disipación de energía no puede despreciarse.

---
# 2.1.1 Two Categories of Wave Motion

## Definición general de onda

Una **[[Wave]]** puede definirse como cualquier perturbación reconocible que se transfiere de una parte de un medio a otra con una velocidad de propagación identificable. Durante su propagación la perturbación puede:

- deformarse
- atenuarse
- cambiar su velocidad    

mientras la señal siga siendo identificable. 

---

# Clasificación fundamental del movimiento ondulatorio

Un criterio fundamental para clasificar ondas es distinguir entre:

- **[[Hyperbolic Waves]]**
- **[[Dispersive Waves]]**

Esta clasificación sigue siendo válida incluso cuando se restringe el análisis a **[[Linear Waves]]**. 

---

# [[Hyperbolic Waves]]

Las **[[Hyperbolic Waves]]** están descritas por **[[Hyperbolic Partial Differential Equations]]**.

Representan el caso más simple de propagación ondulatoria.

Un ejemplo clásico es la **[[1D Wave Equation]]**:

$$  
\frac{\partial^2 \phi}{\partial x^2} = \frac{1}{c_0^2}\frac{\partial^2 \phi}{\partial t^2}  
$$

- $\phi(x,t)$ : campo de la onda
    
- $x$ : coordenada espacial
    
- $t$ : tiempo
    
- $c_0$ : [[Phase Velocity]]
    


---

# [[d’Alembert Solution]]

La solución general de esta ecuación es la **[[d’Alembert Solution]]**:

$$  
\phi(x,t)=f(x-c_0t)+g(x+c_0t)  
$$

Esto representa la **[[Wave Superposition]]** de dos ondas:

- \(f(x-c_0t)\) → onda propagándose hacia la derecha
    
- \(g(x+c_0t)\) → onda propagándose hacia la izquierda
    

ambas con velocidad **$c_0$**. 

---

![[Pasted image 20260311151531.png]]
---

# Propiedad clave de las ondas hiperbólicas

Las **[[Hyperbolic Waves]]** presentan una propiedad fundamental:

**no se distorsionan durante la propagación.**

Esto ocurre porque:

- la velocidad de propagación **no depende de la frecuencia**
- todos los números de onda viajan con la misma **[[Phase Velocity]]**

$$  
c = c_0  
$$

Por lo tanto, la forma de la señal se conserva mientras se desplaza por el medio. 

---

# [[Dispersive Waves]]

Las **[[Dispersive Waves]]** presentan un comportamiento diferente.

Se caracterizan porque la **[[Angular Frequency]]** depende del **[[Wavenumber]]**:

$$  
\phi(x,t)=A e^{i[kx-\omega(k)t]}  
$$

- $A$ : amplitud
- $k$ : [[Wavenumber]]
- $\omega(k)$ : [[Angular Frequency]] dependiente de \(k\)
    


---

# [[Phase Velocity]]

La **[[Phase Velocity]]** corresponde a la velocidad de propagación de un punto de fase constante:

$$  
kx-\omega(k)t=const  
$$

lo que conduce a

$$  
c=\frac{\omega(k)}{k}  
$$

Si $\omega(k)$ depende de $k$, entonces la velocidad de fase **no es constante**. 

---

# Consecuencia física de la dispersión

Cuando distintas componentes espectrales viajan con diferentes velocidades:

- cada frecuencia se propaga a una velocidad distinta
- las señales con múltiples frecuencias cambian de forma

Este fenómeno se denomina **[[Wave Dispersion]]**.

---

![[Pasted image 20260311152029.png]]


# Representación general de soluciones dispersivas

La solución general de una ecuación de onda dispersiva puede expresarse mediante una **[[Fourier Integral]]**:

$$  
\phi(x,t)=\frac{1}{2\pi}\int_{-\infty}^{\infty}A(k)e^{i[kx-\omega(k)t]}dk  
$$

Esto representa una **[[Wave Superposition]]** de ondas monocromáticas.

Cada componente:

- tiene su propio [[Wavenumber]]
- tiene su propia [[Phase Velocity]]



---

# Ejemplo físico: [[Water Waves]]

Un ejemplo clásico de dispersión ocurre en **[[Surface Water Waves]]**, donde la **[[Dispersion Relation]]** depende de la profundidad del agua.

Tres aproximaciones típicas son:

| Régimen                | Relación de dispersión      |
| ---------------------- | --------------------------- |
| Agua profunda          | $\omega=\sqrt{gk}$          |
| Agua somera            | $\omega=k\sqrt{gh}$         |
| Profundidad intermedia | $\omega=\sqrt{gk\tanh(kh)}$ |



---

![[Pasted image 20260311154523.png]]
---

# Intersección entre ondas hiperbólicas y dispersivas

Las categorías **no son mutuamente excluyentes**.

Existen ondas que:

- son soluciones de **[[Hyperbolic Partial Differential Equations]]**
- pero presentan **[[Wave Dispersion]]**

Ejemplos relevantes:

- **[[Body Waves]] en medios elásticos homogéneos** → no dispersivas
- **[[Body Waves]] en medios disipativos o porosos** → dispersivas

fileciteturn1file8L59-L63

---

# Tipos de dispersión

Es importante distinguir entre:

### [[Material Dispersion]]

Originada por las **propiedades constitutivas del medio**.

Ejemplo:

- [[Viscoelastic Media]]
- [[Porous Media]]

---

### [[Geometric Dispersion]]

Aparece cuando el medio es **[[Vertically Inhomogeneous Media]]** o estratificado.

Consecuencia:

- la [[Phase Velocity]] depende de la frecuencia
- aparecen **[[Surface Wave Modes]]** múltiples



---

# Implicación para [[Surface Waves]]

Un resultado importante discutido posteriormente en el capítulo es que:

- las **[[Rayleigh Waves]] en un [[Elastic Half Space]] homogéneo** son **no dispersivas**

pero

- se vuelven **dispersivas cuando el medio es [[Layered Media]]**.



---
# Group Velocity

## Definición

La **velocidad de grupo** describe la velocidad a la que se propaga la **envolvente** de un paquete de ondas en un medio dispersivo.

$$  
c_g = \frac{d\omega}{dk}  
$$

Si la velocidad de fase es

$$  
c_0 = \frac{\omega}{k}  
$$

entonces también puede escribirse como

$$  
c_g = c_0 + k\frac{dc_0}{dk}  
$$
![[Pasted image 20260311155937.png]]
## Intuición física

Si se superponen dos ondas de frecuencias y números de onda muy cercanos, aparece una oscilación rápida interna y una envolvente lenta que agrupa la energía visible de la señal.

- la **onda portadora** se mueve con [[Phase Velocity]]
    
- la **envolvente** se mueve con **group velocity**
    

En un medio dispersivo, ambas velocidades no coinciden en general.

## Desarrollo conceptual

La idea surge naturalmente al estudiar [[Dispersive Waves]]. Si se considera la superposición de dos ondas monocromáticas de amplitud igual:

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

Esta expresión muestra explícitamente:

- una portadora senoidal de número de onda medio $k_m$ y frecuencia media $\omega_m$
    
- una envolvente moduladora que se desplaza con velocidad $\Delta\omega/\Delta k$
    

Al tomar el límite para $\Delta k \to 0$ se obtiene:

$$  
c_g = \lim_{\Delta k \to 0}\frac{\Delta \omega}{\Delta k}=\frac{d\omega}{dk}  
$$

## Interpretación física

La velocidad de grupo puede interpretarse como la velocidad a la que se propaga la modulación de un paquete de ondas. En medios dispersivos, esto también se asocia con la propagación de energía de la perturbación.

Esto implica que:

- si $c_0 > c_g$, la portadora parece avanzar desde la parte trasera del grupo hacia el frente
    
- si $c_0 < c_g$, la portadora parece desplazarse desde el frente hacia atrás
    
![[Pasted image 20260311155917.png]]
## Aplicación a geófonos

En arreglos de geófonos no se registra una onda monocromática ideal, sino paquetes de ondas con contenido espectral finito. Por eso, la velocidad de grupo tiene impacto directo en cómo llega la energía al arreglo.

Impacto práctico:

- controla el avance de la envolvente observable en el registro
    
- afecta la localización temporal de máximos de energía
    
- influye en la interpretación de señales dispersivas de [[Surface Waves]], [[Rayleigh Waves]] y [[Love Waves]]
    
- ayuda a distinguir entre propagación de fase y propagación efectiva del paquete registrado
    

## Implicaciones para el diseño experimental

- El espaciamiento entre geófonos debe permitir resolver el desplazamiento de la envolvente.
    
- El largo total del arreglo debe ser suficiente para observar la dispersión del paquete.
    
- El ancho de banda de adquisición condiciona qué tan bien puede estimarse $d\omega/dk$.
    
- Confundir [[Phase Velocity]] con velocidad de transporte de energía lleva a interpretaciones físicas erróneas.
    
# Body Waves in Unbounded Homogeneous Elastic Media

Esta sección introduce el modelo fundamental de propagación de ondas en medios elásticos continuos.

A partir de las ecuaciones de movimiento de la elastodinámica lineal se demuestra la existencia de dos tipos fundamentales de ondas de cuerpo:

- [[P-waves]]
- [[S-Waves]]

Estas ondas constituyen los modos básicos de propagación en sólidos elásticos y sirven como base física para la formación de [[Surface Waves]].

---

# Marco físico

El modelo considera un medio continuo con las siguientes hipótesis:

- medio **elástico lineal**
- medio **isotrópico**
- **deformaciones pequeñas**
- medio **homogéneo**
- dominio **no acotado**

Bajo estas hipótesis el comportamiento mecánico del medio puede describirse mediante las ecuaciones de la [[Linear Waves]] en medios elásticos.

---

# Campo de desplazamiento

La variable fundamental es el **campo de desplazamiento**

$$
u(x,t)
$$

donde:

- $x$ → posición espacial
- $t$ → tiempo

Este campo describe el desplazamiento de cada punto material del continuo respecto a su posición de equilibrio.

Las perturbaciones del campo de desplazamiento generan **deformaciones internas** del material.

---

# Tensor de deformación

Las deformaciones se describen mediante el [[Strain Tensor]].

Para deformaciones pequeñas:

$$
\varepsilon =
\frac{1}{2}
(\nabla u + (\nabla u)^T)
$$

Este tensor mide **cómo cambian las distancias entre puntos vecinos del medio**.

Componentes:

- términos diagonales → **deformaciones normales**
- términos fuera de diagonal → **deformaciones de corte**

---

# Tensor de esfuerzos

Las fuerzas internas del medio se describen mediante el [[Stress Tensor]].

El tensor de Cauchy:

$$
\sigma
$$

es un tensor $3\times3$ cuyos elementos representan **fuerzas por unidad de área** actuando en planos internos del material.

Cada columna del tensor puede interpretarse como el **vector de tracción** aplicado sobre una cara del volumen diferencial.

---

# Fuerzas internas en el continuo

Las fuerzas internas que actúan sobre un volumen diferencial se obtienen mediante la **divergencia del tensor de esfuerzos**:

$$
\nabla \cdot \sigma
$$

Este término representa la **densidad de fuerza interna (fuerza por unidad de volumen)**.

Aplicando el principio de [[d’Alembert Solution]] al continuo se obtiene la ecuación de movimiento:

$$
\nabla \cdot \sigma =
\rho \frac{\partial^2 u}{\partial t^2}
$$

donde:

- $\rho$ → densidad
- $\partial^2 u / \partial t^2$ → aceleración

Esta ecuación es la versión continua de la ley de Newton.

---

# Relación constitutiva (ley de Hooke)

Para un material elástico isotrópico el esfuerzo está relacionado con la deformación mediante:

$$
\sigma =
\lambda\,tr(\varepsilon)\,I
+
2\mu\,\varepsilon
$$

donde:

- $\lambda, \mu$ → constantes de Lamé
- $I$ → tensor identidad
- $tr(\varepsilon)$ → traza del tensor de deformación

La traza del tensor de deformación:

$$
tr(\varepsilon) =
\varepsilon_{11} + \varepsilon_{22} + \varepsilon_{33}
$$

representa el **cambio volumétrico relativo del material**.

Por lo tanto:

- término $ \lambda tr(\varepsilon)I $ → **deformación volumétrica**
- término $ 2\mu\varepsilon $ → **deformación de corte**

Esta separación física es la clave para entender la existencia de dos tipos de ondas.

---

# Ecuaciones de Navier

Sustituyendo la ley de Hooke en la ecuación de movimiento se obtiene:

$$
\mu \nabla^2 u +
(\lambda + \mu)\nabla(\nabla \cdot u)
=
\rho \frac{\partial^2 u}{\partial t^2}
$$

Estas ecuaciones se conocen como **ecuaciones de Navier**.

Matemáticamente constituyen un sistema de [[Hyperbolic Partial Differential Equations]].

---

# Descomposición del campo de desplazamiento

El campo de desplazamiento puede descomponerse mediante la **descomposición de Helmholtz**:

- componente **irrotacional**
- componente **rotacional**

Esto implica:

- el término $\nabla\cdot u$ describe **deformación volumétrica**
- el término $\nabla\times u$ describe **deformación de corte**

Como consecuencia, el sistema admite dos tipos independientes de ondas:

- [[P-waves]] → asociadas a $\nabla\cdot u$
- [[S-Waves]] → asociadas a $\nabla\times u$

---

# Velocidades de propagación

Las velocidades de propagación dependen de las propiedades elásticas del material.

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

Estas velocidades corresponden a la [[Phase Velocity]] de las ondas de cuerpo.

En medios homogéneos las ondas son **no dispersivas**, por lo que:

[[Group Velocity]] = [[Phase Velocity]].

---

# Polarización de ondas S

Las [[S-Waves]] poseen dos posibles polarizaciones:

- **SV** → polarización vertical
- **SH** → polarización horizontal

Esto es fundamental para la clasificación de las [[Surface Waves]]:

- [[Rayleigh Waves]] → acoplamiento **P + SV**
- [[Love Waves]] → ondas **SH guiadas**

---

# Conversión de modos

Cuando una onda incide sobre una interfaz entre medios elásticos ocurre **conversión de modos**.

- **onda P incidente**
  → ondas reflejadas y transmitidas **P y SV**

- **onda SV incidente**
  → ondas reflejadas y transmitidas **P y SV**

- **onda SH incidente**
  → solo ondas **SH**

Este fenómeno es esencial para comprender la propagación en:

- [[Layered Media]]
- [[Vertically Inhomogeneous Media]]

y la generación de [[Surface Waves]].

---

# Ondas armónicas

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

---

# Importancia para métodos de ondas superficiales

Aunque esta sección describe **ondas de cuerpo**, su análisis es esencial para comprender los métodos de caracterización basados en [[Surface Waves]].

Las ondas superficiales pueden interpretarse como combinaciones de ondas de cuerpo que satisfacen condiciones de frontera en la superficie libre.

En particular:

- [[Rayleigh Waves]] → acoplamiento **P + SV**
- [[Love Waves]] → ondas **SH guiadas**

Por lo tanto, las propiedades de las ondas superficiales dependen directamente de:

- $V_P$
- $V_S$

y de la estructura del medio descrita en [[Layered Media]].

Estos principios constituyen la base física de los métodos utilizados en [[Métodos Sísmicos No Invasivos]].

---

# Fuente

PDF: **Sebastiano Foti Chapter 2**

Sección:  
**2.1.3 Body waves in unbounded homogeneous elastic media**