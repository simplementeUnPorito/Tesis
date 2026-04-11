---
name: Layered Media
description: Modelo del subsuelo como apilamiento de capas horizontales planas con propiedades elásticas distintas; base física de la dispersión geométrica de ondas superficiales
type: reference
---

# Medios Estratificados (Layered Media)

> [!CONCEPT] Definición
> Los **medios estratificados** (layered media) son el modelo de subsuelo estándar en métodos de ondas superficiales: un apilamiento de $N$ capas horizontales planas, cada una con propiedades elásticas homogéneas ($V_S$, $V_P$, $\rho$, espesor $h$), sobre un semiespacio semi-infinito. La estratificación es la causa de la [[Geometric Dispersion|dispersión geométrica]] de las [[Rayleigh Waves]]: ondas de diferente frecuencia penetran distintas profundidades y "ven" diferentes velocidades, produciendo la curva de dispersión $c_R(f)$ que se invierte para obtener $V_S(z)$.
>
> — Foti et al. (2018), §2.4, pp. 64–95; §6.1, pp. 273–280.

## Intuición física

En un [[Elastic Half Space]] perfectamente homogéneo, las [[Rayleigh Waves]] no son dispersivas: cualquier frecuencia viaja a la misma velocidad (~0.92 Vs). Esto cambia radicalmente cuando el subsuelo está estratificado. Cada frecuencia tiene una longitud de onda diferente y, por tanto, *penetra una profundidad diferente*. Una onda de alta frecuencia (longitud de onda corta) "siente" solo las capas superficiales; una onda de baja frecuencia (longitud de onda larga) penetra profundamente y promedia las propiedades de muchas capas.

Si las capas tienen rigideces distintas, esas ondas de diferente frecuencia viajan a diferentes velocidades: esto es la [[Geometric Dispersion|dispersión geométrica]]. La forma de la curva de dispersión experimental es, en esencia, una firma de cómo varía la rigidez del subsuelo con la profundidad. Este es el principio físico que hace posible la caracterización del subsuelo con métodos de ondas superficiales.

## Definición técnica

Un medio estratificado consiste en $N$ capas horizontales planas superpuestas, numeradas desde la superficie:

| Capa | Espesor | Vs | Vp | ρ |
|---|---|---|---|---|
| 1 | $h_1$ | $V_{S,1}$ | $V_{P,1}$ | $\rho_1$ |
| 2 | $h_2$ | $V_{S,2}$ | $V_{P,2}$ | $\rho_2$ |
| ⋮ | ⋮ | ⋮ | ⋮ | ⋮ |
| N (semiespacio) | ∞ | $V_{S,N}$ | $V_{P,N}$ | $\rho_N$ |

La última capa se modela como un semiespacio semi-infinito. En la interfaz entre capas $n$ y $n+1$ se imponen condiciones de continuidad de desplazamiento y esfuerzo.

## Condiciones de contorno en interfaces

En cada interfaz a profundidad $z = H_n = h_1 + h_2 + \cdots + h_n$, se exige continuidad de las cuatro cantidades:

$$[u_1]^- = [u_1]^+, \quad [u_2]^- = [u_2]^+, \quad [\sigma_{12}]^- = [\sigma_{12}]^+, \quad [\sigma_{22}]^- = [\sigma_{22}]^+$$

donde $u_1$, $u_2$ son desplazamientos horizontal y vertical, y $\sigma_{12}$, $\sigma_{22}$ son los esfuerzos de corte y normal. En la superficie libre ($z = 0$): $\sigma_{12} = \sigma_{22} = 0$.

## Método de la matriz de transferencia (Thomson–Haskell)

El algoritmo de Thomson (1950) y Haskell (1953) propaga la solución analítica capa por capa mediante matrices de transferencia. Para cada capa se construye la **matriz de capa** $\mathbf{T}_n$ que relaciona el estado $\mathbf{f} = [u_1, u_2, \sigma_{12}, \sigma_{22}]^T$ en la superficie superior de la capa con el estado en su superficie inferior:

$$\mathbf{f}(z = H_n^-) = \mathbf{T}_n \cdot \mathbf{f}(z = H_{n-1}^+)$$

La **función secular** se forma aplicando la condición de radiación en el semiespacio (ondas solo descendentes) y la condición de superficie libre. Tiene ceros exactamente en los pares $(k, \omega)$ que corresponden a modos de propagación:

$$\Phi_R[k, \omega; \mathbf{m}] = 0$$

donde $\mathbf{m}$ es el modelo de capas. Resolver esta ecuación para distintas frecuencias da la curva de dispersión.

