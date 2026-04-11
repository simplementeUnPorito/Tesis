---
name: Cross-Power Spectrum
description: Espectro cruzado entre dos señales sísmicas — base del método SASW para extraer la fase (y por tanto la velocidad de fase) entre pares de receptores
type: reference
---

# Cross-Power Spectrum — Espectro de Potencia Cruzado

> [!CONCEPT] Definición
> El **espectro de potencia cruzado** (o *cross-power spectrum*, CPS) entre dos señales sísmicas $u_1(t)$ y $u_2(t)$ es la transformada de Fourier de su función de correlación cruzada: $G_{12}(f) = U_1^*(f) \cdot U_2(f)$, donde $U_1, U_2$ son las DFTs de las señales. Su **fase** $\phi_{12}(f) = \angle[G_{12}(f)]$ contiene el retardo de fase entre los dos receptores, directamente relacionado con la velocidad de fase: $c_R(f) = 2\pi f \Delta x / \phi_{12}(f)$ ([[SASW Method|método SASW]]). Su **módulo** normalizado es la [[Coherence Function|función de coherencia]] $\gamma^2(f) = |G_{12}|^2 / (G_{11} \cdot G_{22})$ — indicador de calidad SNR para cada frecuencia. El CPS es el procesamiento central del [[SASW Method|SASW]] y se usa también en el [[MOPA|método MOPA]] como herramienta de diagnóstico de calidad. Se estima en la práctica promediando sobre múltiples disparos: $\hat{G}_{12}(f) = \frac{1}{N_{shots}} \sum_s U_{1,s}^*(f) U_{2,s}(f)$.
>
> — Nazarian & Stokoe (1984), Paper 003; Foti et al. (2018), Cap. 4, §4.2.

## Definición matemática

Para dos señales $u_1(t)$ y $u_2(t)$ con DFTs $U_1(f)$ y $U_2(f)$:

$$G_{12}(f) = U_1^*(f) \cdot U_2(f) = |G_{12}(f)| \cdot e^{i\phi_{12}(f)}$$

La **fase** del CPS:
$$\phi_{12}(f) = \angle[G_{12}(f)] = \angle[U_2(f)] - \angle[U_1(f)]$$

La **velocidad de fase** (SASW):
$$c_R(f) = \frac{2\pi f \cdot \Delta x}{\phi_{12}(f)}$$

donde $\Delta x$ es la separación entre los dos receptores.

## Estimación práctica

En campo se promedian múltiples disparos para reducir el ruido incoherente:
$$\hat{G}_{12}(f) = \frac{1}{N} \sum_{s=1}^{N} U_{1,s}^*(f) \cdot U_{2,s}(f)$$

El promediado mejora la SNR: el ruido incoherente decrece como $1/\sqrt{N}$, mientras que la señal coherente (ondas de Rayleigh) se acumula.

## Phase unwrapping

La fase $\phi_{12}(f)$ del CPS está restringida al intervalo $(-\pi, \pi]$. Para grandes separaciones $\Delta x$ o bajas frecuencias, el retardo de fase puede superar $2\pi$, produciendo saltos de $\pm2\pi$ (*phase wrapping*). El **phase unwrapping** detecta y corrige estos saltos para obtener una fase continua. Errores de unwrapping se propagan directamente como errores en $c_R(f)$ — la limitación principal del [[SASW Method|método SASW]] con solo dos receptores.

> [!EXAMPLE] Evidencia empírica: Nazarian & Stokoe (1984) — espectro cruzado como base del SASW
> **Paper 003 (Nazarian & Stokoe 1984)** introduce el espectro cruzado entre pares de receptores como la herramienta central para extraer la velocidad de fase de ondas de Rayleigh en el [[SASW Method|método SASW]]. Los autores demuestran que la fase de $G_{12}(f)$, una vez corregida por phase unwrapping, es proporcional al número de onda del modo fundamental de Rayleigh con alta precisión en el rango de frecuencias con alta coherencia ($\gamma^2 > 0.9$). El trabajo establece el uso del CPS como estimador eficiente de la velocidad de fase para dos receptores, sin necesidad de un arreglo multicanal completo — clave en la época (1984) cuando los sismógrafos de muchos canales no estaban disponibles comercialmente.
>
> — Research Database, entrada 003 (core); Nazarian & Stokoe (1984), *8th World Conf. on Earthquake Engineering*.

## Referencias

| Fuente | Sección / Página |
|--------|-----------------|
| Foti et al. (2018), *Surface Wave Methods* | Cap. 4, §4.2 — CPS en procesamiento SASW/MASW |
| Nazarian & Stokoe (1984), *8th WCEE* | Paper 003 — espectro cruzado como base del SASW |
