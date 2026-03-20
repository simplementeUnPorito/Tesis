---
name: Attenuation
description: Disminución de amplitud de una onda durante su propagación; distingue atenuación material (disipativa) de geométrica (expansión del frente de onda)
type: reference
---

# Atenuación (Attenuation)

> **Contexto:** Describe la disminución de amplitud de una onda superficial a medida que se aleja de la fuente. En la práctica, la atenuación observada resulta de la contribución simultánea de dos mecanismos físicamente distintos: la atenuación material (intrínseca) y la atenuación geométrica.
> **Fuente:** Foti et al. (2014), Cap. 2.5, pp. 96–120; Cap. 5, pp. 255–271.

## Intuición física

Cuando una onda superficial se propaga alejándose de la fuente, su amplitud disminuye por dos razones fundamentales:

1. **La energía se distribuye sobre un área creciente** (frente de onda que se expande). Esta pérdida de amplitud es puramente geométrica: no hay disipación real de energía, simplemente la misma energía cubre más espacio.

2. **El material disipa energía en calor** a través de fricción viscosa entre partículas, flujo del fluido poral o histéresis de contacto. Esta es la atenuación *intrínseca* o *material*.

Separar ambas contribuciones es imprescindible si el objetivo es caracterizar el amortiguamiento material del suelo $D_S$. No hacerlo equivale a atribuir pérdidas geométricas al material, sobreestimando sistemáticamente $D_S$.

## Atenuación material

En [[Viscoelastic Media]], el número de onda se vuelve complejo:

$$\tilde{k} = k_R - i\,\alpha$$

La amplitud de una onda armónica decae espacialmente como:

$$u(x) \propto e^{-\alpha x}\, e^{i(k_R x - \omega t)}$$

donde $\alpha$ es el **coeficiente de atenuación espacial** (en m⁻¹ o Np/m). Su relación con el **material damping ratio** $D$ y el factor de calidad $Q$:

$$D = \frac{\alpha V_R}{2\omega} = \frac{1}{2Q}$$

Para [[Rayleigh Waves]] en medios débilmente disipativos, el coeficiente de atenuación $\alpha_R(\omega)$ se relaciona con el perfil de amortiguamiento $D_S(z)$ mediante una integral ponderada:

$$\alpha_R(\omega) = \frac{\omega}{[V_R(\omega)]^2}\int_0^\infty \left[V_S D_S \frac{\partial V_R}{\partial V_S} + V_P D_P \frac{\partial V_R}{\partial V_P}\right] dx_2$$

Esta expresión (Foti Ec. 2.133) muestra que $\alpha_R$ es una función lineal de los perfiles $D_S(z)$ y $D_P(z)$, lo que hace que la inversión de atenuación sea un **problema lineal** una vez conocido el perfil de velocidades (a diferencia de la inversión de velocidad, que es no lineal).

## Atenuación geométrica

Para una fuente puntual vertical sobre la superficie libre, la amplitud de las [[Rayleigh Waves]] decae con la distancia $r$ como:

$$A_R(r) \propto \frac{1}{\sqrt{r}}$$

Esta ley $r^{-0.5}$ corresponde a la expansión cilíndrica del frente de onda. En medios [[Layered Media|estratificados]], la función de atenuación geométrica real $Y(r, \omega)$ puede desviarse de la ley $r^{-0.5}$ según la interferencia modal, especialmente a alta frecuencia.

En contraste, las ondas de cuerpo en la misma superficie decaen como $r^{-2}$ — mucho más rápido. Por eso a distancias $r \gtrsim \lambda_R$ el campo queda dominado por ondas superficiales.

## Distinción experimental

En un arreglo de geófonos, la amplitud registrada incluye ambas contribuciones:

$$A(r, \omega) = \frac{C(\omega)}{\sqrt{r}} \cdot e^{-\alpha_R(\omega) \cdot r}$$

Para extraer $\alpha_R(\omega)$, se grafica $\ln[A(r,\omega)\sqrt{r}]$ vs. $r$: la pendiente es $-\alpha_R(\omega)$. Este procedimiento requiere:

1. Corrección de la atenuación geométrica (término $1/\sqrt{r}$).
2. Corrección del [[Near-field Effect|efecto de campo cercano]] en los receptores más próximos a la fuente.
3. Suficientes receptores y rango de offset para una regresión confiable.
4. Verificación de que la función de transferencia del receptor esté bien calibrada (para no confundir diferencias instrumentales con atenuación).

## Implicaciones para la tesis

Si el objetivo es solo el perfil $V_S$, la atenuación es de segundo orden en la velocidad de fase (efecto $\propto D^2$) y puede ignorarse. Si el objetivo incluye el perfil $D_S$, los requisitos instrumentales son significativamente más exigentes: calibración de amplitud, fuente calibrada (para función de transferencia), y corrección cuidadosa de la geometría.

## Referencias

- Foti et al. (2014), Cap. 2.5, pp. 96–120, Ec. 2.133 — atenuación material en Rayleigh.
- Foti et al. (2014), Cap. 5, pp. 255–271 — procedimientos experimentales para medir αR(ω).
