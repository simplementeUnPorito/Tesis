---
name: Hann Window
description: Función de ventana temporal que reduce la fuga espectral en el análisis de Fourier de señales sísmicas — estándar en procesamiento [[MASW Method|MASW]] para espectrogramas f-k
type: reference
---

# Hann Window — Ventana de Hann (Von Hann)

> [!CONCEPT] Definición
> La **ventana de Hann** (también llamada "ventana de von Hann" o incorrectamente "ventana de Hanning") es una función de apodización temporal que reduce la **fuga espectral** (*spectral leakage*) en el análisis de Fourier de señales sísmicas. Se define como:
> $$w(n) = \frac{1}{2}\left[1 - \cos\!\left(\frac{2\pi n}{N-1}\right)\right], \quad n = 0, 1, \ldots, N-1$$
> La aplicación de la ventana multiplica la señal temporal antes de la [[2D Fourier Transform|Transformada de Fourier]]: $x_w(n) = x(n) \cdot w(n)$. Esto hace que la señal comience y termine en cero, eliminando las discontinuidades en los bordes del segmento que causan fuga espectral — energía que se "derrama" desde el pico real hacia frecuencias adyacentes. En [[MASW Method|MASW]], la ventana de Hann se aplica tanto en el **dominio temporal** (antes de la FFT temporal) como en el **dominio espacial** (sobre el arreglo de geófonos antes de la FFT espacial) para mejorar la resolución del espectrograma f-k y reducir los lóbulos laterales. **Compromiso**: la ventana reduce el ancho de banda efectivo de la señal en un factor ~1.5, disminuyendo la resolución espectral; se compensa usando segmentos suficientemente largos.
>
> — Foti et al. (2018), Cap. 4, §4.2; Harris (1978), *Proc. IEEE*.

## Propiedades espectrales

La Transformada de Fourier de la ventana de Hann es una sinc modificada con lóbulos laterales de −31.5 dB (vs −13 dB de la ventana rectangular). El ancho del lóbulo principal (lóbulo central) es el doble que la ventana rectangular:

| Propiedad | Ventana rectangular | Ventana de Hann |
|-----------|-------------------|-----------------|
| Lóbulo lateral (dB) | −13 dB | −31.5 dB |
| Ancho lóbulo principal | $2/N$ | $4/N$ |
| Pérdida de coherencia | 0 dB | 1.5 dB |
| Pérdida de resolución | 0 | Factor 2 |

**En [[MASW Method|MASW]]**: la reducción de −31.5 dB en lóbulos laterales es crucial para resolver el **modo fundamental** de Rayleigh cuando hay modos superiores cercanos en el espectrograma f-k. Sin ventana, los lóbulos laterales del modo fundamental pueden contaminar la energía del modo 1, confundiendo la identificación modal.

## Aplicación en el dominio espacial

En el dominio espacial (a lo largo del arreglo de $N$ geófonos), la ventana de Hann actúa como un **tapering** del arreglo:

$$g_w(x_j) = g(x_j) \cdot w(j)$$

El efecto en el espectrograma f-k es análogo al temporal: reduce los **grating lobes** (lóbulos de rejilla) que aparecen periódicamente en el espectro de [[Wavenumber|número de onda]] $k$ a intervalos de $2\pi/\Delta x$. Esto mejora la claridad de la cresta modal en el espectrograma.

## Comparación con otras ventanas en contexto sísmico

| Ventana | Atenuación lóbulos | Resolución | Uso típico |
|---------|-------------------|------------|------------|
| Rectangular | −13 dB | Máxima | Sin ventana (no recomendado) |
| Hann | −31.5 dB | Media | [[MASW Method|MASW]] estándar |
| Hamming | −42 dB | Media | [[SASW Method|SASW]], señales largas |
| Blackman | −58 dB | Baja | Análisis modal de alta precisión |
| Kaiser-Bessel | Ajustable | Ajustable | Flexible según SNR |

> [!EXAMPLE] Evidencia empírica: Park et al. (1999) — ventana temporal en espectrograma f-k [[MASW Method|MASW]]
> **Paper 001 (Park, Miller & Xia 1999)** describe el procesamiento del sismograma de Kansas usando una ventana de Hann temporal aplicada antes de la [[2D Fourier Transform|FFT 2D]]. El espectrograma f-k resultante (Fig. 2 del paper) muestra la cresta del modo fundamental de Rayleigh con lóbulos laterales bien suprimidos en el rango 5–50 Hz — la ventana de Hann produce una cresta limpia sin contaminación de modos superiores. Los autores justifican el uso de la ventana de Hann (frente a la rectangular) citando la mejora en la relación señal-lóbulo-lateral de ~18 dB, que es crítica para el [[Picking|picking]] preciso de la [[Dispersion Curve|curva de dispersión]] en el espectrograma. El mismo protocolo de ventana se adoptó como estándar en las implementaciones SurfSeis (KGS) y posteriores.
>
> — Research Database, entrada 001 (core); Park, Miller & Xia (1999), *Geophysics* 64(3):800–808.

## Referencias

| Fuente | Sección / Página |
|--------|-----------------|
| Foti et al. (2018), *Surface Wave Methods* | Cap. 4, §4.2 — procesamiento f-k y ventanas |
| Park, Miller & Xia (1999), *Geophysics* 64(3) | Paper 001 — ventana Hann en espectrograma [[MASW Method|MASW]] |
| Harris (1978), *Proc. IEEE* | Revisión de ventanas para análisis espectral |
