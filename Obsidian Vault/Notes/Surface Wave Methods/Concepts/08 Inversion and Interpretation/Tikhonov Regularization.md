---
name: Tikhonov Regularization
description: Técnica matemática para estabilizar la inversión ill-posed de [[Dispersion Curve|curvas de dispersión]] añadiendo penalización por complejidad del modelo; base del algoritmo de Occam
type: reference
---

# Tikhonov Regularization — [[Regularization|Regularización]] de Tikhonov

> [!CONCEPT] Definición
> La **[[Regularization|regularización]] de Tikhonov** convierte el problema [[Inversión|inverso]] *ill-posed* de la inversión de [[Dispersion Curve|curvas de dispersión]] en una familia de problemas bien condicionados añadiendo un término de penalización a la función de error: $\min\{\|\mathbf{Gm} - \mathbf{d}\|^2 + \mu^2\|\mathbf{L}^n \mathbf{m}\|^2\}$. El parámetro $\mu$ controla el balance entre ajuste a los datos y simplicidad del modelo. La matriz $\mathbf{L}$ define qué se penaliza: orden 0 → amplitud de $\mathbf{m}$, orden 1 → gradiente (suavidad del perfil), orden 2 → curvatura. El **algoritmo de Occam** es la aplicación iterativa que ajusta $\mu$ automáticamente hasta que el residuo coincide con la incertidumbre de los datos. La [[Regularization|regularización]] mitiga la [[Non-uniqueness|no-unicidad]] pero no la elimina: solo restringe el espacio de soluciones hacia las más simples que son compatibles con los datos.
>
> — Foti et al. (2018), Cap. 6, §6.4.2.3, pp. 298–301; §6.4.3.4, pp. 312–320; Tikhonov & Arsenin (1977).

## Intuición física

El problema fundamental de la inversión es que el sistema $\mathbf{G}\mathbf{m} = \mathbf{d}$ está mal condicionado: pequeñas variaciones en los datos producen grandes variaciones en la solución porque el operador $\mathbf{G}$ tiene valores singulares muy pequeños que amplifican el ruido al invertir. La [[Regularization|regularización]] añade un término extra que "penaliza" soluciones complicadas, obligando al algoritmo a buscar no solo el mejor ajuste a los datos sino también la **solución más simple** entre todas las que ajustan bien.

## Definición técnica

El problema de minimización regularizado de **orden cero** (Tikhonov & Arsenin 1977):

$$\min \left\{ \|\mathbf{Gm} - \mathbf{d}\|_2^2 + \mu^2 \|\mathbf{m}\|_2^2 \right\}$$

Con solución analítica (mínimos cuadrados amortiguados):

$$\mathbf{m} = (\mathbf{G}^T\mathbf{G} + \mu^2 \mathbf{I})^{-1} \mathbf{G}^T \mathbf{d}$$

En términos de la descomposición SVD $\mathbf{G} = \mathbf{Q}_1 \mathbf{\Sigma} \mathbf{Q}_2^T$, los **factores de filtro** $s_i^2/(s_i^2 + \mu^2)$ suprimen los componentes asociados a valores singulares pequeños (alta frecuencia espacial en el modelo), evitando la amplificación del ruido.

## [[Regularization|Regularización]] de orden superior

$$\min \left\{ \|\mathbf{Gm} - \mathbf{d}\|_2^2 + \mu^2 \|\mathbf{L}^n \mathbf{m}\|_2^2 \right\}$$

| Orden $n$ | $\|\mathbf{L}^n \mathbf{m}\|^2$ penaliza | Favorece |
|-----------|-------------------------------------------|---------|
| 0 | Amplitud de $\mathbf{m}$ | Perfiles de pequeña norma |
| 1 | Gradiente de $\mathbf{m}$ | Perfiles suaves (sin saltos bruscos) |
| 2 | Curvatura de $\mathbf{m}$ | Perfiles con variación casi lineal |

Para la inversión [[MASW Method|MASW]], el **orden 1** es el más apropiado para sitios con variación gradual de $V_S$ en profundidad.

## Elección del parámetro $\mu$

- **Curva L**: grafica $\|\mathbf{Gm} - \mathbf{d}\|^2$ vs $\|\mathbf{L}^n\mathbf{m}\|^2$ para distintos $\mu$; el punto de mayor curvatura ("codo") es el compromiso óptimo.
- **Principio de discrepancia**: elige $\mu$ tal que el error de ajuste sea consistente con la incertidumbre conocida de los datos.
- **Algoritmo de Occam**: ajusta $\mu$ iterativamente hasta que el residual normalizado coincide con el valor objetivo.

## Algoritmo de Occam

El **algoritmo de Occam** (Constable et al. 1987; Lai 2005) aplica [[Regularization|regularización]] de Tikhonov de primer y segundo orden al problema no lineal de inversión de la [[Dispersion Curve|curva de dispersión]]. En cada iteración, linealiza el problema en torno al modelo actual, resuelve el sistema regularizado, actualiza el modelo, y ajusta $\mu$ para que el error residual converja al objetivo $\tilde{E}_r$ determinado por la incertidumbre experimental. El resultado es el **modelo más suave** compatible con los datos — aplica el principio de parsimonia (navaja de Occam).

## Limitación ante inversiones de velocidad

Para sitios con capas rígidas superficiales o **inversiones de velocidad** (capa blanda bajo capa dura), la [[Regularization|regularización]] de suavidad dificulta la recuperación de discontinuidades bruscas. En esos casos son preferibles:
- **[[Regularization|Regularización]] de variación total** (norma $L_1$ en lugar de $L_2$) — permite saltos bruscos.
- Información a priori explícita sobre la interfaz (número de capas, posición de la interfaz).
- Métodos de búsqueda global ([[Monte Carlo Methods]]) que no imponen suavidad.

> [!EXAMPLE] Evidencia empírica: Foti et al. (2018) — algoritmo de Occam en inversión multimodal
> Foti et al. (2018, §6.4.2.3) aplican el algoritmo de Occam a la inversión de la [[Dispersion Curve|curva de dispersión]] en sitios con diferentes niveles de contraste de impedancia. En el sitio La Salle (depósito moderadamente heterogéneo), la [[Regularization|regularización]] de orden 1 con $\mu$ determinado por la curva L produce perfiles $V_S(z)$ con suavidad compatible con la resolución real del experimento, sin oscilaciones espurias. Comparado con la inversión sin [[Regularization|regularización]], el perfil regularizado presenta un error de ajuste marginalmente mayor (~2% en misfit RMS) pero es estable frente a perturbaciones en los datos. El ejemplo demuestra que la [[Regularization|regularización]] de Tikhonov de orden 1 es la opción estándar para inversión [[MASW Method|MASW]] en sitios sin inversiones de velocidad severas.
>
> — Foti et al. (2018), §6.4.2.3, pp. 298–301; §6.4.3.4, pp. 312–320.

## Referencias

| Fuente | Sección / Página |
|--------|-----------------|
| Foti et al. (2018), *Surface Wave Methods* | Cap. 6, §6.4.2.3, pp. 298–301; §6.4.3.4, pp. 312–320 |
| Tikhonov & Arsenin (1977), *Solutions of Ill-Posed Problems* | Formulación matemática original |
| Constable et al. (1987) | Algoritmo de Occam — modelo más suave compatible con datos |
| Lai (2005) | Aplicación de Occam a [[Joint Inversion|inversión conjunta]] VS + DS |
