# Elastic Wave Potentials

## 1. Concepto

Los **potenciales de onda elástica** son funciones escalares y vectoriales que permiten descomponer el campo de desplazamientos en dos partes independientes: una irrotacional (asociada a [[P-waves]]) y una rotacional (asociada a [[S-Waves]]).

---

## 2. Fundamento físico

En un sólido elástico isotrópico, las ecuaciones de Navier acoplan los movimientos compresional y de corte. La descomposición de Helmholtz desacopla el sistema, permitiendo tratar cada tipo de onda por separado y luego recombinarlas satisfaciendo las condiciones de frontera.

---

## 3. Formulación matemática

### Descomposición de Helmholtz

El campo de desplazamientos $\mathbf{u}$ se escribe como:

$$
\mathbf{u} = \nabla \phi + \nabla \times \mathbf{\psi}
$$

donde:

- $\phi$ → potencial escalar (campo irrotacional, ondas P)
- $\mathbf{\psi}$ → potencial vectorial (campo solenoidal, ondas S)

Cada potencial satisface su propia ecuación de onda:

$$
\nabla^2 \phi = \frac{1}{V_P^2}\frac{\partial^2 \phi}{\partial t^2}
$$

$$
\nabla^2 \mathbf{\psi} = \frac{1}{V_S^2}\frac{\partial^2 \mathbf{\psi}}{\partial t^2}
$$

### Solución armónica para el half-space (problema 2D)

Para propagación en $x$ con profundidad $z \geq 0$, se proponen soluciones de la forma:

$$
\phi = A \, e^{-\alpha z} \, e^{i(kx - \omega t)}, \qquad \psi = B \, e^{-\beta z} \, e^{i(kx - \omega t)}
$$

con:

$$
\alpha = \sqrt{k^2 - \frac{\omega^2}{V_P^2}}, \qquad \beta = \sqrt{k^2 - \frac{\omega^2}{V_S^2}}
$$

La condición $\text{Re}(\alpha) > 0$, $\text{Re}(\beta) > 0$ garantiza decaimiento con la profundidad — condición necesaria para que existan como ondas superficiales.

### Condiciones de frontera en superficie libre

En $z = 0$ los esfuerzos deben ser nulos:

$$
\sigma_{zz}\big|_{z=0} = 0, \qquad \sigma_{xz}\big|_{z=0} = 0
$$

Estas dos condiciones sobre $A$ y $B$ conducen a la [[Rayleigh Waves|ecuación secular de Rayleigh]] como condición de solución no trivial.

---

## 4. Aplicación a geófonos

Este formalismo es el punto de partida para el **forward modeling** de ondas superficiales. Toda la teoría de inversión de ondas de Rayleigh descansa en la solución del sistema de potenciales con condiciones de frontera en cada interfaz del modelo de capas.

---

## 5. Implicaciones para el diseño experimental

Los potenciales muestran que la existencia de ondas superficiales es una consecuencia estricta de la condición de superficie libre. Sin ella, solo existirían [[Body Waves]]. Esto implica que cualquier irregularidad en la superficie (como un geófono mal acoplado o una capa de material suelto superficial) puede alterar las condiciones de frontera y distorsionar las amplitudes registradas.

---

## 6. Fuente

- PDF: Sebastiano Foti Chapter 2
- Sección: 2.2 Rayleigh waves in homogeneous elastic continua