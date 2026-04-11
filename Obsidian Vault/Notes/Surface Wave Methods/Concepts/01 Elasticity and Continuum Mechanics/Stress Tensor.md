---
name: Stress Tensor
description: Tensor de Cauchy que describe las fuerzas internas por unidad de área en un medio continuo; su divergencia es la fuerza interna que equilibra la inercia; base de las ecuaciones de movimiento elástico
type: reference
---

# Tensor de Esfuerzos (Stress Tensor)

> [!CONCEPT] Definición
> El **tensor de esfuerzos** $\boldsymbol{\sigma}$ (tensor de Cauchy) describe completamente el estado de carga interna en un punto de un medio continuo: cuánta fuerza actúa por unidad de área sobre cualquier plano imaginario a través de ese punto, en cualquier orientación. Su divergencia aparece en la segunda ley de Newton para medios continuos ($\nabla \cdot \boldsymbol{\sigma} = \rho\,\ddot{\mathbf{u}}$), que combinada con la ley de Hooke conduce a las **ecuaciones de Navier** — la base de la propagación de [[Body Waves|ondas sísmicas]]. Las condiciones de esfuerzo nulo en la superficie libre ($\sigma_{zz} = \sigma_{xz} = 0$) son las que dan lugar a las [[Rayleigh Waves]] y [[Love Waves]].
>
> — Foti et al. (2018), §2.1.1, pp. 36–41.

## Intuición física

Imagina un corte plano imaginario que divide un volumen de suelo en dos partes. La parte superior ejerce una fuerza sobre la parte inferior a través de ese plano, y viceversa. Esta fuerza por unidad de área es la **tracción** sobre ese plano. El tensor de esfuerzos $\boldsymbol{\sigma}$ es la entidad matemática que permite calcular la tracción sobre cualquier plano (con cualquier normal $\hat{n}$) a partir de un único objeto: $\mathbf{t} = \boldsymbol{\sigma}\,\hat{n}$ (teorema de Cauchy).

Hay dos tipos de esfuerzo:
- **Esfuerzo normal** ($\sigma_{ii}$): componente de la tracción perpendicular al plano; produce compresión o tracción.
- **Esfuerzo de corte** ($\sigma_{ij}$, $i \neq j$): componente de la tracción paralela al plano; produce distorsión.

## Definición matemática

El tensor de esfuerzos de Cauchy en 3D es un tensor simétrico de segundo orden:

$$\boldsymbol{\sigma} = \begin{bmatrix} \sigma_{11} & \sigma_{12} & \sigma_{13} \\ \sigma_{12} & \sigma_{22} & \sigma_{23} \\ \sigma_{13} & \sigma_{23} & \sigma_{33} \end{bmatrix}$$

La simetría ($\sigma_{ij} = \sigma_{ji}$) proviene del equilibrio de momentos sobre un volumen diferencial (sin momentos de par distribuidos). Tiene **seis componentes independientes** en 3D.

### Teorema de Cauchy

La tracción sobre un plano con normal unitaria $\hat{n}$ es:

$$\mathbf{t} = \boldsymbol{\sigma}\,\hat{n}, \quad t_i = \sigma_{ij}\,n_j$$

Este resultado permite calcular la fuerza por unidad de área en cualquier dirección y plano sin necesidad de resolver el sistema para cada orientación.

## Componentes y convención de índices

| Tipo | Componentes | Significado físico |
|---|---|---|
| **Esfuerzos normales** | $\sigma_{11}, \sigma_{22}, \sigma_{33}$ | Tracción/compresión en $x_1, x_2, x_3$ |
| **Esfuerzos de corte** | $\sigma_{12}, \sigma_{13}, \sigma_{23}$ | Fuerza tangencial sobre planos normales a $x_i$ en dirección $x_j$ |

Convención de signos estándar: $\sigma_{ii} > 0$ implica tracción (extensión); $\sigma_{ii} < 0$ implica compresión.

## Ecuación de movimiento del continuo elástico

La segunda ley de Newton para un volumen diferencial del medio (incluyendo la fuerza de inercia):

