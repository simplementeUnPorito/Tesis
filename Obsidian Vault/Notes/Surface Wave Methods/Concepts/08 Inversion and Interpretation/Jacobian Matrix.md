---
name: Jacobian Matrix
description: Matriz de derivadas parciales de la curva de dispersión respecto a los parámetros del modelo — base del problema linealizado de inversión MASW; columnas = kernels de sensibilidad por capa
type: reference
---

# Jacobian Matrix — Matriz Jacobiana

> [!CONCEPT] Definición
> La **Matriz Jacobiana** $\mathbf{J}$ (o matriz de sensibilidad) es la matriz de **derivadas parciales** de los datos observados respecto a los parámetros del modelo, evaluada en el modelo actual $\mathbf{m}_k$:
> $$J_{ij} = \frac{\partial d_i}{\partial m_j}\bigg|_{\mathbf{m}_k}$$
> En la [[Inversión|inversión]] de [[Dispersion Curve|curvas de dispersión]] de [[MASW Method|MASW]], los datos son las velocidades de fase de Rayleigh $d_i = c_R(f_i)$ y los parámetros del modelo son las velocidades de onda de corte $m_j = V_{S,j}$ de cada capa $j$:
> $$J_{ij} = \frac{\partial c_R(f_i)}{\partial V_{S,j}}$$
> Esta es precisamente la columna $j$ del [[Sensitivity Kernel|kernel de sensibilidad]] — la derivada de la velocidad de Rayleigh a la frecuencia $f_i$ respecto al $V_S$ de la capa $j$. La matriz Jacobiana tiene dimensiones $N_f \times N_{capas}$ (número de frecuencias × número de capas). El Jacobiano es el elemento central de la [[Levenberg-Marquardt|inversión iterativa de Levenberg-Marquardt]]:
> $$\Delta\mathbf{m} = (\mathbf{J}^T\mathbf{J} + \lambda\mathbf{I})^{-1}\mathbf{J}^T\mathbf{r}$$
> y de la propagación de incertidumbre del [[First-Order Second-Moment Method|FOSM]]: $\mathbf{C}_m \approx (\mathbf{J}^T\mathbf{C}_d^{-1}\mathbf{J})^{-1}$.
>
> — Foti et al. (2018), §6.4.2; Xia et al. (1999), *Geophysics*; Tarantola (2005), §2.3.

## Cálculo del Jacobiano para ondas de Rayleigh

### Método analítico (variacional)

Usando los [[Variational Principles|principios variacionales]], la derivada analítica de $c_R$ respecto a $V_{S,j}$ en la capa $j$ (de espesor $h_j$, entre $z_j$ y $z_{j+1}$):

$$\frac{\partial c_R}{\partial V_{S,j}} = \frac{2\rho_j V_{S,j}}{c_R I_2} \int_{z_j}^{z_{j+1}} \left[|\partial_z u_r|^2 + k^2|u_z|^2\right] dz$$

donde $u_r$ y $u_z$ son las autofunciones de desplazamiento horizontal y vertical, $I_2$ es el factor de normalización y $k = \omega/c_R$.

### Método numérico (diferencias finitas)

$$J_{ij} \approx \frac{c_R(f_i; \mathbf{m} + \epsilon_j \hat{e}_j) - c_R(f_i; \mathbf{m})}{\epsilon_j V_{S,j}}$$

donde $\hat{e}_j$ es el vector unitario en la dirección del parámetro $j$ y $\epsilon_j$ = 0.01–0.05 (perturbación del 1–5%). Menos preciso que el método analítico pero más fácil de implementar.

## Propiedades del Jacobiano en MASW

- **Número de condición elevado**: $\text{cond}(\mathbf{J}^T\mathbf{J})$ puede ser $10^6$–$10^{10}$ → sistema mal condicionado → requiere [[Tikhonov Regularization|regularización]]
- **Dominancia de $V_S$**: las columnas del Jacobiano para $V_S$ son 10–50× mayores que para $V_P$ y $\rho$ → el problema es casi independiente de $V_P$ y $\rho$ → estos parámetros pueden fijarse a priori
- **Decaimiento con profundidad**: la sensibilidad disminuye con la profundidad → las capas profundas están menos determinadas → la incertidumbre crece con $z$

> [!EXAMPLE] Evidencia empírica: Xia et al. (1999) — Jacobiano en inversión MASW con sensibilidad dominante de VS
> **Paper 002 (Xia, Miller & Park 1999)** presenta el análisis completo del Jacobiano para la inversión de curvas de dispersión MASW en el sitio de Kansas. Los autores calculan $\partial c_R/\partial V_{S,j}$, $\partial c_R/\partial V_{P,j}$, y $\partial c_R/\partial \rho_j$ para cada capa del modelo. El resultado cuantitativo: la norma de las columnas del Jacobiano para $V_S$ es 80–95% de la norma total del Jacobiano aumentado — confirmando que $c_R$ es casi exclusivamente una función de $V_S(z)$. La matriz $\mathbf{J}^T\mathbf{J}$ tiene número de condición ~$10^7$ antes de regularizar; con [[Tikhonov Regularization|regularización]] ($\lambda$ = 0.1), el número de condición baja a ~$10^3$ y el sistema linealizado es estable. Este análisis del Jacobiano fue la justificación cuantitativa para usar MASW (con inversión de $V_S$ solamente) en lugar de inversión conjunta $V_S$/$V_P$/$\rho$.
>
> — Research Database, entrada 002 (core); Xia, Miller & Park (1999), *Geophysics* 64(3):691–700.

## Referencias

| Fuente | Sección / Página |
|--------|-----------------|
| Foti et al. (2018), *Surface Wave Methods* | §6.4.2 — Jacobiano en inversión MASW |
| Xia, Miller & Park (1999), *Geophysics* 64(3) | Paper 002 — análisis de sensibilidad y Jacobiano |
| Tarantola (2005), *Inverse Problem Theory* | §2.3 — formulación del Jacobiano en problemas inversos |
