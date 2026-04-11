---
name: Hankel Function
description: Función de Hankel H₀⁽²⁾ — función especial de cilindros que describe la propagación de frentes de onda cilíndricos en 2D desde fuente puntual — aparece en la solución de Lamb's Problem para el campo de Rayleigh en campo lejano
type: reference
---

# Hankel Function — Función de Hankel $H_0^{(2)}$

> [!CONCEPT] Definición
> Las **funciones de Hankel** $H_n^{(1,2)}(z)$ son soluciones de la ecuación de Bessel de orden $n$ que representan ondas viajeras en coordenadas cilíndricas. Se definen como combinaciones lineales de las funciones de Bessel $J_n$ y $Y_n$:
> $$H_n^{(1)}(z) = J_n(z) + i Y_n(z), \qquad H_n^{(2)}(z) = J_n(z) - i Y_n(z)$$
> La función $H_0^{(2)}(k_R r)$ de orden cero y segunda clase aparece en la solución del [[Lamb's Problem|problema de Lamb]] para el campo de Rayleigh en campo lejano (Foti Ec. 2.75):
> $$u_2^R(r, 0, \omega) \approx A(\omega) \cdot H_0^{(2)}(k_R r)$$
> donde $r = \sqrt{x_1^2 + x_3^2}$ es la distancia horizontal a la fuente y $k_R = \omega/V_R$ es el [[Wavenumber|número de onda]] de Rayleigh. Para $|k_R r| \gg 1$ (campo lejano, condición esencial en [[MASW Method|MASW]]), la expansión asintótica simplifica:
> $$H_0^{(2)}(k_R r) \approx \sqrt{\frac{2}{\pi k_R r}} \, e^{-i(k_R r - \pi/4)}$$
> Lo que muestra que la amplitud decae como $r^{-1/2}$ (**decaimiento geométrico cilíndrico**) y la fase avanza como $e^{-ik_R r}$ — frentes de onda circulares centrados en la fuente. Este comportamiento justifica la corrección de amplitud $\sqrt{r}$ aplicada en la normalización de señales [[MASW Method|MASW]] antes del análisis en el dominio $f$-$k$.
>
> — Foti et al. (2018), §2.4.3, pp. 107–111, Ec. 2.75; Watson (1944), *Treatise on Bessel Functions*; Lamb (1904).

## Propiedades relevantes para ondas superficiales

### Decaimiento geométrico

El factor $r^{-1/2}$ del campo lejano se denomina **decaimiento geométrico cilíndrico** o *geometrical spreading*. Contrasta con las ondas de cuerpo (P y S) que decaen como $r^{-1}$ (esféricas). Esta diferencia tiene implicaciones prácticas:

| Tipo de onda | Geometría | Decaimiento de amplitud |
|-------------|-----------|------------------------|
| P, S (campo lejano) | Esférica | $\propto r^{-1}$ |
| Rayleigh (campo lejano) | Cilíndrica | $\propto r^{-1/2}$ |
| P confinada (guía de agua) | Cilíndrica | $\propto r^{-1/2}$ |

La atenuación total de la onda Rayleigh es:
$$A(r) = A_0 \cdot r^{-1/2} \cdot e^{-\alpha_R r}$$
donde $\alpha_R$ es el [[Attenuation Coefficient|coeficiente de atenuación]] por pérdidas materiales. La corrección por *geometrical spreading* es esencial para estimar $\alpha_R$ a partir de la razón de amplitudes entre dos receptores en [[MASW Method|MASW]].

### Desfase de π/4

El factor $e^{i\pi/4}$ (o $-\pi/4$ para $H^{(2)}$) en la expansión asintótica implica un adelanto de fase de 45° respecto a la onda plana equivalente. Este desfase es constante (independiente de $r$ y $\omega$) y se cancela al comparar fases entre dos receptores — no afecta la medición de $V_R$ en [[MASW Method|MASW]] siempre que ambos receptores estén en campo lejano.

### Condición de campo lejano

La expansión asintótica es válida cuando $k_R r \gg 1$, es decir:
$$r \gg \frac{\lambda_R}{2\pi} = \frac{V_R}{2\pi f}$$

Para $V_R = 200$ m/s y $f = 10$ Hz: $r \gg 3.2$ m. En la práctica, se requiere una distancia mínima de la fuente al primer receptor $d_1 \geq \lambda_{\max}/2$ para asegurar campo lejano (véase [[Near-field Effect]]).

## Aparición en SPAC y correlación cruzada

La función de Bessel $J_0(kr)$ — parte real de $H_0^{(2)}$ — aparece también en la **correlación cruzada** entre dos receptores a distancia $r$ para un campo de ondas isótropo (método [[SPAC Method|SPAC]]):

$$\frac{\Re\{S_{12}(f)\}}{\sqrt{S_{11}(f) \cdot S_{22}(f)}} = J_0(kr) = J_0\left(\frac{2\pi f r}{V_R(f)}\right)$$

Esto convierte la inversión SPAC en un ajuste de $J_0$ a los datos de correlación — el papel de las funciones de Hankel/Bessel en los métodos de ondas superficiales es, por tanto, doble: decaimiento de amplitud (Hankel) y coherencia espacial (Bessel).

> [!EXAMPLE] Evidencia empírica: Lamb (1904) — solución original de campo lejano para fuente superficial
> Lamb (1904, *Phil. Trans. R. Soc. A*, 203) resuelve analíticamente el problema de la respuesta dinámica de un semiespacio elástico a una carga puntual en superficie — el [[Lamb's Problem|problema de Lamb]]. La solución en campo lejano expresa el desplazamiento vertical de Rayleigh exactamente mediante la función $H_0^{(2)}(k_R r)$, verificando la propagación cilíndrica del frente de onda. Foti et al. (2018, §2.4.3, Ec. 2.75) reproducen este resultado como base teórica del decaimiento $r^{-1/2}$ observado en ensayos [[MASW Method|MASW]]: las mediciones de amplitud en el tendido de receptores confirman el decaimiento $r^{-1/2}$ para distancias $r > \lambda/2$, validando la hipótesis de campo lejano cilindricamente simétrico. La desviación del decaimiento teórico a distancias cortas (campo cercano) es el [[Near-field Effect|efecto de campo cercano]].
>
> — Foti et al. (2018), §2.4.3, pp. 107–111; Lamb (1904), *Phil. Trans. R. Soc. A* 203, 1–42.

## Referencias

| Fuente | Sección / Página |
|--------|-----------------|
| Foti et al. (2018), *Surface Wave Methods* | §2.4.3, Ec. 2.75 — campo de Rayleigh en campo lejano |
| Lamb, H. (1904), *Phil. Trans. R. Soc. A* 203 | Solución original del problema de carga superficial |
| Watson, G.N. (1944), *Treatise on Bessel Functions* | Propiedades asintóticas de funciones de Hankel |
