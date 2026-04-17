---
name: Ill-Posed Problem
description: Problema matemático que no satisface los criterios de Hadamard — la inversión de la [[Dispersion Curve|curva de dispersión]] es ill-posed por [[Non-uniqueness|no-unicidad]] y falta de estabilidad, requiriendo [[Regularization|regularización]]
type: reference
---

# Ill-Posed Problem — Problema Mal Planteado (Hadamard)

> [!CONCEPT] Definición
> Un **problema bien planteado** (*well-posed problem*, según Hadamard 1902) satisface tres condiciones: (1) **existencia** de solución, (2) **unicidad** de la solución, y (3) **estabilidad** — la solución depende continuamente de los datos. Un **problema mal planteado** (*ill-posed problem*) viola al menos una de estas condiciones. La [[Inversión|inversión]] de la [[Dispersion Curve|curva de dispersión]] de ondas de Rayleigh es un problema mal planteado por las razones siguientes:
> - **Unicidad violada**: múltiples perfiles $V_S(z)$ producen la misma [[Dispersion Curve|curva de dispersión]] (dentro de la incertidumbre experimental) → [[Non-uniqueness|no-unicidad]] inherente al problema inverso
> - **Estabilidad violada**: pequeñas perturbaciones en los datos $c_R(f)$ producen grandes cambios en el modelo $V_S(z)$ — especialmente a profundidades cercanas al límite de resolución → inestabilidad numérica
> La violación de la unicidad es el aspecto dominante: la inversión de [[MASW Method|MASW]] produce una **familia de modelos equivalentes**, no un único modelo verdadero. El tratamiento estándar del ill-posedness es la **[[Regularization|regularización]]** ([[Tikhonov Regularization]]), que añade información a priori (suavidad del modelo) para seleccionar una solución única y estable dentro de la familia de modelos equivalentes.
>
> — Foti et al. (2018), §6.4; Tarantola (2005), §1.2; Hadamard (1902).

## Criterios de Hadamard aplicados a [[MASW Method|MASW]]

| Criterio | Estado en inversión [[MASW Method|MASW]] | Consecuencia |
|---------|------------------------|-------------|
| Existencia | Generalmente satisfecho | La [[Dispersion Curve|curva de dispersión]] observada siempre tiene al menos un modelo consistente |
| Unicidad | **Violado** | Familia de soluciones equivalentes → [[Non-uniqueness|no-unicidad]] |
| Estabilidad | **Violado parcialmente** | Amplificación del error de datos en el modelo → necesita [[Tikhonov Regularization|regularización]] |

## Fuentes de la ill-posedness en [[MASW Method|MASW]]

1. **Finitud del rango de frecuencias**: la [[Dispersion Curve|curva de dispersión]] se mide en $[f_{min}, f_{max}]$ → el perfil $V_S(z)$ solo se puede resolver para $z \in [c_{R,min}/(3f_{max}), c_{R,max}/(3f_{min})]$ → información nula fuera de este rango
2. **Equivalencia paramétrica**: el mismo perfil $V_S(z)$ puede representarse con diferente número de capas, diferentes espesores, etc. → infinitos modelos parametrizados equivalentes
3. **Insensibilidad a parámetros**: $c_R$ es muy insensible a $V_P$ (en suelos saturados) y a $\rho$ → estos parámetros no pueden determinarse por [[MASW Method|MASW]] → se deben fijar a priori

## [[Regularization|Regularización]] como tratamiento estándar

El problema mal planteado se convierte en uno bien planteado (regularizado) reemplazando la minimización del misfit puro por la minimización del **funcional de Tikhonov**:

$$\Phi(\mathbf{m}) = \|\mathbf{d} - F(\mathbf{m})\|^2 + \lambda \|\mathbf{Rm}\|^2$$

El término $\lambda \|\mathbf{Rm}\|^2$ ([[Regularization|regularización]]) actúa como información a priori que selecciona el modelo más suave (más simple) con buen ajuste a los datos — transformando el problema ill-posed en uno well-posed.

> [!EXAMPLE] Evidencia empírica: Tarantola (2005) — ill-posedness en inversión geofísica
> Tarantola (2005, §1.2) formaliza la noción de ill-posedness en el contexto de la inversión geofísica, distinguiendo entre los problemas de datos insuficientes (información faltante → [[Non-uniqueness|no-unicidad]]) y datos ruidosos (información imprecisa → inestabilidad). Para la inversión de [[Dispersion Curve|curvas de dispersión]], Foti et al. (2018, §6.4) cuantifican la ill-posedness: en el sitio La Salle con 30 puntos de dispersión, el espacio de modelos aceptables (misfit < umbral estadístico) comprende ~500 de 100,000 modelos evaluados por [[Monte Carlo Methods|Monte Carlo]] — todos con el mismo misfit estadísticamente, pero con $[[Vs30|Vs,30]]$ variando 480–505 m/s. Esta variabilidad cuantifica el grado de ill-posedness residual del problema, que no puede reducirse sin información adicional (pozos, refracción, [[HVSR|HVSR]]).
>
> — Tarantola (2005), §1.2; Foti et al. (2018), §6.4, pp. 285–295.

## Referencias

| Fuente | Sección / Página |
|--------|-----------------|
| Foti et al. (2018), *Surface Wave Methods* | §6.4, pp. 285–295 — ill-posedness en inversión [[MASW Method|MASW]] |
| Tarantola (2005), *Inverse Problem Theory* | §1.2 — formulación del ill-posedness |
| Hadamard (1902) | Criterios originales de problema bien planteado |
