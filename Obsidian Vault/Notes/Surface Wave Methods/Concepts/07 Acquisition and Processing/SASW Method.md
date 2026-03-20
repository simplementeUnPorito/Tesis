---
name: SASW Method
description: Spectral Analysis of Surface Waves — método de dos estaciones para obtener la curva de dispersión a partir del espectro cruzado entre pares de receptores
type: reference
---

# SASW Method — Análisis Espectral de Ondas Superficiales

> **Fuente:** Sebastiano Foti, Chapters 4 y 7 · Nazarian & Stokoe (1984)

## Intuición física

El método SASW explota el hecho de que las [[Rayleigh Waves|ondas de Rayleigh]] son dispersivas: diferentes frecuencias viajan a distintas velocidades. Si se coloca un par de sensores a una distancia conocida y se mide el retardo temporal con que llega cada componente de frecuencia, puede calcularse la [[Phase Velocity|velocidad de fase]] como función de la frecuencia. La colección de estos pares velocidad-frecuencia constituye la [[Dispersion Curve|curva de dispersión experimental]].

## Definición técnica

SASW es un método de dos estaciones que evalúa la velocidad de fase de las ondas de superficie mediante el análisis del espectro cruzado entre dos receptores alineados con la fuente. El procedimiento fue formalizado por Nazarian & Stokoe (1984) como extensión del método SSRM para múltiples separaciones de receptor.

## Procedimiento de medición

1. **Generación de la onda:** fuente activa (impacto, vibrador electromecánico swept-sine) en superficie.
2. **Registro de la señal:** dos receptores colocados a distancias $x_1$ y $x_2$ de la fuente (o un par a distancia $\Delta x$ entre ellos).
3. **Cálculo del espectro cruzado (Cross-Power Spectrum, CPS):**
   $$G_{12}(f) = X_1^*(f) \cdot X_2(f)$$
   donde $X_1, X_2$ son las DFTs de las señales.
4. **Extracción de la fase:** $\phi(f) = \arg[G_{12}(f)]$ — representa el retardo de fase acumulado al propagarse entre los dos receptores.
5. **Cálculo de la velocidad de fase:**
   $$V_R(f) = \frac{2\pi f \cdot \Delta x}{\phi(f)}$$
6. **Evaluación de la coherencia:**
   $$\gamma^2(f) = \frac{|G_{12}(f)|^2}{G_{11}(f) \cdot G_{22}(f)}$$
   Solo se retienen los pares (f, VR) donde γ² ≈ 1 (alta SNR).

## Phase unwrapping

La fase $\phi(f)$ es periódica en el intervalo $(-\pi, \pi]$. Para grandes distancias entre receptores o bajas frecuencias, la fase acumulada puede superar $2\pi$, generando saltos aparentes. El proceso de **phase unwrapping** consiste en identificar y corregir dichos saltos para obtener una fase continua. Un error de unwrapping se propaga directamente como un error en la velocidad de fase:

$$\Delta V_R = \frac{2\pi f \cdot \Delta x}{(\phi \pm 2\pi)^2} \cdot 2\pi$$

La corrección es más difícil en frecuencias bajas donde el SNR es bajo. Esta es la limitación principal del método SASW.

## Estrategia multi-par

Para cubrir un rango amplio de frecuencias y profundidades:
- **Receptores cercanos** → alta frecuencia, alta SNR, buena resolución superficial.
- **Receptores lejanos** → baja frecuencia, mayor profundidad de investigación.

Las ramas de la curva de dispersión de distintos pares deben superponerse en los rangos de frecuencia compartidos. Discrepancias entre ramas son una señal de alerta de errores de unwrapping o de la presencia de [[Surface Wave Modes|modos superiores]].

## Implicación en geófonos / MASW

El SASW es el precursor directo del [[MASW]] (que generaliza a múltiples estaciones simultáneas), y del método [[MOPA]]. Con geófonos de campo, el SASW puede implementarse con solo dos canales activos, siendo útil cuando los recursos de hardware son limitados. Sin embargo, su sensibilidad al phase unwrapping y la necesidad de repetir el ensayo para múltiples separaciones hacen que los métodos multiestación (f-k, MASW) sean preferibles cuando se dispone de más canales.

## Comparación con f-k

| Característica | SASW (2 estaciones) | f-k / MASW (multiestación) |
|---|---|---|
| Hardware mínimo | 2 geófonos | ≥8 geófonos |
| Sensibilidad a phase unwrapping | Alta | Baja (max espectral) |
| Juicio del operador | Requerido | Menor |
| Rango de frecuencia | Depende del par | Función del arreglo completo |
| Identificación de modos | Difícil | Posible con alta resolución |

## Referencias
- Nazarian, S. & Stokoe, K.H. (1984). In situ shear wave velocities from spectral analysis of surface waves. *8th World Conference on Earthquake Engineering*, San Francisco.
- Foti, S. et al. (2014). *Surface Wave Methods for Near-Surface Site Characterization*, CRC Press. Cap. 4, 7.
