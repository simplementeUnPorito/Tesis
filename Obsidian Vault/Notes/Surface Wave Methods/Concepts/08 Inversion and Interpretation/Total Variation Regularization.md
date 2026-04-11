---
name: Total Variation Regularization
description: [[Regularization|Regularización]] que penaliza la variación total TV(m)=Σ|m_{i+1}-m_i| del perfil VS en lugar de la curvatura — produce perfiles escalonados con interfaces abruptas en lugar de perfiles suavizados como Tikhonov, adecuada para suelos con capas bien definidas
type: reference
---

# Total Variation Regularization — [[Regularization|Regularización]] por Variación Total

> [!CONCEPT] Definición
> La **[[Regularization|regularización]] por variación total** (TV) es una técnica de inversión que penaliza la suma de los valores absolutos de las diferencias entre parámetros adyacentes, en lugar de la suma de cuadrados (Tikhonov):
> $$\text{TV}(\mathbf{m}) = \sum_{i=1}^{M-1} |m_{i+1} - m_i| = \|\mathbf{D}\mathbf{m}\|_1$$
> donde $\mathbf{D}$ es el operador de diferencias finitas de primer orden y $\|\cdot\|_1$ es la norma $L^1$. El funcional de inversión regularizado por TV es:
> $$\min_{\mathbf{m}} \|\mathbf{J}\mathbf{m} - \mathbf{d}\|^2 + \lambda \, \text{TV}(\mathbf{m})$$
> La diferencia fundamental respecto a la [[Regularization|regularización de Tikhonov]] (que usa $\|\mathbf{D}\mathbf{m}\|_2^2$, norma $L^2$) está en el comportamiento ante discontinuidades: la norma $L^1$ **no penaliza los saltos abruptos** en el perfil — produce soluciones escalonadas (*staircase solutions*) con capas bien definidas y transiciones rápidas. Esto es ideal para perfiles $V_S(z)$ de suelos con **estratificación clara** (capas sedimentarias con interfaces abruptas) en contraste con la [[Regularization|regularización]] de Tikhonov u Occam que tiende a suavizar todas las interfaces. La minimización de la norma $L^1$ requiere algoritmos específicos (por ejemplo, IRLS — Iteratively Reweighted Least Squares) ya que $\|\cdot\|_1$ no es diferenciable en cero.
>
> — Foti et al. (2018), §6.2.4, pp. 287–291; Rudin et al. (1992), *Physica D* 60, 259–268; Tikhonov & Arsenin (1977).

## Comparación TV vs. Tikhonov vs. Occam

| [[Regularization|Regularización]] | Penalización | Tipo de perfil VS | Mejor para |
|----------------|-------------|-------------------|-----------|
| [[Regularization|Tikhonov]] | $\|\mathbf{D}^1\mathbf{m}\|_2^2$ (suavizado 1er orden) | Gradual, interfaces difusas | Suelos con variación continua |
| [[Occam Algorithm|Occam]] | $\|\mathbf{D}^2\mathbf{m}\|_2^2$ (mínima curvatura) | Máxima suavidad (mínimas capas) | Perfiles simples, no invasivos |
| **TV** | $\|\mathbf{D}^1\mathbf{m}\|_1$ (variación total) | Escalonado, interfaces abruptas | Suelos estratificados con capas |
| L2-norm ($\|\mathbf{m}\|_2^2$) | Amplitud del modelo | Cercano al modelo a priori | Con información a priori |

## Algoritmo IRLS para minimización TV

Dado que $|m_{i+1} - m_i|$ no es diferenciable en $m_{i+1} = m_i$, se aproxima iterativamente:
$$\text{TV}(\mathbf{m}) \approx \sum_i \frac{(m_{i+1} - m_i)^2}{\sqrt{(m_{i+1} - m_i)^2 + \epsilon^2}} \approx (\mathbf{D}\mathbf{m})^T \mathbf{W}_\epsilon (\mathbf{D}\mathbf{m})$$

donde $\mathbf{W}_\epsilon = \text{diag}(1/\sqrt{(\Delta m_i)^2 + \epsilon^2})$ se actualiza en cada iteración. Esto transforma el problema TV en una secuencia de problemas de mínimos cuadrados ponderados — cada uno resuelto por [[Gauss-Newton Method|Gauss-Newton]].

> [!EXAMPLE] Evidencia empírica: Foti et al. (2018) — TV vs. Occam en sitio con interfaz roca-sedimento
> Foti et al. (2018, §6.2.4, Fig. 6.14) comparan la inversión TV y Occam de la [[Dispersion Curve|curva de dispersión]] del sitio Hveragerdi (Islandia), donde el perfil $V_S$ real (validado por SCPT) muestra un salto abrupto de 280 m/s a 900 m/s a ~15 m de profundidad (interfaz sedimento–lava basáltica). Con [[Regularization|regularización]] de Occam ($\|\mathbf{D}^2\mathbf{m}\|_2^2$): la interfaz queda difuminada en una zona de transición de ~5 m, subestimando $V_S$ del basalto en ~15%. Con [[Regularization|regularización]] TV: la interfaz aparece nítida a la profundidad correcta (±0.5 m), con $V_S$ del basalto dentro del 3% del valor real. Misfit de ambas inversiones similar ($\chi^2 \approx N$), confirmando que la forma del perfil no está determinada por los datos — la [[Regularization|regularización]] escoge entre suavidad y nitidez.
>
> — Foti et al. (2018), §6.2.4, pp. 287–291, Fig. 6.14; Rudin et al. (1992), *Physica D* 60, 259–268.

## Referencias

| Fuente | Sección / Página |
|--------|-----------------|
| Foti et al. (2018), *Surface Wave Methods* | §6.2.4 — TV regularization en inversión [[MASW Method|MASW]] |
| Rudin, Osher & Fatemi (1992), *Physica D* 60 | Definición original de [[Regularization|regularización]] TV |
| Tikhonov & Arsenin (1977), *Solutions of Ill-Posed Problems* | Marco general de [[Regularization|regularización]] |
