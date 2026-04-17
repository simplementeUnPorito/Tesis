---
aliases: [ley de Hooke, ley de Hooke generalizada, relación constitutiva elástica]
tags: [elasticity, constitutive-law, continuum-mechanics]
---

# Hooke's Law (Ley de Hooke generalizada)

La **ley de Hooke generalizada** para un sólido [[Elasticity|elástico]] lineal isotrópico establece la relación entre el [[Stress Tensor|tensor de esfuerzos]] $\boldsymbol{\sigma}$ y el [[Strain Tensor|tensor de deformaciones]] $\boldsymbol{\varepsilon}$:

$$
\boldsymbol{\sigma} = \lambda\,\text{tr}(\boldsymbol{\varepsilon})\,\mathbf{I} + 2\mu\,\boldsymbol{\varepsilon}
$$

donde:
- $\lambda, \mu$ — [[Lamé Constants|constantes de Lamé]] (únicos parámetros independientes de un medio isotrópico)
- $\text{tr}(\boldsymbol{\varepsilon}) = \nabla \cdot \mathbf{u}$ — deformación volumétrica (traza del tensor de deformación)
- $\mathbf{I}$ — tensor identidad de segundo orden

## Interpretación física

| Término | Significado físico |
|---------|-------------------|
| $\lambda\,\text{tr}(\boldsymbol{\varepsilon})\,\mathbf{I}$ | Respuesta esférica: esfuerzo isótropo proporcional al cambio de volumen. Asociado a [[P-waves\|ondas P]]. |
| $2\mu\,\boldsymbol{\varepsilon}$ | Respuesta desviadora: esfuerzo cortante proporcional a la deformación de corte. Asociado a [[S-Waves\|ondas S]]. |

El parámetro $\mu = G = \rho V_S^2$ es el **[[Shear Modulus|módulo de corte dinámico]]** — la propiedad geotécnica de mayor interés en la caracterización sísmica de sitio.

## Escalar para materiales isótropos

Para el caso uniaxial (1D) o en el límite de una onda plana monocromática:

$$
\sigma = E\,\varepsilon, \qquad E = \mu\,\frac{3\lambda+2\mu}{\lambda+\mu}
$$

donde $E$ es el módulo de Young. La relación entre $\lambda$ y $\mu$ y el [[Poisson Ratio|coeficiente de Poisson]] $\nu$ es:

$$
\lambda = \frac{E\nu}{(1+\nu)(1-2\nu)}, \qquad \mu = \frac{E}{2(1+\nu)}
$$

## Extensión viscoelástica

En [[Viscoelastic Media|medios viscoelásticos]], la ley de Hooke instantánea se reemplaza por la **integral de Boltzmann**:

$$
\boldsymbol{\sigma}(t) = \int_{-\infty}^{t} \mathbf{G}(t-\tau) : \frac{d\boldsymbol{\varepsilon}(\tau)}{d\tau}\, d\tau
$$

donde $\mathbf{G}(t)$ es el tensor de función de relajación. En el dominio frecuencial, los módulos elásticos reales se reemplazan por módulos complejos $G^*(\omega)$ — base del [[Correspondence Principle|principio de correspondencia]].

## Relevancia para métodos de ondas superficiales

La ley de Hooke es el fundamento de la relación $V_S = \sqrt{\mu/\rho}$: la [[MASW Method|inversión MASW]] recupera $\mu(z) = \rho(z) V_S^2(z)$, es decir, el perfil del **módulo de corte dinámico** con la profundidad — la cantidad que necesitan los ingenieros para el análisis de respuesta sísmica de sitio y el diseño de cimentaciones dinámicas.

## Véase también

- [[Lamé Constants]] — $\lambda$ y $\mu$ son los parámetros constitutivos de la ley de Hooke isótropa
- [[Navier Equations]] — sistema EDPs que combina Hooke con la ecuación de movimiento
- [[Strain Tensor]] — el tensor $\boldsymbol{\varepsilon}$ que aparece en la ley de Hooke
- [[Poisson Ratio]] — parámetro que relaciona $\lambda$ y $\mu$ con el comportamiento volumétrico
- [[Correspondence Principle]] — extensión viscoelástica de la ley de Hooke

*Fuente: Foti et al. (2014), Sec. 2.1.3, pp. 44–48.*
