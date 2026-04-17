---
name: Tau-P Transform
description: Transformada slant-stack que convierte registros tiempo-espacio a intercepción temporal-slowness; alternativa al análisis f-k para extracción de la [[Dispersion Curve|curva de dispersión]] en [[MASW Method|MASW]]
type: reference
---

# Tau-P Transform — Transformada Tau-P (Slant-Stack)

> [!CONCEPT] Definición
> La **transformada $\tau$-$p$** (o *slant-stack*) transforma el sismograma $u(x, t)$ del dominio tiempo-espacio al dominio intercepción temporal–slowness ($\tau$-$p$), acumulando energía a lo largo de líneas de pendiente $p = 1/c_p$ (slowness): $S(\tau, p) = \sum_j u(x_j, \tau + p\cdot x_j)$. Es numéricamente equivalente al análisis f-k ([[2D Fourier Transform|2D FFT]]) — ambos son transformadas de Fourier 2D — pero con diferentes propiedades de resolución y sensibilidad al ruido. En el espacio $\tau$-$p$, los modos de [[Rayleigh Waves|Rayleigh]] aparecen como crestas a la slowness $p^* = 1/c_R(f)$ del modo dominante. La resolución en slowness es $\Delta p \propto 1/(D \cdot f)$: mejor en altas frecuencias y arreglos largos. Se implementa eficientemente mediante la DFT en el dominio de la frecuencia: para cada $f$, se acumula la DFT espacial con fase lineal $e^{i2\pi f p x_j}$.
>
> — Foti et al. (2018), Cap. 4, §4.3, pp. 216–220; McMechan & Yedlin (1981).

## Definición matemática

**Dominio tiempo** (slant-stack directo):
$$S(\tau, p) = \sum_{j=1}^{N_x} u(x_j, \tau + p\, x_j)$$

**Dominio frecuencia** (implementación eficiente):
$$S(f, p) = \sum_{j=1}^{N_x} U(x_j, f)\, e^{i 2\pi f p x_j}$$

donde $U(x_j, f) = \text{FFT}[u(x_j, \cdot)]$. El máximo de $|S(f, p)|$ para cada $f$ da la slowness $p^*(f) = 1/c_R(f)$.

## Comparación con análisis f-k

| Aspecto | $\tau$-$p$ (slant-stack) | f-k (2D FFT) |
|---|---|---|
| Variable de salida | Intercepción $\tau$, slowness $p$ | Frecuencia $f$, [[Wavenumber|número de onda]] $k$ |
| Resolución en velocidad | $\Delta c \propto c^2/(D \cdot f)$ — varía con $c$ | $\Delta c = c^2 \Delta k / (2\pi f)$ — uniforme en $k$ |
| Presencia de [[Aliasing|aliasing]] | Posible si muestreo $\Delta x$ inadecuado | Igual |
| Implementación | DFT espacial por frecuencia | DFT 2D completa |
| Equivalencia matemática | Sí (misma información) | Referencia |

La diferencia práctica principal: la resolución en slowness es **no uniforme en velocidad** — la $\tau$-$p$ resuelve mejor velocidades bajas (slowness alta) que altas. El f-k tiene resolución uniforme en $k$, lo que favorece altas velocidades.

## Aplicaciones en [[MASW Method|MASW]]

- **Método [[ReMi Method|ReMi]]**: la $\tau$-$p$ es la base del [[ReMi Method|método ReMi]] — el borde inferior de velocidad en el panel $\tau$-$p$ corresponde a la [[Dispersion Curve|curva de dispersión]] del modo fundamental.
- **Separación de ondas directas y refractadas**: en el panel $\tau$-$p$, las ondas P (alta velocidad → baja slowness) y las ondas de Rayleigh (baja velocidad → alta slowness) ocupan regiones distintas → filtrado de uno u otro tipo es posible.
- **Combinación activo-pasivo**: al apilar en $\tau$-$p$ datos de diferente duración y tipo de fuente, se combina información de diferentes rangos de frecuencia.

> [!EXAMPLE] Evidencia empírica: Park et al. (1999) — equivalencia tau-p y f-k en procesamiento [[MASW Method|MASW]]
> **Paper 001 (Park, Miller & Xia 1999)** utiliza el análisis f-k como método principal pero discute su equivalencia con el análisis $\tau$-$p$. Ambas transformadas aplicadas al mismo dataset de Kansas producen [[Dispersion Curve|curvas de dispersión]] del modo fundamental de Rayleigh idénticas dentro de la incertidumbre de la resolución espectral. La diferencia práctica observada: el f-k muestra la energía total en el espacio $(f, c)$ con igual resolución en todas las velocidades, mientras que la $\tau$-$p$ concentra mejor la energía de las ondas de baja velocidad (ondas de Rayleigh superficiales) pero tiene menor resolución para las ondas rápidas ([[Body Waves|ondas de cuerpo]]). Para el [[MASW Method|MASW]] estándar donde el interés está en el modo fundamental de Rayleigh (baja velocidad), ambos métodos son igualmente válidos.
>
> — Research Database, entrada 001 (core); Park, Miller & Xia (1999), *Geophysics* 64(3); McMechan & Yedlin (1981), *Bull. Seism. Soc. Am.*

## Referencias

| Fuente | Sección / Página |
|--------|-----------------|
| Foti et al. (2018), *Surface Wave Methods* | Cap. 4, §4.3, pp. 216–220 — tau-p en [[MASW Method|MASW]] |
| McMechan & Yedlin (1981), *Bull. Seism. Soc. Am.* | Introducción de la transformada tau-p para [[Surface Waves|ondas superficiales]] |
| Park, Miller & Xia (1999), *Geophysics* 64(3) | Paper 001 — f-k vs tau-p en [[MASW Method|MASW]] |