**Limitación numérica**: la matriz global de Thomson–Haskell es numéricamente inestable a alta frecuencia (los términos exponenciales crecientes/decrecientes de cada capa crean overflow). Esta limitación se supera con la **matriz de rigidez dinámica** (Kausel y Roesset, 1981) o el algoritmo recursivo de Kennett.

## Tipos de perfiles estratificados

**Normalmente dispersivo** (velocidad aumenta con profundidad): el modo fundamental domina y la curva de dispersión tiene pendiente negativa (mayor Vr a baja frecuencia). Es el caso más frecuente en depósitos sedimentarios compactados.

**Inversamente dispersivo** (capa blanda debajo de capa rígida): los modos superiores pueden contribuir significativamente incluso a bajas frecuencias. La curva de dispersión tiene pendiente positiva en parte del rango. La inversión asumiendo modo fundamental introduce errores severos.

**Presencia de capa blanda intercalada** (velocity reversal): genera energía atrapada dentro de la capa suave, excitando modos superiores con frecuencias de corte definidas. Este es el caso más problemático para inversión estándar.

## Parámetros del modelo y sensibilidad

Los parámetros del modelo de capas son:
- **Incógnitas primarias**: $V_{S,n}$ (espesores $h_n$ pueden también ser incógnitas)
- **Parámetros a priori**: $V_{P,n}$ (o ratio de Poisson), $\rho_n$, posición del nivel freático

La sensibilidad de la curva de dispersión a $V_S$ es alta; la sensibilidad a $V_P$ y $\rho$ es mucho menor. Esto justifica el procedimiento estándar de fijar $V_P$ y $\rho$ a partir de información geológica o refracción P y concentrar la inversión en $V_S$.

## Implicación práctica en MASW

El modelo de capas horizontales es el supuesto estándar de todos los métodos de inversión de ondas superficiales (MASW, SASW, métodos pasivos). Sus implicaciones en la adquisición:

- **Apertura del arreglo**: debe cubrir al menos las longitudes de onda más largas de interés ($\lambda_{\max} = V_{R,\min}/f_{\min}$) para resolver las capas más profundas.
- **Espaciado entre receptores**: determina la frecuencia máxima antes del aliasing espacial ($\Delta x \leq \lambda_{\min}/2$).
- **Variaciones laterales**: el modelo de capas horizontales es un supuesto 1D. Si existen buzamientos o heterogeneidades laterales, la inversión produce un perfil promediado cuya representatividad depende de la longitud del arreglo.

## Relaciones con otros conceptos

- [[Elastic Half Space]] — caso límite N = 1 (semiespacio homogéneo, sin dispersión)
- [[Vertically Inhomogeneous Media]] — generalización continua del modelo de capas
- [[Dispersion Relation]] — la forma de la curva de dispersión es determinada por el modelo de capas
- [[Surface Wave Modes]] — en medios estratificados existen múltiples modos de propagación
- [[Mode Superposition]] — el campo registrado es superposición de modos del sistema estratificado
- [[Rayleigh Eigenproblem]] — el problema de autovalores que define los modos de Rayleigh en capas

> [!EXAMPLE] Evidencia empírica: Xia et al. (1999) — modelo de capas como base de la inversión MASW
> **Paper 002 (Xia, Miller & Park 1999)** implementa el modelo de capas horizontales como estructura del problema inverso de MASW. El modelo de prueba usa 8 capas con espesores entre 1.5 m y 14 m, y la curva de dispersión teórica se calcula con el método de Thomson-Haskell para cada iteración de inversión. Los sitios de Kansas validados tienen perfiles $V_S$ que varían de 150 m/s (capa superficial) a 400 m/s (semiespacio), confirmando que el modelo de capas horizontales es adecuado para suelos sedimentarios con estratificación aproximadamente horizontal.
>
> — Research Database, entrada 002 (core).

## Referencias

| Fuente | Sección / Página |
|--------|-----------------|
| Foti et al. (2018), *Surface Wave Methods* | §2.4, pp. 64–76 — formulación completa |
| Foti et al. (2018), *Surface Wave Methods* | §6.1, pp. 273–280 — uso en inversión |
| Thomson (1950), *J. Appl. Phys.* | 21, 89–93 — matriz de transferencia original |
| Haskell (1953), *Bull. Seismol. Soc. Am.* | 43, 17–34 — extensión a P-SV |
| Xia, Miller & Park (1999), *Geophysics* 64(3) | Paper 002 — modelo de capas en inversión MASW |
