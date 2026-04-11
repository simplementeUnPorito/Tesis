---
name: Thomson-Haskell Matrix
description: Método de matriz de transferencia para calcular la curva de dispersión de Rayleigh en medios estratificados — propaga condiciones de borde entre capas multiplicando matrices 4x4
type: reference
---

# Thomson-Haskell Matrix — Matriz de Transferencia de Thomson-Haskell

> [!CONCEPT] Definición
> El **método de la matriz de transferencia de Thomson-Haskell** (Thomson 1950; Haskell 1953) es el algoritmo estándar para resolver el **problema directo** de la propagación de ondas en medios estratificados: calcular la [[Dispersion Curve|curva de dispersión]] teórica $c_R(f)$ para un modelo de capas dado $\{V_{S,i}, V_{P,i}, \rho_i, h_i\}$. Para cada par $(\omega, k)$, la solución en cada capa es una combinación de cuatro funciones de modo ($e^{\pm\alpha z}$, $e^{\pm\beta z}$ para P y SV); la matriz de transferencia $\mathbf{T}_i$ propaga el vector de estado $[u_z, u_x, \sigma_{zz}, \sigma_{xz}]^T$ a través de la capa $i$. La matriz total es el producto $\mathbf{T} = \prod_i \mathbf{T}_i$. La condición de dispersion de Rayleigh — superficie libre arriba y decaimiento exponencial hacia abajo — equivale a $\det[\mathbf{T}_{2\times2}^{(top)}] = 0$. Las raíces de esta condición dan los eigenvalores $k_n(\omega)$ de cada modo $n$. Ver [[Rayleigh Eigenproblem]].
>
> — Thomson (1950), *J. Appl. Phys.*; Haskell (1953), *Bull. Seism. Soc. Am.*; Foti et al. (2018), Cap. 2, §2.2.

## Formulación por capas

### Solución en una capa homogénea

En la capa $i$ (homogénea, $V_S$, $V_P$, $\rho$, espesor $h_i$), la solución general del sistema de Rayleigh es:

$$\mathbf{f}(z) = \begin{bmatrix} u_z \\ u_x \\ \sigma_{zz}/(\rho\omega^2) \\ \sigma_{xz}/(\rho\omega^2) \end{bmatrix} = \mathbf{T}_i(h_i) \cdot \mathbf{f}(0)$$

donde $\mathbf{T}_i$ es la **matriz de transferencia de Thomson-Haskell** de dimensión $4\times4$. Sus entradas dependen de $\omega$, $k$, $V_S$, $V_P$, $\rho$ y $h_i$.

### Propagación a través de N capas

$$\mathbf{f}_{N+1}(top) = \mathbf{T}_N \cdot \mathbf{T}_{N-1} \cdots \mathbf{T}_1 \cdot \mathbf{f}_1(top)$$

La multiplicación de matrices es el núcleo computacional del algoritmo.

### Condición de dispersión

Aplicando condición de superficie libre (esfuerzos = 0 en la superficie) y decaimiento en el semispacio inferior, se obtiene:

$$\mathbf{M}(c_R, f) \cdot \mathbf{a} = \mathbf{0} \quad \Leftrightarrow \quad \det[\mathbf{M}] = 0$$

Las raíces $c_R(f)$ de esta ecuación implícita son la **curva de dispersión** de cada modo.

## Ventajas e inconvenientes

| Aspecto | Método Thomson-Haskell | Formulación matricial de rigidez |
|---|---|---|
| Implementación | Simple | Más compleja |
| Estabilidad numérica | Problemas para alta frecuencia × espesor | Numéricamente robusta |
| Coste computacional | $O(N)$ multiplicaciones de matrices $4\times4$ | Similar |
| Inversión | No directa | Permite inversión directa del Jacobiano |

Para aplicaciones MASW estándar, las inestabilidades numéricas aparecen cuando $\omega h / V_S \gg 1$ (capas gruesas a alta frecuencia). Se evitan usando la **formulación de la matriz de rigidez** (Kausel & Roësset 1981) o el método de propagador de Dunkin (1965).

## Extensión a medios viscoelásticos

Por el **principio de correspondencia elástico-viscoelástico** ([[Viscoelastic Media]]), todas las constantes de Lamé se reemplazan por módulos complejos $\tilde{\mu}(\omega) = \mu(1+2iD_s)$. La matriz de Thomson-Haskell pasa a ser compleja → las raíces de $\det[\mathbf{M}] = 0$ son complejas → se obtiene simultáneamente la velocidad de fase real $c_R$ y el coeficiente de atenuación $\alpha_R$, base de la estimación de [[Shear Damping Ratio|$D_s$]].

> [!EXAMPLE] Evidencia empírica: Xia et al. (1999) — Thomson-Haskell como motor del problema directo en inversión MASW
> **Paper 002 (Xia et al. 1999)** implementa el método de Thomson-Haskell como el motor del **problema directo** en su algoritmo de inversión MASW por mínimos cuadrados. Para cada modelo candidato $\{V_{S,i}, V_{P,i}, \rho_i, h_i\}$, se calcula la curva de dispersión teórica resolviendo $\det[\mathbf{M}(c_R, f)] = 0$ numéricamente (bisección en $c_R$ para cada $f$). El Jacobiano $\partial c_R / \partial V_{S,i}$ se calcula por diferencias finitas. El algoritmo ejecuta ~10 iteraciones con ~100 evaluaciones del problema directo por iteración → ~1000 evaluaciones del método de Thomson-Haskell por inversión completa. La eficiencia del método es la que hace posible la inversión iterativa en tiempo razonable.
>
> — Research Database, entrada 002 (core); Xia et al. (1999), *Geophysics* 64(3); Thomson (1950); Haskell (1953).

## Referencias

| Fuente | Sección / Página |
|--------|-----------------|
| Foti et al. (2018), *Surface Wave Methods* | Cap. 2, §2.2, pp. 50–64 — derivación completa |
| Thomson (1950), *J. Appl. Phys.* 21 | Formulación original de la matriz de transferencia |
| Haskell (1953), *Bull. Seism. Soc. Am.* 43 | Extensión a ondas de Love y Rayleigh |
| Kausel & Roësset (1981) | Formulación de matriz de rigidez (numéricamente estable) |
| Xia et al. (1999), *Geophysics* 64(3) | Paper 002 — Thomson-Haskell en inversión MASW |
