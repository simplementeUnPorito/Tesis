---
name: Lamb's Problem
description: Solución clásica (Lamb 1904) para la generación de ondas elásticas por carga puntual en la superficie de un semiespacio; demuestra que las ondas de Rayleigh dominan el campo de onda superficial en el campo lejano y que decaen como 1/√r
type: reference
---

# Problema de Lamb (Lamb's Problem)

> **Contexto:** El Problema de Lamb es la solución analítica exacta para el campo de ondas generado por una carga puntual aplicada sobre la superficie de un [[Elastic Half Space|semiespacio elástico]] homogéneo e isótropo. Publicado por Horace Lamb en 1904, constituye la base teórica que justifica por qué los registros sísmicos de superficie están dominados por ondas de Rayleigh, y establece el criterio de **campo cercano vs. campo lejano** que determina el offset mínimo en MASW.
> **Fuente:** Foti et al. (2014), Cap. 2.2.1, pp. 52–60.

## Contexto histórico

En 1904, Horace Lamb resolvió analíticamente el problema de determinar el campo de desplazamientos en la superficie de un semiespacio elástico sometido a una carga puntual impulsiva vertical. La solución, obtenida mediante transformadas de Laplace y técnicas de residuos, mostró por primera vez que las ondas de Rayleigh no son solo una solución matemática abstracta sino la **contribución dominante** del campo de ondas en condiciones realistas de excitación superficial. Este resultado es el fundamento teórico de todos los métodos sísmicos de superficie.

## Formulación del problema

El problema considera:
- Medio: [[Elastic Half Space]] elástico, homogéneo, isótropo.
- Condición de contorno: carga vertical puntual (t) = F_0\,\delta(t)$ aplicada en el punto $ de la superficie libre.
- Incógnita: desplazamientos (x, z, t)$ y (x, z, t)$ en la superficie y en el interior.

La solución exacta involucra la suma de contribuciones de ondas P, ondas S y ondas de Rayleigh, cada una expresada como una integral de contorno en el plano complejo. Los polos del integrando corresponden a las raíces de la [[Rayleigh Waves|ecuación secular de Rayleigh]], y la contribución de residuos en estos polos es la onda de Rayleigh.

## Resultado principal: dominancia de las ondas de Rayleigh

La solución muestra que a distancias $ **grandes respecto a la longitud de onda** ( \gg \lambda_R$), el campo en la superficie está dominado por la onda de Rayleigh. La partición de energía es aproximadamente:

| Tipo de onda | Fracción de energía | Decaimiento de amplitud en superficie |
|---|---|---|
| Ondas de Rayleigh | ~67% | $\propto 1/\sqrt{r}$ |
| Ondas S (de cuerpo) | ~26% | $\propto 1/r$ |
| Ondas P (de cuerpo) | ~7% | $\propto 1/r$ |

Las ondas de Rayleigh decaen más lentamente porque su energía se propaga en 2D (frente cilíndrico, perímetro $\propto r$), mientras que las ondas de cuerpo decaen en 3D (frente esférico, área $\propto r^2$). A distancias moderadas (unos pocos metros a decenas de metros en MASW), las ondas de Rayleigh son el componente señal; las ondas de cuerpo son ruido que decae más rápido.

## Campo cercano y campo lejano

El resultado de Lamb no es uniforme en distancia: distingue dos regímenes.

### Campo lejano ( \gg \lambda_R$)

A grandes distancias, la solución puede aproximarse por expansión asintótica. Las ondas de Rayleigh, P y S están bien separadas en tiempo (el sismograma muestra primeras llegadas P, luego S, luego ground-roll de Rayleigh). El campo está en **campo lejano** (far-field): la curvatura del frente de onda es despreciable y las ondas se pueden tratar como planas.

### Campo cercano ( \lesssim \lambda_R/2$)

Cerca de la fuente, las contribuciones de ondas P, S y Rayleigh no están separadas; sus frentes de onda se superponen y el campo es complejo. En esta zona:
- La velocidad de fase **aparente** medida por un arreglo de geófonos difiere de la velocidad de fase real de Rayleigh.
- La superposición de ondas de cuerpo introduce un sesgo sistemático en la curva de dispersión.
- La hipótesis de onda plana del análisis f-k estándar no es válida.

La transición entre ambos regímenes ocurre aproximadamente a:

274271x_{\min} pprox rac{\lambda_{R,\max}}{2}274271

donde $\lambda_{R,\max} = V_{R,\min}/f_{\min}$ es la longitud de onda más larga del experimento. Esta es la **regla del offset mínimo** para el diseño de arreglos MASW.

## Implicaciones para el diseño del arreglo MASW

La condición de campo lejano implica que el primer geófono del arreglo debe estar al menos a {\min}$ de la fuente:

274271x_{\min} pprox rac{\lambda_{R,\max}}{2} = rac{V_{R,\min}}{2\,f_{\min}}274271

Si este offset mínimo no se respeta, las frecuencias bajas (correspondientes a $\lambda$ largas) están en campo cercano y la curva de dispersión a esas frecuencias estará sesgada hacia velocidades artificialmente altas (por contaminación de ondas de cuerpo más rápidas).

**Ejemplo**: con  pprox 200$ m/s y {\min} = 5$ Hz:
274271x_{\min} pprox rac{200}{2 	imes 5} = 20 	ext{ m}274271

El arreglo debe comenzar a $\geq m de la fuente para que todas las frecuencias estén en campo lejano. Esto está en tensión con el requisito de distancia máxima para atenuación (offset máximo $pprox L/2$): el diseño del arreglo requiere equilibrar ambos criterios.

## Extensiones del Problema de Lamb

La solución original de Lamb (1904) para fuente vertical impulsiva ha sido extendida a:
- **Fuente horizontal**: produce principalmente ondas SH y SV, con menor contribución de Rayleigh.
- **Fuente en el interior del semiespacio** (solución de Stokes): genera ondas de cuerpo directas y ondas de Rayleigh por conversión en la superficie.
- **Medio estratificado**: la solución exacta no existe analíticamente; se calcula numéricamente mediante el [[Layered Media|método de la matriz de transferencia]].

## Referencias

- Foti et al. (2014), Cap. 2.2.1, pp. 52–60 — solución de Lamb, partición de energía y criterio de campo cercano.
- Lamb, H. (1904), *On the propagation of tremors over the surface of an elastic solid*, Phil. Trans. R. Soc. Lond. A, 203, 1–42.
