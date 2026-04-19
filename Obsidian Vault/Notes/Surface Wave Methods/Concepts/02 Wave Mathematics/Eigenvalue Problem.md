---
name: Eigenvalue Problem
description: Problema de autovalores diferencial para [[Surface Waves|ondas superficiales]] en medios continuamente estratificados — la [[Phase Velocity|velocidad de fase]] como autovalor y la distribución de amplitud vertical como autovector — generalización del [[Thomson-Haskell Matrix|Thomson-Haskell]] a perfiles continuos
type: reference
---

# Eigenvalue Problem — Problema de Autovalores para Ondas Superficiales

> [!CONCEPT] Definición
> En medios **continuamente estratificados** donde las propiedades elásticas $\lambda(x_2)$, $\mu(x_2)$, $\rho(x_2)$ varían con la profundidad $x_2$, la búsqueda de soluciones de onda superficial del tipo $e^{i(kx_1 - \omega t)}$ conduce a un **problema de autovalores diferencial** (eigenvalue problem). Sustituyendo en las ecuaciones de Navier (Foti Ec. 2.56), las funciones de amplitud vertical $U(x_2)$ (desplazamiento) satisfacen un sistema diferencial ordinario de la forma:
> $$\mathbf{L}[U] = -k^2 \rho(x_2)\, \omega^2 / c^2 \cdot U$$
> donde $\mathbf{L}$ es el operador diferencial de segundo orden que depende de $\mu(x_2)$. Los **autovalores** son los pares $(k, \omega)$ —equivalentemente la [[Phase Velocity|velocidad de fase]] $c = \omega/k$— que satisfacen las condiciones de contorno (superficie libre: $\tau_{12} = 0$; campo lejano: $U \to 0$ para $x_2 \to \infty$). Los **autovectores** (eigenfunctions) son los perfiles de amplitud vertical $U_n(x_2)$ para cada modo $n$ — equivalentes a las funciones de sensibilidad o *kernels* de Fréchet. Para el caso de capas discretas, el problema de autovalores se resuelve mediante el [[Thomson-Haskell Matrix|método de matrices de Thomson-Haskell]] o el método de rigidez global.
>
> — Foti et al. (2018), §2.4.2, pp. 100–105; Aki & Richards (2002), §7; Kausel & Roësset (1981).

## Formulación para ondas SH (Love)

Para ondas SH en medio continuo, el desplazamiento $u_3(x_1, x_2, t) = U(x_2)\, e^{i(kx_1 - \omega t)}$ satisface:

$$\frac{d}{dx_2}\left[\mu(x_2) \frac{dU}{dx_2}\right] + [\rho(x_2)\omega^2 - \mu(x_2)k^2] U = 0$$

Condiciones de contorno:
- Superficie libre ($x_2 = 0$): $\mu \, dU/dx_2 = 0$ (esfuerzo de corte nulo)
- Campo lejano ($x_2 \to \infty$): $U \to 0$ (decaimiento evanescente)

Este es un problema de Sturm-Liouville cuya solución no trivial existe solo para valores discretos de $k(\omega)$ — la **[[Dispersion Curve|curva de dispersión]]** de Love. Para cada frecuencia $\omega$, los autovalores $k_n(\omega)$ con $n = 0, 1, 2, \ldots$ (modo fundamental y superiores) definen la dispersión multimodal.

## Formulación para ondas P-SV (Rayleigh)

Para [[Rayleigh Waves|ondas Rayleigh]], la ecuación de movimiento genera un sistema de dos ODEs acopladas para las amplitudes de desplazamiento vertical $W$ y horizontal $V$ (Foti Ec. 2.56):

$$\frac{d}{dx_2}\begin{bmatrix} \sigma_{22} \\ \tau_{12} \end{bmatrix} = \mathbf{A}(x_2, k, \omega) \begin{bmatrix} W \\ V \\ \sigma_{22} \\ \tau_{12} \end{bmatrix}$$

El operador $\mathbf{A}$ depende de $\lambda(x_2)$, $\mu(x_2)$, $\rho(x_2)$, $k$ y $\omega$. Los autovalores del sistema (valores de $c$ que satisfacen las condiciones de contorno) conforman la [[Dispersion Curve|curva de dispersión]] de Rayleigh — problema resuelto numéricamente por el [[Thomson-Haskell Matrix|método de Thomson-Haskell]] o la formulación de rigidez.

## Relación con kernels de sensibilidad

Las eigenfunctions $U_n(x_2)$ tienen interpretación física directa: son proporcionales a los **kernels de Fréchet** $\partial c_R/\partial V_S$ — la sensibilidad de la [[Phase Velocity|velocidad de fase]] al [[Shear Modulus|módulo de corte]] a cada profundidad (ver [[Jacobian Matrix]]). Esto hace que el cálculo de los autovectores sea equivalente al cálculo de las derivadas parciales necesarias para la inversión lineal.

> [!EXAMPLE] Evidencia empírica: Kausel & Roësset (1981) — método de rigidez como eigenvalue problem
> Kausel & Roësset (1981, *Bull. Seism. Soc. Am.*) reformulan el cálculo de modos propios de [[Surface Waves|ondas superficiales]] como un problema de autovalores matricial global mediante el método de rigidez (*stiffness matrix method*). Para un sistema de 30 capas, el problema de autovalores de la matriz de rigidez global (60×60 para Rayleigh, 30×30 para Love) produce automáticamente todos los modos propios a una frecuencia dada. La eficiencia numérica es superior al [[Thomson-Haskell Matrix|método de Thomson-Haskell]] porque evita el overflow exponencial que ocurre con capas gruesas. Foti et al. (2018, §2.4.2) utilizan la formulación de autovalores de Kausel-Roësset como motor de cálculo forward en el software GPDC (Geopsy) usado en la inversión de [[Surface Waves|ondas superficiales]].
>
> — Foti et al. (2018), §2.4.2, pp. 100–105; Kausel & Roësset (1981), *BSSA* 71(6), 1743–1761.

## Referencias

| Fuente | Sección / Página |
|--------|-----------------|
| Foti et al. (2018), *Surface Wave Methods* | §2.4.2 — ondas en medios continuamente estratificados |
| Kausel & Roësset (1981), *Bull. Seism. Soc. Am.* | Método de rigidez como problema de autovalores |
| Aki & Richards (2002), *Quantitative Seismology* | §7.2 — eigenfunctions y kernels de Love/Rayleigh |