$$\nabla \cdot \boldsymbol{\sigma} = \rho\,\frac{\partial^2 \mathbf{u}}{\partial t^2}$$

En notación indicial:

$$\frac{\partial \sigma_{ij}}{\partial x_j} = \rho\,\ddot{u}_i$$

Esta es la **ecuación de movimiento** del medio continuo. Combinada con la ley de Hooke (que relaciona $\boldsymbol{\sigma}$ con el [[Strain Tensor|tensor de deformación]] $\boldsymbol{\varepsilon}$), produce las **ecuaciones de Navier**:

$$(\lambda + \mu)\,\nabla(\nabla \cdot \mathbf{u}) + \mu\,\nabla^2\mathbf{u} = \rho\,\ddot{\mathbf{u}}$$

Estas ecuaciones admiten soluciones de ondas P y S con velocidades $V_P = \sqrt{(\lambda+2\mu)/\rho}$ y $V_S = \sqrt{\mu/\rho}$ respectivamente.

## Condiciones de contorno en la superficie libre

En la superficie libre del suelo ($z = 0$), la condición de **esfuerzo libre** (no hay tracción atmosférica relevante a frecuencias sísmicas) requiere:

$$\sigma_{zz}(z=0) = 0, \quad \sigma_{xz}(z=0) = 0, \quad \sigma_{yz}(z=0) = 0$$

Estas tres condiciones son las que dan lugar a las [[Rayleigh Waves]] (por acoplamiento de $\sigma_{zz}$ y $\sigma_{xz}$ con ondas P–SV) y a las [[Love Waves]] (por la condición sobre $\sigma_{yz}$ para ondas SH). Sin estas condiciones de contorno, las ondas superficiales no existirían.

## Condiciones en interfaces entre capas

En la interfaz entre dos medios elásticos (a profundidad $z = h$), las condiciones de continuidad son:

1. Continuidad de la **tracción**: $\sigma_{zz}^{(1)} = \sigma_{zz}^{(2)}$, $\sigma_{xz}^{(1)} = \sigma_{xz}^{(2)}$, $\sigma_{yz}^{(1)} = \sigma_{yz}^{(2)}$.
2. Continuidad del **desplazamiento**: $u_x^{(1)} = u_x^{(2)}$, $u_y^{(1)} = u_y^{(2)}$, $u_z^{(1)} = u_z^{(2)}$.

Estas cuatro condiciones (para el caso P–SV) son las que se imponen en el método de la matriz de transferencia de [[Layered Media|Thomson-Haskell]] para calcular la [[Dispersion Curve|curva de dispersión]] de medios estratificados.

> [!EXAMPLE] Evidencia empírica: Xia et al. (1999) — tensor de esfuerzos como núcleo del problema directo [[MASW Method|MASW]]
> **Paper 002 (Xia, Miller & Park 1999)** implementa el problema directo de [[MASW Method|MASW]] sobre las ecuaciones de Navier derivadas del tensor de esfuerzos en cada capa elástica. El Jacobiano analítico $\partial c_R / \partial V_S$ — que permite la convergencia del algoritmo de inversión en < 10 iteraciones — se deriva directamente de la condición de esfuerzo libre en superficie ($\boldsymbol{\sigma} = 0$ en $z=0$) aplicada en el contexto de la ecuación secular de Rayleigh. La validación en múltiples sitios de Kansas confirma que el tensor de esfuerzos lineal isótropo es una aproximación suficientemente precisa para los suelos reales ensayados.
>
> — Research Database, entrada 002 (core).

## Referencias

| Fuente | Sección / Página |
|--------|-----------------|
| Foti et al. (2018), *Surface Wave Methods* | §2.1.1, pp. 36–39 — tensor de Cauchy y ecuación de movimiento |
| Foti et al. (2018), *Surface Wave Methods* | §2.1.3, pp. 43–46 — condición de esfuerzo libre y Navier |
| Xia, Miller & Park (1999), *Geophysics* 64(3) | Paper 002 — tensor de esfuerzos en problema directo [[MASW Method|MASW]] |
