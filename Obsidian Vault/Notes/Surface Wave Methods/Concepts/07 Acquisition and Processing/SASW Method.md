---
name: SASW Method
description: Spectral Analysis of Surface Waves — método de dos estaciones para obtener la [[Dispersion Curve|curva de dispersión]] a partir del espectro cruzado entre pares de receptores
type: reference
---

# SASW Method — Análisis Espectral de Ondas Superficiales

> [!CONCEPT] Definición
> El **SASW** (*Spectral Analysis of Surface Waves*, Nazarian & Stokoe 1984) es el precursor del [[MASW Method|MASW]]: un método de **dos estaciones** que extrae la [[Phase Velocity|velocidad de fase]] de las [[Rayleigh Waves|ondas de Rayleigh]] a partir de la **fase del espectro cruzado** entre dos receptores. Su principal limitación es el *phase unwrapping*: la fase medida es periódica en $(-\pi, \pi]$ y debe desenvuelta continuamente — errores de unwrapping producen errores directos en la [[Dispersion Curve|curva de dispersión]]. Requiere múltiples adquisiciones con diferentes separaciones de receptor para cubrir un rango amplio de frecuencias.
>
> — Nazarian & Stokoe (1984), *8th WCEE*; Foti et al. (2018), Caps. 4 y 7.

## Intuición física

El método SASW explota el hecho de que las [[Rayleigh Waves|ondas de Rayleigh]] son dispersivas: diferentes frecuencias viajan a distintas velocidades. Si se coloca un par de sensores a una distancia conocida y se mide el retardo temporal con que llega cada componente de frecuencia, puede calcularse la [[Phase Velocity|velocidad de fase]] como función de la frecuencia. La colección de estos pares velocidad-frecuencia constituye la [[Dispersion Curve|curva de dispersión experimental]].

## Definición técnica

SASW es un método de dos estaciones que evalúa la [[Phase Velocity|velocidad de fase]] de las ondas de superficie mediante el análisis del espectro cruzado entre dos receptores alineados con la fuente. El procedimiento fue formalizado por Nazarian & Stokoe (1984) como extensión del método SSRM para múltiples separaciones de receptor.

## Procedimiento de medición

1. **Generación de la onda:** fuente activa (impacto, vibrador electromecánico swept-sine) en superficie.
2. **Registro de la señal:** dos receptores colocados a distancias $x_1$ y $x_2$ de la fuente (o un par a distancia $\Delta x$ entre ellos).
3. **Cálculo del espectro cruzado (Cross-Power Spectrum, CPS):**
   $$G_{12}(f) = X_1^*(f) \cdot X_2(f)$$
   donde $X_1, X_2$ son las DFTs de las señales.
4. **Extracción de la fase:** $\phi(f) = \arg[G_{12}(f)]$ — representa el retardo de fase acumulado al propagarse entre los dos receptores.
5. **Cálculo de la [[Phase Velocity|velocidad de fase]]:**
   $$V_R(f) = \frac{2\pi f \cdot \Delta x}{\phi(f)}$$
6. **Evaluación de la coherencia:**
   $$\gamma^2(f) = \frac{|G_{12}(f)|^2}{G_{11}(f) \cdot G_{22}(f)}$$
   Solo se retienen los pares (f, VR) donde γ² ≈ 1 (alta SNR).

## Phase unwrapping

La fase $\phi(f)$ es periódica en el intervalo $(-\pi, \pi]$. Para grandes distancias entre receptores o bajas frecuencias, la fase acumulada puede superar $2\pi$, generando saltos aparentes. El proceso de **phase unwrapping** consiste en identificar y corregir dichos saltos para obtener una fase continua. Un error de unwrapping se propaga directamente como un error en la [[Phase Velocity|velocidad de fase]]:

$$\Delta V_R = \frac{2\pi f \cdot \Delta x}{(\phi \pm 2\pi)^2} \cdot 2\pi$$

La corrección es más difícil en frecuencias bajas donde el SNR es bajo. Esta es la limitación principal del método SASW.

## Estrategia multi-par

Para cubrir un rango amplio de frecuencias y profundidades:
- **Receptores cercanos** → alta frecuencia, alta SNR, buena resolución superficial.
- **Receptores lejanos** → baja frecuencia, mayor profundidad de investigación.

Las ramas de la [[Dispersion Curve|curva de dispersión]] de distintos pares deben superponerse en los rangos de frecuencia compartidos. Discrepancias entre ramas son una señal de alerta de errores de unwrapping o de la presencia de [[Surface Wave Modes|modos superiores]].

## Implicación en geófonos / [[MASW Method|MASW]]

El SASW es el precursor directo del [[MASW Method]] (que generaliza a múltiples estaciones simultáneas), y del método [[MOPA]]. Con geófonos de campo, el SASW puede implementarse con solo dos canales activos, siendo útil cuando los recursos de hardware son limitados. Sin embargo, su sensibilidad al phase unwrapping y la necesidad de repetir el ensayo para múltiples separaciones hacen que los métodos multiestación (f-k, [[MASW Method|MASW]]) sean preferibles cuando se dispone de más canales.

## Comparación con f-k

| Característica | SASW (2 estaciones) | f-k / [[MASW Method|MASW]] (multiestación) |
|---|---|---|
| Hardware mínimo | 2 geófonos | ≥8 geófonos |
| Sensibilidad a phase unwrapping | Alta | Baja (max espectral) |
| Juicio del operador | Requerido | Menor |
| Rango de frecuencia | Depende del par | Función del arreglo completo |
| Identificación de modos | Difícil | Posible con alta resolución |

> [!EXAMPLE] Evidencia empírica: Nazarian & Stokoe (1984) — fundación del SASW como método de caracterización
> **Paper 003 (Nazarian & Stokoe 1984)** introduce formalmente el método SASW para determinar $V_S(z)$ in situ a partir de la dispersión geométrica de ondas de Rayleigh. Los autores aplican el método en múltiples sitios con suelos de diversas características y demuestran que la [[Dispersion Curve|curva de dispersión]] extraída mediante espectro cruzado, una vez invertida, produce perfiles $V_S(z)$ consistentes con ensayos de campo independientes. El trabajo establece el marco metodológico completo: fuente activa, dos receptores, espectro cruzado, phase unwrapping, y regla de profundidad $z \approx \lambda/2$.
>
> — Research Database, entrada 003 (core).

## Referencias

| Fuente | Sección / Página |
|--------|-----------------|
| Nazarian & Stokoe (1984), *8th WCEE* | Paper 003 — método SASW original |
| Foti et al. (2018), *Surface Wave Methods* | Caps. 4, 7 — procesamiento y aplicaciones |
