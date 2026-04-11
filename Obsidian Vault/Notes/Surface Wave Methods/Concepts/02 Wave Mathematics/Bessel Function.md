---
name: Bessel Function
description: Funciones especiales J_n(z) que son soluciones de la ecuación de Bessel — aparecen en la autocorrelación espacial de ondas superficiales isotrópicas (SPAC: ρ=J₀(kr)) y en la expansión asintótica de las funciones de Hankel en el campo lejano
type: reference
---

# Bessel Function — Función de Bessel $J_n$

> [!CONCEPT] Definición
> Las **funciones de Bessel** $J_n(z)$ son soluciones de la **ecuación de Bessel** de orden $n$:
> $$z^2 \frac{d^2 y}{dz^2} + z \frac{dy}{dz} + (z^2 - n^2) y = 0$$
> La función de primer tipo $J_n(z)$ es regular en $z = 0$ y describe oscilaciones amortiguadas para $z \gg 1$:
> $$J_n(z) \approx \sqrt{\frac{2}{\pi z}} \cos\!\left(z - \frac{n\pi}{2} - \frac{\pi}{4}\right) \qquad (z \gg 1)$$
> La función $J_0(z)$ (orden cero) es especialmente importante en el método [[SPAC Method|SPAC]]: para un campo de ondas Rayleigh **isotrópico** (fuentes distribuidas uniformemente en azimut), la **correlación cruzada normalizada** entre dos receptores a distancia $r$ es:
> $$\rho(f, r) = \frac{\Re\{C_{12}(f)\}}{\sqrt{C_{11}(f) C_{22}(f)}} = J_0\!\left(\frac{2\pi f \, r}{V_R(f)}\right) = J_0(k r)$$
> donde $k = 2\pi f / V_R(f)$ es el número de onda de Rayleigh. Esta relación — conocida como la **fórmula de Aki (1957)** — convierte la inversión SPAC en un ajuste de $J_0$ a los datos de coherencia espacial. La función de Bessel también es la parte real de la [[Hankel Function|función de Hankel]]: $J_n(z) = \Re\{H_n^{(1)}(z)\} = \Re\{H_n^{(2)}(z)\}$.
>
> — Aki (1957), *Bull. Earthquake Res. Inst.* 35, 415–456; Foti et al. (2018), §4.5.2, pp. 215–220; Watson (1944), *Treatise on Bessel Functions*.

## La fórmula de Aki y el método SPAC

La derivación de Aki (1957) para un campo de ondas isotrópico con fuente de densidad espectral $\Phi(f)$:

$$C_{12}(f) = \Phi(f) \int_0^{2\pi} e^{ikr\cos\theta} \frac{d\theta}{2\pi} = \Phi(f) \cdot J_0(kr)$$

La coherencia normalizada $\rho(f, r) = J_0(kr)$ puede invertirse para $V_R(f) = 2\pi f r / J_0^{-1}(\rho)$. La inversión numérica se realiza ajustando $J_0(kr)$ a los datos mediante mínimos cuadrados no lineales. Los ceros de $J_0$ ($z_1 = 2.405$, $z_2 = 5.520$, $z_3 = 8.654$, ...) determinan los rangos de $kr$ donde la correlación espacial cambia de signo — regiones problemáticas que deben excluirse del ajuste.

## Funciones de Bessel modificadas en medios porosos

Las funciones de Bessel modificadas $I_n(z)$ y $K_n(z)$ (ecuación de Bessel con argumento imaginario) aparecen en la solución de la onda P lenta de Biot a frecuencias sub-críticas (ver [[Biot Theory]]), donde la onda es difusiva y la solución decae exponencialmente.

> [!EXAMPLE] Evidencia empírica: Aki (1957) — validación de J₀ en correlación de microtremores en Tokio
> Aki (1957, *Bull. Earthquake Res. Inst.* 35, 415–456) verifica experimentalmente la relación $\rho = J_0(kr)$ en el primer estudio sistemático del método SPAC usando registros de microtremores en Tokio. Con 4 sismómetros en configuración circular (radio 50, 150 y 350 m), Aki calcula la correlación espacial de los microtremores entre 0.1 y 1 Hz y ajusta $J_0(kr)$ a los datos. El ajuste es excelente para el rango $kr < 3$ (antes del primer cero de $J_0$), con desviación < 5% de la curva teórica. Las velocidades de fase extraídas (70–200 m/s entre 0.2 y 1 Hz) revelan la estratificación de sedimentos de la Cuenca de Tokio hasta ~600 m de profundidad — primera aplicación del método SPAC a escala regional. Este trabajo establece $J_0(kr)$ como la firma espectral de un campo de ondas isotrópico.
>
> — Aki (1957), *Bull. Earthquake Res. Inst.* 35, 415–456; Foti et al. (2018), §4.5.2, pp. 215–220.

## Referencias

| Fuente | Sección / Página |
|--------|-----------------|
| Aki, K. (1957), *Bull. Earthquake Res. Inst.* 35, 415–456 | Derivación de J₀ para campos isotrópicos — fundamento SPAC |
| Foti et al. (2018), *Surface Wave Methods* | §4.5.2 — autocorrelación espacial y función de Bessel |
| Watson, G.N. (1944), *Treatise on Bessel Functions* | Propiedades completas de las funciones de Bessel |
